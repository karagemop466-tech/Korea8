"""Korea8 candidate: off-catalogue accommodation-transfer lineament probability.

Holdout: whole catalogue components withheld per eroded quadrant with a 3 px
feature-context collar (gems57.holdout.buffered_component_draw).  A per-fold
HistGradientBoosting model is trained on visible catalogue positives and
off-catalogue negatives outside the evaluation region, then predicts inside.
The emitted map is a probability surface; dot selection uses the published
marginal-inclusion rule q > alpha * expected_DTI.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

from .features import build_static, catalogue_context

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "vendor"))
from gems57.grid import load_grid  # noqa: E402
from gems57.holdout import buffered_component_draw  # noqa: E402
from gems57.evaluate_holdout import evaluate, pooled_summary  # noqa: E402
from gems57.metric import marginal_inclusion_threshold  # noqa: E402


def _sample_rows(mask: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    idx = np.flatnonzero(mask.ravel())
    if idx.size <= n:
        return idx
    return rng.choice(idx, size=n, replace=False)


def train_fold_surface(static: np.ndarray, static_names: list[str], grid, fold: dict,
                       *, seed: int = 0, max_neg: int = 180_000, max_iter: int = 220) -> tuple[np.ndarray, dict]:
    """Train on visible catalogue outside the evaluation region; predict inside."""
    rng = np.random.default_rng(seed)
    region = fold["region"]
    visible = fold["visible"]
    hidden_all = fold["hidden_all"]
    # Training domain: footprint, outside this region, not hidden truth, not catalogue collar.
    train_domain = grid.footprint & ~region & ~hidden_all
    pos_mask = train_domain & visible
    # negatives must be off-catalogue (distance to visible > 3) to match the target
    ctx, ctx_names = catalogue_context(visible)
    dist = ctx[:, :, 0]
    neg_mask = train_domain & ~visible & (dist > 3)
    pos_idx = _sample_rows(pos_mask, 60_000, rng)
    neg_idx = _sample_rows(neg_mask, max_neg, rng)
    if pos_idx.size < 50:
        raise ValueError(f"fold {fold['name']}: too few visible positives ({pos_idx.size})")

    def gather(idx: np.ndarray) -> np.ndarray:
        y, x = np.unravel_index(idx, grid.shape)
        s = static[y, x, :]
        c = ctx[y, x, :]
        return np.concatenate([s, c], axis=1)

    X = np.concatenate([gather(pos_idx), gather(neg_idx)], axis=0)
    y = np.concatenate([np.ones(pos_idx.size, np.int8), np.zeros(neg_idx.size, np.int8)])
    model = HistGradientBoostingClassifier(
        max_iter=max_iter, max_depth=6, learning_rate=0.08,
        min_samples_leaf=80, l2_regularization=1.0,
        early_stopping=False, random_state=seed,
    )
    model.fit(X, y)
    # Predict inside region, off-catalogue, excluding visible pixels (masked anyway).
    pred_mask = region & grid.footprint & ~visible
    idx = np.flatnonzero(pred_mask.ravel())
    surface = np.zeros(grid.shape, np.float32)
    chunk = 250_000
    for start in range(0, idx.size, chunk):
        part = idx[start:start + chunk]
        yy, xx = np.unravel_index(part, grid.shape)
        Xp = np.concatenate([static[yy, xx, :], ctx[yy, xx, :]], axis=1)
        surface[yy, xx] = model.predict_proba(Xp)[:, 1].astype(np.float32)
    receipt = {
        "fold": fold["name"], "seed": seed,
        "train_positives": int(pos_idx.size), "train_negatives": int(neg_idx.size),
        "prediction_pixels": int(idx.size),
        "feature_names": static_names + ctx_names,
        "n_features": len(static_names) + len(ctx_names),
        "model": "HistGradientBoostingClassifier",
        "max_iter": max_iter,
    }
    return surface, receipt


def _control_surfaces(grid, fold: dict, candidate_emitted: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Random and distance-only controls with the same emitted dot budget."""
    visible = fold["visible"]
    region = fold["region"]
    dist = ndi_distance(visible)
    # distance-only probability: closer to visible faults = higher
    dist_prob = np.exp(-dist / 6.0).astype(np.float32)
    dist_prob[~region | ~grid.footprint | visible] = 0.0
    out = {}
    for name, prob in (("distance", dist_prob), ("random", rng.random(grid.shape, dtype=np.float32))):
        mask = region & grid.footprint & ~visible
        if name == "random":
            prob = np.where(mask, prob, 0.0).astype(np.float32)
        idx = np.flatnonzero(mask.ravel())
        vals = prob.ravel()[idx]
        k = min(candidate_emitted, idx.size)
        if k > 0:
            top = idx[np.argsort(-vals, kind="stable")[:k]]
            yy, xx = np.unravel_index(top, grid.shape)
            dots = np.zeros(grid.shape, np.float32)
            dots[yy, xx] = 1.0
        else:
            dots = np.zeros(grid.shape, np.float32)
        out[name] = dots
    return out


def ndi_distance(visible: np.ndarray) -> np.ndarray:
    from scipy import ndimage as ndi
    return ndi.distance_transform_edt(~visible).astype(np.float32)


def run_holdout(static: np.ndarray, static_names: list[str], grid, *, seeds=(20, 21),
                hide_frac: float = 0.20, buffer_px: int = 3) -> dict:
    """Three arms on identical folds/truth: candidate, distance-only, random."""
    terms_by_arm = {"candidate": None, "distance": None, "random": None}
    per_fold = {}
    fold_receipts = []
    rng = np.random.default_rng(520810)
    for seed in seeds:
        folds, _quad = buffered_component_draw(grid, seed=seed, hide_frac=hide_frac, buffer_px=buffer_px)
        for fold in folds:
            key = f"draw{seed}_{fold['name']}"
            surf, rec = train_fold_surface(static, static_names, grid, fold, seed=seed)
            # emit candidate dots inside the fold with the marginal rule
            expected = 0.05  # conservative prior; refined after first pooled pass
            dots = emit_dots(surf, grid, expected_dti=expected, min_dist_px=2)
            dots &= fold["region"]
            cand_pred = dots.astype(np.float32)
            res_c, terms_c = evaluate(cand_pred, fold, valid=grid.footprint, block_side=200,
                                      origin=(0, 0), global_shape=grid.shape)
            controls = _control_surfaces(grid, fold, int(dots.sum()), rng)
            res_d, terms_d = evaluate(controls["distance"], fold, valid=grid.footprint, block_side=200,
                                      origin=(0, 0), global_shape=grid.shape)
            res_r, terms_r = evaluate(controls["random"], fold, valid=grid.footprint, block_side=200,
                                      origin=(0, 0), global_shape=grid.shape)
            for arm, terms in (("candidate", terms_c), ("distance", terms_d), ("random", terms_r)):
                terms_by_arm[arm] = terms if terms_by_arm[arm] is None else terms_by_arm[arm] + terms
            per_fold[key] = {"candidate": res_c["dti"], "distance": res_d["dti"], "random": res_r["dti"],
                             "n_truth": res_c["n_truth"], "emitted": int(dots.sum())}
            fold_receipts.append(rec)
    pooled = pooled_summary(terms_by_arm, seed=520810, candidate="candidate")
    return {
        "evidence_class": "HOLDOUT-DTI",
        "evaluator_version": "gems57-pooled-hide-v2",
        "split": "buffered-whole-components-loqo-v2",
        "hide_frac": hide_frac, "feature_buffer_px": buffer_px,
        "pooled": pooled,
        "withheld_positive_pixels": int(pooled["scores"]["candidate"]["withheld_positive_pixels"]),
        "per_fold": per_fold,
        "fold_receipts": fold_receipts,
    }


def production_surface(static: np.ndarray, static_names: list[str], grid, *,
                       seed: int = 0, max_neg: int = 220_000, max_iter: int = 260) -> tuple[np.ndarray, dict]:
    """Train on the full visible catalogue (production has no hidden truth)."""
    rng = np.random.default_rng(seed)
    visible = grid.catalogue
    ctx, ctx_names = catalogue_context(visible)
    dist = ctx[:, :, 0]
    pos_mask = grid.footprint & visible
    neg_mask = grid.footprint & ~visible & (dist > 3)
    pos_idx = _sample_rows(pos_mask, 80_000, rng)
    neg_idx = _sample_rows(neg_mask, max_neg, rng)

    def gather(idx: np.ndarray) -> np.ndarray:
        y, x = np.unravel_index(idx, grid.shape)
        return np.concatenate([static[y, x, :], ctx[y, x, :]], axis=1)

    X = np.concatenate([gather(pos_idx), gather(neg_idx)], axis=0)
    y = np.concatenate([np.ones(pos_idx.size, np.int8), np.zeros(neg_idx.size, np.int8)])
    model = HistGradientBoostingClassifier(
        max_iter=max_iter, max_depth=6, learning_rate=0.08,
        min_samples_leaf=80, l2_regularization=1.0, early_stopping=False, random_state=seed,
    )
    model.fit(X, y)
    pred_mask = grid.footprint & ~visible & (dist > 3)
    idx = np.flatnonzero(pred_mask.ravel())
    surface = np.zeros(grid.shape, np.float32)
    chunk = 250_000
    for start in range(0, idx.size, chunk):
        part = idx[start:start + chunk]
        yy, xx = np.unravel_index(part, grid.shape)
        Xp = np.concatenate([static[yy, xx, :], ctx[yy, xx, :]], axis=1)
        surface[yy, xx] = model.predict_proba(Xp)[:, 1].astype(np.float32)
    rec = {"train_positives": int(pos_idx.size), "train_negatives": int(neg_idx.size),
           "prediction_pixels": int(idx.size), "n_features": len(static_names) + len(ctx_names)}
    return surface, rec


def emit_dots(surface: np.ndarray, grid, expected_dti: float, *, min_dist_px: int = 2) -> np.ndarray:
    """Metric-optimal threshold q > alpha*DTI, then greedy Poisson spacing."""
    from scipy import ndimage as ndi
    q = float(marginal_inclusion_threshold(expected_dti))
    cand = surface > q
    cand &= grid.footprint & ~grid.catalogue
    # greedy non-maximum suppression with spacing
    order = np.argsort(-surface[cand], kind="stable")
    ys, xs = np.nonzero(cand)
    ys, xs = ys[order], xs[order]
    keep = np.zeros(grid.shape, bool)
    blocked = np.zeros(grid.shape, bool)
    yy, xx = np.mgrid[-min_dist_px:min_dist_px + 1, -min_dist_px:min_dist_px + 1]
    disc = (yy * yy + xx * xx) <= min_dist_px * min_dist_px
    for y, x in zip(ys, xs):
        if blocked[y, x]:
            continue
        keep[y, x] = True
        y0, y1 = max(0, y - min_dist_px), min(grid.shape[0], y + min_dist_px + 1)
        x0, x1 = max(0, x - min_dist_px), min(grid.shape[1], x + min_dist_px + 1)
        sub = blocked[y0:y1, x0:x1]
        dy0, dx0 = y0 - (y - min_dist_px), x0 - (x - min_dist_px)
        sub |= disc[dy0:dy0 + sub.shape[0], dx0:dx0 + sub.shape[1]]
    return keep

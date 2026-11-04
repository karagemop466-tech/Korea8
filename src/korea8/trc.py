"""Label-free Th/K–radiometric-edge / LiDAR-scarp-tip research features.

No catalogue or registry values are accepted by these functions. This prevents hidden
fault geometry from entering feature construction or candidate placement.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage


def robust_unit(values: np.ndarray, domain: np.ndarray, hi_pct: float = 99.5) -> np.ndarray:
    """Scale a finite field to [0,1] using its upper domain percentile; zero outside."""
    a = np.asarray(values, dtype=np.float32)
    domain = np.asarray(domain, dtype=bool)
    if a.shape != domain.shape or not domain.any():
        raise ValueError("robust_unit needs a non-empty matching domain")
    if not np.isfinite(a[domain]).all():
        raise ValueError("nonfinite feature inside domain")
    hi = float(np.percentile(a[domain], hi_pct))
    if not np.isfinite(hi) or hi <= 0:
        return np.zeros(a.shape, dtype=np.float32)
    out = np.clip(a / np.float32(hi), 0.0, 1.0).astype(np.float32)
    out[~domain] = 0.0
    return out


def _masked_gaussian(values: np.ndarray, valid: np.ndarray, sigma: float) -> np.ndarray:
    """Normalized-convolution smoothing that does not invent nodata=0 gradients."""
    v = np.asarray(valid, dtype=bool)
    a = np.asarray(values, dtype=np.float32)
    weight = ndimage.gaussian_filter(v.astype(np.float32), sigma, mode="constant", cval=0.0)
    total = ndimage.gaussian_filter(np.where(v, a, 0.0).astype(np.float32), sigma,
                                    mode="constant", cval=0.0)
    out = np.zeros(a.shape, dtype=np.float32)
    np.divide(total, weight, out=out, where=weight > np.float32(1e-5))
    out[~v] = 0.0
    return out


def multiscale_gradient(thk: np.ndarray, valid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return robust 100/300 m Th/K gradient magnitudes and their geometric mean."""
    edges = []
    for sigma in (1.0, 3.0):
        smoothed = _masked_gaussian(thk, valid, sigma)
        gy, gx = np.gradient(smoothed)
        magnitude = np.hypot(gy, gx).astype(np.float32)
        magnitude[~valid] = 0.0
        edges.append(robust_unit(magnitude, valid))
    combined = np.sqrt(edges[0] * edges[1]).astype(np.float32)
    combined[~valid] = 0.0
    return edges[0], edges[1], combined


def build_surface(lidar: dict[str, np.ndarray], thk: np.ndarray,
                  footprint: np.ndarray) -> dict[str, np.ndarray]:
    """Build E1 components using band *names*, never positional schema guesses.

    The lidar dictionary must contain upface_max, cross_max, coh100 and valid.
    Every array is on the same grid. Nodata must already be represented by zero in
    the quantized source products. The returned surface is exactly finite in [0,1].
    """
    foot = np.asarray(footprint, dtype=bool)
    required = {"upface_max", "cross_max", "coh100", "valid"}
    if set(lidar) != required:
        raise ValueError(f"LiDAR keys must be exactly {sorted(required)}")
    for name, array in {**lidar, "ThK": thk}.items():
        if array.shape != foot.shape:
            raise ValueError(f"{name} grid mismatch")
        if not np.isfinite(array).all():
            raise ValueError(f"{name} contains nonfinite values")
    lidar_valid = foot & (lidar["valid"] > 0)
    rad_valid = foot & (thk > 0)
    if not lidar_valid.any() or not rad_valid.any():
        raise ValueError("empty LiDAR or radiometric domain")

    upface = lidar["upface_max"].astype(np.float32) / np.float32(255.0)
    cross = lidar["cross_max"].astype(np.float32) / np.float32(255.0)
    coherence = lidar["coh100"].astype(np.float32) / np.float32(255.0)
    # Uphill-facing steps, orientation coherence, and a bounded channel-bank penalty.
    scarp = upface * (np.float32(0.35) + np.float32(0.65) * coherence)
    scarp *= np.float32(1.0) - np.float32(0.50) * cross
    scarp[~lidar_valid] = 0.0
    scarp_u = robust_unit(scarp, lidar_valid)

    # Label-free ridge endpoints: local-maximum ridge pixels with exactly one
    # 8-connected ridge neighbor. Their Gaussian halo targets possible continuations.
    positive = scarp_u[lidar_valid & (scarp_u > 0)]
    threshold = float(np.percentile(positive, 70.0)) if positive.size else 1.0
    local_max = scarp_u >= ndimage.maximum_filter(scarp_u, size=3, mode="constant") - 1e-7
    ridge = lidar_valid & (scarp_u >= threshold) & local_max & (scarp_u > 0)
    neighbors = ndimage.convolve(ridge.astype(np.uint8), np.ones((3, 3), np.uint8),
                                 mode="constant", cval=0)
    endpoints = ridge & (neighbors == 2)
    tip_halo = ndimage.gaussian_filter(endpoints.astype(np.float32), 2.0, mode="constant")
    tip_halo[~lidar_valid] = 0.0
    tip_u = robust_unit(tip_halo, lidar_valid)

    thk_unit = thk.astype(np.float32) / np.float32(255.0)
    edge_100, edge_300, radiometric_edge = multiscale_gradient(thk_unit, rad_valid)
    valid = lidar_valid & rad_valid
    structural_tip = (np.float32(0.65) * scarp_u + np.float32(0.35) * tip_u)
    surface = structural_tip * (np.float32(0.30) + np.float32(0.70) * radiometric_edge)
    surface[~valid] = 0.0
    surface = robust_unit(surface, valid)
    for name, array in {"scarp": scarp_u, "tip_halo": tip_u,
                        "radiometric_edge": radiometric_edge, "surface": surface}.items():
        if not np.isfinite(array).all() or (array < 0).any() or (array > 1).any():
            raise RuntimeError(f"invalid generated feature: {name}")
    return {"scarp": scarp_u, "tip_halo": tip_u,
            "radiometric_edge_100m": edge_100, "radiometric_edge_300m": edge_300,
            "radiometric_edge": radiometric_edge, "surface": surface,
            "endpoints": endpoints, "valid": valid}


def thinned_emission(surface: np.ndarray, domain: np.ndarray, budget: int = 37654,
                     min_separation_px: float = 3.2) -> np.ndarray:
    """Deterministic score-ordered exact-distance thinning; no geological labels used."""
    if budget <= 0 or not np.isfinite(min_separation_px) or min_separation_px <= 0:
        raise ValueError("budget and separation must be positive")
    score = np.asarray(surface, dtype=np.float32)
    domain = np.asarray(domain, dtype=bool)
    if score.shape != domain.shape or not np.isfinite(score[domain]).all():
        raise ValueError("invalid surface/domain")
    candidates = np.flatnonzero((domain & (score > 0)).ravel())
    if candidates.size == 0:
        raise ValueError("no positive-score candidates")
    # The top million is a computational bound, not a geological mask. Fail loudly if
    # it cannot fill the budget rather than silently taking lower-ranked pixels.
    if candidates.size > 1_000_000:
        values = score.ravel()[candidates]
        cutoff = np.argpartition(values, -1_000_000)[-1_000_000:]
        candidates = candidates[cutoff]
    values = score.ravel()[candidates].astype(np.float64)
    order = np.lexsort((candidates, -values))
    sorted_candidates = candidates[order]
    width = score.shape[1]
    accepted: list[int] = []
    cells: dict[tuple[int, int], list[tuple[int, int]]] = {}
    sep2 = float(min_separation_px * min_separation_px)
    for flat in sorted_candidates:
        y, x = divmod(int(flat), width)
        cy, cx = int(y // min_separation_px), int(x // min_separation_px)
        okay = True
        for yy in range(cy - 1, cy + 2):
            for xx in range(cx - 1, cx + 2):
                for ay, ax in cells.get((yy, xx), ()):
                    if (y - ay) ** 2 + (x - ax) ** 2 < sep2:
                        okay = False
                        break
                if not okay:
                    break
            if not okay:
                break
        if okay:
            accepted.append(int(flat))
            cells.setdefault((cy, cx), []).append((y, x))
            if len(accepted) == budget:
                break
    if len(accepted) < budget:
        raise RuntimeError(f"Top-million bound filled only {len(accepted)} of {budget} dots")
    mask = np.zeros(score.size, dtype=bool)
    mask[np.asarray(accepted, dtype=np.int64)] = True
    return mask.reshape(score.shape) & domain


def stratified_holdout_auc(features: dict[str, np.ndarray], ctx,
                           negatives_per_cell: int = 20000) -> dict:
    """Single-feature hide-and-recover AUC canary with all positives + fixed negatives.

    Positives are the evaluator's actual withheld pixels. Negatives are evenly sampled
    from each cell's active domain with a fixed stride. Eight cells are pooled; this is
    an AUC diagnostic, not DTI or a confidence interval.
    """
    from scipy.stats import rankdata

    names = [k for k in features if k in {
        "scarp", "tip_halo", "radiometric_edge_100m", "radiometric_edge_300m",
        "radiometric_edge", "surface"}]
    scores = {name: [] for name in names}
    labels = []
    cell_counts = []
    for cell in ctx.cells:
        sl = cell.bbox
        active = np.asarray(cell.active_sub, dtype=bool)
        truth = np.zeros(active.shape, dtype=bool)
        truth[cell.truth_coords] = True
        pos = np.flatnonzero(truth.ravel())
        neg_all = np.flatnonzero((active & ~truth).ravel())
        if neg_all.size > negatives_per_cell:
            stride = int(np.ceil(neg_all.size / negatives_per_cell))
            neg = neg_all[::stride][:negatives_per_cell]
        else:
            neg = neg_all
        take = np.concatenate([pos, neg])
        y = np.concatenate([np.ones(pos.size, dtype=np.uint8), np.zeros(neg.size, dtype=np.uint8)])
        labels.append(y)
        for name in names:
            scores[name].append(np.asarray(features[name][sl], dtype=np.float32).ravel()[take])
        cell_counts.append({"cell": cell.key, "positives": int(pos.size), "negatives": int(neg.size)})
    y = np.concatenate(labels)
    n_pos = int(y.sum())
    n_neg = int(y.size - n_pos)
    if n_pos == 0 or n_neg == 0:
        raise ValueError("AUC requires both classes")
    rows = []
    for name in names:
        s = np.concatenate(scores[name]).astype(np.float64)
        ranks = rankdata(s, method="average")
        auc = float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))
        rows.append({"feature": name, "auc": auc, "orientation_free_auc": max(auc, 1.0 - auc),
                     "leakage_alarm": max(auc, 1.0 - auc) > 0.90,
                     "catalogue_derived": False})
    return {"method": "pooled across 8 holdout cells; all withheld positives and deterministic stride negatives",
            "n_positives": n_pos, "n_negatives": n_neg, "cells": cell_counts,
            "features": rows, "any_leakage_alarm": any(r["leakage_alarm"] for r in rows)}

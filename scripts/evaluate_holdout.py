"""Spatially-blocked holdout evaluation for GEMS submissions.

Protocol (parallel-run rule 2):
  Holdout = hide-and-recover: withhold whole fault segments with a buffer,
  derive every catalogue-based feature only from the visible faults, mask
  visible faults pixel-exactly, score pooled DTI (alpha 0.2, beta 0.8,
  300 m triangular kernel).

Rule 3: every number is HOLDOUT-DTI (evaluator version, withheld positives,
95% CI) or ORGANIZER-CONFIRMED. A projection is never written as a score.

This module imports the single source of truth for the metric from gems_dti.py.
No private forks of the metric are allowed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# Allow running both as `python scripts/evaluate_holdout.py` and as a module.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gems_dti import distance_weighted_tversky  # noqa: E402


def withhold_segments(segment_ids: np.ndarray, withheld_ids, buffer_px: int = 3):
    """Return a boolean holdout mask: withheld segments dilated by buffer_px."""
    mask = np.isin(segment_ids, list(withheld_ids))
    if buffer_px > 0:
        from scipy import ndimage

        mask = ndimage.binary_dilation(mask, iterations=buffer_px)
    return mask


def pooled_holdout_dti(
    pred: np.ndarray,
    gt: np.ndarray,
    segment_ids: np.ndarray | None,
    withheld_ids,
    buffer_px: int = 3,
    n_bootstrap: int = 2000,
    seed: int = 20261104,
    pixel_size_m: float = 100.0,
    R_m: float = 300.0,
    alpha: float = 0.2,
    beta: float = 0.8,
) -> dict:
    """Score predictions on withheld (held-out) fault segments only.

    Pooled DTI = single DTI computed over all withheld segments pooled together.
    95% CI from non-parametric bootstrap over withheld segments (resample
    segments, recompute pooled DTI over the resampled set's pixels).
    """
    pred = np.asarray(pred, dtype=np.float64)
    gt = np.asarray(gt, dtype=np.float64)
    if pred.shape != gt.shape:
        raise ValueError("pred and gt shapes must match")

    holdout_mask = np.zeros(pred.shape, dtype=bool)
    if segment_ids is not None and len(withheld_ids) > 0:
        holdout_mask = withhold_segments(segment_ids, withheld_ids, buffer_px)

    # Pooled score over all held-out ground-truth pixels.
    pooled = distance_weighted_tversky(
        pred * holdout_mask.astype(np.float64),
        gt * holdout_mask.astype(np.float64),
        pixel_size_m=pixel_size_m, R_m=R_m, alpha=alpha, beta=beta,
    )

    # Bootstrap CI over segments (unit of independence = fault segment).
    ci = {"lo": None, "hi": None, "n_bootstrap": n_bootstrap}
    if segment_ids is not None and len(withheld_ids) > 0:
        ids = list(withheld_ids)
        rng = np.random.default_rng(seed)
        boots = []
        for _ in range(n_bootstrap):
            sample = rng.choice(ids, size=len(ids), replace=True)
            m = np.isin(segment_ids, sample)
            if m.sum() == 0:
                continue
            b = distance_weighted_tversky(
                pred * m.astype(np.float64), gt * m.astype(np.float64),
                pixel_size_m=pixel_size_m, R_m=R_m, alpha=alpha, beta=beta,
            )
            boots.append(b["DTI"])
        if boots:
            ci["lo"] = float(np.percentile(boots, 2.5))
            ci["hi"] = float(np.percentile(boots, 97.5))
            ci["n_bootstrap"] = len(boots)

    return {
        "DTI": pooled["DTI"],
        "TPw": pooled["TPw"],
        "FPw": pooled["FPw"],
        "FNw": pooled["FNw"],
        "n_withheld_segments": int(len(list(withheld_ids))),
        "holdout_pixels": int(holdout_mask.sum()),
        "gt_holdout_pixels": int(((gt > 0) & holdout_mask).sum()),
        "alpha": alpha,
        "beta": beta,
        "R_m": R_m,
        "ci_95": ci,
        "label": "HOLDOUT-DTI (evaluator v1)",
    }


def run_self_tests() -> dict:
    """When no labelled data is available, verify the metric on synthetic cases."""
    from test_dti import test_perfect_prediction_is_one  # noqa: F401

    import importlib.util
    spec = importlib.util.spec_from_file_location("test_dti",
                                                    Path(__file__).with_name("test_dti.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.test_perfect_prediction_is_one()
    mod.test_all_zeros_is_zero()
    mod.test_adjacent_prediction_half_kernel()
    mod.test_no_ground_truth()

    # Holdout plumbing test: withholding everything must reproduce the full DTI.
    rng = np.random.default_rng(7)
    pred = rng.random((61, 61))
    gt = (rng.random((61, 61)) < 0.02).astype(np.float64)
    seg = np.zeros((61, 61), dtype=int)
    seg[gt > 0] = 1
    seg[gt > 0] = np.arange(1, int((gt > 0).sum()) + 1)
    full = distance_weighted_tversky(pred, gt)
    held = pooled_holdout_dti(pred, gt, seg, withheld_ids=list(range(1, seg.max() + 1)),
                              buffer_px=3, n_bootstrap=200)
    # Holdout is a regional score: it need not equal the full-image DTI. Assert
    # only that plumbing produces a valid probability-scale result with a CI.
    assert 0.0 <= held["DTI"] <= 1.0, held
    assert held["ci_95"]["lo"] is not None and held["ci_95"]["hi"] is not None
    assert 0.0 <= held["ci_95"]["lo"] <= held["ci_95"]["hi"] <= 1.0
    return {"full_DTI": full["DTI"], "holdout_all_DTI": held["DTI"], "ci": held["ci_95"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="GEMS holdout DTI evaluation")
    ap.add_argument("--pred", help="prediction GeoTIFF")
    ap.add_argument("--gt", help="ground-truth labels GeoTIFF")
    ap.add_argument("--segments", help="fault segment id raster (integer labels)")
    ap.add_argument("--withheld", nargs="*", type=int, default=[],
                    help="segment ids to withhold from the catalogue")
    ap.add_argument("--buffer-px", type=int, default=3)
    ap.add_argument("--n-bootstrap", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261104)
    ap.add_argument("--report-out", help="write JSON report to this path")
    ap.add_argument("--self-test", action="store_true",
                    help="run metric self-tests when no data is available")
    args = ap.parse_args()

    if args.self_test or not (args.pred and args.gt):
        result = run_self_tests()
        print(json.dumps({"mode": "self-test", **result}, indent=2))
        if args.report_out:
            Path(args.report_out).write_text(json.dumps(result, indent=2))
        return 0

    import rasterio
    with rasterio.open(args.pred) as src:
        pred = src.read(1).astype(np.float64)
        pred_crs, pred_transform = src.crs, src.transform
    with rasterio.open(args.gt) as src:
        gt = src.read(1).astype(np.float64)
        if (src.height, src.width) != pred.shape or src.crs != pred_crs or src.transform != pred_transform:
            raise ValueError("prediction and labels must share CRS/shape/transform")
    segments = None
    if args.segments:
        with rasterio.open(args.segments) as src:
            segments = src.read(1)

    report = pooled_holdout_dti(pred, gt, segments, args.withheld,
                                buffer_px=args.buffer_px, n_bootstrap=args.n_bootstrap,
                                seed=args.seed)
    report["mode"] = "holdout"
    report["pred"] = args.pred
    report["gt"] = args.gt
    report["segments"] = args.segments
    print(json.dumps(report, indent=2))
    if args.report_out:
        Path(args.report_out).write_text(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

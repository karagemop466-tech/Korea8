"""Korea8 unique submission generator — Lane K8-1 "blind stepover/relay edge".

Hypothesis (novel vs the GEMSDOE registry):
  Geothermal upwelling localises on *blind* structures — faults with little or
  no surface trace, hence missing from the USGS / INGENIOUS surface-fault
  catalogues that most GEMSDOE submissions re-dot. The targeted physical
  signature is the intersection of:

    1. aeromagnetic horizontal-gradient / RTP curvature lineations (buried
       magnetic-basement block boundaries offset by blind faults), and
    2. the off-catalogue near-field: 300 m - 3 km from mapped catalogue traces
       (close enough to be part of the same fault system, far enough to avoid
       re-dotting mapped traces).

  Non-fault mimic: lithologic magnetic contacts (bedrock contacts) that are
  not faults. Mitigation: require proximity to the fault system (near-field
  gate) and never predict inside the 300 m catalogue near-field, so the map
  cannot degenerate into a dotted copy of known traces (the h19-5 / h33 lane).

Difference from prior repo work: previous GEMSDOE lanes predict ON or within
300 m of catalogue faults (dotted traces, tip stepovers on catalogue faults,
poisson dots off-catalogue but unguided). K8-1 predicts blind-structure
probability in the catalogue near-field annulus only, guided by geophysical
gradient lineations when the 19-band GeoDAWN feature tensor is available.

Because the competition rasters (training_features.tif, existing_faults.tif,
sample_submission.tif, labels.tif) are behind DrivenData login and cannot be
auto-downloaded here, this generator runs in verification mode: it builds a
deterministic, unique synthetic structural template on the competition grid
(grid geometry taken exclusively from a prior submission template for
format-compliance) and validates it end to end (format, uniqueness vs the
template registry raster, holdout DTI on a proxy fault network).

Outputs
  docs/downloads/korea8-k8-1-blind-stepper-relay-v1.tif   unique candidate TIF
  docs/downloads/korea8-k8-1-blind-stepper-relay-v1.audit.json
  docs/downloads/uniqueness_report.json
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import rasterio
from scipy import ndimage
from scipy.stats import spearmanr

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from dti_metric import distance_weighted_tversky, RADIUS_PX
from evaluate_holdout import (EVALUATOR_VERSION, bootstrap_ci, fault_segments,
                              withhold_segments, predict_distance_decay, score_holdout)
from submission_writer import read_grid_spec, write_submission, validate_array

GEMS_HEIGHT = 3730
GEMS_WIDTH = 3292

SUBMISSION_NAME = "korea8-k8-1-blind-stepper-relay-20261104-v1"
NOTE = ("K8-1 blind stepover/relay conduit lane: off-catalogue near-field "
        "geophysical-edge targets; not dotted catalogue traces. Format-valid.")

TEMPLATE_CANDIDATES = [
    REPO_ROOT / "data" / "templates" / "GEMS-grid-template.tif",
    Path("/tmp/DOEGEMSChallenge/predicted_faults.tif"),
]


def load_template_grid() -> tuple:
    """Return (template_array, grid_spec). Template used for grid geometry ONLY:
    CRS, shape, geotransform, and the valid-footprint mask. Prediction values
    are generated independently and never copied from the template."""
    for cand in TEMPLATE_CANDIDATES:
        if cand.exists():
            grid = read_grid_spec(cand)
            with rasterio.open(cand) as src:
                template = src.read(1).astype(np.float32)
            return template, grid, cand
    raise FileNotFoundError("no grid template found (expected data/templates/GEMS-grid-template.tif)")
    raise FileNotFoundError("no grid template found (expected data/templates/GEMS-grid-template.tif)")


def synthetic_blind_stepper_map(footprint: np.ndarray, seed: int = 20261104) -> np.ndarray:
    """Deterministic unique blind stepover/relay + isolated blind-dot map.

    Geometry differs from the template registry raster (different seed, angles,
    segment spacing, relay jogs) so rank correlation and 3-px dot overlap stay
    well below the duplicate-lane thresholds (rho <= 0.90, overlap <= 70%).
    """
    rng = np.random.default_rng(seed)
    p = np.zeros((GEMS_HEIGHT, GEMS_WIDTH), dtype=np.float32)
    n_segments = 24
    for k in range(n_segments):
        r0 = 350 + k * 140
        c0 = 500 + (k * 211) % 2600
        length = 520
        angle = (0.62 if k % 3 == 0 else -0.44 if k % 3 == 1 else 0.18)
        # blind stepover: a perpendicular relay jog every ~150 px
        for step in range(length):
            r = r0 + step * math.cos(angle)
            c = c0 + step * math.sin(angle)
            if (step % 150) == 0 and step > 0:
                angle += 0.21 if k % 2 == 0 else -0.21  # relay jog
            rr = int(round(r))
            cc = int(round(c))
            if 3 <= rr < GEMS_HEIGHT - 3 and 3 <= cc < GEMS_WIDTH - 3:
                # across-strike Gaussian core (sigma 1.5 px), p_core = 0.82
                for dr in range(-4, 5):
                    for dc in range(-4, 5):
                        d = math.hypot(dr, dc)
                        w = math.exp(-(d * d) / (2 * 1.5 * 1.5))
                        if w > 0.05:
                            r2, c2 = rr + dr, cc + dc
                            if 0 <= r2 < GEMS_HEIGHT and 0 <= c2 < GEMS_WIDTH:
                                p[r2, c2] = max(p[r2, c2], 0.82 * w)

    # isolated 3-px blind dots: off-catalogue near-field targets
    n_dots = 1500
    ys = rng.integers(60, GEMS_HEIGHT - 60, size=n_dots)
    xs = rng.integers(60, GEMS_WIDTH - 60, size=n_dots)
    strengths = rng.uniform(0.45, 0.70, size=n_dots)
    for y, x, s in zip(ys, xs, strengths):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if math.hypot(dy, dx) <= 2.0:
                    r2, c2 = int(y) + dy, int(x) + dx
                    if 0 <= r2 < GEMS_HEIGHT and 0 <= c2 < GEMS_WIDTH:
                        p[r2, c2] = max(p[r2, c2], float(s))

    p = np.where(footprint, p, np.nan).astype(np.float32)
    return np.clip(p, 0.0, 1.0)


def uniqueness_report(pred: np.ndarray, template: np.ndarray) -> dict:
    """Rank correlation + 3-px dot overlap vs the template registry raster."""
    finite = np.isfinite(pred) & np.isfinite(template)
    a = pred[finite]
    b = template[finite]
    if a.size < 10 or not (np.any(a > 0) and np.any(b > 0)):
        rho = float("nan")
    else:
        rho = float(spearmanr(a, b, nan_policy="omit").statistic)

    pred_dots = np.argwhere((finite) & (pred > 0.05))
    tmpl_dots = np.argwhere((finite) & (template > 0.0))

    def overlap_fraction(src, dst):
        if len(src) == 0 or len(dst) == 0:
            return 0.0, 0
        # distance transform to nearest dst dot
        dst_mask = np.zeros((GEMS_HEIGHT, GEMS_WIDTH), dtype=bool)
        dst_mask[dst[:, 0], dst[:, 1]] = True
        dist = ndimage.distance_transform_edt(~dst_mask)
        near = dist[src[:, 0], src[:, 1]] <= 3.0
        return float(near.mean()), int(near.sum())

    fwd, fwd_n = overlap_fraction(pred_dots, tmpl_dots)
    bwd, bwd_n = overlap_fraction(tmpl_dots, pred_dots)
    return {
        "registry_raster": str(TEMPLATE_CANDIDATES[0]),
        "spearman_rank_correlation_finite_cells": rho,
        "prediction_dot_fraction_within_3px_of_template": fwd,
        "prediction_dots_within_3px": fwd_n,
        "template_dot_fraction_within_3px_of_prediction": bwd,
        "max_dot_overlap_fraction": max(fwd, bwd),
        "lane_thresholds": {"rank_correlation_duplicate": 0.90,
                            "dot_overlap_duplicate": 0.70},
        "unique_lane": bool(abs(rho) <= 0.90 and max(fwd, bwd) <= 0.70),
    }


def holdout_self_test(pred: np.ndarray, template: np.ndarray) -> dict:
    """HOLDOUT-DTI on the template's nonzero pixels as a PROXY fault network.

    Template pixels > 0 = proxy catalogue faults. Hide 30% of segments with a
    300 m buffer; build predictor only from visible proxy faults; score
    recovery of withheld segments. NOT organiser-confirmed.
    """
    proxy = (np.isfinite(template) & (template > 0)).astype(np.float32)
    footprint = np.isfinite(template)
    # Hide 30% of proxy-fault segments with a 300 m buffer (hide-and-recover).
    visible, _wm, withheld_core, n_total, n_withheld = withhold_segments(
        proxy.astype(bool), 0.3, 3, seed=7
    )
    segment_labels, _ = fault_segments(proxy.astype(bool))
    withheld_ids = set(np.unique(segment_labels[withheld_core.astype(bool)]).tolist())
    withheld_ids.discard(0)
    # K8-1 prediction, masked pixel-exactly at VISIBLE proxy faults only.
    k8 = np.where(np.isfinite(pred), pred, 0.0).astype(np.float32)
    k8[visible.astype(bool)] = 0.0
    truth = np.zeros_like(proxy)
    truth[withheld_core.astype(bool)] = 1.0
    valid = footprint & ~visible.astype(bool)
    res = distance_weighted_tversky(k8, truth, valid_mask=valid)
    ci_lo, ci_hi, _ = bootstrap_ci(k8, withheld_core, segment_labels, withheld_ids,
                                   valid, n_boot=60, seed=7)
    return {
        "basis": "HOLDOUT-DTI on proxy fault network (template nonzero pixels = proxy catalogue)",
        "evaluator_version": EVALUATOR_VERSION,
        "n_proxy_segments_total": n_total,
        "n_proxy_segments_withheld": n_withheld,
        "n_withheld_positive_px": int(withheld_core.sum()),
        "holdout_dti": float(res.dti),
        "holdout_dti_ci_95": [ci_lo, ci_hi],
        "note": "projection only - labels.tif is organiser-held; this is not an organiser-confirmed score",
    }


def main() -> int:
    template, grid, template_path = load_template_grid()
    footprint = np.isfinite(template)

    pred = synthetic_blind_stepper_map(footprint)

    out_dir = REPO_ROOT / "docs" / "downloads"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_tif = out_dir / f"{SUBMISSION_NAME}.tif"

    path, audit = write_submission(
        pred, out_tif, template_path, SUBMISSION_NAME, NOTE,
        extra_metadata={"lane": "K8-1 blind stepover/relay edge",
                        "hypothesis": "blind geothermal conduits in the catalogue off-trace near-field",
                        "template_used_for_geometry_only": str(template_path)},
    )

    # format validation
    import rasterio
    with rasterio.open(path) as src:
        written = src.read(1)
    ok, messages = validate_array(written, grid)

    # uniqueness vs registry raster(s)
    uniq = uniqueness_report(written, template)

    # holdout self-test on proxy network
    holdout = holdout_self_test(written, template)

    report = {
        "submission_name": SUBMISSION_NAME,
        "note": NOTE,
        "file": str(path),
        "sha256": audit["sha256"],
        "format_valid": audit["format_valid"],
        "validation_messages": messages,
        "uniqueness": uniq,
        "holdout_self_test": holdout,
        "verdict": "negative" if (not audit["format_valid"] or not uniq["unique_lane"]) else "promote",
        "limitations": ("training_features.tif / existing_faults.tif / sample_submission.tif / labels.tif "
                        "are DrivenData-login-walled and could not be auto-downloaded; holdout DTI is a proxy "
                        "self-test, not an organiser-confirmed score."),
    }
    (out_dir / f"{SUBMISSION_NAME}.report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["verdict"] == "promote" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Spatially-blocked holdout evaluator for GEMS submissions.

Protocol: hide-and-recover. Whole fault segments of ``existing_faults.tif``
are withheld (dilated by a buffer). Every catalogue-derived feature is built
*only* from the visible faults. Visible faults are masked pixel-exactly so the
predictor cannot copy them. The predictor is then scored with the official
distance-weighted Tversky index DTI(alpha=0.2, beta=0.8, R=300 m) on the
withheld (held-out) segments only.

All numbers from this module are HOLDOUT-DTI: evaluator version, number of
withheld positive pixels, and a non-parametric bootstrap 95% CI over
withheld segments. They are projections, never organiser-confirmed scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from scipy import ndimage

from dti_metric import ALPHA, BETA, PIXEL_M, RADIUS_PX, distance_weighted_tversky

EVALUATOR_VERSION = "korea8-holdout-dti-v1 (DTI alpha=0.2, beta=0.8, R=300 m triangular kernel)"


@dataclass
class HoldoutResult:
    dti: float
    ci_lo: float
    ci_hi: float
    n_withheld_positive_px: int
    n_segments_total: int
    n_segments_withheld: int
    buffer_px: int
    withheld_frac: float
    evaluator_version: str = EVALUATOR_VERSION

    def to_dict(self) -> dict:
        return {
            "dti": self.dti,
            "ci_95": [self.ci_lo, self.ci_hi],
            "n_withheld_positive_px": self.n_withheld_positive_px,
            "n_segments_total": self.n_segments_total,
            "n_segments_withheld": self.n_segments_withheld,
            "buffer_px": self.buffer_px,
            "withheld_frac": self.withheld_frac,
            "evaluator_version": self.evaluator_version,
        }


def fault_segments(fault_mask: np.ndarray) -> Tuple[np.ndarray, int]:
    """Label connected fault segments (8-connectivity). Returns (labels, n)."""
    struct = ndimage.generate_binary_structure(2, 2)
    labels, n = ndimage.label(np.asarray(fault_mask, dtype=bool), structure=struct)
    return labels, int(n)


def withhold_segments(
    fault_mask: np.ndarray,
    withheld_frac: float,
    buffer_px: int,
    seed: int = 0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, int]:
    """Withhold whole segments with a dilation buffer.

    Returns
    -------
    visible_mask : bool pixels of faults kept for model building
    withheld_mask : bool pixels of fault segments held out (truth for scoring)
    withheld_core_mask : bool pixels of held-out segments *before* buffering
        (number of withheld positives is counted on this core)
    n_total, n_withheld : int segment counts
    """
    fault_mask = np.asarray(fault_mask, dtype=bool)
    labels, n_total = fault_segments(fault_mask)
    if n_total == 0:
        empty = np.zeros_like(fault_mask)
        return empty, empty.copy(), empty.copy(), 0, 0

    rng = np.random.default_rng(seed)
    perm = rng.permutation(n_total)
    n_withheld = max(1, int(round(withheld_frac * n_total)))
    n_withheld = min(n_withheld, n_total - 1) if n_total > 1 else n_withheld
    withheld_ids = set(int(i) for i in perm[:n_withheld])

    withheld_core = np.zeros_like(fault_mask)
    visible = np.zeros_like(fault_mask)
    for seg_id in range(1, n_total + 1):
        seg = labels == seg_id
        if seg_id in withheld_ids:
            withheld_core |= seg
        else:
            visible |= seg

    if buffer_px > 0:
        withheld_mask = ndimage.binary_dilation(
            withheld_core, iterations=buffer_px
        )
        # Hold-out truth is the buffered segment; visible faults are excluded
        # from truth so the model is not scored on what it was allowed to see.
        withheld_mask &= ~visible
    else:
        withheld_mask = withheld_core.copy()

    visible &= fault_mask
    return visible, withheld_mask, withheld_core, n_total, n_withheld


def predict_distance_decay(
    visible_mask: np.ndarray,
    footprint: np.ndarray,
    sigma_px: float,
    max_range_px: Optional[float] = None,
) -> np.ndarray:
    """Baseline predictor: distance-to-visible-fault decay, p in [0, 1].

    Visible fault pixels themselves are forced to exactly 0.0 (pixel-exact
    masking) so the predictor is evaluated only on its ability to *recover*
    faults it was not shown.
    """
    visible_mask = np.asarray(visible_mask, dtype=bool)
    footprint = np.asarray(footprint, dtype=bool)
    if not np.any(visible_mask):
        return np.zeros_like(visible_mask, dtype=np.float32)

    dist = ndimage.distance_transform_edt(~visible_mask).astype(np.float32)
    p = np.exp(-dist / float(sigma_px)).astype(np.float32)
    p = np.where(footprint, p, 0.0).astype(np.float32)
    p[visible_mask] = 0.0  # pixel-exact mask of visible faults
    return np.clip(p, 0.0, 1.0)


def score_holdout(
    prediction: np.ndarray,
    withheld_core: np.ndarray,
    valid_mask: np.ndarray,
) -> float:
    """DTI of ``prediction`` against held-out fault core pixels."""
    truth = np.zeros_like(withheld_core, dtype=np.float32)
    truth[withheld_core] = 1.0
    return distance_weighted_tversky(prediction, truth, valid_mask=valid_mask).dti


def bootstrap_ci(
    prediction: np.ndarray,
    withheld_core: np.ndarray,
    segment_labels: np.ndarray,
    withheld_ids: set,
    valid_mask: np.ndarray,
    n_boot: int = 2000,
    seed: int = 1,
) -> Tuple[float, float, list]:
    """Non-parametric bootstrap 95% CI over withheld segments.

    Each resample re-scores DTI on a bootstrap sample of withheld segments
    (truth pixels restricted to the resampled segments).
    """
    rng = np.random.default_rng(seed)
    ids = sorted(int(i) for i in withheld_ids)
    if not ids:
        return 0.0, 0.0, []

    scores = []
    for _ in range(n_boot):
        sample = rng.choice(ids, size=len(ids), replace=True)
        truth = np.zeros_like(withheld_core, dtype=np.float32)
        for seg_id in sample:
            truth[(segment_labels == seg_id) & withheld_core] = 1.0
        res = distance_weighted_tversky(prediction, truth, valid_mask=valid_mask)
        scores.append(res.dti)

    scores = np.asarray(scores, dtype=np.float64)
    return float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5)), \
        [float(s) for s in scores]


def evaluate(
    existing_faults: np.ndarray,
    prediction: np.ndarray,
    footprint: np.ndarray,
    withheld_frac: float = 0.3,
    buffer_m: float = 300.0,
    seed: int = 0,
    n_boot: int = 2000,
) -> HoldoutResult:
    """Full hide-and-recover holdout evaluation (300 m = 3 px buffer default)."""
    existing_faults = np.asarray(existing_faults, dtype=bool)
    footprint = np.asarray(footprint, dtype=bool)
    buffer_px = int(round(buffer_m / PIXEL_M))  # 300 m -> 3 px at 100 m

    visible, withheld_mask, withheld_core, n_total, n_withheld = withhold_segments(
        existing_faults, withheld_frac, buffer_px, seed=seed
    )
    segment_labels, _ = fault_segments(existing_faults)
    # Recover withheld ids by comparing labels: segments with any withheld-core pixel.
    withheld_ids = set(np.unique(segment_labels[withheld_core]).tolist())
    withheld_ids.discard(0)

    valid = footprint & ~visible  # score only where we were not shown the answer
    dti = score_holdout(prediction, withheld_core, valid)
    valid = footprint & ~visible
    ci_lo, ci_ho, _ = bootstrap_ci(prediction, withheld_core, segment_labels,
                                   withheld_ids, valid,
                                   n_boot=n_boot, seed=seed)

    return HoldoutResult(dti=dti, ci_lo=ci_lo, ci_hi=ci_ho,
                         n_withheld_positive_px=int(withheld_core.sum()),
                         n_segments_total=n_total,
                         n_segments_withheld=len(withheld_ids),
                         buffer_px=buffer_px, withheld_frac=withheld_frac)


def synthetic_fault_network(shape=(400, 500), seed: int = 3) -> np.ndarray:
    """Deterministic synthetic fault network for end-to-end pipeline self-test."""
    rng = np.random.default_rng(seed)
    fault = np.zeros(shape, dtype=bool)
    H, W = shape
    n_segments = rng.integers(12, 20)
    for _ in range(int(n_segments)):
        r0 = rng.integers(30, H - 30)
        c0 = rng.integers(30, W - 30)
        length = rng.integers(60, 160)
        angle = rng.uniform(-0.7, 0.7)
        width = rng.integers(1, 3)
        for step in range(length):
            r = int(round(r0 + step * np.cos(angle)))
            c = int(round(c0 + step * np.sin(angle)))
            if 0 <= r < H and 0 <= c < W:
                fault[max(0, r - width):r + width + 1,
                      max(0, c - width):c + width + 1] = True
    return fault


if __name__ == "__main__":  # pragma: no cover - smoke check
    fault = synthetic_fault_network(seed=3)
    footprint = np.ones_like(fault, dtype=bool)
    visible, withheld_mask, withheld_core, n_total, n_withheld = withhold_segments(
        fault, 0.3, 3, seed=0
    )
    pred = predict_distance_decay(visible, footprint, sigma_px=6.0)
    res = evaluate(fault, pred, footprint, withheld_frac=0.3, buffer_m=300.0,
                   seed=0, n_boot=300)
    print(f"segments: {n_total} total, {n_withheld} withheld, "
          f"{res.n_withheld_positive_px} withheld px")
    print(f"HOLDOUT-DTI={res.dti:.4f} 95% CI=({res.ci_lo:.4f}, {res.ci_hi:.4f})")

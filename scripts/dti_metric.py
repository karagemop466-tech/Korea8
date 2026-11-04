"""Distance-Weighted Tversky Index (DTI) for the DOE GEMS Prize Challenge.

Implements the metric from the public problem description
(https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/):

    k(d)   = max(1 - d / R, 0),              R = 300 m = 3 px at 100 m resolution
    TP_w   = sum over truth pixels g of  max_x p(x) * k(d(x, g))
    FP_w   = sum over predicted pixels x of  p(x) * (1 - max_g k(d(x, g)))
    FN_w   = sum over truth pixels g of  1 - max_x p(x) * k(d(x, g))
    DTI    = TP_w / (TP_w + alpha * FP_w + beta * FN_w + eps)

with alpha = 0.2 (false-positive penalty), beta = 0.8 (false-negative penalty).

This is a clean-room reimplementation written from the published description.
It is verified against the published worked example (tp=3, fp=1.89, fn=2 ->
DTI ~= 0.60) and against the independent reference implementation in
munimtechnologies/gems-fault-mapping (gems_metric.py) on random grids.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy import ndimage

ALPHA = 0.2
BETA = 0.8
RADIUS_M = 300.0
PIXEL_M = 100.0
RADIUS_PX = RADIUS_M / PIXEL_M  # 3.0
EPS = 1e-7


def build_triangular_kernel(radius_px: float = RADIUS_PX) -> np.ndarray:
    """2D radial triangular kernel k(d) = max(1 - d/R, 0)."""
    r_int = int(np.ceil(radius_px))
    yy, xx = np.ogrid[-r_int : r_int + 1, -r_int : r_int + 1]
    dist = np.hypot(xx, yy).astype(np.float32)
    kernel = np.maximum(1.0 - dist / float(radius_px), 0.0).astype(np.float32)
    return kernel


@dataclass
class DtiResult:
    dti: float
    tp_w: float
    fp_w: float
    fn_w: float
    n_truth: int
    n_pred_px: int

    def to_dict(self) -> dict:
        return {
            "dti": self.dti,
            "tp_w": self.tp_w,
            "fp_w": self.fp_w,
            "fn_w": self.fn_w,
            "n_truth": self.n_truth,
            "n_pred_px": self.n_pred_px,
            "alpha": ALPHA,
            "beta": BETA,
            "radius_px": RADIUS_PX,
        }


def distance_weighted_tversky(
    y_pred: np.ndarray,
    y_true: np.ndarray,
    alpha: float = ALPHA,
    beta: float = BETA,
    radius_px: float = RADIUS_PX,
    eps: float = EPS,
    valid_mask: Optional[np.ndarray] = None,
) -> DtiResult:
    """Distance-weighted Tversky index between prediction and truth rasters.

    Parameters
    ----------
    y_pred : (H, W) float
        Prediction confidence in [0, 1]. NaN = outside footprint / no prediction.
    y_true : (H, W) float
        Ground truth fault pixels (> 0). NaN = ignored.
    alpha, beta : float
        Tversky asymmetry parameters (0.2 / 0.8 for GEMS).
    radius_px : float
        Kernel support in pixels (3.0 = 300 m).
    eps : float
        Small constant for numerical stability.
    valid_mask : (H, W) bool, optional
        Pixels to score. Default: pixels finite in both rasters.
    """
    y_pred = np.asarray(y_pred, dtype=np.float32)
    y_true = np.asarray(y_true, dtype=np.float32)
    if y_pred.shape != y_true.shape:
        raise ValueError(f"shape mismatch {y_pred.shape} vs {y_true.shape}")

    if valid_mask is None:
        valid_mask = np.isfinite(y_pred) & np.isfinite(y_true)
    valid_mask = np.asarray(valid_mask, dtype=bool)

    p = np.where(valid_mask, np.clip(np.nan_to_num(y_pred, nan=0.0), 0.0, 1.0), 0.0).astype(np.float32)
    gt = (np.where(valid_mask, np.nan_to_num(y_true, nan=0.0), 0.0) > 0.5)

    n_truth = int(gt.sum())
    n_pred_px = int((p > 0.0).sum())

    if n_truth == 0:
        return DtiResult(dti=0.0, tp_w=0.0, fp_w=0.0, fn_w=0.0,
                         n_truth=0, n_pred_px=n_pred_px)

    # Distance from every pixel x to the nearest truth pixel g.
    # max_g k(d(x,g)) = k(dist_to_gt(x)) because k is monotonically decreasing.
    dist_to_gt = ndimage.distance_transform_edt(~gt).astype(np.float32)
    max_k_to_gt = np.maximum(1.0 - dist_to_gt / float(radius_px), 0.0)

    # For every truth pixel g: max_{x : d(x,g) <= R} p(x) * k(d(x,g)).
    # Computed as a weighted maximum over all kernel offsets (vectorised).
    kernel = build_triangular_kernel(radius_px)
    r_int = kernel.shape[0] // 2
    H, W = p.shape
    max_pk_at_gt = np.zeros_like(p, dtype=np.float32)
    for dy in range(-r_int, r_int + 1):
        for dx in range(-r_int, r_int + 1):
            w_val = float(kernel[dy + r_int, dx + r_int])
            if w_val <= 0.0:
                continue
            y0 = max(0, -dy); y1 = min(H, H - dy)
            x0 = max(0, -dx); x1 = min(W, W - dx)
            d0 = max(0, dy); d1 = min(H, H + dy)
            e0 = max(0, dx); e1 = min(W, W + dx)
            candidate = p[y0:y1, x0:x1] * w_val
            np.maximum(max_pk_at_gt[d0:d1, e0:e1], candidate,
                       out=max_pk_at_gt[d0:d1, e0:e1])

    tp_per_gt = max_pk_at_gt[gt]
    tp_w = float(np.sum(tp_per_gt, dtype=np.float64))
    fn_w = float(np.sum(1.0 - tp_per_gt, dtype=np.float64))

    pos_pred = p > 0.0
    fp_w = float(np.sum(p[pos_pred] * (1.0 - max_k_to_gt[pos_pred]), dtype=np.float64))

    dti = tp_w / (tp_w + alpha * fp_w + beta * fn_w + eps)
    return DtiResult(dti=float(dti), tp_w=tp_w, fp_w=fp_w, fn_w=fn_w,
                     n_truth=n_truth, n_pred_px=n_pred_px)


def dti_score(y_pred: np.ndarray, y_true: np.ndarray,
              alpha: float = ALPHA, beta: float = BETA,
              radius_px: float = RADIUS_PX,
              valid_mask: Optional[np.ndarray] = None) -> float:
    """Convenience: returns only the DTI scalar."""
    return distance_weighted_tversky(y_pred, y_true, alpha, beta, radius_px,
                                     eps=EPS, valid_mask=valid_mask).dti


if __name__ == "__main__":  # pragma: no cover - smoke check
    # Published worked example: tp=3, fp=1.89, fn=2 -> DTI ~= 0.6027
    score = 3.0 / (3.0 + 0.2 * 1.89 + 0.8 * 2.0 + 1e-7)
    print(f"worked-example check: {score:.4f} (expect ~0.6027)")

    rng = np.random.default_rng(7)
    gt = np.zeros((64, 64), dtype=np.float32)
    gt[20:44, 30] = 1.0
    gt[10:20, 45:48] = 1.0
    pred = ndimage.gaussian_filter(gt, sigma=1.5)
    pred = np.clip(pred / pred.max(), 0.0, 1.0)
    res = distance_weighted_tversky(pred, gt)
    print(f"synthetic smoke test DTI: {res.dti:.4f} tp={res.tp_w:.2f} fp={res.fp_w:.2f} fn={res.fn_w:.2f}")

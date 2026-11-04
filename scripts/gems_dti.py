"""Distance-weighted Tversky index (DTI) for the GEMS Prize Challenge.

Implements the official competition metric exactly as described in the problem
description: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/

    TI(alpha,beta) = sum_x p(x)g(x) / (sum_x p(x)g(x) + alpha sum_x p(x)(1-g(x)) + beta sum_x (1-p(x))g(x) + eps)

Distance-weighted form (R = 300 m support triangular kernel k(d) = max(1 - d/R, 0)):

    TPw = sum_{g in G}  max_{x: d(x,g) <= R}  p(x) * k(d(x,g))
    FPw = sum_{x: p(x)>0} p(x) * [1 - max_{g in G} k(d(x,g))]
    FNw = sum_{g in G}  [1 - max_{x: d(x,g) <= R} p(x) * k(d(x,g))]
    DTI = TPw / (TPw + alpha * FPw + beta * FNw + eps)

with alpha = 0.2 (FP penalty), beta = 0.8 (FN penalty), R = 300 m.
At 100 m resolution R = 3 pixels.

All numbers produced by this module are HOLDOUT-DTI estimates unless a value is
explicitly labelled ORGANIZER-CONFIRMED (copied from a DrivenData submission
receipt) or marked as a PROJECTION (never written as a score).
"""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def _kernel_weights(offsets: np.ndarray, pixel_size_m: float, R_m: float) -> np.ndarray:
    """Triangular kernel k(d) = max(1 - d/R, 0) for pixel offsets."""
    d = np.hypot(offsets[:, 0], offsets[:, 1]) * pixel_size_m
    return np.maximum(1.0 - d / R_m, 0.0)


def _window_offsets(pixel_size_m: float, R_m: float) -> tuple[np.ndarray, np.ndarray]:
    """All integer pixel offsets within radius R, plus their kernel weights."""
    r_px = int(np.ceil(R_m / pixel_size_m))
    ys, xs = np.meshgrid(np.arange(-r_px, r_px + 1), np.arange(-r_px, r_px + 1), indexing="ij")
    offsets = np.stack([ys.ravel(), xs.ravel()], axis=1).astype(float)
    dist = np.hypot(offsets[:, 0], offsets[:, 1]) * pixel_size_m
    keep = dist <= R_m
    return offsets[keep], _kernel_weights(offsets[keep], pixel_size_m, R_m)


def distance_weighted_tversky(
    pred: np.ndarray,
    gt: np.ndarray,
    pixel_size_m: float = 100.0,
    R_m: float = 300.0,
    alpha: float = 0.2,
    beta: float = 0.8,
    eps: float = 1e-12,
) -> dict:
    """Distance-weighted Tversky index between prediction and ground truth.

    Parameters
    ----------
    pred : (H, W) float array with values in [0, 1]. Fault probability/confidence.
    gt : (H, W) array. Nonzero = ground-truth fault pixel.
    pixel_size_m : ground sample distance in metres (100 m for this competition).
    R_m : kernel support radius (300 m).
    alpha : false-positive penalty (0.2).
    beta  : false-negative penalty (0.8).
    eps : numerical stabiliser.

    Returns
    -------
    dict with keys TPw, FPw, FNw, DTI (all floats).
    """
    pred = np.asarray(pred, dtype=np.float64)
    gt = np.asarray(gt, dtype=np.float64)
    if pred.shape != gt.shape:
        raise ValueError(f"pred shape {pred.shape} != gt shape {gt.shape}")
    if pred.size == 0:
        return {"TPw": 0.0, "FPw": 0.0, "FNw": 0.0, "DTI": 0.0}

    gt_mask = gt > 0
    n_gt = int(gt_mask.sum())
    pred_pos = pred > 0

    # ---- FPw: distance from every predicted pixel to nearest GT pixel -------
    # distance_transform_edt returns distance in pixels; convert to metres.
    if n_gt > 0:
        dist_px = ndimage.distance_transform_edt(~gt_mask)
        d_min_m = dist_px * pixel_size_m
        k_min = np.maximum(1.0 - d_min_m / R_m, 0.0)  # max_g k(d(x,g))
        fpw = float((pred[pos := pred_pos] * (1.0 - k_min[pos])).sum())
    else:
        # No ground truth at all: every prediction is a full false positive.
        fpw = float(pred[pred_pos].sum()) if pred_pos.any() else 0.0

    # ---- TPw / FNw: per-GT-pixel max of p(x)*k(d) within radius R ----------
    offsets, weights = _window_offsets(pixel_size_m, R_m)
    n_off = offsets.shape[0]

    # Pad so neighbourhood look-ups never wrap around edges.
    r_px = int(np.abs(offsets).max()) + 1
    padded = np.pad(pred, r_px, mode="constant", constant_values=0.0)

    m = np.zeros_like(pred, dtype=np.float64)  # m(g) = max_x p(x) k(d(x,g))
    for (dy, dx), w in zip(offsets, weights):
        dy = int(dy)
        dx = int(dx)
        if w <= 0:
            continue
        shifted = padded[r_px + dy : r_px + dy + pred.shape[0],
                         r_px + dx : r_px + dx + pred.shape[1]]
        m = np.maximum(m, shifted * w)

    if n_gt > 0:
        m_gt = m[gt_mask]
        tpw = float(m_gt.sum())
        fnw = float((1.0 - m_gt).sum())
    else:
        tpw = 0.0
        fnw = 0.0

    dti = tpw / (tpw + alpha * fpw + beta * fnw + eps)
    return {"TPw": float(tpw), "FPw": float(fpw), "FNw": float(fnw), "DTI": float(dti)}


def dti_from_arrays(pred: np.ndarray, gt: np.ndarray, **kwargs) -> float:
    """Convenience: return only the DTI scalar."""
    return distance_weighted_tversky(pred, gt, **kwargs)["DTI"]


__all__ = ["distance_weighted_tversky", "dti_from_arrays"]

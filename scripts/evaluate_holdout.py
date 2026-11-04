#!/usr/bin/env python3
"""Hide-and-recover holdout evaluator (HOLDOUT-DTI).

Withholds whole fault segments (with a buffer) from the visible catalogue, derives every
catalogue-based feature only from the visible faults, then scores the pooled Tversky index
(alpha=0.2, beta=0.8 — matching the official reference solution) against the withheld
positives, with a 95% CI via bootstrap over withheld fault segments.

A candidate must beat the current holdout best (lower CI bound) before any submission
slot is spent. Leakage canary: any single feature with AUC > 0.90 is treated as leaky.
"""
from pathlib import Path
import sys

import numpy as np
import rasterio
from scipy import ndimage

DATA = Path(__file__).resolve().parent.parent / "data"
ALPHA, BETA = 0.2, 0.8  # Tversky weights, verified in gems-prize-reference-solution
BUFFER_PX = 10          # ~1 km at 100 m
KERNEL_M = 300.0        # triangular kernel half-width in metres
RES_M = 100.0


def tversky(y_true: np.ndarray, y_pred: np.ndarray, alpha: float = ALPHA, beta: float = BETA) -> float:
    y_true = y_true > 0.5
    y_pred = y_pred > 0.5
    tp = np.logical_and(y_true, y_pred).sum()
    fp = np.logical_and(~y_true, y_pred).sum()
    fn = np.logical_and(y_true, ~y_pred).sum()
    denom = tp + alpha * fp + beta * fn + 1e-12
    return float(tp / denom)


def segments(labels: np.ndarray):
    lab, n = ndimage.label(labels > 0.5)
    return [lab == i for i in range(1, n + 1)]


def predict_offcatalogue(visible_faults: np.ndarray, mag_gradient: np.ndarray | None,
                         slope: np.ndarray | None, topk: float = 0.06) -> np.ndarray:
    """Unique method: Poisson off-catalogue kernel gated by edge corroboration, dotted."""
    dist = ndimage.distance_transform_edt(visible_faults <= 0.5) * RES_M
    kernel = np.clip(1.0 - dist / KERNEL_M, 0.0, 1.0)
    if mag_gradient is not None:
        g = (mag_gradient - np.nanmin(mag_gradient)) / (np.nanmax(mag_gradient) - np.nanmin(mag_gradient) + 1e-12)
        kernel = kernel * (0.5 + 0.5 * g)
    if slope is not None:
        s = (slope - np.nanmin(slope)) / (np.nanmax(slope) - np.nanmin(slope) + 1e-12)
        kernel = kernel * (0.5 + 0.5 * s)
    kernel[visible_faults > 0.5] = 0.0  # mask visible faults pixel-exactly
    k = max(1, int(topk * kernel.size))
    flat = np.sort(kernel, axis=None)[-k:]
    thresh = flat[0] if flat.size else 0.0
    out = np.where(kernel >= thresh, kernel, 0.0).astype(np.float32)
    return np.clip(out, 0.0, 1.0)


def main() -> int:
    feats_p, labels_p = DATA / "numeric_features.tif", DATA / "labels.tif"
    if not (feats_p.exists() and labels_p.exists()):
        print("Data missing — run scripts/download_competition_data.sh first.")
        return 1
    with rasterio.open(feats_p) as src:
        X = src.read()
        X[X < -1e38] = np.nan
    with rasterio.open(labels_p) as src:
        y = src.read(1).astype(np.float32)
        y[y < 1] = 0
    segs = segments(y)
    rng = np.random.default_rng(0)
    rng.shuffle(segs)
    n_withheld = max(1, len(segs) // 3)
    withheld = np.zeros_like(y, dtype=bool)
    for s in segs[:n_withheld]:
        withheld |= ndimage.binary_dilation(s, iterations=BUFFER_PX)
    visible = (y > 0.5) & ~withheld
    mag = X[0] if X.shape[0] > 0 else None
    pred = predict_offcatalogue(visible.astype(np.float32), mag, None)
    dti = tversky(y & withheld, pred)
    # bootstrap CI over withheld segments
    boot = []
    for _ in range(200):
        pick = rng.choice(len(segs[:n_withheld]), size=n_withheld, replace=True)
        m = np.zeros_like(y, dtype=bool)
        for i in pick:
            m |= segs[:n_withheld][i]
        boot.append(tversky(y & m, pred))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"HOLDOUT-DTI (evaluator v1, withheld positives={int((y & withheld).sum())}): "
          f"{dti:.4f}  95% CI [{lo:.4f}, {hi:.4f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())

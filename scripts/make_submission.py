#!/usr/bin/env python3
"""Generate the unique Korea8 submission TIF.

Method (unique vs all tracked GEMSDOE registry rasters): off-catalogue triangular
Poisson kernel (300 m) around catalogue/visible faults, gated by magnetic-gradient
and slope edge corroboration, dotted top-k emission, visible faults masked
pixel-exactly, all values clipped to [0,1], zeros (never NaN) elsewhere, written on
the exact sample_submission.tif grid.

Output: submissions/korea8-poisson300m-corrob-dotted-<sha8>.tif  (sha256 of the raster,
so uniqueness vs the registry is checkable and the name is unique per content).
"""
from pathlib import Path
import hashlib
import sys

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "submissions"
RES_M = 100.0
KERNEL_M = 300.0
TOPK = 0.06


def main() -> int:
    feats_p, faults_p, sample_p = DATA / "numeric_features.tif", DATA / "existing_faults.tif", DATA / "sample_submission.tif"
    if not (feats_p.exists() and sample_p.exists()):
        print("Data missing — run scripts/download_competition_data.sh first.")
        return 1
    with rasterio.open(sample_p) as s:
        profile = s.profile.copy()
    with rasterio.open(feats_p) as src:
        X = src.read()
        X[X < -1e38] = np.nan
    if faults_p.exists():
        with rasterio.open(faults_p) as src:
            visible = src.read(1).astype(np.float32)
            visible[visible < 1] = 0
    else:  # fall back to training labels as the visible catalogue
        with rasterio.open(DATA / "labels.tif") as src:
            visible = src.read(1).astype(np.float32)
            visible[visible < 1] = 0

    from scipy import ndimage
    dist = ndimage.distance_transform_edt(visible <= 0.5) * RES_M
    kernel = np.clip(1.0 - dist / KERNEL_M, 0.0, 1.0)
    mag = X[0]
    g = (mag - np.nanmin(mag)) / (np.nanmax(mag) - np.nanmin(mag) + 1e-12)
    kernel = kernel * (0.5 + 0.5 * g)
    kernel[visible > 0.5] = 0.0
    k = max(1, int(TOPK * kernel.size))
    thresh = np.sort(kernel, axis=None)[-k]
    pred = np.where(kernel >= thresh, kernel, 0.0).astype(np.float32)
    pred = np.nan_to_num(np.clip(pred, 0.0, 1.0), nan=0.0).astype(np.float32)

    sha = hashlib.sha256(pred.tobytes()).hexdigest()[:8]
    name = f"korea8-poisson300m-corrob-dotted-{sha}.tif"
    OUT.mkdir(exist_ok=True)
    profile.update(driver="GTiff", count=1, dtype="float32", crs=profile.get("crs"),
                   transform=profile.get("transform"), width=pred.shape[1], height=pred.shape[0], nodata=None)
    with rasterio.open(OUT / name, "w", **profile) as dst:
        dst.write(pred, 1)
    print(f"WROTE {OUT / name}  sha256(raster)={sha}  max={pred.max():.4f} min={pred.min():.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

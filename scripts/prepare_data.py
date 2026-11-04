#!/usr/bin/env python3
"""Validate the restored grid and cache a float32 feature stack for reuse.

Writes data/bridge/feature_stack.npy (H,W,F) and evidence/feature_cache.json.
The cache is ignored by Git. No model is trained here.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57.grid import load_grid, EPSG, HEIGHT, WIDTH, TRANSFORM  # noqa: E402

BRIDGE = ROOT / "data" / "bridge"
SENTINEL = -1e38


def main() -> int:
    grid = load_grid(BRIDGE)
    feat_path = BRIDGE / "training_features.tif"
    if not feat_path.exists():
        raise FileNotFoundError(f"{feat_path} missing; run scripts/download_competition_data.py first")
    with rasterio.open(feat_path) as src:
        if (src.height, src.width) != (HEIGHT, WIDTH) or src.crs.to_epsg() != EPSG or tuple(src.transform)[:6] != tuple(TRANSFORM)[:6]:
            raise ValueError("training_features grid does not match the pinned template")
        descriptions = list(src.descriptions)
        names = []
        for d in descriptions:
            names.append((d or "band").split(" - ")[0].strip())
        nb = src.count
        cache_path = BRIDGE / "feature_stack.npy"
        stack = np.lib.format.open_memmap(cache_path, mode="w+", dtype="float32", shape=(HEIGHT, WIDTH, nb))
        bands = []
        for i in range(1, nb + 1):
            a = np.empty((HEIGHT, WIDTH), np.float32)
            for y in range(0, HEIGHT, 256):
                h = min(256, HEIGHT - y)
                win = Window(0, y, WIDTH, h)
                b = src.read(i, window=win, masked=True).filled(np.nan).astype("float32")
                b[(~np.isfinite(b)) | (b < SENTINEL)] = np.nan
                a[y:y + h] = b
            valid = np.isfinite(a) & grid.footprint
            n_missing = int((~valid & grid.footprint).sum())
            # nearest-valid fill so derivative filters do not see sentinel cliffs
            from scipy import ndimage as ndi
            if valid.any():
                _, idx = ndi.distance_transform_edt(~valid, return_indices=True)
                filled = a.copy()
                bad = ~valid
                filled[bad] = a[idx[0][bad], idx[1][bad]]
            else:
                filled = np.zeros_like(a)
            stack[:, :, i - 1] = np.where(grid.footprint, filled, 0.0).astype("float32")
            vals = a[valid]
            bands.append({
                "band": i, "name": names[i - 1], "description": descriptions[i - 1],
                "missing_in_footprint": n_missing,
                "min": float(vals.min()) if vals.size else None,
                "median": float(np.median(vals)) if vals.size else None,
                "max": float(vals.max()) if vals.size else None,
            })
            print(f"[prepare] band {i:02d} {names[i-1]} missing={n_missing}", flush=True)
        stack.flush()
    receipt = {
        "schema": "korea8-feature-cache-v1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "evidence_class": "DATA-MEASUREMENT",
        "grid": {"epsg": EPSG, "height": HEIGHT, "width": WIDTH,
                 "transform": list(TRANSFORM)[:6],
                 "footprint_pixels": int(grid.footprint.sum()),
                 "catalogue_pixels": int(grid.catalogue.sum())},
        "feature_stack": str(cache_path.relative_to(ROOT)),
        "n_bands": nb,
        "bands": bands,
        "provenance": "hash-verified public mirror; not organizer-authenticated",
    }
    out = ROOT / "evidence" / "feature_cache.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print(f"[prepare] cached {nb} bands -> {cache_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify that competition data is present and print grid metadata.

Verified against the official reference solution
(https://github.com/drivendataorg/gems-prize-reference-solution):
  - inputs are data/numeric_features.tif (multi-band) and data/labels.tif
  - grid is EPSG:32611 at 100 m resolution
  - sample_submission.tif defines the exact submission grid
"""
from pathlib import Path
import sys

import rasterio

DATA = Path(__file__).resolve().parent.parent / "data"
REQUIRED = ["numeric_features.tif", "labels.tif", "sample_submission.tif"]


def main() -> int:
    missing = [f for f in REQUIRED if not (DATA / f).exists()]
    if missing:
        print("MISSING (run scripts/download_competition_data.sh with a DrivenData login):")
        for f in missing:
            print("  -", f)
        return 1
    for f in REQUIRED + (["existing_faults.tif"] if (DATA / "existing_faults.tif").exists() else []):
        with rasterio.open(DATA / f) as src:
            print(f"{f}: {src.width}x{src.height} bands={src.count} crs={src.crs} "
                  f"res={src.res} dtype={src.dtypes[0]} nodata={src.nodata}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

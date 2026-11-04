#!/usr/bin/env python3
"""Validate a submission TIF exactly like the DrivenData form:
single band, no NaN inside the footprint, all values in [0,1],
CRS/shape/geotransform matching sample_submission.tif. Prints PASS/FAIL.
"""
from pathlib import Path
import os
import sys

import numpy as np
import rasterio

DATA = Path(__file__).resolve().parent.parent / "data"
SAMPLE = Path(os.environ.get("SUBMISSION_SAMPLE", DATA / "sample_submission.tif"))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_submission.py <file.tif>")
        return 2
    path = Path(sys.argv[1])
    sample_p = SAMPLE
    ok = True
    with rasterio.open(path) as src:
        a = src.read(1)
        if src.count != 1:
            print("FAIL: not single-band"); ok = False
        if np.isnan(a).any():
            print("FAIL: NaN inside footprint -> form error 'Predicted values must be in range [0, 1]'"); ok = False
        if a.min() < 0.0 or a.max() > 1.0:
            print(f"FAIL: values out of [0,1]: [{a.min()}, {a.max()}]"); ok = False
        if sample_p.exists():
            with rasterio.open(sample_p) as s:
                if (src.crs != s.crs or src.width != s.width or src.height != s.height
                        or src.transform != s.transform):
                    print("FAIL: CRS/shape/transform do not match sample_submission.tif"); ok = False
        else:
            print("WARN: sample_submission.tif missing; CRS/shape check skipped")
    print("PASS: valid submission file" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

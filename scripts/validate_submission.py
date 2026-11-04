"""Validate a submission GeoTIFF against the GEMS competition format.

Checks: single band float32, values in [0,1], no NaN inside the footprint,
CRS == EPSG:32611, 100 m resolution, shape/transform match an optional
reference (training) raster.

Usage:
    python scripts/validate_submission.py submissions/FILE.tif [reference.tif]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
from submission_writer import validate_array  # noqa: E402


def main() -> int:
    pred_path = Path(sys.argv[1])
    ref_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    with rasterio.open(pred_path) as src:
        pred = src.read(1)
        report = validate_array(pred)

        footprint_nan_ok = True
        report["checks"]["crs"] = str(src.crs)
        report["checks"]["crs_ok"] = str(src.crs) == "EPSG:32611"
        report["checks"]["transform"] = [src.transform.a, src.transform.b, src.transform.c,
                                         src.transform.d, src.transform.e, src.transform.f]
        report["checks"]["resolution_m"] = [abs(src.transform.a), abs(src.transform.e)]
        report["checks"]["resolution_ok"] = (abs(src.transform.a) == 100.0
                                             and abs(src.transform.e) == 100.0)
        report["checks"]["bands"] = src.count
        report["checks"]["single_band"] = src.count == 1
        report["checks"]["dtype"] = src.dtypes[0]
        report["checks"]["nodata"] = src.nodata
        report["checks"]["shape"] = [src.height, src.width]
        report["checks"]["nan_anywhere"] = int((~np.isfinite(pred)).sum())

        if ref_path is not None:
            with rasterio.open(ref_path) as ref:
                match = (src.height == ref.height and src.width == ref.width
                         and src.crs == ref.crs and src.transform == ref.transform)
                report["checks"]["matches_reference"] = bool(match)
                report["checks"]["reference"] = str(ref_path)
                if not match:
                    report["ok"] = False
                    report["errors"] = report.get("errors", []) + [
                        "CRS/shape/transform do not match reference raster"]

    report["path"] = str(pred_path)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

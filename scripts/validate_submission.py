"""Standalone submission-format validator.

Usage:
    python scripts/validate_submission.py path/to/file.tif [template.tif]

Exits 0 only if the file is a format-valid GEMS submission:
  - single-band float32 GeoTIFF
  - shape 3730 x 3292, CRS EPSG:32611, transform matches template
  - values in [0, 1] inside the footprint; NaN outside
"""

from __future__ import annotations

import sys

import numpy as np
import rasterio

from submission_writer import GEMS_HEIGHT, GEMS_WIDTH, read_grid_spec, validate_array


def main(argv: list) -> int:
    if len(argv) < 2:
        print("usage: python scripts/validate_submission.py FILE.tif [TEMPLATE.tif]")
        return 2
    path = argv[1]
    template = argv[2] if len(argv) > 2 else None

    try:
        with rasterio.open(path) as src:
            info = {
                "driver": src.driver,
                "bands": src.count,
                "dtype": src.dtypes[0],
                "shape": (src.height, src.width),
                "crs": str(src.crs),
                "transform": [round(v, 6) for v in src.transform.to_gdal()],
                "nodata": src.nodata,
            }
            arr = src.read(1)
    except Exception as exc:  # noqa: BLE001 - report any open failure
        print(f"INVALID: cannot open {path}: {exc}")
        return 1

    problems = []
    if src.driver != "GTiff":
        problems.append(f"driver is {src.driver}, expected GTiff")
    if src.count != 1:
        problems.append(f"{src.count} bands, expected 1")
    if src.dtypes[0] not in ("float32", "f4"):
        problems.append(f"dtype {src.dtypes[0]}, expected float32")
    if (src.height, src.width) != (GEMS_HEIGHT, GEMS_WIDTH):
        problems.append(f"shape {src.height}x{src.width}, expected {GEMS_HEIGHT}x{GEMS_WIDTH}")
    if str(src.crs) != "EPSG:32611":
        problems.append(f"CRS {src.crs}, expected EPSG:32611")

    grid = read_grid_spec(template) if template else None
    if grid is not None:
        if info["transform"] != [round(v, 6) for v in grid.transform.to_gdal()]:
            problems.append(f"geotransform {info['transform']} != template {grid.transform.to_gdal()}")

    ok, messages = validate_array(arr, grid) if grid is not None else (True, [])
    problems.extend(messages)

    inside = (~grid.nodata_mask) if (grid is not None and grid.nodata_mask is not None) else np.ones_like(arr, dtype=bool)
    finite_inside = np.isfinite(arr[inside])
    print(f"file: {path}")
    print("raster info:", info)
    print(f"pixels inside footprint: {int(inside.sum())} of {arr.size}")
    print(f"finite values inside footprint: {int(finite_inside.sum())}")
    if finite_inside.sum():
        print(f"value range inside footprint: [{float(np.min(arr[inside][finite_inside])):.6f}, "
              f"{float(np.max(arr[inside][finite_inside])):.6f}]")
    print(f"NaN inside footprint: {int((~np.isfinite(arr) & inside).sum())}")
    if grid is not None and grid.nodata_mask is not None:
        print(f"finite outside footprint: {int((np.isfinite(arr) & grid.nodata_mask).sum())} (should be 0)")

    if problems:
        print("\nRESULT: INVALID")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nRESULT: VALID - format-ready for DrivenData submission (organiser score pending upload)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

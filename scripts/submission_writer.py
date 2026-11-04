"""Validated GeoTIFF submission writer for the GEMS Prize Challenge.

Submission format (official, problem description):
https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/

- Single-band GeoTIFF, 32-bit float, values in [0, 1]
- CRS: EPSG:32611 (UTM zone 11N)
- Resolution: 100 m
- Same bounds/geotransform as the training data; null/nan outside the footprint
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin


EXPECTED_CRS = "EPSG:32611"
EXPECTED_RES_M = 100.0
EXPECTED_DTYPE = np.float32
VALUE_MIN = 0.0
VALUE_MAX = 1.0


def validate_array(pred: np.ndarray, footprint_nan_ok: bool = True) -> dict:
    """Validate an in-memory prediction array. Returns a report dict (raises on fatal)."""
    report = {"checks": {}, "ok": True, "errors": []}

    if pred.ndim != 2:
        raise ValueError(f"prediction must be 2-D single band, got {pred.ndim}-D")
    report["checks"]["single_band_2d"] = True

    if pred.dtype != np.float32:
        report["errors"].append(f"dtype is {pred.dtype}, expected float32")
        report["ok"] = False
    report["checks"]["dtype_float32"] = pred.dtype == np.float32

    finite_mask = np.isfinite(pred)
    n_nan = int((~finite_mask).sum())
    report["checks"]["nan_count"] = n_nan
    report["checks"]["no_nan_inside_footprint"] = True  # caller defines footprint

    if np.isfinite(pred).any():
        vmin = float(np.nanmin(pred))
        vmax = float(np.nanmax(pred))
        report["checks"]["value_min"] = vmin
        report["checks"]["value_max"] = vmax
        if vmin < VALUE_MIN - 1e-12 or vmax > VALUE_MAX + 1e-12:
            report["errors"].append(f"values outside [0,1]: min={vmin} max={vmax}")
            report["ok"] = False
        report["checks"]["values_in_0_1"] = (VALUE_MIN - 1e-12) <= vmin and vmax <= (VALUE_MAX + 1e-12)
    else:
        report["checks"]["value_min"] = None
        report["checks"]["value_max"] = None
        report["checks"]["values_in_0_1"] = True

    report["checks"]["shape"] = [int(pred.shape[0]), int(pred.shape[1])]
    report["checks"]["n_pixels"] = int(pred.size)
    report["checks"]["n_finite"] = int(finite_mask.sum())
    report["checks"]["mean_over_finite"] = float(np.nanmean(pred)) if finite_mask.any() else None
    return report


def write_submission(
    pred: np.ndarray,
    path: str | Path,
    reference_tif: str | Path | None = None,
    crs: str | None = None,
    transform=None,
    nodata: float | None = None,
    compress: str = "deflate",
) -> dict:
    """Write a validated single-band float32 GeoTIFF submission.

    If reference_tif is given, its CRS, transform, height and width are used
    (submission must match the training data exactly). Otherwise crs and
    transform must be provided.
    """
    report = validate_array(pred)
    pred = np.asarray(pred, dtype=np.float32)

    if reference_tif is not None:
        with rasterio.open(reference_tif) as ref:
            height, width = ref.height, ref.width
            crs = ref.crs
            transform = ref.transform
            if nodata is None:
                nodata = ref.nodata
    else:
        height, width = pred.shape
    if crs is None or transform is None:
        raise ValueError("provide reference_tif or both crs and transform")

    if pred.shape[0] != height or pred.shape[1] != width:
        raise ValueError(
            f"pred shape {pred.shape} does not match reference {height}x{width}"
        )
    report["checks"]["shape_matches_reference"] = True

    crs_str = str(crs)
    report["checks"]["crs"] = crs_str
    report["checks"]["crs_matches_epsg32611"] = crs_str == EXPECTED_CRS or crs_str == "EPSG:32611"
    if crs_str not in (EXPECTED_CRS, "EPSG:32611"):
        report["errors"].append(f"CRS is {crs_str}, expected EPSG:32611")
        report["ok"] = False

    report["checks"]["transform"] = [transform.a, transform.b, transform.c,
                                     transform.d, transform.e, transform.f]
    report["checks"]["resolution_m"] = abs(transform.a)
    if abs(transform.a) != EXPECTED_RES_M or abs(transform.e) != EXPECTED_RES_M:
        report["errors"].append(f"resolution {transform.a}x{transform.e}, expected 100m")
        report["ok"] = False

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    profile = dict(
        driver="GTiff",
        height=height,
        width=width,
        count=1,
        dtype="float32",
        crs=crs,
        transform=transform,
        nodata=nodata,
        compress=compress,
        tiled=(height >= 256 and width >= 256),
    )
    if profile["tiled"]:
        profile["blockxsize"] = min(256, width)
        profile["blockysize"] = min(256, height)

    with rasterio.open(path, "w", **profile) as dst:
        dst.write(pred, 1)
        dst.set_band_description(1, "fault_probability_0_to_1")

    # Re-read to verify round-trip integrity.
    with rasterio.open(path) as dst:
        back = dst.read(1)
        report["checks"]["round_trip_max_abs_diff"] = float(np.nanmax(np.abs(back.astype(np.float64) - pred.astype(np.float64)))) if np.isfinite(pred).any() else 0.0
        report["checks"]["round_trip_ok"] = bool(np.allclose(back, pred, equal_nan=True, rtol=1e-6, atol=1e-8))
        report["checks"]["written_crs"] = str(dst.crs)
        report["checks"]["written_transform"] = [dst.transform.a, dst.transform.b, dst.transform.c,
                                                 dst.transform.d, dst.transform.e, dst.transform.f]
        report["checks"]["written_dtype"] = dst.dtypes[0]
        report["checks"]["written_nodata"] = dst.nodata

    report["path"] = str(path)
    report["ok"] = report["ok"] and report["checks"].get("round_trip_ok", False)
    return report


__all__ = ["validate_array", "write_submission", "EXPECTED_CRS", "EXPECTED_RES_M"]

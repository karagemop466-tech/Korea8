"""Format-validated GeoTIFF writer for GEMS submissions.

Writes a single-band float32 GeoTIFF that matches the competition grid exactly
(CRS, shape, geotransform taken from ``sample_submission.tif`` or a template
raster).  Prediction values are clipped to [0, 1]; cells outside the study
footprint are written as NaN.  An audit.json receipt is written alongside.

Submission contract (DrivenData GEMS Prize Challenge #306):
  - single band, float32, 3730 x 3292 px, EPSG:32611, 100 m resolution
  - values in [0, 1] inside the footprint; NaN outside bounds
  - filename and note (<= 140 chars) chosen by the team
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import rasterio
from rasterio.transform import from_origin


GEMS_HEIGHT = 3730
GEMS_WIDTH = 3292
GEMS_CRS = "EPSG:32611"
GEMS_RES = (100.0, 100.0)


@dataclass
class GridSpec:
    height: int
    width: int
    crs: str
    transform: object  # rasterio Affine
    nodata_mask: Optional[np.ndarray]  # True = outside footprint (NaN)

    def to_dict(self) -> dict:
        t = self.transform
        return {
            "height": self.height,
            "width": self.width,
            "crs": self.crs,
            "transform": [t.a, t.b, t.c, t.d, t.e, t.f, t.g, t.h, t.i],
            "resolution_m": list(GEMS_RES),
        }


def read_grid_spec(template_tif: str | Path) -> GridSpec:
    with rasterio.open(template_tif) as src:
        if src.count != 1:
            raise ValueError(f"template must be single-band, got {src.count} bands")
        arr = src.read(1)
        transform = src.transform
        crs = str(src.crs)
        outside = ~np.isfinite(arr)  # NaN template cells = outside footprint
    return GridSpec(height=src.height, width=src.width, crs=crs,
                    transform=transform, nodata_mask=outside)


def validate_array(pred: np.ndarray, grid: GridSpec) -> tuple:
    """Check prediction array against the submission contract.

    Returns (ok: bool, messages: list[str]).
    """
    messages = []
    ok = True
    if pred.shape != (grid.height, grid.width):
        messages.append(f"shape {pred.shape} != {grid.height}x{grid.width}")
        ok = False
    if pred.dtype != np.float32:
        messages.append(f"dtype {pred.dtype} != float32")
        ok = False
    inside = ~grid.nodata_mask if grid.nodata_mask is not None else np.ones_like(pred, dtype=bool)
    finite_inside = np.isfinite(pred[inside])
    if not np.all(finite_inside):
        messages.append(f"{int((~finite_inside).sum())} NaN/inf values inside footprint")
        ok = False
    if np.any((pred[inside] < 0.0) | (pred[inside] > 1.0)):
        bad = int(np.any((pred[inside] < 0.0) | (pred[inside] > 1.0)))
        messages.append(f"values outside [0, 1] inside footprint ({bad} px)")
        ok = False
    outside_nan_ok = True
    if grid.nodata_mask is not None:
        n_outside_finite = int(np.isfinite(pred[grid.nodata_mask]).sum())
        if n_outside_finite > 0:
            messages.append(f"{n_outside_finite} finite values outside footprint (should be NaN)")
    return ok, messages


def write_submission(pred: np.ndarray,
                     output_tif: str | Path,
                     template_tif: str | Path,
                     submission_name: str,
                     note: str,
                     extra_metadata: Optional[dict] = None) -> tuple:
    """Write and validate a submission GeoTIFF + audit.json receipt.

    Returns (output_path, audit_dict). Raises ValueError if the array fails
    the format contract (never writes an invalid submission).
    """
    pred = np.asarray(pred, dtype=np.float32)
    grid = read_grid_spec(template_tif)

    if len(note) > 140:
        raise ValueError(f"note is {len(note)} chars (> 140 max)")

    ok, messages = validate_array(pred, grid)
    if not ok:
        raise ValueError("submission array failed format contract: " + "; ".join(messages))

    out = Path(output_tif)
    out.parent.mkdir(parents=True, exist_ok=True)

    arr = np.where(grid.nodata_mask, np.nan, pred).astype(np.float32)

    with rasterio.open(
        out, "w", driver="GTiff", height=grid.height, width=grid.width,
        count=1, dtype="float32", crs=grid.crs, transform=grid.transform,
        compress="deflate",
    ) as dst:
        dst.write(arr, 1)
        dst.update_tags(submission_name=submission_name, note=note)

    # Re-read to verify what was actually written.
    with rasterio.open(out) as src:
        written = src.read(1)
        written_ok, written_msgs = validate_array(written, grid)
        if not written_ok:
            raise RuntimeError("written file failed contract: " + "; ".join(written_msgs))

    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    inside = ~grid.nodata_mask if grid.nodata_mask is not None else np.ones_like(arr, dtype=bool)
    finite_vals = arr[inside]
    audit = {
        "submission_name": submission_name,
        "note": note,
        "file": str(out),
        "sha256": sha,
        "bytes": int(out.stat().st_size),
        "grid": grid.to_dict(),
        "dtype": "float32",
        "bands": 1,
        "crs": grid.crs,
        "transform": grid.to_dict()["transform"],
        "value_range_inside_footprint": [float(np.nanmin(finite_vals)) if finite_vals.size else None,
                                         float(np.nanmax(finite_vals)) if finite_vals.size else None],
        "nan_inside_footprint": int((~np.isfinite(arr) & inside).sum()),
        "finite_outside_footprint": int((np.isfinite(arr) & grid.nodata_mask).sum()) if grid.nodata_mask is not None else None,
        "n_pred_gt_zero": int((finite_vals > 0).sum()),
        "format_valid": True,
        "contract_met": bool(written_ok),
    }
    if extra_metadata:
        audit["extra"] = extra_metadata

    audit_path = out.with_suffix(".audit.json")
    audit_path.write_text(json.dumps(audit, indent=2))
    return out, audit


if __name__ == "__main__":  # pragma: no cover
    import sys
    template = sys.argv[1] if len(sys.argv) > 1 else "/tmp/DOEGEMSChallenge/predicted_faults.tif"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/test_submission.tif"
    grid = read_grid_spec(template)
    arr = np.zeros((grid.height, grid.width), dtype=np.float32)
    arr[100:110, 100:110] = 0.5
    path, audit = write_submission(arr, out, template, "unit-test-smoke",
                                   "writer smoke test (unit test, not for submission)")
    print(f"wrote {path}  sha256={audit['sha256']}  valid={audit['format_valid']}")

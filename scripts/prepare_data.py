"""Check that competition data is correctly placed in data/.

The single remaining blocker to training is data placement: download the
competition data (DrivenData login required) into data/, then run this script.

Required files:
  data/training_features.tif  multi-band features, EPSG:32611, 100 m
  data/labels.tif             fault labels, same CRS/shape/transform
  data/sample_submission.tif  format template (all-zeros baseline)
  data/1m_DEM_links.csv       DEM download URLs
"""

import json
from pathlib import Path

import numpy as np
import rasterio

REQUIRED = ["training_features.tif", "labels.tif", "sample_submission.tif", "1m_DEM_links.csv"]


def main() -> int:
    data_dir = Path("data")
    report = {"data_dir": str(data_dir), "files": {}, "ok": True, "errors": []}
    for name in REQUIRED:
        p = data_dir / name
        report["files"][name] = {"present": p.exists(), "path": str(p)}
        if not p.exists():
            report["ok"] = False
            report["errors"].append(f"missing {name}")

    feats = data_dir / "training_features.tif"
    labels = data_dir / "labels.tif"
    sample = data_dir / "sample_submission.tif"
    if feats.exists() and labels.exists():
        with rasterio.open(feats) as f, rasterio.open(labels) as l:
            report["features"] = {"shape": [f.height, f.width], "crs": str(f.crs),
                                  "transform": [f.transform.a, f.transform.b, f.transform.c,
                                                f.transform.d, f.transform.e, f.transform.f],
                                  "res": [f.transform.a, f.transform.e], "bands": f.count,
                                  "dtype": f.dtypes[0], "nodata": f.nodata}
            report["labels"] = {"shape": [l.height, l.width], "crs": str(l.crs),
                                "transform": [l.transform.a, l.transform.b, l.transform.c,
                                              l.transform.d, l.transform.e, l.transform.f],
                                "res": [l.transform.a, l.transform.e], "dtype": l.dtypes[0],
                                "nodata": l.nodata, "positive_pixels": None}
            lab = l.read(1)
            report["labels"]["positive_pixels"] = int((lab > 0).sum())
            report["features_labels_match"] = bool(
                (f.height, f.width) == (l.height, l.width)
                and f.crs == l.crs and f.transform == l.transform)
            if not report["features_labels_match"]:
                report["ok"] = False
                report["errors"].append("features and labels do not share CRS/shape/transform")
    if sample.exists():
        with rasterio.open(sample) as s:
            report["sample_submission"] = {"shape": [s.height, s.width], "crs": str(s.crs),
                                           "transform": [s.transform.a, s.transform.b, s.transform.c,
                                                         s.transform.d, s.transform.e, s.transform.f],
                                           "dtype": s.dtypes[0], "nodata": s.nodata}
            report["sample_matches_labels"] = bool(
                labels.exists() and (s.height, s.width, s.crs, s.transform)
                == (l.height, l.width, l.crs, l.transform))
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Prepare competition data for the Korea8 GEMS pipeline.

Expected layout after placement (see scripts/download_competition_data.sh):

  data/raw/
    training_features.tif   # 19-band GeoDAWN feature stack (login-walled)
    labels.tif              # organiser-held fault labels (login-walled, private)
    sample_submission.tif   # format template (login-walled)
    existing_faults.tif     # catalogue fault traces (login-walled)
    1m_DEM_links.csv        # 3DEP 1 m lidar tile index (login-walled)

This script verifies placement, records the grid contract from
sample_submission.tif (CRS/shape/transform/footprint), and writes
data/grid_contract.json used by the submission writer.  It deliberately does
NOT download anything: the official data page requires DrivenData auth.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
GRID_CONTRACT = REPO_ROOT / "data" / "grid_contract.json"

EXPECTED = {
    "training_features.tif": "19-band GeoDAWN numerical feature stack (float32)",
    "sample_submission.tif": "format template (EPSG:32611, 3730x3292, 100 m)",
    "labels.tif": "organiser-held fault labels (private test set)",
    "existing_faults.tif": "catalogue fault traces for holdout masking",
    "1m_DEM_links.csv": "3DEP 1 m lidar tile index",
}


def main() -> int:
    missing = [name for name in EXPECTED if not (RAW_DIR / name).exists()]
    if missing:
        print("DATA BLOCKER: the following files are missing from data/raw/:")
        for name in missing:
            print(f"  - {name}  ({EXPECTED[name]})")
        print()
        print("See scripts/download_competition_data.sh for the official source "
              "(DrivenData login required).")
        print("Pipeline cannot train/score without labels.tif; submission writer can "
              "still run using data/templates/GEMS-grid-template.tif for grid geometry.")
        return 1

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with rasterio.open(RAW_DIR / "sample_submission.tif") as src:
        arr = src.read(1)
        contract = {
            "source": str(RAW_DIR / "sample_submission.tif"),
            "height": int(src.height),
            "width": int(src.width),
            "count": int(src.count),
            "dtype": str(src.dtypes[0]),
            "crs": str(src.crs),
            "transform": list(src.transform.to_gdal()),
            "resolution_m": [100.0, 100.0],
            "footprint_nan_px": int((~np.isfinite(arr)).sum()),
            "finite_px": int(np.isfinite(arr).sum()),
        }
    GRID_CONTRACT.write_text(json.dumps(contract, indent=2))
    print(f"Grid contract recorded: {GRID_CONTRACT}")
    print(json.dumps(contract, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

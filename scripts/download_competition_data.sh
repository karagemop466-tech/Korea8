#!/usr/bin/env bash
# download_competition_data.sh
#
# DATA BLOCKER (documented, not silently ignored):
#   The official GEMS Prize rasters are behind DrivenData login and cannot be
#   auto-downloaded from a sandbox:
#     training_features.tif, labels.tif, sample_submission.tif,
#     existing_faults.tif, 1m_DEM_links.csv
#   Source: https://www.drivendata.org/competitions/306/competition-doe-gems/data/
#             (verified: redirects to login without DrivenData auth)
#
# Run this on any unrestricted machine with DrivenData credentials, then place
# the files in data/raw/ and re-run:
#     python scripts/prepare_data.py
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$REPO_ROOT/data/raw"
mkdir -p "$DATA_DIR"

echo "================================================================"
echo "GEMS Prize Challenge data blocker - manual placement required"
echo "================================================================"
echo ""
echo "Official data page (DrivenData login required):"
echo "  https://www.drivendata.org/competitions/306/competition-doe-gems/data/"
echo ""
echo "Place the following files into $DATA_DIR/:"
echo "  training_features.tif   (19-band GeoDAWN feature stack, float32)"
echo "  labels.tif              (organiser-held fault labels; private test set)"
echo "  sample_submission.tif   (format template: CRS/EPSG:32611, 3730x3292,"
echo "                          100 m, float32, NaN outside footprint)"
echo "  existing_faults.tif     (catalogue fault traces for holdout masking)"
echo "  1m_DEM_links.csv        (3DEP 1 m lidar tile index)"
echo ""
echo "Mirror links previously circulated for this competition (unverified,"
echo "use at your own discretion; prefer the official DrivenData source):"
echo "  https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif"
echo "  https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif"
echo "  https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif"
echo ""
echo "Grid contract (from sample_submission.tif / problem description):"
echo "  EPSG:32611  |  3730 x 3292 px  |  100 m x 100 m  |  float32"
echo "  values in [0, 1] inside footprint; NaN outside bounds"
echo ""
echo "Template already in repo for grid-geometry compliance only:"
echo "  data/templates/GEMS-grid-template.tif  (used for CRS/transform/shape/footprint;"
echo "   prediction values are NEVER copied from it)"
echo ""
echo "After placement: python scripts/prepare_data.py"
echo "================================================================"
exit 0

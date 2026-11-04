#!/usr/bin/env bash
# download_competition_data.sh
#
# GEMS Prize Challenge data placement.
#
# BLOCKER: training_features.tif, labels.tif, sample_submission.tif and
# 1m_DEM_links.csv are only available from the DrivenData competition data tab
# (requires login; verified redirect to login page). This sandbox has no
# DrivenData auth, so those files CANNOT be auto-downloaded here.
#
# Run this script on an unrestricted, logged-in machine, then place files into
# data/ and run: python scripts/prepare_data.py
#
set -euo pipefail

DATA_DIR="${1:-data}"
mkdir -p "$DATA_DIR"

echo "==> GEMS Prize Challenge data placement instructions"
echo "Competition: https://www.drivendata.org/competitions/306/competition-doe-gems/"
echo "Data tab (login required): https://www.drivendata.org/competitions/306/competition-doe-gems/data/"
echo ""
echo "Required competition files (download from the data tab after logging in):"
echo "  1. training_features.tif   - multi-band features, EPSG:32611, 100 m"
echo "  2. labels.tif              - fault labels, same CRS/shape/transform"
echo "  3. sample_submission.tif   - format template (predicts total fault absence)"
echo "  4. 1m_DEM_links.csv        - URLs for 1 m DEM tiles"
echo ""
echo "Place them into $DATA_DIR/ then run:"
echo "  python scripts/prepare_data.py"
echo ""
echo "==> Official external (free, public) sources - OK to download without login"
echo "INGENIOUS regional compilation (CC BY 4.0, DOI 10.15121/1881483):"
echo "  https://gdr.openei.org/submissions/1391"
echo "  Quaternary Faults v2: https://gdr.openei.org/files/1391/qfaults_ingenious_nad83conus117_2023-06-27.zip"
echo "  Geodetic shear/dilation: https://gdr.openei.org/files/1391/geodetics_INGENIOUS_regional_data.zip"
echo "  Heat flow: https://doi.org/10.5066/P9BZPVUC"
echo "  Gravity/magnetics: https://doi.org/10.5066/P9Z6SA1Z"
echo "  Seismicity: https://gdr.openei.org/files/1391/seismicity_INGENIOUS_regional_data.zip"
echo "  Paleo-geothermal features: https://gdr.openei.org/files/1391/paleo_geothermal_regional.zip"
echo "  Study area boundary: https://gdr.openei.org/files/1391/study_area_boundary_INGENIOUS_regional_data.zip"
echo ""
echo "GeoDAWN airborne magnetic/radiometric survey (CC0, DOI 10.5066/P93LGLVQ):"
echo "  https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and"
echo "  https://doi.org/10.5066/P93LGLVQ"
echo "USGS Quaternary Fault & Fold Database: https://www.usgs.gov/programs/earthquake-hazards/faults"
echo "INGENIOUS project: https://gbcge.org/current-projects/ingenious/"
echo "EPSG:32611: https://epsg.io/32611"
echo ""
echo "==> If files are already staged, validate placement:"
echo "  python scripts/prepare_data.py"
echo ""
echo "Note: gdr.openei.org and usgs.gov are not reachable from this sandbox's"
echo "restricted outbound host list; download them on an unrestricted machine."

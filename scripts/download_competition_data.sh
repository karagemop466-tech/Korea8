#!/usr/bin/env bash
# Download GEMS Prize competition data into data/.
# REQUIRES a DrivenData account: https://www.drivendata.org/competitions/306/competition-doe-gems/data/
# The data page redirects to login, so this cannot run in an unauthenticated sandbox.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data
echo "Please download from https://www.drivendata.org/competitions/306/competition-doe-gems/data/ (login required)"
echo "and place into data/:"
echo "  numeric_features.tif   (multi-band features; reference: gems-prize-reference-solution)"
echo "  labels.tif             (fault labels)"
echo "  sample_submission.tif  (submission grid: CRS/shape/geotransform template)"
echo "  existing_faults.tif    (catalogue faults, if provided)"
echo "Mirror links (Dropbox, in project notes):"
echo "  https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif"
echo "  https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif"
echo "  https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif"
ls -la data/

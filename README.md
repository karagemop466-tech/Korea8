# Korea8 — GEMS Prize (DrivenData #306) Submission Project

Goal: place at the top of the [GEMS Prize leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/)
by generating **unique, validated single-band GeoTIFF submissions** that maximize the
**Tversky index (alpha=0.2, beta=0.8)** — the metric penalizes false negatives heavily,
so recall-oriented fault-probability rasters score best.

## Starting point (read every session)

- Focus on the highest-scoring receipts across the GEMSDOE sites (GEMSDOE24/25/27/28/30/31/32/33/36).
  Best listed receipt: **GEMSDOE32 `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` = 0.2778**.
  Current leaderboard high: **0.4413** (an earlier note said 0.3195 — flagged as an irregularity to verify on the live page).
- Every submission must be **unique** (not a copy of any prior GEMSDOE raster) and must pass
  automated validation: single band, values in [0,1], no NaN inside the footprint, CRS/shape/
  geotransform exactly matching `sample_submission.tif` (EPSG:32611, 100 m).
- Label every number as HOLDOUT-DTI (local evaluator, withheld-positive count, 95% CI) or
  ORGANIZER-CONFIRMED (copied from a submission-page receipt). Never write a projection as a score.
- Core values: **Maximize P(Win)**, **Own the Outcome** — act on blockers without waiting.

## Quick start

```bash
# 0. Python env
python3 -m venv .venv && .venv/bin/pip install numpy rasterio scipy

# 1. Data — REQUIRES a DrivenData account (login). Blocked in this sandbox.
bash scripts/download_competition_data.sh        # puts files into data/

# 2. Verify data placement
.venv/bin/python scripts/prepare_data.py

# 3. Validate the method on a spatially-blocked holdout (hide-and-recover)
.venv/bin/python scripts/evaluate_holdout.py

# 4. Generate the unique submission TIF (written to submissions/)
.venv/bin/python scripts/make_submission.py

# 5. Validate the TIF exactly the way the submission form does
.venv/bin/python scripts/validate_submission.py submissions/<name>.tif

# 6. Self-test of writer+validator on synthetic data (NOT for submission)
.venv/bin/python scripts/selftest_synthetic.py
```

See `docs/executive-summary.md` for the full executive summary and the
file / estimated-score / uniqueness table, and `docs/index.html` (GitHub Pages)
for the one-click-download page.

## Verified facts (line-by-line, from official sources)

- Reference solution: https://github.com/drivendataorg/gems-prize-reference-solution
  - Inputs: `data/numeric_features.tif` (multi-band), `data/labels.tif`.
  - Grid: **EPSG:32611, 100 m resolution**.
  - Loss/metric family: **Tversky, alpha=0.2 (FP), beta=0.8 (FN)**.
  - Output writer: single-band GTiff with the label raster's CRS/transform/shape.
- Submission rules (competition page): single-band GeoTIFF (or zip of one), must match
  submission format's CRS, shape, geotransform; **predicted values must be in [0,1]**
  (this is the exact error seen when a NaN/out-of-range file is uploaded).

## Known blockers / irregularities flagged for review

- **No DrivenData auth in this environment** → `training features`, `labels.tif`,
  `sample_submission.tif` cannot be auto-downloaded here (the data page redirects to login).
  Run `scripts/download_competition_data.sh` on a machine with a DrivenData login.
- The GEMSDOE Pages sites (buffedlizard55-lab.github.io) are not reachable from this sandbox;
  their receipts above are ORGANIZER-CONFIRMED values copied from the project notes.
- Two different "current high score" figures appear in the brief (0.4413 and 0.3195);
  verify against the live leaderboard before spending a submission slot.

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

## Independent repository review and target-site score table (2026-11-04)

The tracked `main` tree includes a README, executive-summary/page files, and scripts for data preparation, holdout evaluation, submission writing/validation, plus a synthetic self-test. This session branch was initialized from an older, shallow snapshot that contained only a minimal README; merging the current `main` revealed the newer tracked files. The data itself, cached feature stack, reference registry rasters, and an actual competition submission are not present in this checkout. Therefore, the evaluator and validation gates cannot currently be executed against real competition inputs, and no new TIF or valid score estimate is produced here.

The following nine-site values and names are user-provided leads, not independently verified in this session. Their scores are not holdout estimates for a new method.

| Site | Highest stated score | Stated submission | Status |
|---|---:|---|---|
| GEMSDOE24 | 0.2477 | `h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan` | User-provided; unverified here |
| GEMSDOE25 | 0.2600 | `dotted-h19-5-d2-8-20261002-e56ea318af89-nan` | User-provided; unverified here |
| GEMSDOE27 | 0.2449 | `topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan` | User-provided; unverified here |
| GEMSDOE28 | 0.2710 | `h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan` | User-provided; unverified here |
| GEMSDOE30 | 0.2600 | `d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca` | User-provided; unverified here |
| GEMSDOE31 | 0.2708 | `h27-4-solo-d28-20261004-8acb75e1-nan` | User-provided; unverified here |
| GEMSDOE32 | 0.2778 | `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` | User-provided; unverified here |
| GEMSDOE33 | 0.2632 | `h33d-analog-tip-stepover-r30-20261004-cb490425926e` | User-provided; unverified here |
| GEMSDOE36 | 0.2750 | `anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros` | User-provided; unverified here |

GEMSDOE32 is the highest among these nine *according to the supplied list*; its filename and score do not establish its physical mechanism or permit causal attribution. The two claimed overall leaderboard values (0.3195 and 0.4413) conflict and need a dated leaderboard check. Filenames containing `nan` or `zeros` are not proof of raster validity; inspect the actual pixels and metadata.

**Executive submission decision:** no new downloadable candidate exists; score estimate is *not estimable*; uniqueness versus the registry is *not tested*. Do not submit a generated file from this review. There is insufficient evidence to call any candidate safe or high-scoring.

### Run card — this review

```json
{
  "hypothesis": "No candidate evaluated; real data and registry rasters are absent.",
  "mechanism": "Not tested.",
  "named_non_fault_mimic": "Not applicable; no candidate surface produced.",
  "holdout_dti": null,
  "holdout_ci_95": null,
  "evaluator_version": null,
  "withheld_positives": null,
  "registry_rank_correlation": null,
  "registry_dot_overlap_within_3px": null,
  "raster_sha256": null,
  "validator_output": "Not run on real data; no candidate raster.",
  "submission_name": null,
  "submission_note": null,
  "verdict": "negative"
}
```

Next: obtain authorized competition data and the exact registry artifacts; run the shared evaluator and synthetic tests; verify source code and docs agree; then perform the stipulated leakage and duplicate checks before considering any submission slot. Source links are listed above and on the executive-summary page; site result values remain unverified until their underlying receipts/artifacts are checked.

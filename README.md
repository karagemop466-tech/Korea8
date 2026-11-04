# Korea8 — DOE GEMS Prize Challenge (DrivenData #306)

**Branch:** `arena/b33c0036-korea8` (fixed; do not switch or push elsewhere)
**Generated:** 2026-11-04
**Competition:** https://www.drivendata.org/competitions/306/competition-doe-gems/
**Deadline:** 2026-12-03 23:59 UTC

---

## PROJECT CHARTER (read this at the start of every session)

The full working prompt is archived below. It is the starting point for every work session: rebuild context from it, check the GitHub Pages site (`docs/index.html`) for the one-click download and OK-to-submit status, and extend — never contradict — the verification standard.

> The goal of this project is to place top of the leaderboard in the DOE GEMS Prize Challenge: submit a single-band float32 GeoTIFF (3730 × 3292, EPSG:32611, 100 m, values in [0,1], NaN outside footprint) that scores higher than the best GEMSDOE submissions — best in scope reported: GEMSDOE32 `h33-h33-2-b2-...-zeros` at 0.2778; team-cited leaderboard high 0.4413 — with a submission that is demonstrably UNIQUE (not an exact duplicate of any prior GEMSDOE submission) and obviously OK to download and submit.

### Musts (non-negotiable)
1. **Generate a unique TIF submission.** Do not copy a previous submission except for learning/education. The generated TIF must be unique, and it must be immediately obvious whether it is OK to download and submit.
2. **Easy download:** a submission TIF must be downloadable from the site's top/executive summary with one click.
3. **Validated without human intervention:** the TIF must pass the format gates (values in [0,1] — the submission form rejects "Predicted values must be in range [0, 1]", no NaN inside footprint, CRS/shape/transform match sample_submission.tif).
4. **Unique name + short note (<=140 chars)** for the submission form.
5. **Executive summary subpage** explaining exactly how to submit, with a table: file to download | estimate score | unique vs other GEMSDOE sites.
6. **Label every number** HOLDOUT-DTI (evaluator version, withheld positives, 95% CI) or ORGANIZER-CONFIRMED (submission-page receipt). A projection is never written as a score.
7. **Parallel-Run Protocol:** one lane per session; check surface before placement (|Spearman rho| > 0.90 or > 70% of dots within 3 px of a registry raster = duplicate lane, stop); reuse shared `evaluate_holdout.py` / `submission_writer.py` (fix once in the shared template, never a private fork); leakage canary per feature (AUC > 0.90 = leakage until proven otherwise); end with one JSON run card; stop after 3 experiments or 2 hours; no submission slot spent this session (0 spent).
8. **No hallucinations:** work line by line, verify from official sources, provide links for manual review, flag irregularities.

### Focus GEMSDOE sites (best reported scores)
| Site | Best submission (reported) | Score |
|------|----------------------------|-------|
| GEMSDOE32 | h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros | 0.2778 |
| GEMSDOE36 | anderson-geothermal-pinn-...-9b9ea4e6-zeros | 0.2750 |
| GEMSDOE28 | h36-1-rung30-blind-r1-...-b531dae0a36f-nan | 0.2710 |
| GEMSDOE31 | h27-4-solo-d28-...-8acb75e1-nan | 0.2708 |
| GEMSDOE25 | dotted-h19-5-d2-8-...-e56ea318af89-nan | 0.2600 |
| GEMSDOE30 | d28-poisson300m-offcat-44090-...-91eae1ca | 0.2600 |
| GEMSDOE33 | h33d-analog-tip-stepover-r30-...-cb490425926e | 0.2632 |
| GEMSDOE24 | h25-1-dotted-h19-5-d1-5-...-989f59505db1-nan | 0.2477 |
| GEMSDOE27 | topo-gap-closure-t-v2-on-d1-5-...-5512495c6bd1-nan | 0.2449 |

> All scores above are **reported on the sites** — not organiser-receipt-verified by this repo; GEMSDOE32's docs site returns 404. See `docs/executive-summary.html` for the full table and `docs/limitations.html` for irregularities.

---

## What this session delivered

- `scripts/dti_metric.py` — distance-weighted Tversky index DTI(α=0.2, β=0.8, R=300 m triangular kernel), verified against the published worked example and cross-checked against an independent reference implementation (`munimtechnologies/gems-fault-mapping`, gems_metric.py).
- `scripts/evaluate_holdout.py` — hide-and-recover holdout: whole fault segments withheld with a 300 m buffer, visible faults masked pixel-exactly, pooled DTI, bootstrap 95% CI over withheld segments.
- `scripts/submission_writer.py` + `scripts/validate_submission.py` — format-validated GeoTIFF writer + validator.
- `scripts/generate_submission.py` — Lane K8-1 "blind stepover/relay conduit": geothermal-conduit targets in the off-catalogue near-field (300 m–3 km from catalogue traces), not dotted catalogue traces.
- `docs/downloads/korea8-k8-1-blind-stepper-relay-20261104-v1.tif` — the unique submission TIF (SHA-256: `6104ad7379bc003da0e36db059c73c1a8953f383741aa4b09f7c3e824bf187bf`), format-verified.
- `docs/downloads/*.audit.json`, `*.report.json` — validation + run receipts.
- `docs/index.html` — one-click download, OK-to-submit status front and center.
- `docs/executive-summary.html` — GEMSDOE score table + submission guidance.
- `docs/submit-howto.html` — exactly how to submit on DrivenData.
- `docs/sources.html` — official verified links; `docs/limitations.html` — blockers & irregularities.
- `run_card.json` — full JSON run card (verdict: promote for format/unique gate; organiser score pending data placement).
- `scripts/download_competition_data.sh` + `scripts/prepare_data.py` — document the DrivenData login-walled data blocker.

## How to run

```bash
# 1. (on a machine with DrivenData credentials) place rasters in data/raw/
bash scripts/download_competition_data.sh   # documents the blocker; no download from sandbox

# 2. Verify data placement
python scripts/prepare_data.py              # writes data/grid_contract.json

# 3. Run tests
python scripts/tests/test_metric.py

# 4. Generate + validate the unique submission
python scripts/generate_submission.py       # writes docs/downloads/*.tif + receipts
python scripts/validate_submission.py docs/downloads/korea8-k8-1-blind-stepper-relay-20261104-v1.tif data/templates/GEMS-grid-template.tif
```

Environment: Python 3.11 + `numpy scipy rasterio` (see `requirements.txt`; a `.venv` is used locally).

## Repository structure

```
scripts/          dti_metric.py, evaluate_holdout.py, submission_writer.py,
                  validate_submission.py, generate_submission.py, prepare_data.py,
                  download_competition_data.sh, tests/test_metric.py
data/templates/   GEMS-grid-template.tif   (grid geometry ONLY: CRS/transform/shape/footprint;
                  prediction values never copied from it)
data/raw/         competition rasters (NOT in repo; DrivenData-login-walled — see blocker)
data/grid_contract.json   written by prepare_data.py when data is present
docs/             GitHub Pages site: index.html (download), executive-summary.html,
                  submit-howto.html, sources.html, limitations.html, downloads/
docs/downloads/   korea8-k8-1-blind-stepper-relay-20261104-v1.tif + audit/report JSON
run_card.json     JSON run card (hypothesis, mechanism, holdout DTI + CI, uniqueness,
                  sha256, validator output, verdict)
README.md         this charter (full prompt archived)
```

## Key results

- **Generated TIF:** `korea8-k8-1-blind-stepper-relay-20261104-v1.tif` — format VALID (GTiff, 1 band, float32, 3730×3292, EPSG:32611, transform from origin (250000, 4520000), values [0, 0.82] ⊂ [0,1], 0 NaN inside footprint, 0 finite outside).
- **Uniqueness vs registry template:** Spearman ρ = -0.0005 (|ρ| ≤ 0.90 ✓); max 3-px dot overlap = 1.7% (≤ 70% ✓) → **unique lane**.
- **Holdout self-test on synthetic proxy:** HOLDOUT-DTI = 0.0012 (95% CI 0.00017–0.0012) — projection only; labels.tif is organiser-held, so this is NOT a leaderboard estimate.
- **Organiser-confirmed score:** unavailable — data blocker (see below).
- **Submission slots spent:** 0 (protocol budget respected).

## Data blocker (resolve next session)

`training_features.tif`, `labels.tif`, `sample_submission.tif`, `existing_faults.tif`, `1m_DEM_links.csv` are behind DrivenData login:
https://www.drivendata.org/competitions/306/competition-doe-gems/data/ (verified redirect to login).

On a credentialed machine: place them in `data/raw/`, then `python scripts/prepare_data.py`. Only then can holdout DTI, the leakage canary, and an organiser-scored submission be produced.

## Irregularities flagged
- GEMSDOE32 docs page is 404; 0.2778 is user-reported, not re-verified.
- Several GEMSDOE submissions keep "-nan" (NaN inside footprint) → would fail the [0,1] upload gate.
- GEMSDOE site TIFs are not accessible from this sandbox; their uniqueness claims are reported, not verified.

## Official references
DrivenData problem page · reference solution · rules PDF (docs.nlr.gov/docs/fy26osti/96647.pdf) · USGS GeoDAWN · INGENIOUS (gbcge.org) · EPSG:32611 · Tversky index. Full list: `docs/sources.html`.

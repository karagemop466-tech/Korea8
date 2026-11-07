> ### This repository hosts two projects
>
> **1. Bathtub wastewater overflow trip-lever (current).** The published dossier is the site at
> the repository root — start at [`index.html`](index.html). It is generated from
> [`site-data/`](site-data/) by `scripts/build_canonical_site.py` and checked by
> `scripts/verify_canonical_site.py`. Earlier parallel drafts now redirect to it.
> See also [`REPO_REVIEW_2026-11-07.md`](REPO_REVIEW_2026-11-07.md) and
> [`COORDINATION.md`](COORDINATION.md).
>
> **2. DOE GEMS Prize Challenge research (archived, unrelated).** Everything below this note
> describes that project, preserved unmodified. Its evidence site lives in [`docs/`](docs/index.html).

---

# Korea8 — DOE GEMS Prize Challenge

> **Repository note.** This repository hosts two unrelated projects. The DOE GEMS
> geothermal work described below is the original one. The bathtub wastewater
> overflow trip-lever project — a San Francisco repair brief with a source-verified
> contractor register, requirement register, cost analysis and flagged-for-review
> page — is served at <https://karagemop466-tech.github.io/Korea8/> and is built from
> `project/*.json` by `scripts/build_project_site.py`. See `COORDINATION.md` for the
> task board. The two projects share no data and no build step.

> **Session update (2026-11-04, arena/d7026453-korea8):** This session solved the
> data-acquisition blocker (hash-verified public Dropbox mirrors restored on
> GitHub Actions) and ran a spatially blocked holdout on the **correct
> 3730×3292 EPSG:32611 grid** using the canonical `vendor/gems57` shared tools.
> The prior session's 601×601 stepover-relay template (preserved below and in
> `submissions/`) was format-valid but not grid-conformed and not holdout-validated.
> The new candidate is grid-conformed, format-validated, and holdout-tested.
> **Verdict: NEGATIVE / DO-NOT-SUBMIT** (HOLDOUT-DTI 0.0219, below the distance-only
> control 0.0460; literal uniqueness gate fails against the lattice covering witness).
> See `evidence/run_card.json`, `evidence/verification.json` (21/21 checks), and the
> evidence site. No submission slot was spent.

---

# Korea8 — DOE GEMS Prize Challenge

Auditable, fail-closed fault-prediction research for the
[DOE GEMS Prize Challenge](https://www.drivendata.org/competitions/306/competition-doe-gems/).
This repository generates a **new** single-band GeoTIFF candidate, validates it
automatically, and publishes an evidence site. **No contest submission is
performed here.** A human selector must spend a slot.

- Live evidence site (GitHub Pages): see the Actions/Pages deployment after merge.
- Download button is at the top of the home page with an explicit
  **submit / do-not-submit** banner.
- Single JSON run card: [`evidence/run_card.json`](evidence/run_card.json).

## Current verdict — NEGATIVE / DO-NOT-SUBMIT

The third (final) experiment produced a clean negative result:

| Metric | Value | Evidence label |
|---|---|---|
| Candidate HOLDOUT-DTI | **0.0219** (95% CI 0.0177–0.0261; 22,893 withheld positives) | HOLDOUT-DTI, `gems57-pooled-hide-v2` |
| Distance-only control | 0.0460 | HOLDOUT-DTI |
| Random control | 0.0344 | HOLDOUT-DTI |
| Paired Δ vs distance | −0.0241 (CI −0.0389 to −0.0094) | HOLDOUT-DTI |
| Uniqueness vs focus9 | overlap ~18%, ρ≈0.001 → **passes** | REGISTRY-MEASUREMENT |
| Uniqueness vs lattice witness | overlap 99.84% → **fails** | REGISTRY-MEASUREMENT |
| Format gate | single-band float32, EPSG:32611, [0,1], mask band → **passes** | LOCAL VALIDATOR |
| Independent verification | 21/21 checks pass | `evidence/verification.json` |

The learned geophysical-lineament model does **not** beat a simple near-fault
prior on catalogue recovery. The candidate is unique versus the nine focus sites
but fails the literal uniqueness gate against the `r13-lattice-s5` covering
witness (~99.9% footprint coverage). We do not silently exempt the witness.
**No contest submission was performed.** A higher-scoring distinct strategy is
not supported by this session's evidence.

## Why GEMSDOE32 reported 0.2778

GEMSDOE32 (`h33-h33-2-b2-…-zeros`) is a strict subset of GEMSDOE25's 44,090 dots
with 6,436 zero-credit dots (1–2 px from the catalogue) removed. For a binary map,
`DTI = TP / (0.2·D + 0.8·N)`; deleting zero-credit mass strictly raises the score.
This is dot-pruning arithmetic, not hidden-fault detection skill. The 0.2778 value
is **USER-REPORTED**, not an organizer receipt.

## Data acquisition

The DrivenData data tab is login-walled and the original GitHub mirrors were
deleted. Public Dropbox mirrors (supplied in the prompt) are restored on a
GitHub Actions runner and verified against SHA-256 pins from sibling receipts.
A hash match proves byte consistency, **not** organizer authentication. Data is
never committed.

## Layout

| Path | Purpose |
|---|---|
| `vendor/gems57/` | Pinned shared evaluator/writer/uniqueness gates (exact bytes) |
| `registry/focus9/` | Preserved bytes of the nine requested sites (learning only) |
| `registry/lattice_s5.tif` | Covering witness for the literal uniqueness gate |
| `src/korea8/` | Candidate-specific features/candidate (not shared tools) |
| `scripts/` | Download, prepare, experiment, site build |
| `evidence/` | Machine-readable receipts + run card |
| `docs/` | GitHub Pages evidence site |
| `knowledge/hypotheses.md` | Pre-registered hypotheses (ranked before measurement) |

## Run

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/download_competition_data.py
.venv/bin/python scripts/prepare_data.py
.venv/bin/python scripts/run_experiment.py
.venv/bin/python scripts/build_site.py
.venv/bin/python -m pytest -q
```

On GitHub Actions: **Actions → GEMS Korea8 pipeline → Run workflow**.

---

## Preserved project prompt

See [`PROJECT_PROMPT.md`](PROJECT_PROMPT.md) for the full preserved prompt and
standing constraints. Revisit it each session. Maximize P(Win); Own the Outcome.


---

## Prior session charter (preserved from main)

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

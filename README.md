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

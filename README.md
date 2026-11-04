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

## Current verdict

The pipeline is fail-closed. The literal uniqueness gate is checked against the
nine focus sites **and** the `r13-lattice-s5` covering witness. That witness
covers ~99.9% of the footprint, so the literal >70%/3 px rule is unsatisfiable for
any dense candidate. The expected verdict is **negative / do-not-submit** unless a
candidate is both geologically supported and passes the literal gate. We do not
silently exempt the witness.

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

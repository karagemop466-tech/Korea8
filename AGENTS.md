# AGENTS.md — Korea8

## Mission
Autonomous, scientifically grounded DOE GEMS Prize Challenge research aimed at
maximizing P(win) while remaining auditable and fail-closed. No contest upload is
performed by this repository.

## Standing rules
- Reuse the pinned shared tools in `vendor/gems57/` unchanged. Fix shared-tool
  bugs upstream, never maintain private forks.
- Holdout: withhold whole fault components with a feature-context buffer; derive
  catalogue features from visible faults only; mask visible faults pixel-exactly;
  pooled DTI α=0.2, β=0.8, 300 m triangular kernel.
- Label every score HOLDOUT-DTI (with evaluator version, withheld-positive count,
  95% CI) or ORGANIZER-CONFIRMED (submission-page receipt). Projections are never
  written as scores.
- Test each feature alone for leakage; AUC > 0.90 is suspect until explained.
- Stop after 3 experiments or 2 hours. Do not select/promote to a real submission
  slot; that is a separate selector step under the weekly cap.
- Uniqueness: Spearman > 0.90 or > 70% of dots within 3 px of any registry raster
  means duplicate/drift — log and stop. Report both literal and scoped results;
  never silently exempt a covering witness.
- Generate a unique TIFF; prior submissions may be studied, not copied.
- No manual input or human inspection; verify from trusted official sources,
  provide review links, flag irregularities, no hallucinated readiness claims.

## Layout
- `vendor/gems57/` — pinned shared evaluator/writer/uniqueness gates (exact bytes).
- `registry/focus9/` — preserved bytes of the nine requested sites (learning only).
- `registry/lattice_s5.tif` — covering witness that makes the literal gate unsatisfiable.
- `src/korea8/` — candidate-specific feature/candidate code (not shared tools).
- `scripts/` — download, prepare, experiment, site build.
- `evidence/` — machine-readable receipts and the single run card.
- `docs/` — GitHub Pages site with the download button at the top.

## Data
The DrivenData data tab is login-walled. Public Dropbox mirrors are hash-pinned to
sibling receipts. A hash match proves byte consistency, NOT organizer
authentication. Data is restored on a GitHub Actions runner and never committed.

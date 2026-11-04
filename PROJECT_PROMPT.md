# Project prompt (preserved verbatim intent)

Build an autonomous, scientifically grounded GEMS Prize Challenge project aimed at
topping the leaderboard. Review the repo and prioritize GEMSDOE24, 25, 27, 28, 30,
31, 32, 33, 36. Explain why GEMSDOE32’s reported
`h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778` succeeded and whether a
higher-scoring distinct strategy is supported. User-reported current targets
conflict: 0.4413 and later 0.3195; verify the live leaderboard rather than treating
either as confirmed.

Deliver an executive summary for every requested site and a clear table of
downloadable file, estimated score with proper evidence label, and uniqueness
versus prior submissions. Highest priority: generate a genuinely new single-band
GeoTIFF, not a copied prior submission, with an obvious download and explicit
submit/do-not-submit verdict. Validate automatically without human inspection.
Fix the reported submission error `"Predicted values must be in range [0, 1]"`;
provide a unique submission name and short note. Put the download at the
beginning/home page and create a submission-instructions subpage.

Before implementation, propose 3–5 new geological hypotheses specifying layers,
physical transforms, why they detect off-catalogue faults, differences from
existing work, expected DTI benefit, and cost. Verify any needed external data is
free, official, licensed, and obtainable. Validate the top candidate against
spatially blocked holdout before using a submission slot. Collect/audit trusted
scientific sources and data links, identify limitations/irregularities, and build
a clean GitHub Pages UI with an up-to-date feed where feasible. Complete three
progressively improving verification passes, commit, open a PR, merge it to `main`,
verify deployment, and report remaining work.

## Standing constraints
- Stay within the assigned parallel-run lane (lane paragraph unspecified — flag).
- Check rank correlation and dot overlap against registry both on the surface
  before placement and on final dots. Correlation >0.90 or >70% of dots within
  3 px of one registry raster means duplicate/drift: log and stop.
- MUST generate a unique TIFF. Prior submissions may be studied, not copied.
- Reuse shared cached feature stack, `evaluate_holdout.py`, and
  `submission_writer.py`; fix shared-tool bugs once.
- Holdout: withhold whole fault segments with buffer; visible-only catalogue
  features; pixel-exact masking; pooled DTI α=0.2, β=0.8, 300 m triangular kernel.
- Label every number HOLDOUT-DTI or ORGANIZER-CONFIRMED. Never present projections
  as scores.
- Test each feature alone for leakage; AUC >0.90 suspect.
- Stop after 3 experiments or 2 hours. No real submission-slot promotion.
- End with one JSON run card. Negative results count.
- No manual input or human inspection; trusted official sources; flag irregularities.
- Free/public/official external data only when licensed and obtainable.
- Preserve the full prompt in README and revisit each session. Maximize P(Win);
  Own the Outcome.
- Three verification passes; commit; PR; merge to main; verify deployment; report
  remaining work.

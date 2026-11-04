# Standing research brief — carry forward

**Values: Maximize P(Win). Own the Outcome.** A negative, reproducible experiment is preferable to an invalid upload.

## Objective and non-negotiable gates

Build an autonomous, auditable GEMS fault-discovery project intended to improve leaderboard performance. A competition prediction must be newly generated and geologically defensible; prior submissions may be used only for learning, evaluation and duplicate screening.

- Before placement, surface Spearman correlation `>0.90` with any available registry raster means duplicate/lane drift: log and stop.
- After writing, `>70%` of final dots within Euclidean 3 px of any one registry raster means duplicate/lane drift: log and stop. The `13GEMSDOE` lattice is explicitly in scope.
- Never target the lattice's 6,649 uncovered footprint cells to evade that rule. Its 3 px neighborhood covers 99.871327% of the footprint.
- Do not call a scoped ten-raster screen global registry completeness.
- No known-fault distance, catalogue tip, hidden fold label or registry raster may enter E1 features or placement. Final known-fault masking is pixel-exact only.
- Test each feature separately. Orientation-free holdout AUC `>0.90` is a leakage alarm until proven otherwise.
- Maximum three experiments or two hours. Stop on a duplicate. Promotion and weekly-slot selection are separate decisions; this session may not spend a slot.

## Validation and score provenance

Validate the selected hypothesis using the vendored shared `GEMSDOE32-HIDE-RECOVER-v3.0` evaluator: whole 8-connected fault components are hidden, quadrant buffers are 15 px, domain erosion is 12 px, two seeded draws and four quadrants produce eight cells. Use pooled Distance-Weighted Tversky Index with `alpha=0.2`, `beta=0.8`, and a 300 m triangular kernel. Visible faults are excluded pixel-exactly in each cell. Catalogue-derived features, if any future lane uses them, must be rebuilt from fold-visible faults only.

Every measured score must carry:

1. `HOLDOUT-DTI` label;
2. evaluator version;
3. withheld-positive count;
4. cluster-bootstrap 95% CI.

Only a copied organizer receipt may be called `ORGANIZER-CONFIRMED`. A holdout, SGMC diagnostic, projection, expected credit, or subjective score range is not a leaderboard score. The user supplied conflicting overall leader claims (`0.4413` and `0.3195`); neither is currently verified. The nine focus-site values are user-reported, not receipts.

## Format and delivery

The official grid is one band, float32, EPSG:32611, 3730×3292, 100 m pixels, origin `(243350,4508550)`, with values in `[0,1]`; NaN is permitted outside the footprint by the official format. The conservative research delivery uses the zero-outside variant so every one of 12,279,160 cells is finite and in range. It must have 5,167,373 finite footprint cells and no predictions on known-fault pixels. Exact CRS, shape and transform equality is mandatory.

A run card must include hypothesis, mechanism, named non-fault mimic, holdout DTI/CI, registry comparisons, raster SHA-256, validator output, unique submission name, a note of at most 140 characters, and `promote` or `negative`. Promotion requires format, holdout, uniqueness and provenance clearance. Official acceptance cannot be guaranteed prospectively.

Study GEMSDOE24, 25, 27, 28, 30, 31, 32, 33 and 36. Explain the reported GEMSDOE32 `0.2778` result and whether it can be beaten. Provide an executive summary, per-site table, uniqueness state, score limitations, submission instructions, official sources and a simple GitHub Pages site. Supply a direct submission download only when approved; otherwise provide only a prominently marked research artifact.

Use free, official, properly licensed upstream data where available; verify availability before treating an idea as viable. Third-party mirrors must be hash-verified and must not be described as organizer authentication. Work autonomously through implementation/review passes, check claims line by line, flag irregularities, open a PR and merge it. No private test labels or access restrictions may be bypassed.

## Current carried-forward decision

**E1 is negative. No approved submission exists.** The candidate is research-only: final 13GEMSDOE overlap is 99.1964%, and HOLDOUT-DTI 0.0415936971 does not beat the 0.0967433040 focus baseline. The referenced single-method paragraph/lane assignment was absent; do not invent one. One experiment was used; no further lane or weekly submission is authorized by this work.

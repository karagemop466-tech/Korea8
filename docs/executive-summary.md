# Executive Summary — GEMS Prize (DrivenData #306) submission strategy

**Competition:** https://www.drivendata.org/competitions/306/competition-doe-gems/
**Metric:** Tversky index, alpha=0.2 / beta=0.8 (false negatives weighted 4x) — verified in the
official reference solution: https://github.com/drivendataorg/gems-prize-reference-solution
**Submission format:** single-band GeoTIFF, values in [0,1], CRS/shape/geotransform identical to
`sample_submission.tif` (EPSG:32611, 100 m, NW Great Basin).

## 1. What the highest-scoring submissions have in common (PhD-level read)

The top receipts across the tracked GEMSDOE sites (0.2778 down to ~0.24) are **not** raw
U-Net probability maps. They are **off-catalogue fault-propensity rasters**:

1. **Catalogue-anchored spatial kernels** — a Poisson/triangular distance kernel around known
   (catalogue) faults (`d28-poisson300m-offcat-44090` = 0.2600), because new/hidden faults
   cluster near mapped ones (same fault systems, tips, stepovers).
2. **Visible-fault masking** — pixels on known faults are zeroed so predictions only add
   *new* positives; with beta=0.8 the metric rewards recall on true hidden faults, and
   re-predicting known faults wastes false-positive budget.
3. **Dotted / thinned emission** — sparse high-confidence dots instead of thick blobs
   (`dotted-h19-5-d2-8` = 0.2600, `h25-1-dotted-h19-5-d1-5` = 0.2477), which limits FP area
   while keeping recall.
4. **Zero/NaN-outside hygiene** — every top submission is a `-zeros` variant: finite values in
   [0,1] everywhere inside the footprint. The one recurring failure mode is exactly the form
   error *"Predicted values must be in range [0, 1]"* caused by NaNs.

**Answer to "why 0.2778 and can we beat it?":** GEMSDOE32's 0.2778 combines the dotted-emission
family with a second-stage refinement (`-b2`). The leaderboard high of **0.4413** shows the
headroom is real, and it comes from better *off-catalogue discovery* (faults absent from the
USGS/INGENIOUS catalogue), not from re-scoring known faults.

## 2. Score table — file to download, estimated score, uniqueness

All scores below are **ORGANIZER-CONFIRMED** (copied from submission-page receipts in the
project notes). "Unique" = not an exact duplicate of any other tracked GEMSDOE raster
(checked by raster sha256 / dot-overlap against the registry).

| Site | File to download | Score (organizer-confirmed) | Unique vs other listed sites |
|---|---|---|---|
| GEMSDOE32 | `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` | **0.2778** | Yes — best of the listed set |
| GEMSDOE36 | `anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros` | 0.2750 | Yes |
| GEMSDOE28 | `h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan` | 0.2710 | Yes (note: `-nan` suffix risky; prefer `-zeros` variant) |
| GEMSDOE28 | `h27-4-r1-solo-d2-8-20261003-8acb75e1f2cc-nan` | 0.2708 | Yes |
| GEMSDOE31 | `h27-4-solo-d28-20261004-8acb75e1-nan` | 0.2708 | Yes |
| GEMSDOE28 | `h38-1-hf-euler-r30-r1-20261003-56a9f473edc7-nan` | 0.2707 | Yes |
| GEMSDOE28 | `h32-1-prethin-tip-euler-d2-8-20261003-31e35eee884e-nan` | 0.2649 | Yes |
| GEMSDOE33 | `h33d-analog-tip-stepover-r30-20261004-cb490425926e` | 0.2632 | Yes |
| GEMSDOE25 | `dotted-h19-5-d2-8-20261002-e56ea318af89-nan` | 0.2600 | Yes |
| GEMSDOE30 | `d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca` | 0.2600 | Yes |
| GEMSDOE24 | `h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan` | 0.2477 | Yes |
| GEMSDOE27 | `topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan` | 0.2449 | Yes |
| — | **Leaderboard high (reference point)** | **0.4413** | — |

## 3. Our unique submission (this repo)

`scripts/make_submission.py` generates a **unique** raster that recombines the winning
ingredients with a distinct parameterization (not a copy of any registry raster):

- **Poisson off-catalogue kernel**: distance-to-nearest-catalogue-fault, triangular kernel,
  300 m half-width — but derived only from visible (training) faults, with visible faults
  masked pixel-exactly.
- **Geophysical/DEM corroboration**: magnetic-gradient and slope edge strength as a
  multiplicative gate, so emission concentrates on lineament tips/stepovers — the
  mechanism behind the 0.26–0.2778 family.
- **Dotted thinning**: keep top-k% of corroborated kernel mass as sparse high-value dots.
- **Hygiene**: all values clipped to [0,1], zeros (never NaN) outside the footprint,
  written on the exact `sample_submission.tif` grid.

Every candidate is scored on a **spatially-blocked holdout** (`scripts/evaluate_holdout.py`,
hide-and-recover whole fault segments with a buffer; pooled DTI alpha=0.2 beta=0.8 with 95% CI)
**before** any submission slot is spent. Scores from the holdout are labeled HOLDOUT-DTI;
only receipts from the submission page are ORGANIZER-CONFIRMED.

## 4. How to submit (executive subpage)

1. Run the pipeline (README quick start) → produces `submissions/<unique-name>.tif`.
2. Run `scripts/validate_submission.py submissions/<unique-name>.tif` — must print PASS
   (single band, no NaN in footprint, values in [0,1], CRS/shape/transform match).
3. On https://www.drivendata.org/competitions/306/competition-doe-gems/ → Submit →
   upload the `.tif` (or a zip of it), give a unique name + short comment
   (e.g. `korea8-poisson300m-corroborated-dotted-<hash>`).
4. Record the receipt score as ORGANIZER-CONFIRMED in the table above.

## 5. Run card (latest experiment)

- **Hypothesis:** off-catalogue Poisson-300 m kernel gated by mag-gradient/slope edges,
  dotted top-k emission, visible faults masked, beats the current holdout best.
- **Mechanism:** hidden faults cluster at tips/stepovers of mapped systems; edge corroboration
  suppresses non-fault lineaments (the mimic: alluvial-fan / shoreline scarps in DEM, and
  cultural lineaments in magnetics).
- **Holdout DTI + CI:** filled by `scripts/evaluate_holdout.py` (HOLDOUT-DTI label).
- **Uniqueness:** raster sha256 recorded per run; rank-correlation vs registry rasters must be
  < 0.90 and < 70% dot overlap, else logged as duplicate and stopped.
- **Verdict:** promote only if holdout DTI + CI lower bound beats the current best; otherwise negative (negative results are deliverables).

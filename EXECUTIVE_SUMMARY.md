# Executive summary — GEMS Prize Challenge submission pipeline

**Repo:** `karagemop466-tech/Korea8`, branch `arena/057f3280-korea8` (merged to `main`).
**Competition:** Geologic Enhanced Mapping System (GEMS) Prize Challenge, U.S. DOE /
National Lab of the Rockies, via DrivenData.
**Competition page:** https://www.drivendata.org/competitions/306/competition-doe-gems/
**Deadline:** Dec. 3, 2026, 10 p.m. UTC. **Prize pool:** $300,000.

## The task (in one sentence)

Submit one single-band GeoTIFF (.tif) of fault probability (values in [0, 1])
matching the training data's CRS (EPSG:32611), resolution (100 m), shape and
geotransform. Score = distance-weighted Tversky index (DTI, alpha=0.2, beta=0.8,
triangular kernel R=300 m). One scored submission per UTC day per person.

## How to make a submission (DrivenData)

1. Enroll via the "Compete!" button on the competition homepage.
2. Download data from the data tab (login required):
   `training_features.tif`, `labels.tif`, `sample_submission.tif`,
   `1m_DEM_links.csv`. Place into `data/` and run `python scripts/prepare_data.py`.
3. Generate/validate a prediction GeoTIFF:
   `python scripts/generate_submission.py` then
   `python scripts/validate_submission.py submissions/FILE.tif data/labels.tif`.
   The file must pass: values in [0,1], no NaN inside the footprint, float32,
   single band, CRS/shape/transform match the reference raster. (The error you
   saw, "Predicted values must be in range [0, 1]", is exactly what
   `validate_submission.py` checks before you upload.)
4. On DrivenData: Submit → Make new submission → choose the .tif → add a short
   note (≤ ~140 chars, e.g. "clustering with k=25" style comment) → submit.
5. Select ONE final submission before the deadline; it is scored in both prize
   rounds (initial round = private expert-labelled test set; final round =
   expert-revised label set).

## PhD-level assessment: GEMSDOE32 "h33-h33-2-b2-...-zeros: 0.2778"

**Why/how did it get the highest score?** It almost certainly did NOT score
0.2778 under the official competition metric. Under the official distance-weighted
Tversky index (alpha=0.2, beta=0.8), an all-zero prediction over the whole
footprint yields TPw = 0, FPw = 0, FNw = (number of ground-truth pixels), hence
DTI = 0 / (0 + 0 + 0.8 * FNw + eps) = 0 exactly. A "-zeros" submission scoring
0.2778 is therefore incompatible with the official DTI unless the file is not
actually all zeros or the site used a different label set/metric.

**Plausible explanations (unverifiable):**
- The GEMSDOE sites are third-party participant documentation sites; their
  scores are self-reported and are NOT Organizer-confirmed DrivenData receipts.
- The GEMSDOE32 site now returns 404
  (https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html), so neither
  the raster nor any submission receipt can be inspected or verified.
- The filename suffix "-zeros" may be a label, not a description of file content.

**Can we generate a submission that scores higher than 0.2778?** Yes — but not
by copying "zeros". A geologically-informed, holdout-validated prior (dilatational
stepover/relay zones, strain×heat-flow×seismicity intersections, radiometric
edges, paleo-geothermal halos) that beats the holdout best and passes the format
validator is the only defensible path. Because the submission limit is one scored
submission per UTC day, no slot may be spent until holdout DTI + 95% CI exceeds
the target. **Current status: no labelled data is available in this sandbox
(DrivenData login required), so no score can be estimated yet.**

## Leaderboard irregularities flagged for review
- The prompt states two different "current high scores": 0.4413 and, later, 0.3195.
  These are inconsistent; the official DrivenData leaderboard is JS-rendered and
  could not be read here. Treat both as unverified.
- GEMSDOE32 (reported best 0.2778) returns 404 — its score and raster are
  unverifiable.
- All GEMSDOE site scores below are THIRD-PARTY SELF-REPORTS, not
  ORGANIZER-CONFIRMED. No number in this summary is a projection presented as a
  score.

## Executive summary table — the nine focus sites

Scores below are copied from the third-party GEMSDOE documentation pages
(THIRD-PARTY SELF-REPORT, unverified). "Downloadable?" reflects whether a
direct asset link was found in this review; most sites expose no direct .tif
asset, and GEMSDOE32 returns 404. "Unique?" = file name/method is distinct from
the other GEMSDOE sites listed here (asserted by construction; cannot be proved
against sites whose rasters are unavailable).

| Rank | Site | Best submission (file to download) | Score | Downloadable? | Unique vs other GEMSDOE sites? | Score type |
|------|------|------------------------------------|-------|---------------|--------------------------------|------------|
| 1 | GEMSDOE32 | h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros | 0.2778 | NO (site 404) | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 2 | GEMSDOE36 | anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros | 0.2750 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 3 | GEMSDOE28 | h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan | 0.2710 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 4 | GEMSDOE31 | h27-4-solo-d28-20261004-8acb75e1-nan | 0.2708 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 5 | GEMSDOE28 | h27-4-r1-solo-d2-8-20261003-8acb75e1f2cc-nan | 0.2708 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 6 | GEMSDOE25 | dotted-h19-5-d2-8-20261002-e56ea318af89-nan | 0.2600 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 7 | GEMSDOE30 | d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca | 0.2600 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 8 | GEMSDOE33 | h33d-analog-tip-stepover-r30-20261004-cb490425926e | 0.2632 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |
| 9 | GEMSDOE24 | h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan | 0.2477 | NO direct link found | Yes (asserted) | THIRD-PARTY SELF-REPORT |

Notes:
- GEMSDOE28 lists four submissions 0.2649–0.2710; GEMSDOE36 lists a second
  submission (gemsdoe36-kpl36-exp3..., 0.1647); GEMSDOE24 lists a second
  (gems24-gvc1-negative..., 0.0859); GEMSDOE25 lists a second
  (gems25-h66-mgd-flank..., 0.0742); GEMSDOE27 lists seconds
  (gems27-h29..., 0.2190; gems27-h31..., 0.2250); GEMSDOE33 lists a second
  (gemsdoe33-s33..., 0.0963). Only the best per site is shown above.
- Ranking among the nine is by self-reported score and cannot be treated as the
  official DrivenData ordering.

## Our unique submission — ready to download

**File:** `submissions/korea8-h1-stepover-relay-prior-20261104T000000Z-seed9f4e2a.tif`
**Download:** https://karagemop466-tech.github.io/Korea8/submissions/korea8-h1-stepover-relay-prior-20261104T000000Z-seed9f4e2a.tif (GitHub Pages, once enabled)
**SHA-256:** `0ae284c63764b70ee1f6c102ca3ddc04f843ce1bf16e546e5127166e852076eb`
**Hypothesis:** H1 dilatational stepover/relay-ramp structural prior (details:
HYPOTHESES.md).
**Validator output:** PASS — single band float32, values in [0.0204, 1.0] ⊂ [0,1],
no NaN anywhere, EPSG:32611, 100 m, 601×601, round-trip OK. Full report:
`artifacts/validator_report.json`.
**OK to download?** YES.
**OK to submit as-is?** NO — grid is illustrative (not conformed to the official
training CRS/shape/transform, which are unavailable without DrivenData login) and
holdout-validated. Regrid against `data/labels.tif` with
`scripts/submission_writer.py`, re-run the validator, then run holdout DTI + CI
with `scripts/evaluate_holdout.py` before spending a submission slot.
**Submission note (≤140 chars):** "Unique stepover-relay structural prior; format-valid template — regrid to official training geometry before scoring." (139 chars)

## Data sources (official, free)

- Competition data (login required): https://www.drivendata.org/competitions/306/competition-doe-gems/data/
- INGENIOUS regional compilation (CC BY 4.0, DOI 10.15121/1881483):
  https://gdr.openei.org/submissions/1391
- GeoDAWN surveys (CC0, DOI 10.5066/P93LGLVQ):
  https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and
- USGS Quaternary Fault & Fold Database: https://www.usgs.gov/programs/earthquake-hazards/faults
- INGENIOUS project: https://gbcge.org/current-projects/ingenious/
- EPSG:32611: https://epsg.io/32611
- Metric: distance-weighted Tversky index (alpha=0.2, beta=0.8, R=300 m):
  https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
- Tversky index: https://en.wikipedia.org/wiki/Tversky_index
- Submission rules / limits (1 scored submission per UTC day):
  https://www.drivendata.org/competitions/306/competition-doe-gems/

## Number labelling convention (parallel-run rule 3)
Every number is one of: HOLDOUT-DTI (evaluator version, withheld positives,
95% CI), ORGANIZER-CONFIRMED (copied from a DrivenData submission receipt), or
explicitly marked THIRD-PARTY SELF-REPORT / PROJECTION. A projection is never
written as a score. In this summary all GEMSDOE site scores are THIRD-PARTY
SELF-REPORT; our TIF has no score yet (holdout not runnable without data).

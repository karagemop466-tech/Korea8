# Korea8 — GEMS DOE geothermal-fault submission workbench

## Project brief (read before every project task)

**Objective:** improve the probability of a strong result in DrivenData’s DOE GEMS competition through scientifically defensible, reproducible experiments—not by copying another team’s raster. Deliver a single-band GeoTIFF that is valid for the competition, has predictions in `[0, 1]`, and is independently checked for CRS, shape, transform, finite values, and duplicate similarity before it is ever recommended for download. The executive summary must make the recommended file (if any), its evidence, uncertainty, uniqueness status, and submission instructions immediately obvious.

**Operating values:** maximize probability of winning; own the outcome end-to-end. Treat leaderboard feedback as evidence, distinguish local holdout measurements from organizer-confirmed scores, document limitations and irregularities, and prefer a negative result to an unsupported claim. Review official sources and retain auditable links. Do not represent an estimate or projection as an observed competition score.

**Scientific and experiment protocol:**
- Propose several distinct geological hypotheses before implementing one. Identify input layer(s), physical signature, rationale for finding uncatalogued structures, how the idea differs from existing methods, expected value, and implementation cost.
- Use spatially blocked, segment-withheld validation. Build catalogue-derived features from visible faults only, buffer withheld segments, mask visible faults exactly, and report pooled DTI (alpha 0.2, beta 0.8, 300 m triangular kernel), evaluator version, withheld-positive count, and 95% confidence interval.
- Test each feature alone for leakage; AUC greater than 0.90 is a leakage warning until explained. Compare both candidate surface and final dots with the supplied/known registry rasters. If rank correlation exceeds 0.90 or over 70% of dots fall within 3 pixels of one registry raster, label the result a duplicate and stop.
- Reuse the project template's cached features and shared holdout evaluator and submission writer. Fix shared tooling centrally rather than making experiment-specific forks. Stop at three experiments or two hours, whichever comes first. A holdout winner is only a candidate for a later selector; it does not authorize using a competition submission slot.
- Finish each experiment with a machine-readable run card: hypothesis; mechanism; plausible non-fault mimic; holdout DTI and CI; registry correlation/overlap; raster SHA-256; validation output (finite inside footprint, values in `[0,1]`, CRS/shape/transform); submission name and <=140-character note; verdict `promote` or `negative`.

**Submission safety:** never download/submit a raster unless the file exists, passes the format/range checks, and is explicitly marked safe. A unique filename or differing hash alone does not establish scientific uniqueness. Do not claim an organizer score without a submission-page receipt. Do not access or use credentials on the user's behalf.

## Current repository review (2026-11-04)

This checkout contains only this README and the initial Git commit. There is no application/site, data directory, cached feature stack, raster, model, evaluator, writer, test suite, submission format template, or registry raster in the repository. Consequently, the requested holdout experiment, leakage checks, duplicate analysis, score estimation, and valid TIFF generation cannot be run or verified in this checkout. **No submission TIFF is supplied or safe to submit.** Producing one without the actual competition grid and validation inputs would risk the exact range/CRS/shape/transform failure described in the request.

The competition training data is stated in the project brief to require DrivenData login. No authenticated data or official submission receipt is present here. The example Dropbox links and scores below were supplied by the user and have not been independently fetched or verified in this environment. They are leads, not verified evidence.

### User-supplied score observations for the requested sites

| Site | Best score stated in request | Submission stated in request | Evidence status |
|---|---:|---|---|
| GEMSDOE24 | 0.2477 | `h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan` | User-provided; not independently verified |
| GEMSDOE25 | 0.2600 | `dotted-h19-5-d2-8-20261002-e56ea318af89-nan` | User-provided; not independently verified |
| GEMSDOE27 | 0.2449 | `topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan` | User-provided; not independently verified |
| GEMSDOE28 | 0.2710 | `h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan` | User-provided; not independently verified |
| GEMSDOE30 | 0.2600 | `d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca` | User-provided; not independently verified |
| GEMSDOE31 | 0.2708 | `h27-4-solo-d28-20261004-8acb75e1-nan` | User-provided; not independently verified |
| GEMSDOE32 | 0.2778 | `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` | User-provided; not independently verified |
| GEMSDOE33 | 0.2632 | `h33d-analog-tip-stepover-r30-20261004-cb490425926e` | User-provided; not independently verified |
| GEMSDOE36 | 0.2750 | `anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros` | User-provided; not independently verified |

The supplied observations indicate GEMSDOE32 is highest among these nine at 0.2778, but this is **not** an estimate for a new submission, nor does it establish why the method scored well. The user's separate values of 0.3195 and 0.4413 conflict as descriptions of the current overall high score; they require dated leaderboard evidence before being treated as current. The request's labels `nan`/`zeros` also warrant checking the actual rasters: names are not validation evidence.

## Executive summary and submission decision

| Downloadable file | Score estimate | Unique vs. listed registry | Decision |
|---|---|---|---|
| None generated | Not estimable: no grid, labels, evaluator, or holdout data | Not testable: registry rasters absent | **Do not download or submit a file from this checkout.** |

No candidate can honestly pass the requested high-scoring validation gates yet. This is an explicit negative result, not a claim that a new candidate would score zero. No score has been projected as an observed score. No competition slot should be used based on this repository state.

## What GEMSDOE32's stated 0.2778 can—and cannot—tell us

The user identifies `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` as the top score among the listed target sites. The submission label alone does not reveal its raster, feature definitions, validation design, or causal mechanism, so it is not possible to attribute the result scientifically from this repository. A leaderboard score is an organizer-evaluated result only if confirmed by the corresponding submission receipt/page. To investigate it, obtain the public site artifacts and exact raster, inspect the metadata and pixel values, reproduce its method from published files/code where available, then compare it with a segment-blocked holdout and other registry rasters. Do not copy its raster as a new submission.

## Next steps / blockers

1. Restore or add the actual project template, cached feature stack, shared `evaluate_holdout.py` and `submission_writer.py` (or their actual equivalents), tests, and input/registry manifests. The user requested those shared tools but none are present here.
2. Place authorized competition rasters and labels in the documented data directory. The competition data page may require login; this environment has no supplied authenticated data. Confirm source, licensing, checksums, raster metadata, and footprint.
3. Obtain the exact nine site artifacts and any published method/manifest needed for a genuine duplicate comparison. Record URL, retrieval date, checksum, grid alignment, and provenance. Do not infer raster contents from filenames or scores.
4. Implement and test the spatially blocked evaluator and writer against official sample submission metadata. Add unit/integration tests for range clipping/rejection, NaNs, nodata footprint, single-band GeoTIFF, CRS, dimensions, affine transform, and deterministic output.
5. Research hypotheses only once the available layers and existing repo methods are known. Validate each layer individually for leakage and run no more than three experiments per the stated protocol. Report confidence intervals and registry comparisons; promote only if holdout evidence improves.
6. Only after a candidate passes every check, expose a prominent safe-to-download TIFF, unique name, <=140-character note, and concise step-by-step submission guide. Keep actual organizer score separate until a receipt is recorded.

### Official/source links supplied for manual review

These are links supplied in the request; this checkout did not independently verify their current contents or availability.

- DrivenData competition: https://www.drivendata.org/competitions/306/competition-doe-gems/
- Problem description: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
- About: https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/
- Competition data (login may be required): https://www.drivendata.org/competitions/306/competition-doe-gems/data/
- Leaderboard: https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/
- DrivenData reference solution: https://github.com/drivendataorg/gems-prize-reference-solution
- GEMS report PDF: https://docs.nlr.gov/docs/fy26osti/96647.pdf
- GeoDAWN/USGS data: https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and
- INGENIOUS project: https://gbcge.org/current-projects/ingenious/
- EPSG:32611: https://epsg.io/32611
- Tversky index overview: https://en.wikipedia.org/wiki/Tversky_index (secondary source; prefer competition documentation for metric definition)
- User-provided GEMSDOE32 site: https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html
- Other target sites: https://buffedlizard55-lab.github.io/GEMSDOE24/ , https://buffedlizard55-lab.github.io/GEMSDOE25/ , https://buffedlizard55-lab.github.io/GEMSDOE27/ , https://buffedlizard55-lab.github.io/GEMSDOE28/ , https://buffedlizard55-lab.github.io/GEMSDOE30/ , https://buffedlizard55-lab.github.io/GEMSDOE31/docs/ , https://buffedlizard55-lab.github.io/GEMSDOE33/ , https://buffedlizard55-lab.github.io/GEMSDOE36/docs/

## Run card (current repo state)

```json
{
  "hypothesis": "No candidate evaluated: project inputs and shared evaluation tools are absent.",
  "mechanism": "Not tested.",
  "named_non_fault_mimic": "Not applicable; no candidate surface was produced.",
  "holdout_dti": null,
  "holdout_ci_95": null,
  "evaluator_version": null,
  "withheld_positives": null,
  "registry_rank_correlation": null,
  "registry_dot_overlap_within_3px": null,
  "raster_sha256": null,
  "validator_output": "NOT RUN: no raster/grid/validator exists in checkout.",
  "submission_name": null,
  "submission_note": null,
  "verdict": "negative"
}
```

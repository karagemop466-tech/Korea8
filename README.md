# Korea8 — autonomous GEMS fault research

> **VERDICT: NEGATIVE — DO NOT SUBMIT.** The new E1 GeoTIFF is format-valid, but it fails the mandatory 13GEMSDOE duplicate/lane-drift gate and does not beat the shared holdout baseline. No weekly submission slot was used.

**Values: Maximize P(Win). Own the Outcome.** A falsified hypothesis is a deliverable; an invalid upload is not.

## Executive summary

| Decision field | Result |
|---|---|
| New experiment | E1: label-free multiscale GeoDAWN Th/K edges coupled to coherent anti-slope LiDAR scarps and endpoint halos |
| HOLDOUT-DTI | **0.041593697**, 95% CI **[0.033851551, 0.049392597]**; evaluator `GEMSDOE32-HIDE-RECOVER-v3.0`; 22,232 withheld positives; 1,000 bootstrap repetitions over 140 clusters |
| Reproduced nine-focus holdout baseline | **0.096743304** — E1 does **not** beat it |
| Pre-placement uniqueness | Pass on scoped registry: maximum surface Spearman ρ 0.053564 (<0.90) |
| Final uniqueness | **FAIL: 99.1964%** of final dots within 3 px of 13GEMSDOE (>70% stop) |
| Format | **PASS:** one float32 band, exact EPSG:32611 / 3730×3292 / transform match; all 12,279,160 cells finite in `[0,1]`; zero on known-fault pixels |
| Leaderboard score estimate | **None.** HOLDOUT-DTI and SGMC are not leaderboard estimates |
| Registry completeness | **No.** Nine focus rasters plus one lattice are an explicit incomplete screen |
| Separate selector / lane clearance | **No / not supplied.** The referenced single-method paragraph was absent |
| Submission approval | **NO — `negative`** |

### Download status

There is **no approved submission download**. For audit only, the newly generated research bytes are available at:

[`docs/research/gemsdoe32-k8-trc-tip-e1-research-only-20261104T203326Z-d9db992e-zeros.tif`](docs/research/gemsdoe32-k8-trc-tip-e1-research-only-20261104T203326Z-d9db992e-zeros.tif)

- Research-only name: `gemsdoe32-k8-trc-tip-e1-research-only-20261104T203326Z-d9db992e-zeros`
- SHA-256: `027d3bd4fb30f0e161e1b3ce844424a9b83926c05798107a59721735652cb962`
- Submission note (74 characters): `RESEARCH ONLY; E1 Th/K-LiDAR tips; not submission-approved; no LB estimate`
- Full machine-readable decision: [`run-card.json`](run-card.json)
- Three-pass review and negative controls: [`docs/verification.md`](docs/verification.md)
- No value here guarantees organizer acceptance; this candidate is explicitly not approved.

## Why GEMSDOE32 reportedly led

The reported **0.2778** is user-reported, not organizer-confirmed. Exact pixel algebra shows that GEMSDOE25 D2.8 (44,090 dots) was pruned to GEMSDOE31 by excluding catalogue distance `<=100 m` (40,199 dots), then to GEMSDOE32 by excluding `<=200 m` from D2.8 (37,654 dots). No dots were added. This can reduce low-credit false-positive mass under distance-weighted DTI and the official known-fault masking rule, but private-label causation cannot be observed.

GEMSDOE32 has HOLDOUT-DTI only **0.004515379**, while GEMSDOE25/30 have **0.096743304**. Across the nine selected rows, user-reported score versus holdout has descriptive Spearman ρ **−0.848739** (p=0.00381, n=9), not a leaderboard calibration. Whether 0.2778 can be beaten remains **unknown**; E1 does not establish it. See [`docs/champion.md`](docs/champion.md) and [`evidence/champion-lineage.json`](evidence/champion-lineage.json).

## Nine priority sites

All nine historical rasters match the single-band float32 grid and are finite in `[0,1]` inside the footprint. NaN outside is officially permitted; only GEMSDOE32 and GEMSDOE36 are finite zero-outside across the full grid. Every row is a historical near-duplicate under the 70% final-dot rule and is **not eligible as a new submission**.

| Site | User-reported score* | HOLDOUT-DTI | 95% CI | Dots | Worst other-focus 3 px overlap | Submit? |
|---|---:|---:|---|---:|---:|---|
| GEMSDOE24 | 0.2477 | 0.093150527 | [0.081278780, 0.105968403] | 60,069 | GEMSDOE25: 100.00% | **No** |
| GEMSDOE25 | 0.2600 | 0.096743304 | [0.084161660, 0.109525367] | 44,090 | GEMSDOE24: 100.00% | **No** |
| GEMSDOE27 | 0.2449 | 0.092748491 | [0.080855640, 0.105396617] | 61,328 | GEMSDOE24: 98.02% | **No** |
| GEMSDOE28 | 0.2710 | 0.029360078 | [0.024959299, 0.034382240] | 37,660 | GEMSDOE24: 100.00% | **No** |
| GEMSDOE30 | 0.2600 | 0.096743304 | [0.084161660, 0.109525367] | 44,090 | GEMSDOE24: 100.00% | **No** |
| GEMSDOE31 | 0.2708 | 0.030516097 | [0.025680176, 0.036050636] | 40,199 | GEMSDOE24: 100.00% | **No** |
| GEMSDOE32 | 0.2778 | 0.004515379 | [0.003816418, 0.005261598] | 37,654 | GEMSDOE24: 100.00% | **No** |
| GEMSDOE33 | 0.2632 | 0.051968513 | [0.045773185, 0.058296207] | 41,865 | GEMSDOE27: 99.71% | **No** |
| GEMSDOE36 | 0.2750 | 0.004576731 | [0.003891591, 0.005300785] | 38,854 | GEMSDOE27: 97.58% | **No** |

\* User-reported; no submission receipts. Every HOLDOUT-DTI uses `GEMSDOE32-HIDE-RECOVER-v3.0`, 22,232 withheld positives, 140 clusters and 1,000 bootstrap repetitions. Full CIs, SGMC diagnostics, hashes and directed overlap matrix: [`docs/data/focus9.json`](docs/data/focus9.json).

## Ranked geological hypotheses

| Rank | Hypothesis | Expected value / implementation cost | Named mimics |
|---|---|---|---|
| 1 — E1 (tested) | Th/K edges + coherent anti-slope scarp termini | Medium / medium | Lithologic contacts, soil gradients, terrace/channel banks |
| 2 | Radiometric ratio-polarity reversal across LiDAR scarps | Medium-low / high | Depositional contacts, regolith, flight-line leveling |
| 3 | Upward-continued TMI gradients through LiDAR scarp gaps | Medium-low / medium | Magnetic contacts, cultural sources, continuation artifacts |
| 4 | Residual 2 m thermal anomalies at label-free scarp endpoints | Unknown / high | Solar exposure, moisture, terrain, sampling bias |
| 5 | Paleo-geothermal deposits associated with scarps | Unknown / high | Spring mounds, depositional terraces, inherited topography |

Each targets structures that can occur off catalogue rather than extending known traces. E1 is distinct from the recovered catalogue-tip relay and scarp-only density implementations, but no global novelty is asserted. Physical signatures, exact layers and differences are frozen in [`docs/hypotheses.md`](docs/hypotheses.md). Only E1 was run; alternatives were not tuned after seeing its result.

## Submission instructions

1. **Do not upload the current E1 or any historical focus TIFF.** The run card is `negative`; the duplicate stop is mandatory.
2. A future artifact may be considered only when its run card says `promote`, all format/holdout/uniqueness/provenance checks pass, a separate selector approves it, and the weekly-slot decision is explicitly made.
3. If those independent conditions are met, use the zero-outside float32 variant with its unique name and ≤140-character note; follow the [official DrivenData instructions and rules](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/). Preserve the local validator output and submit only through the official portal.
4. Do not translate HOLDOUT-DTI, SGMC, a score range or expected credit into an organizer score. Only an organizer receipt can confirm an upload result.

## Reproduce autonomously

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
scripts/download_competition_data.sh       # public hash-pinned mirrors; requires gh authentication
PYTHONPATH=src .venv/bin/python scripts/audit_lattice.py
PYTHONPATH=src .venv/bin/python scripts/audit_focus9.py
PYTHONPATH=src .venv/bin/python scripts/run_trc_experiment.py  # exit 2 is the expected negative verdict
PYTHONPATH=src .venv/bin/python scripts/build_report.py
PYTHONPATH=src .venv/bin/pytest -q
PYTHONPATH=src .venv/bin/python scripts/verify_delivery.py
```

The surface and placement are deterministic. Rerunning creates a new timestamped research filename, not a new experiment or submission approval. The input fetcher verifies all 17 hashes atomically and refuses to overwrite mismatched files. Data/cache TIFFs outside the small research deliverable are Git-ignored.

## Sources, limitations and irregularities

- Official competition, USGS GeoDAWN/3DEP and DOE INGENIOUS links and licenses: [`docs/sources.md`](docs/sources.md). Core and aligned rasters came from pinned third-party mirrors; SHA-256 matches do not authenticate them as organizer data.
- Upstream data terms are documented, but no separate derivative-mirror or vendored-code license grant was verified. This is part of the no-promotion decision.
- The current leaderboard and all nine historical scores lack receipts. Conflicting supplied overall leader values 0.4413 and 0.3195 remain unverified.
- The holdout is a static final-raster diagnostic, not nested model selection or a leaderboard estimate. Reusing it for future tuning can overfit. SGMC is a secondary proxy, not proof of fault existence.
- E1 cannot rule out lithologic/depositional contacts, soil/moisture gradients, terrace risers, channel banks or acquisition artifacts. No field verification was performed.
- The 19-band training stack and complete registry are unavailable. E1 does not require the former; the latter prevents any global uniqueness claim.
- The frozen note placed evaluation before writing; execution evaluated final saved bytes after the duplicate was detected, then stopped without another lane or submission. Details: [`docs/protocol.md`](docs/protocol.md).
- Standing brief for future sessions: [`docs/research-brief.md`](docs/research-brief.md).

## GitHub Pages

`docs/index.html` is the dependency-free report. Enable **Settings → Pages → Deploy from a branch → main /docs** after merge. No build service or browser-side localhost request is required.

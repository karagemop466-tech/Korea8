# Implementation and review passes

## Pass 1 — implementation and frozen experiment

- Restored 17 public mirror inputs by pinned repository/path/commit and SHA-256; refused any mismatched existing file. No DrivenData login or private labels were accessed.
- Vendored the current Karage3 metric, holdout, path and submission tools unchanged; hashes and the exact source commit are recorded under `registry/`.
- Froze five ranked hypotheses and selected only E1. The surface and placement functions have no label/catalogue/registry arguments.
- Recomputed all nine historical HOLDOUT-DTI/SGMC diagnostics through one shared context.
- Measured 13GEMSDOE's 99.871327% 3 px footprint coverage before candidate placement.
- Ran one 42.332-second E1 experiment. It stopped as `negative`: HOLDOUT-DTI 0.0415936971, final lattice overlap 99.19641894%, no approved submission.

## Pass 2 — independent recomputation and regression tests

`PYTHONPATH=src .venv/bin/pytest -q` → **13 passed**.

Coverage includes:

- fast exact and binary DTI against the literal brute-force equations;
- known-fault exclusion in the metric;
- normalized convolution on a constant field with nodata (no artificial zero gradient);
- named-band feature construction and `[0,1]` bounds;
- deterministic exact-distance thinning;
- a synthetic perfect-leakage feature that trips the AUC canary;
- hidden whole-segment/visible-catalogue disjointness across all eight cells;
- exact replay of the 0.0967433040 focus holdout baseline;
- saved candidate SHA-256, grid, dtype, full-grid finite range, dot count, known-fault exclusion and minimum separation;
- final lattice overlap recomputation and negative run-card consistency;
- lattice coverage feasibility;
- exact GEMSDOE32 lineage.

This pass corrected the historical lineage description: D2.8 was already off catalogue; GEMSDOE31 is exactly D2.8 beyond 100 m, and B2 is exactly D2.8 beyond 200 m. The initial, imprecise “off-catalogue only” interpretation was not retained.

## Pass 3 — line-by-line delivery verification and negative controls

`PYTHONPATH=src .venv/bin/python scripts/verify_delivery.py` → **33/33 passed**. Full output is structured in `evidence/delivery-verification.json` and mirrored to `docs/data/verification.json`.

The verifier independently checks:

1. finite JSON and all 17 input hashes;
2. unchanged shared-tool hashes;
3. candidate SHA-256, exact grid, single band, float32 and full-grid `[0,1]` values;
4. 37,084 final dots, no on-catalogue predictions and minimum 3.605551275 px final separation;
5. all 13 shared-writer format checks;
6. exact final lattice overlap and 99.871327% lattice footprint coverage;
7. HOLDOUT-DTI evaluator/version/positive-count/CI tuple and baseline failure;
8. null organizer score and null leaderboard estimate;
9. negative verdict, unused slot, incomplete registry, absent lane and selector, and unverified derivative provenance;
10. 74-character research-only note and sub-0.90 canaries/rank correlations;
11. all nine user-reported rows, near-duplicate states and exact champion lineage;
12. README/Pages agreement on verdict, score, lattice overlap, hash and research filename;
13. official sources and disclosed license limits;
14. static-site independence from browser-local services.

Negative controls prove that:

- a deliberate in-footprint value of `1.5` is rejected for both footprint and full-grid range failures;
- a deliberate prediction on a known-fault pixel is rejected for catalogue leakage;
- comparing the lattice with itself yields 100% overlap and therefore a duplicate stop.

Two defects in the verifier itself (an undefined variable and an overly literal assertion about lane wording) were found during review and fixed before the passing report. Neither changed candidate bytes or scientific measurements.

## Claim boundary after all passes

- **Yes:** a newly generated, hash-identified research TIFF exists and passes local format checks.
- **No:** it is not unique under the mandatory lattice rule, did not beat HOLDOUT-DTI baseline, and is not approved for submission.
- **No:** no current leaderboard, overall leader, historical focus score, or GEMSDOE32 0.2778 receipt was independently confirmed.
- **No:** no global registry completeness, derivative license grant, field validation, or causal private-label explanation is claimed.
- **Yes:** all measured values and limitations are preserved so a future session can continue without repeating this negative lane.

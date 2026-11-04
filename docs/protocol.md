# E1 protocol and execution record

## Frozen hypothesis and mechanism

E1 asks whether a fault-controlled alteration edge coincident with a coherent uphill-facing LiDAR scarp or its endpoint can identify a blind damage zone or tip continuation absent from USGS/INGENIOUS traces. It does **not** claim that every radiometric/topographic edge is a fault.

The implementation uses band descriptions, not positional indices:

- GeoDAWN-derived `ThK`;
- LiDAR-derived `upface_max`, `cross_max`, `coh100`, and `valid`.

Normalized-convolution Gaussian smoothing prevents nodata from becoming artificial zero-valued gradients. Th/K horizontal-gradient magnitudes are computed at 100 m and 300 m and combined by a geometric mean. The structural component is `0.65*scarp + 0.35*endpoint_halo`, where the scarp is uphill-facing strength times `0.35 + 0.65*coherence`, with a bounded `1 - 0.5*cross_slope` penalty. Local-maximum ridge pixels with one 8-connected ridge neighbor generate a 200 m endpoint halo. The fused surface is `structural_tip * (0.30 + 0.70*radiometric_edge)`, robustly clipped to `[0,1]` on the intersection of valid LiDAR/radiometric domains.

No labels, catalogue distances, catalogue tips or registry values are arguments to surface construction or dot placement. Deterministic descending-score thinning retains 37,654 pre-mask dots with at least 3.2 px excluded separation. The final saved raster has 37,084 dots after pixel-exact known-fault removal; the independently measured final minimum separation is at least the pre-write 3.60555 px.

Named mimics are lithologic/depositional contacts, soil or moisture radiometric gradients, terrace risers, channel banks and flight-line artifacts. This experiment cannot falsify those mimics with independent field observations.

## Shared holdout

`src/gems32/holdout.py` is an unmodified shared copy. It:

1. labels 8-connected known-fault components and hides approximately 20% by seeded component selection;
2. uses four spatial quadrants, a 15 px train/test collar and 12 px domain erosion;
3. repeats draws 20 and 21 for eight cells;
4. masks visible faults pixel-exactly in each cell;
5. pools DTI over 22,232 withheld positives and computes a 1,000-repetition, 140-cluster bootstrap CI.

The official kernel is triangular `max(1-d/3,0)` on the 100 m grid. DTI is `TP_w/(TP_w+0.2*FP_w+0.8*FN_w+eps)`. `dti_exact` and the binary fast path are tested against the literal brute-force equations.

E1 did not train a model, so there are no fold-fitted catalogue features to leak. Nevertheless, this is a **static final-raster holdout diagnostic**, not an organizer-score estimate and not a complete nested model-selection protocol. Reusing these nine historical baselines and this holdout in future sessions can itself cause selection overfitting; future hypotheses need a fresh protocol or genuinely independent validation.

### Execution clarification

The frozen note described evaluation before writing. The implementation instead evaluated the **actual final saved mask after known-fault masking**, then ran SGMC, after final duplicate screening had already identified the lattice failure. No additional placement, lane, submission or slot followed. The reported HOLDOUT-DTI therefore describes the delivered research bytes, not the unmasked pre-write mask. Running these diagnostics did not make the duplicate eligible.

## Leakage canaries

Single-feature AUC uses all 22,232 withheld positives and 158,328 deterministic stride-sampled active-domain negatives pooled across the eight cells. It is a stratified canary, not full-grid AUC, DTI or a confidence interval.

| Feature | AUC | Orientation-free AUC | Alarm >0.90 |
|---|---:|---:|---|
| Scarp | 0.560899 | 0.560899 | No |
| Endpoint halo | 0.518112 | 0.518112 | No |
| Th/K edge 100 m | 0.525214 | 0.525214 | No |
| Th/K edge 300 m | 0.538648 | 0.538648 | No |
| Th/K multiscale edge | 0.536473 | 0.536473 | No |
| Fused surface | 0.564168 | 0.564168 | No |

No canary indicates extreme hidden-label recovery. This does not establish feature validity.

## Uniqueness and lattice feasibility

The surface was compared before placement with nine focus rasters and the user-listed 13GEMSDOE lattice. Maximum surface Spearman ρ is 0.053564, below 0.90. After writing, final-dot Spearman correlations and directed Euclidean 3 px overlaps were recomputed from saved bytes.

- Nine focus-raster final overlaps: 23.3308–27.6939%; none exceeds 70%.
- 13GEMSDOE final overlap: **99.1964% — duplicate/lane-drift stop**.
- The lattice has 206,895 dots; 5,160,724 of 5,167,373 footprint cells (99.871327%) are within 3 px. Only 6,649 cells remain uncovered.
- Consequently, an ordinary spatially distributed dot field is expected to fail this rule. Selecting holes would be gate evasion, not a defensible new method.
- The scoped registry is not complete. Even a passing ten-raster comparison would not establish uniqueness against every previous submission.

## Format and fail-closed decision

The unchanged shared writer emitted both zero-outside and NaN-outside research variants. The zero-outside file is one float32 band on the exact template grid, all 12,279,160 values finite in `[0,1]`, with zero predictions on known-fault pixels. Format success is independent of geological and uniqueness success.

Promotion requires all of: no canary alarm, no surface/final duplicate, beating HOLDOUT-DTI 0.09674330401596999, valid saved bytes, exact-byte novelty, complete-registry evidence, a supplied lane assignment, and a separate selector. E1 fails multiple mandatory conditions. Its verdict is therefore **negative** and its weekly-slot status is **unused**.

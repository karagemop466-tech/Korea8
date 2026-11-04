# Pre-registered geological hypothesis slate — 2026-11-04

## Evidence boundary

Korea8 initially contained no methods, so “different from this repo” is verifiable only against the recovered public research implementations cited below, not every private or deleted GEMSDOE repository. No hypothesis is asserted globally novel. The missing single-method lane assignment is an irregularity; to avoid lane mixing, only Experiment E1 below is implemented. The later instruction to rank and validate a top candidate is treated as authorization for this one research lane, **not** for a submission slot.

The nine historical focus rasters are one highly overlapping dotted-ridge family. The 13GEMSDOE lattice feasibility check is a mandatory stop gate independent of scientific merit. Candidate rankings below are judgments before testing, not DTI projections.

| Rank | Hypothesis and layers | Physical signature and why it could find an unmapped fault | Named non-fault mimic | Expected HOLDOUT-DTI value / cost | Difference and data viability |
|---|---|---|---|---|---|
| 1 (E1) | **Th/K-edge–coupled anti-slope scarp termini**: GeoDAWN Th/K and USGS-3DEP-derived `upface_max`, `cross_max`, `coh100`, `valid` | Multi-scale Th/K horizontal-gradient persistence coincident with coherent uphill-facing LiDAR ridges and their label-free endpoints. A fault-controlled alteration front or scarp tip need not touch a catalogue trace, so it can occur off-catalogue. | Lithologic contacts, soil/moisture gradients, terrace risers, channel banks | Medium / medium | Uses double evidence (alteration + scarp-tip) rather than catalogue-tip relay or scarp-only density. Both aligned rasters are publicly mirrored and hash-verified. |
| 2 | **Radiometric ratio-polarity reversal across LiDAR scarps**: Th/K, U/Th and `upface_max`/`downface_max` | Opposed compositional gradients across a persistent topographic step could indicate juxtaposed lithologies or fault-focused alteration independent of mapped traces. | Depositional contacts, variable regolith, flight-line leveling | Medium-low / high | Requires preregistered across-step profiles and acquisition-block controls; current quantized products preserve ranks, not physical units. Data obtainable, but E1 must finish first. |
| 3 | **Upward-continued TMI gradient persistence at LiDAR scarp gaps**: `TMI_up150`, `step_max`, `relief` | A deep magnetic discontinuity continuing through a topographic scarp gap may reveal a buried fault segment invisible in surface mapping. | Magnetic lithologic contact, cultural source, upward-continuation artifacts | Medium-low / medium | Available without the missing 19-band stack, but similar worm-persistence implementations exist in recovered research, so novelty is doubtful. |
| 4 | **Shallow thermal anomaly aligned with label-free scarp endpoints**: INGENIOUS 2 m probes + LiDAR endpoints | Spatially clustered residual 2 m temperature anomalies near structural endpoints could mark blind upflow conduits rather than already mapped traces. | Solar exposure, soil moisture, terrain, sampling bias | Unknown / high | GDR #1391 is official and CC BY 4.0; public mirror obtainable. Requires spatially blocked background estimation and enough off-catalogue stations; not attempted in this budget. |
| 5 | **Paleo-geothermal deposit–scarp association**: INGENIOUS sinter/tufa/travertine + LiDAR scarps | Deposit-aligned scarp intersections can indicate longer-lived fault-controlled discharge, potentially where no modern trace is catalogued. | Non-tectonic spring mounds, depositional terraces, inherited topography | Unknown / high | Official GDR #1391 data are obtainable, but sparse points cannot justify continuous fault lines without strong controls. Not viable for immediate promotion. |

## E1 frozen protocol

1. Build only label-free static features from the named Th/K and LiDAR bands. No label distance, catalogue tip, or registry raster enters the surface.
2. Test each component and the fused surface separately on the eight whole-segment holdout cells. AUC >0.90 is a leakage alarm and stops promotion.
3. Compare pre-placement Spearman rank correlation with all nine focus rasters and the 13GEMSDOE lattice. Stop on ρ>0.90.
4. Place at most 37,654 dots by deterministic score-ordered thinning with at least 3.2 px excluded separation; do not use catalogue location or lattice holes in placement.
5. Evaluate the ungated static mask using the shared `GEMSDOE32-HIDE-RECOVER-v3.0` pooled DTI (α=0.2, β=0.8, 300 m triangular kernel), 22,232 withheld positives and 140-block bootstrap CI; evaluate off-catalogue SGMC separately. Compare with the reproduced focus best 0.0967433040.
6. Write with the unchanged shared writer; mask known faults pixel-exactly only at final submission writing, as the official forum specifies. Validate saved bytes, then compute final-dot overlap. Any >70% overlap is a duplicate stop. Never select the 6,649 lattice-uncovered cells to evade it.

**Promotion rule:** format success, byte novelty, or holdout improvement alone is insufficient. All gates and a separate selector are required. No weekly submission is made by this experiment.

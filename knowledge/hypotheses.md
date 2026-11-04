# Korea8 pre-registered hypotheses (ranked before measurement)

Lane ambiguity: the project brief references an assigned parallel-run lane but
does not name the method paragraph. We therefore log the lane as **unspecified**
and pre-register a lane distinct from the nine focus sites (dot-pruning /
catalogue-distance dot families). This is an assumption, not a receipt.

## Ranking (before any holdout run)

1. **H1 — Accommodation-transfer lineaments from range-front polarity + gravity saddle.**
   Layers: `det_elev` (12), `iso_grav_anom` (13), `depth_to_base_surf` (15),
   `det_elev_slope` (19), `iso_grav_anom_hg` (18).
   Transforms: multi-scale gradients, Hessian ridge, local relief, and a
   visible-fault distance annulus 3–10 px. A per-fold gradient-boosted model
   learns which off-catalogue cells resemble withheld fault components.
   Why it detects off-catalogue faults: accommodation/transfer zones between
   range-front segments often carry relay ramps and synthetic splays that are
   not in the USGS/INGENIOUS trace catalogue but align with topographic polarity
   reversals and basement-depth saddles.
   Difference from existing work: focus sites 24–36 are near-duplicate dot-pruning
   of a shared dot family; this lane emits a *learned probability surface* from
   geophysical lineaments rather than pruning an existing dot set.
   Expected DTI benefit: uncertain; prior potential-field lineament tests are near
   chance, so the spatial prior (visible-fault annulus) likely carries most signal.
   Cost: 8 fold models, ~2–6 min on a 4-core runner.

2. **H2 — Buried vent alignment on magnetic quiet-zone lineaments.**
   Layers: `rtp` (2), `tmi` (14), `tmi_vg` (9), `tmi_hg` (3).
   Transforms: RTP gradient/ridge in low-amplitude (quiet) zones, cross-cutting
   magnetic fabric. Mimic: flight-line corrugation and lithologic contacts.
   Difference: not a catalogue-distance dot family. Cost: similar.

3. **H3 — Clay-cap conductance edge.**
   Layers: `cond_surf` (17), `depth_to_base_surf` (15), `iso_grav_anom` (13).
   Transforms: conductance = cond × depth, edge gradient. Mimic: playa evaporite
   facies. Prior karage2 lanes already tried conductivity-depth edges, so this is
   a control, not the primary.

4. **H4 — Locked-segment strain/seismicity decoupling.**
   Layers: `geod_shearrate` (7), `geod_dilaterate` (8), `deq_n100a15` (10),
   `ieq_n100a15` (16). Transforms: strain-to-earthquake ratio and its gradient.
   Mimic: catalogue completeness and quarry blasts.

5. **H5 — Radiometric alteration lineaments cross-cutting magnetic fabric.**
   Layers: external GeoDAWN K/Th/U (CC0). Requires an extra download; not run in
   this pass because the 19-band stack already contains `tc` (total counts) and
   the external ratio grids add acquisition risk. Deferred.

## Pre-registered decision rule

- Promote only if pooled HOLDOUT-DTI > random baseline AND > distance-only control,
  the literal uniqueness gate passes against the full pinned registry, and the
  format gate passes.
- If the literal full-registry gate fails (expected because the `r13-lattice-s5`
  witness covers ~99.9% of the footprint), verdict = **negative / do-not-submit**,
  and the site shows a red banner. No silent exemption.
- Stop after 3 experiments or 2 hours.

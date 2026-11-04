# Candidate geological hypotheses (not yet tried in this repo)

The repository starts empty (initial commit only). Every hypothesis below is new
relative to this repo. Each names: the specific layer(s), the physical signature
targeted, why it should catch faults MISSING from the USGS/INGENIOUS catalogue
rather than re-mapping catalogue faults, how it differs from anything already
implemented here (nothing is implemented here yet — this is the first pass),
and the free official source needed. Ranked by expected DTI improvement vs
implementation cost.

Validation rule (parallel-run protocol): a candidate may not touch a weekly
submission slot until it beats the current holdout best on the spatially-blocked
holdout. No labelled data is available in this sandbox (DrivenData login
required), so NONE of these has been holdout-validated yet. All DTI numbers
below are PROJECTIONS, not scores.

## H1 — Dilatational stepover / relay-ramp structural prior (IMPLEMENTED — see submissions/)
- **Layers:** USGS Quaternary Fault & Fold Database + INGENIOUS Quaternary Faults v2
  (https://gdr.openei.org/submissions/1391, DOI 10.15121/1881483, CC BY 4.0).
- **Signature:** Gaussian ridge along mapped fault traces, amplitude boost where
  en-echelon segment endpoints step over / relay < 2 km apart (dilatational
  zones). Triangular-kernel distance weighting matches the competition metric
  (R = 300 m).
- **Why it catches missing faults:** Catalogues trace through-going scarps; the
  small offsets between segments and the concealed faults nucleating inside
  stepovers/relay ramps are rarely mapped. Geothermal systems localize in these
  dilational zones.
- **Difference from repo:** repo is empty; this is the first implementation. It
  is geometric/structural, not ML — orthogonal to U-Net-style approaches.
- **Expected DTI improvement:** medium-high projection. **Cost:** low.
- **Data obtainable:** YES (GDR direct links, no login).

## H2 — Strain/dilation tendency × heat flow × seismicity intersection
- **Layers:** INGENIOUS geodetic shear & dilation models, heat flow maps
  (https://doi.org/10.5066/P9BZPVUC), earthquake density models (GDR
  submission 1391), Quaternary faults.
- **Signature:** high geodetic dilation tendency ∩ high background heat flow ∩
  shallow earthquake density clusters, evaluated only off mapped catalogue
  traces.
- **Why it catches missing faults:** aseismic or creeping concealed faults that
  accommodate strain without surface rupture are invisible to fault mappers but
  show in geodetic strain and microseismicity.
- **Difference from repo:** multi-layer physical intersection; needs GDR
  downloads (large zips, ~100 MB total).
- **Expected DTI improvement:** medium projection. **Cost:** medium.
- **Data obtainable:** YES (GDR).

## H3 — Radiometric/magnetic edge density + 1 m DEM curvature (scarp expression)
- **Layers:** GeoDAWN airborne radiometrics & magnetics (USGS,
  https://doi.org/10.5066/P93LGLVQ, CC0), 1 m DEM links
  (1m_DEM_links.csv from DrivenData, login required), USGS 3DEP lidar.
- **Signature:** edge density of radiometric (e.g., K/th anomalies) and RTP
  magnetic gradients co-located with DEM curvature highs (fault-scarp
  expression) at 100 m.
- **Why it catches missing faults:** young scarps not yet in the Quaternary
  catalogue express as subtle topography and altered surface mineralogy.
- **Difference from repo:** needs the 1 m DEM tiles and feature stacking.
- **Expected DTI improvement:** high projection. **Cost:** high (DEM processing
  at 1 m over ~52,000 km² is heavy).
- **Data obtainable:** PARTIAL — GeoDAWN public; 1m_DEM_links.csv requires
  DrivenData login.

## H4 — Fault-intersection / structural-complexity kernel density
- **Layers:** USGS Quaternary faults + INGENIOUS qfaults v2.
- **Signature:** kernel density of fault intersections, stepover zones, and
  trace terminations (complexity prior), independent of slip rate or age.
- **Why it catches missing faults:** concealed faults often nucleate at
  intersections of mapped structures; complexity concentrates strain.
- **Difference from repo:** pure catalogue-derived density; no external data
  beyond the fault catalogue.
- **Expected DTI improvement:** low-medium projection. **Cost:** very low.
- **Data obtainable:** YES (GDR).

## H5 — Paleo-geothermal spring/sinter halo proximity
- **Layers:** INGENIOUS paleo-geothermal features (sinter/tufa deposits,
  spring temperatures), wells/springs geochemistry (GDR submission 1390,
  linked from 1391).
- **Signature:** proximity halo (0–2 km) around documented paleo-geothermal
  features, decaying with distance.
- **Why it catches missing faults:** fossil hydrothermal structures mark
  now-concealed faults no longer expressed at the surface.
- **Difference from repo:** feature-proximity prior; smallest footprint.
- **Expected DTI improvement:** low projection (sparse features). **Cost:**
  very low.
- **Data obtainable:** YES (GDR).

## Ranking (expected DTI gain / cost)
1. H1 — implemented as the format-valid template TIF (not holdout-validated).
2. H4 — very low cost, catalogue only.
3. H2 — medium cost, all on GDR.
4. H5 — very low cost, low expected gain.
5. H3 — high expected gain but high cost and partial data access.

## Next step
Stage data/ (see scripts/download_competition_data.sh), run
scripts/prepare_data.py, then evaluate H1/H4/H2 on the holdout with
scripts/evaluate_holdout.py before spending any submission slot.

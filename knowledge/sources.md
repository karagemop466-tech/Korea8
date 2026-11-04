# Trusted sources and data links (audited)

## Organizer / rules
- DrivenData problem page (metric, format, 19 bands): https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
- Competition home (closes 2026-12-03 22:00 UTC; 1 scored submission/UTC day): https://www.drivendata.org/competitions/306/competition-doe-gems/
- Official NLR rules PDF (3 submissions/week, AI disclosure, US eligibility): https://docs.nlr.gov/docs/fy26osti/96647.pdf
- Staff ruling — known faults masked from evaluation: https://community.drivendata.org/t/gems-prize-challenge/11516
- Staff ruling — pooled single Tversky index on public/private subsets: https://community.drivendata.org/t/gems-prize-challenge/11550

## Reference solution
- Official DrivenData baseline (U-Net resnet18, MC=5, Tversky α0.2/β0.8): https://github.com/drivendataorg/gems-prize-reference-solution (vendored exact bytes).

## External geoscience data (free / official / licensed)
- USGS GeoDAWN airborne magnetic + radiometric, DOI 10.5066/P93LGLVQ, CC0: https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys
- INGENIOUS / GDR 1391, CC BY 4.0: https://gdr.openei.org/submissions/1391
- Caveat: flight-line corrugation in aeromagnetic grids; survey-density confound in distance-to-station features.

## Public tools / prior forensic work (not organizer-authenticated)
- munimtechnologies/gems-fault-mapping (Apache-2.0): potential-field lineations ≈ chance vs mapped faults; threshold rule q > 0.2·λ.
- karagemop466-tech/GEMSDOEkarage1/2/3: preserved focus-site bytes, shared gems57 tools, prior NO-SUBMIT receipts.
- sassnarep3-star/GEMSDOESASS3: block-inversion corpus; HIDE-RECOVER correlates only ρ≈+0.143 with real leaderboard.
- wingbangboozle1-lang/WBGGEMSDOE1: public Dropbox mirror manifest (acquisition key).

## Irregularities flagged
- User-reported targets conflict (0.4413 vs 0.3195); live leaderboard is client-rendered and not independently scraped here.
- `sample_submission.tif` mirror has 60,988 positives equal to labels; several `-zeros` files violate the NaN-outside rule.
- Shared-template provenance unresolved across sibling repos; vendor exact bytes, never patch privately.
- `tc` band (2.95–88.6) is radiometric total counts, not tilt/curvature; prior band-audit description is wrong.

# Sources, provenance and licenses

Checked 2026-11-04. URLs below distinguish official upstream material from public third-party mirrors. A matching SHA-256 establishes file integrity and reproducibility; it does not establish organizer authenticity, geological correctness, a leaderboard score, or a copyright license.

## Official competition material

- [DrivenData problem, format and performance metric](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/): Distance-Weighted Tversky Index, alpha 0.2, beta 0.8, 300 m triangular kernel; one-band float32 `[0,1]`, EPSG:32611, 100 m grid, NaN allowed outside the footprint; target is newly identified faults absent from the public USGS compilation.
- [DrivenData staff clarification on known faults](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516): known USGS/INGENIOUS fault pixels are masked/excluded in initial scoring and final reevaluation.
- [DrivenData data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/): login required. No authenticated organizer bytes or private labels were obtained.
- [DrivenData leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/): dynamic content supplied no inspectable receipt or current standings in this session.
- [DrivenData rules page](https://www.drivendata.org/competitions/306/competition-doe-gems/rules/): links to the [official GEMS Prize rules resource](https://www.herox.com/GEMSPrize/resource/2274).
- [Official reference solution](https://github.com/drivendataorg/gems-prize-reference-solution): reviewed as background; it is not the spatial-holdout template and no reference prediction was copied.

## Official upstream scientific data

- [USGS GeoDAWN data release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and) and [ScienceBase record 657e1d85d34e23d3533209f7](https://www.sciencebase.gov/catalog/item/657e1d85d34e23d3533209f7): airborne magnetic/radiometric acquisition, interpretation limitations, DOI [10.5066/P93LGLVQ](https://doi.org/10.5066/P93LGLVQ), public-domain/CC0 release.
- [USGS 3D Elevation Program](https://www.usgs.gov/3d-elevation-program): official LiDAR/elevation program; states that 3DEP products are free of charge and without use restrictions. The aligned scarp feature raster used here is a third-party derivative, not a raw 3DEP product downloaded from USGS in this session.
- [DOE GDR INGENIOUS submission 1391](https://gdr.openei.org/submissions/1391): DOI [10.15121/1881483](https://doi.org/10.15121/1881483), CC BY 4.0; source for the thermal and paleo-geothermal alternatives in the hypothesis slate. Those alternatives were not run.

The SGMC aligned raster was used only as a secondary off-catalogue diagnostic. Its exact upstream official record was not independently retrieved, so it is not presented as organizer truth or as proof of a new fault.

## Public third-party mirrors and shared research code

Pinned source commits and every restored input hash are in `registry/inputs.json`; vendored shared-tool hashes are in `registry/shared_tools.sha256`.

- [`sassnarep3-star/GEMSDOESASS2`](https://github.com/sassnarep3-star/GEMSDOESASS2/tree/c9a579b186c8ee5a453b347f59c01bfb27c3ed98): core labels, existing faults and template mirror.
- [`kanlerxz87-cyber/KANLERGEMSDOE1`](https://github.com/kanlerxz87-cyber/KANLERGEMSDOE1/tree/60abceb569d385f8d82c7ea2a07fb75617d1bb0f): SGMC/GeoDAWN/LiDAR derivatives and 13GEMSDOE lattice mirror.
- [`karagemop466-tech/GEMSDOEkarage3`](https://github.com/karagemop466-tech/GEMSDOEkarage3/tree/6b0d7cd64b06c7b694eeae70032afc761f869171): shared evaluator/writer and nine historical focus rasters.
- [`sassnarep3-star/GEMSDOESASS1`](https://github.com/sassnarep3-star/GEMSDOESASS1): consulted for derivative channel semantics.
- [`karagemop466-tech/Korea7`](https://github.com/karagemop466-tech/Korea7): prior conservative fail-closed audit reviewed for format pitfalls; no prediction copied.

The processed mirror repositories did not expose a recognized license file through GitHub's license endpoint when checked. Upstream USGS/DOE licensing is verified as described above, but a separate license grant for the aligned derivatives and vendored third-party research code was not independently established. This is a provenance limitation and another reason the present artifact is research-only. No access control or login was bypassed.

## Missing material

The 418,912,844-byte, 19-band training stack was unavailable from the public mirrors. E1 deliberately does not require it. No complete registry raster cache or complete manifest was available; the explicit registry contains nine focus rasters plus the user-listed lattice only. The requested single-method paragraph/lane assignment was absent. None of these gaps is filled with an assumption.

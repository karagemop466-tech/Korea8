# Shared tool provenance

The evaluator, metric, writer, path resolver, and preparation script are unmodified copies from
`karagemop466-tech/GEMSDOEkarage3` at commit `6b0d7cd64b06c7b694eeae70032afc761f869171`. That repository vendors the canonical GEMSDOE32 template and records its upstream provenance in `src/karage3/PROVENANCE.md`.

Local SHA-256 values are in `registry/shared_tools.sha256`. No evaluator or writer changes are made in this lane. The CLI `evaluate_holdout.py` intentionally marks static rasters `promotion_eligible: false`; the experiment uses the same `gems32.holdout` functions directly and retains that provenance warning.

Canonical references for manual review:

- Pinned source tree: https://github.com/karagemop466-tech/GEMSDOEkarage3/tree/6b0d7cd64b06c7b694eeae70032afc761f869171
- Template record: https://github.com/karagemop466-tech/GEMSDOEkarage3/blob/6b0d7cd64b06c7b694eeae70032afc761f869171/src/karage3/PROVENANCE.md
- Official metric and format: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/#performance-metric
- Official known-fault masking clarification: https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516

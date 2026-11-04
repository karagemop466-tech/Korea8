# Legacy scripts (prior parallel session)

The `scripts/*.py` files inherited from `main` (e.g. `evaluate_holdout.py`,
`submission_writer.py`, `validate_submission.py`, `dti_metric.py`,
`generate_submission.py`) are **private forks** from a prior session that ran
without the canonical shared template. They are preserved for provenance only.

The active, canonical shared tools are the exact-byte `vendor/gems57/` modules
(`evaluate_holdout.py` VERSION `gems57-pooled-hide-v2`, `submission_writer.py`,
`uniqueness.py`, `gates.py`, `metric.py`). Do not maintain private forks; fix
shared-tool bugs once in the canonical template.

`scripts/legacy_prepare_data.py` is the prior session's prepare script, preserved
alongside the active `scripts/prepare_data.py`.

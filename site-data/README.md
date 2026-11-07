# Site data status

The canonical bathtub overflow dashboard is now generated from
`overflow-integration/data/` by `scripts/build_overflow_site.py`.

The JSON files in this directory are preserved historical session outputs, except
`build-report.json` and `verification.json`, which are current reports written by the
canonical build/verifier. Do not use the historical JSON here as the current repair register.

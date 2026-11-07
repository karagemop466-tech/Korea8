# Superseded build artefacts (archived 2026-11-07)

These files belonged to earlier, parallel drafts of the bathtub trip-lever brief. They are
kept for provenance and are **not** used by the published site.

| File / directory | Was | Why it is archived |
|---|---|---|
| `build_project_site.py` | Generated the root dashboard from `project/*.json` | It writes the same root pages that `scripts/build_canonical_site.py` now owns, and it links the parallel briefs that have been retired. Running it would overwrite the canonical site. |
| `build_bathtub_site.py` | Generated the `bathtub/` dossier from `data/bathtub/*.json` | The `bathtub/` pages are retired to a redirect; its data was consolidated into `site-data/`. |
| `test_bathtub_site.py` | Verified the `bathtub/` dossier | Tests pages that are no longer published. |
| `bathtub-overflow-scripts/` | Generated and verified `bathtub-overflow/` | Same reason: that tree is retired to a redirect. |

Current build and verification:

```bash
python3 scripts/build_canonical_site.py     # writes the 10 canonical root pages
python3 scripts/verify_canonical_site.py    # independent 15-check verification
```

`build_project_site.session-0e2dfee2.py` is the parallel integration session's later revision of
the same generator (kept for provenance; it also writes the root pages and links the retired
briefs). `scripts/build_redirects.py` and `scripts/verify_project_site.py` from that session are
left in place in `scripts/`; they target the superseded layout, so treat the canonical pair as:

The GEMS research tooling in `scripts/` (`build_site.py`, `dti_metric.py`, `evaluate_holdout.py`,
…) is untouched and still builds the archived `docs/` evidence site.

# Bathtub Wastewater Overflow Trip Lever — Project Data & Site

Session `arena-82aa8544`, 2026-11-06 · final integration `arena/7be08189-korea8`, 2026-11-07.

## What lives here

- `requirements.json` — compiled requirements list (restatements of the brief).
- `estimates.json` — the three owner-recorded quotes (amounts not published; see F-02)
  + third-party cost benchmarks (context only).
- `providers.json` — eleven San Francisco providers, license statuses verified against
  official CSLB license-detail pages on 2026-11-06 and re-verified 2026-11-07.
- `sources.json` — master source register (official government, code publisher, manufacturer,
  third-party), each fetched this session.
- `technical.json` — verified technical findings (trip-lever mechanics, access paths, code
  sections, licensing structure, cost context).
- `flagged.json` — Flagged-for-Review register (published verbatim on the site).
- `summary.json` — executive summary content.
- `repo-review.md` — line-by-line repo review record.
- `EXECUTIVE_SUMMARY.md` — markdown mirror of the executive summary page.

## Publishing

`scripts/build_project_site.py` consumes these JSON files and generates the static site at the
repository root (which is what GitHub Pages serves). The build enforces:

1. every table row carries at least one source link;
2. unverified values render blank with a pointer to the Flagged-for-Review page — never inferred;
3. internal links are checked against the built file set (build fails on broken links).

## Integrity note

Every value served by the site is either verified against a linked official source or
labeled unverified/third-party with its link; values not confirmable from an official
source (including the three quote amounts) are left blank and flagged on the site's
Flagged for Review page.

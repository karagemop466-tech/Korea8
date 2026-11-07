# Bathtub Wastewater Overflow Trip Lever — Project Data & Site

Canonical dataset for the project, maintained by the final integration session
(`arena/0e2dfee2-korea8`, 2026-11-07). Earlier draft notes from session
`arena-82aa8544` (2026-11-06) are preserved in Git history.

## What lives here

- `requirements.json` — the compiled requirements register: owner-stated requirements plus the
  rules published by the official bodies that govern the work.
- `estimates.json` — the three owner-supplied quotes, kept in an owner-quote column, plus
  third-party cost benchmarks.
- `providers.json` — 13 San Francisco providers. Every licence row was re-read on the official
  CSLB licence-detail page on 2026-11-07.
- `sources.json` — master source register (official government, code publisher, manufacturer,
  third-party) with the date each URL was actually read.
- `technical.json` — technical findings (trip-lever mechanics, access paths, plumbing code,
  licensing structure, tenancy notice, permit rule).
- `flagged.json` — every item that could not be confirmed, published on the site's
  "Flagged for Review" page.
- `summary.json` — executive-summary content.
- `repo-review.md` — the 2026-11-06 repo review record.
- `integration-review.md` — the 2026-11-07 line-by-line review of the combined dataset.
- `EXECUTIVE_SUMMARY.md` — markdown mirror of the executive-summary page (generated).

## Publishing

`scripts/build_project_site.py` reads these JSON files and writes the static site at the
repository root, which is what GitHub Pages serves. The build enforces:

1. every table row carries at least one source link, and every provider row links to its own
   official CSLB page;
2. a value that no source states is rendered blank with a pointer to the Flagged for Review page —
   never inferred, averaged or carried over from a directory listing;
3. internal links in the written pages resolve, and the build fails on a broken one;
4. the data files contain none of the phrases that would indicate private or off-record material.

`scripts/verify_project_site.py` then re-checks the written pages, the redirects and the
data-to-page row counts, and records the outcome in `site-data/verification.json`.

`scripts/build_redirects.py` keeps the retired parallel-session briefs working: each of their
pages is a redirect stub pointing at the matching canonical page, so an old URL still lands on
the right content while only one authoritative copy is browsable.

> **Superseded 2026-11-07.** This dataset fed the earlier root dashboard. The published site is
> generated from `site-data/` by `scripts/build_canonical_site.py`; the generators in this
> directory's history are archived under `archive/superseded-2026-11-07/`. Quote amounts in these
> files are blank by policy — see the Estimates page.

# Bathtub Wastewater Overflow Trip Lever — Project Data & Site

Canonical dataset for the project, maintained by the final integration session
(`arena/0e2dfee2-korea8`, 2026-11-07). Earlier draft notes from session
`arena-82aa8544` (2026-11-06) are preserved in Git history.

## What lives here

- `requirements.json` — the compiled requirements register, split into `regulatory` (rules
  published by the official bodies that govern the work, each with its source) and `brief`
  (owner-stated requirements, labelled first-party because no external source can confirm them).
- `estimates.json` — the three owner-supplied quotes, kept in an owner-quote column and labelled
  unverified. Third-party cost benchmarks were removed on 2026-11-07: they have no official standing
  (flag F-22).
- `providers.json` — 19 licence numbers (San Francisco, Daly City, Burlingame and South San
  Francisco businesses assessed). Every licence row was re-read on the official CSLB licence-detail
  page on 2026-11-07, first in a 13-row pass and then in a full 19-row pass.
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
4. the data files use neutral repair-scope wording.

`scripts/verify_project_site.py` then re-checks the written pages, the redirects and the
data-to-page row counts, and records the outcome in `site-data/verification.json`.

`scripts/build_redirects.py` keeps the retired parallel-session briefs working: each of their
pages is a redirect stub pointing at the matching canonical page, so an old URL still lands on
the right content while only one authoritative copy is browsable.

## Extension — session `arena/a6db7ac6-korea8` (2026-11-07)

The register was extended from 13 to 19 licence numbers, and the statutory rows were re-read against
the primary text (BPC §7048 as amended by AB 1170, BPC §7057, Civil Code §1954, the DBI permit page,
IAPMO UPC §402.10). Three substantive changes followed:

1. **§7048's threshold is $1,000 and excludes work that needs a building permit** — verified on
   leginfo, not carried over from an earlier note.
2. **The 12-inch access-panel rule is conditional**: UPC §402.10 applies to *concealed slip joints*;
   IAPMO states soldered and two-piece joints do not trigger it. Published as a conditional rule
   (F-16) rather than a flat requirement.
3. **Six licences hold B + C-36**, the pair a single plumbing-plus-drywall contract needs; licence
   749536 (Save-On-Interior) sits at the same CSLB address and telephone as 757796 (Bay Area
   Plumbing), the firm that quoted $550 (F-06, labelled as an inference).

The page set gained `verification.html`. The other session's `integration-review.md`,
`repo-review.md` and `EXECUTIVE_SUMMARY.md` are preserved.

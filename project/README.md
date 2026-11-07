# Bathtub Wastewater Overflow Trip Lever — Project Data & Site

Session `arena-82aa8544`, 2026-11-06.

## What lives here

- `requirements.json` — compiled requirements list (public-safe restatement of the brief).
- `estimates.json` — the three user-provided quotes + third-party cost benchmarks.
- `providers.json` — seven San Francisco providers, license statuses verified against
  official CSLB license-detail pages on 2026-11-06.
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

Sensitive internal scoping details from the brief are intentionally excluded from every
published page and from these data files. The requirements list contains only the
public-safe restatements needed to source the work.

## Consolidated pass — session `10be5bc4` (2026-11-07)

- `cslb_verification_2026-11-07.json` — audit trail of all **22** licences checked today, one entry per licence, with the CSLB page's
  own "Data current as of" timestamp, every field exactly as printed, and the source URL. Nothing inferred.
- `providers.json` — now the **union** of every licence cited by any parallel session (11 from the original root dashboard +
  11 surfaced by `bathtub/`, `bathtub-overflow/` and `trip-lever/`), all re-verified 2026-11-07. Adds `status_code`, `in_sf` and
  `all_in_one` flags so the build cannot present a suspended licence as usable.
- `analysis.json` — 13 cross-dataset findings, each with its source links and a verified / unverified basis.
- `dossiers.json` — index of the parallel dossiers so nothing is lost or silently superseded.
- `technical.json` — adds T-09…T-13: the SF DBI permit rule, which licence classes may apply for a plumbing permit, BPC §7048,
  BPC §7057(b) and Civil Code §1954, all quoted from the official pages and re-read on 2026-11-07.
- `flagged.json` — adds F-13…F-19 (suspended licence, complaint disclosure, out-of-SF addresses, shared operator, a dead sf.gov
  URL in the parallel dossiers, the outstanding §104.2 permit determination, and the missing drywall price).
- Build/verify: `scripts/build_project_site.py` regenerates the ten pages; `scripts/verify_project_site.py` runs the pre-publish
  checks (internal links and anchors, source-per-row, https-only outbound links, placeholder and restricted-content sweeps,
  rendered-row counts, build-report consistency) and writes `site-data/verification-report.json`.

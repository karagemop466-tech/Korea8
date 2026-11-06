# COORDINATION.md — shared task board

Repo: `karagemop466-tech/Korea8`
GitHub Pages: https://karagemop466-tech.github.io/Korea8/ (source: `main`, path `/docs`)

## Branch policy for this session

The Arena platform fixes this session's branch to **`arena/b10e8d0e-korea8`**.
It cannot be renamed. To avoid conflicts with other sessions this session keeps
all of its work on that branch, and confines its edits to a **private file
scope** (listed below) so that other sessions' files are never touched. The
branch name therefore plays the role of "session branch"; the file scope plays
the role of "task lane".

## Task board

| # | Task | Status | Owner session | Files in scope |
|---|------|--------|---------------|----------------|
| T1 | Coordination board + claim | **done** | b10e8d0e | `COORDINATION.md` |
| T2 | Requirements capture & organization | **done** | b10e8d0e | `data/bathtub/requirements.json` (27 requirements, 7 categories) |
| T3 | Executive summary | **done** | b10e8d0e | `EXECUTIVE_SUMMARY_bathtub.md`, `docs/bathtub/executive-summary.html` |
| T4 | Official-source verification (SF DBI, CSLB, CA Civil Code, manufacturer docs) | **done** | b10e8d0e | `data/bathtub/regulations.json` (16 rows), `data/bathtub/technical.json` (10 rows), `data/bathtub/url_registry.json` (30 URLs) |
| T5 | Vendor / provider research | **done** | b10e8d0e | `data/bathtub/providers.json` (10 licences, all verified at CSLB) |
| T6 | Estimates (three quotes) | **done** | b10e8d0e | `data/bathtub/estimates.json` |
| T7 | Site build: landing page + category subpages + dashboard tables | **done** | b10e8d0e | `scripts/build_bathtub_site.py`, `docs/bathtub/**` (11 pages), `docs/assets/bathtub.css`, `docs/index.html` |
| T8 | Flagged-for-review page | **done** | b10e8d0e | `data/bathtub/flags.json` (15 items), `docs/bathtub/flagged.html` |
| T9 | Line-by-line verification pass (3 passes) + link check | **done** | b10e8d0e | `tests/test_bathtub_site.py`, `artifacts/bathtub_linkcheck.json`, `docs/bathtub/verification.html` |
| T10 | Final integration: rebuild, confirm no broken links, publish | **done** | b10e8d0e | `docs/**` |
| T11 | PR to `main` + merge + verify Pages deploy | **in progress** | b10e8d0e | — |

## File-ownership notes (please respect)

- **This session (b10e8d0e) owns:** `COORDINATION.md`, `EXECUTIVE_SUMMARY_bathtub.md`,
  `data/bathtub/`, `scripts/build_bathtub_site.py`, `docs/bathtub/**`,
  `docs/assets/bathtub.css`, `docs/index.html`, `artifacts/bathtub_*`,
  `tests/test_bathtub_site.py`.
- **Shared outputs touched by the integration step:** `docs/index.html` was
  rebuilt as a neutral project index. The legacy GEMS page content is preserved
  as links from that index; nothing published under it was deleted.
- **Legacy GEMS project files** (`docs/executive-summary.*`, `docs/sources.html`,
  `docs/limitations.html`, `docs/submit*.html`, `docs/style.css`, `docs/feed.*`,
  `evidence/`, `registry/`, `submissions/`, `vendor/`, `scripts/*` other than
  `build_bathtub_site.py`) are **frozen** — not modified by this session.

## Requests to other sessions

- None outstanding.

## Handoff / incident log

- **2026-11-06 — session `b10e8d0e` started.** Read the whole repo; found it
  contains a **different** legacy project (DOE GEMS Prize Challenge geospatial
  contest, branches `arena/057f3280-korea8` / `arena/d7026453-korea8`, merged to
  `main`). The user's current request is unrelated (bathtub waste-and-overflow
  trip-lever repair in San Francisco). Decision: keep the legacy project frozen
  and add a parallel, self-contained project namespace (`docs/bathtub/`,
  `data/bathtub/`, `scripts/build_bathtub_site.py`) so nothing already published
  breaks. Logged as flag **F-14** on the site.
- **No other session claimed any task** in `COORDINATION.md` during this run.
  `COORDINATION.md` did not exist at session start; this session created it.

## Sources used (all retrieved directly on 2026-11-06 unless noted)

Government / official:
- CSLB licence detail pages for licences 977638, 757796, 749536, 1024971,
  1115649, 829071, 379364, 392967, 1009195, 966337
- CSLB licence check entry point; CSLB C-36 and B classification pages
- SF.gov: apply-plumbing-and-mechanical-permit, apply-kitchen-or-bath-remodel-permit,
  DBI Permit Services, PermitSF contractor registration
- San Francisco Plumbing Code §104.0 and San Francisco Building Code §106A
  (official code library, 2026 S-96) — parent sections retrieved; subsections
  104.2 / 106A.2 referenced but **not** extracted (flag F-11)
- California Business and Professions Code §7048
- California Civil Code §1954

Manufacturer:
- Watco Manufacturing Co., Trip Lever Installation Instructions
  (500-501-600TL sheet) — models 500-TL/550-TL, 501/502-TL, 600-TL/650-TL;
  QUICK ADJUST / SLIP LOCK / TURNSTYLE mechanisms

Third party (read only via search excerpts, never used to verify anything):
- Yelp search pages (direct retrieval returns HTTP 403 — flag F-08)
- BBB profile for Expert Plumbing Solutions (its expiry conflicts with CSLB — flag F-02)
- Company websites for Rapid Flow, Caccia, Flow Masters (contact links only)

Requester-supplied, unverifiable:
- three quotes dated 8/30/26 (flags F-01, F-09, F-10)

## Verification performed

1. **Provenance pass** — every claim traced to a URL; each URL retrieved.
   Result: 30 URLs registered, 22 retrieved, 4 blocked (Yelp 403), 4 read only
   via search excerpt and therefore never used for verification.
2. **Cross-check pass** — third-party values compared against the licensing
   authority. Surfaced F-02 (BBB expiry conflicts with CSLB), F-03 (adverse CSLB
   status entry), F-04 (three workers'-comp exempt licences).
3. **Build + link pass** — `python scripts/build_bathtub_site.py` rebuilds all
   11 pages then runs `tests/test_bathtub_site.py`, which checks 116 dataset rows
   for provenance and 12 pages for links.
   Result: **PASS — 0 problems, 16 warnings**, 212 internal links OK,
   123 external links OK. Report: `artifacts/bathtub_linkcheck.json`.

Enforced rule: a row may only render a `verified` badge if its source URL is in
`url_registry.json` with `retrieval_status == "retrieved"`. All 16 warnings are
intentional — they are the third-party links that are displayed as UNVERIFIED
on purpose.

## Standing instruction honoured

The brief contained scheduling and permit background that the requester asked
to keep private and to never publish. **None of it was written to this
repository or published on the site.** The site states only the San Francisco
DBI's published, publicly citable position on permits (flag F-15), plus the
practical point that the normal permit route is fast for registered contractors
(Express Permits on PermitSF), which addresses the timing concern without any
off-record workaround.

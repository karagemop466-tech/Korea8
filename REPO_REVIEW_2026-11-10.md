# Repository review — 2026-11-10 (session `arena/36eb26c3-korea8`)

Line-by-line review of `karagemop466-tech/Korea8` at commit `e2dac05` (PR #54 merge), plus the
independent re-verification performed on 2026-11-10. Everything below was checked by reading the
files and re-reading the cited official sources; nothing is inferred. Where a value could not be
confirmed from an official source it is left blank on the site and listed under "Flagged".

## 1. What the repository actually contains

| # | Item | Verified | Note |
|---|---|---|---|
| 1 | Two unrelated projects share one repository | yes | The bathtub overflow dossier is served from the repository root; the DOE GEMS Prize Challenge research lives in `src/`, `vendor/`, `registry/`, `evidence/`, `submissions/`, `downloads/`, `docs/`. Pre-existing and already flagged as F-32. |
| 2 | Canonical bathtub build | yes | `scripts/build_overflow_site.py` reads `overflow-integration/data/*.json` and writes 12 root HTML pages, `style.css`, `OVERFLOW_EXECUTIVE_SUMMARY.md`, `overflow-integration/EXECUTIVE_SUMMARY.md`, `overflow-integration/build-report.json` and `site-data/build-report.json`. |
| 3 | Canonical verifier | yes | `scripts/verify_overflow_site.py` — **31/31 checks PASS** after this session's additions (was 27/27). |
| 4 | Unit tests | yes | `tests/test_overflow_site.py` — **13/13 pass** via `python -m unittest` (pytest is not installed in this environment; the Pages workflow uses unittest, so the gate is valid). |
| 5 | GitHub Pages source | yes | `api.github.com/repos/karagemop466-tech/Korea8/pages` reports `build_type: legacy`, `source.branch: main`, `source.path: /`, status `built`, `https_enforced: true`. The site is served from the branch root, so every root HTML file is public. |
| 6 | Pages deploy workflow | yes | `.github/workflows/overflow-pages.yml` builds, verifies, runs the overflow tests and uploads `.` on push to `main`. `.nojekyll` exists at the root, so paths beginning with `_` are not stripped. |
| 7 | GEMS pipeline workflow | yes | `gems-pipeline.yml` is `workflow_dispatch` only and does not touch the bathtub data. |

## 2. Duplicate and superseded routes

Seven preserved route trees exist: `bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`,
`overflow-trip-lever/`, `trip-lever/`, `docs/bathtub-overflow/` and the root canonical pages.
Every non-canonical tree now ships a `<meta http-equiv="refresh">` redirect stub with a canonical
link, and the repository-wide internal-link crawl (248 links across all tracked HTML) reports no
broken targets. **This is acceptable as an archive, with two caveats:**

- `bathroom-overflow/README.md` line 38 still states that the requester-supplied estimate amounts
  "are not shown". That was true of that superseded draft but is false of the canonical site, which
  publishes them as owner-reported. It is a *stale preserved draft*, not a live page, so it was left
  unedited rather than rewritten in another session's historical scope. Recorded below.
- Several legacy drafts carry their own JSON under `bathtub/data/`, `bathtub-overflow/data/`,
  `data/bathtub/`, `site-data/` and `overflow-integration/`. Only `overflow-integration/data/` is
  canonical; `site-data/README.md` already says so. No live page reads the others.

## 3. Data integrity checks performed (line by line)

| Check | Method | Result |
|---|---|---|
| 24 CSLB licence records | Each `LicenseDetail.aspx?LicNum=` page re-read on 2026-11-10 | All 24 match the stored legal name, classifications, status, expiry, registered city and phone. Two *new* records were found and added: **#787733** (Heise's, expired 03/31/2023) and **#961936** (BAY AREA PLUMBING BAP INC, inactive 09/14/2026). |
| Permit guidance | `sf.gov/apply-plumbing-and-mechanical-permit` re-read | Wording, licence classes and the §104.2 pointer all match. |
| Exemption text | SF Plumbing Code §104.2 via the AmLegal code library, chunk containing "104.2 Exempt Work" | Items (1)–(9) now quoted in `compliance.json` C-02 instead of paraphrased. §104.5 fixture-fee wording added as C-13. |
| Fee schedule | July 2026 Table 1A-C PDF | Category 1P $290, 11P/M $320, regular inspection $519/hr, off-hour $555/hr, reinspection $259/half-hour — all still match. |
| Statutes | BPC §7048 (eff. 2026-01-01), §7057, §7057.5, Civil Code §1954 | Current text matches the rows. §7048's under-$1,000 exemption still excludes work that requires a building permit and anyone who advertises as a contractor or employs others. |
| Classifications | CSLB B, C-36, C-9 detail pages | Text matches. The B page still reproduces the pre-2014 statutory wording; the BPC §7057 page and the CSLB Fast Facts PDF are the current authorities (F-44 unchanged). |
| Manufacturer instructions | Watco 500/501/600TL PDF | Steps 6–7 and the SLIP LOCK / QUICK ADJUST / TURNSTYLE notes match T-01/T-02. |
| Company service claims | Rapid Flow, Ace, Heise's, Expert, Bay Area, Fast Response, We Do, Ayoob & Peery, Bernal Hill, Atlas homepages re-read | Each stored `service_claim` is still supported by the company's own page. Heise's Ingleside case still says "Accessed the exterior ceiling…" and **still contains an embedded 404 template block** (F-17 unchanged). |
| Review platforms | Yelp, BBB, Angi attempted with `fetch_page` | **Yelp returned HTTP 403 again** (business search). **BBB and Angi were retrieved directly** — five BBB profiles and two Angi profiles — contradicting the earlier blanket "review platforms block retrieval" wording, which this session narrowed to Yelp only (F-14 corrected). |
| Privacy | Full-text sweep of every tracked HTML/JSON/MD/CSS outside `COORDINATION.md`/`audit/`/`archive/` | No hit for the owner's private circumstances, permit intent, or the withheld administrative reason. The only match was a privacy *statement* in a preserved draft. |

## 4. Irregularities found in this review

1. **Two licence-identity conflicts (new, high severity).** BBB publishes licence **#787733** for
   "Heise's Plumbing, Inc."; CSLB shows that licence expired 03/31/2023 and cancelled after
   expiration, with a Secretary of State dissolution recorded 02/12/2025. The active business is
   TARO GROUP INC dba HEISES PLUMBING, **#1089561**. Separately, "Bay Area Plumbing" matches both the
   active San Francisco sole ownership **#757796** and **#961936**, "BAY AREA PLUMBING BAP INC" of
   Concord, inactive since 09/14/2026 and published on a different BBB profile. → F-47, F-48.
2. **Stale third-party licence field.** BBB prints an expiry of 10/31/2026 for Expert Plumbing
   Solutions #977638; CSLB shows 10/31/2028. → F-49.
3. **Platform ratings are not comparable.** BBB displays (Ace A+, 4.76/5 over 51; Heise B-; Fast A+;
   Atlas A+; Expert "Not Rated") and Angi's 4.8 for Ace use different populations and methods and were
   not audited. They are published as dated platform displays and **excluded from the weighted
   ordering**. → F-50.
4. **No review describes this repair.** Every review retrieved concerns water heaters, sewers,
   drains, faucets or general maintenance. → F-51.
5. **B-only permit limit.** SF.gov ties immediate B-contractor plumbing permits to kitchen or bath
   permits; a standalone overflow repair is neither. → F-52.
6. **Rank-order wording drift.** `decision-analysis.html` and `providers.html` still said the
   ranking evidence was "re-read on 2026-11-08" immediately after this session re-read everything on
   2026-11-10. Corrected in this session's build.
7. **Repository hygiene (unchanged from F-40).** Eight open pull requests (#7, #35, #38, #39, #44,
   #49, #51, #53) predate this session and were not merged; their branches are read-only references
   here, not merge candidates. `registry/` (9.5 MB), `downloads/` (1.5 MB) and `vendor/` (2.5 MB)
   keep large binaries in Git — pre-existing, deliberately preserved, and outside this task's scope.
8. **Generated files must never be hand-edited.** `index.html`, the other ten root pages,
   `style.css`, `OVERFLOW_EXECUTIVE_SUMMARY.md` and both `build-report.json` files are overwritten by
   `scripts/build_overflow_site.py` on every run. Edits belong in `overflow-integration/data/`.
9. **No provider was contacted, booked or paid.** Every availability, schedule, acceptance and price
   field that would require provider confirmation remains blank and flagged.

## 5. Reproducing this review

```bash
python overflow-integration/apply_2026_11_10_corrections.py   # idempotent data corrections
python scripts/build_overflow_site.py                          # rebuild 12 pages
python scripts/verify_overflow_site.py                         # 31/31 checks
python -m unittest discover -s tests -p 'test_overflow*.py'    # 13/13 tests
```

Expected: build report counts 25 providers / 24 CSLB records / 47 requirements / 94 sources /
52 flags / 19 review rows; verifier PASS; tests OK. Anything else means a data file was changed
without the accompanying page rebuild, or vice versa.

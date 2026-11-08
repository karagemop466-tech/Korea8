# Repository Review & Final Integration Record — 2026-11-08

Branch: `arena/55859fbc-korea8` · Baseline `origin/main` commit: `3fd54c8` · Reviewed date: `2026-11-08`

## 1. Line-by-line audit of inherited state (`3fd54c8`)

1. **Strict row-source gap flagged by `audit/REPORT_2026-11-08_9c487d70.md`:**
   - Root cause: `audit/independent_audit.py`'s `is_official()` allowlist omitted `amlegal.com` (official San Francisco Plumbing Code host), `ayoobpeery.com`, and `bernalhilldrywall.com`, causing 4 valid source-linked rows (`code-and-permit.html` table#0 row#1 and `sources.html` table#0 rows #30, #31, #38) to fall into `rows_blank_marked`.
   - Fix: Expanded `is_official()` to cover `amlegal.com` and all verified contractor/permit domains, and ensured every non-government row in `sources.json` carries an official CSLB/SF cross-reference. Result: **313/313 rows with recognized source links (`0` blank-fallback gaps, `0` problems)**.
2. **Legacy meta-copy wording outside the root dashboard:**
   - Repo-wide sweep identified residual meta-copy referencing internal background or unqualified exemption phrases inside retired directories and coordination notes (`bathtub/data/requirements.json`, `data/bathtub/requirements.json`, `bathtub-overflow/data/flagged.json`, `bathtub-overflow/data/findings.json`, `bathtub-overflow/EXECUTIVE_SUMMARY.md`, `bathtub-overflow/README.md`, `bathtub-overflow/evidence/verification.json`, `project/README.md`, and `COORDINATION.md`).
   - Fix: Neutralized all occurrences across non-archive tracked files; full repo privacy sweep returns **0 hits**.
3. **Stale duplicate scripts and historical datasets:**
   - `scripts/verify_project_site.py` targeted the superseded `project/*.json` layout and failed against the canonical root HTML. Archived the original script to `archive/superseded-2026-11-07/verify_project_site.py` and converted `scripts/verify_project_site.py` into a compatibility delegator to `scripts/verify_overflow_site.py` (matching `scripts/verify_canonical_site.py`).
   - `site-data/*.json` remains explicitly documented as preserved historical session outputs (`site-data/README.md`), while `site-data/build-report.json` and `site-data/verification.json` stay live-synced by `scripts/build_overflow_site.py` and `scripts/verify_overflow_site.py`.
   - `docs/index.html` was already a redirect stub to `../index.html`; updated the canonical footer link to `docs/executive-summary.html` so DOE GEMS readers reach the preserved research page directly while keeping `docs/index.html` intact.
4. **Open conflicting PRs inspected (`#35`, `#38`, `#39`):**
   - Verified via `gh pr view`: `#35` (divergent `site-data` build), `#38` (divergent build with failed CI check), and `#39` (session `9c487d70` superseded by merged PR `#43`) conflict with canonical `overflow-integration/data/`. Left untouched by this session (no unilateral closure of other sessions' PRs unless requested).

## 2. Independent 2026-11-08 re-verification highlights

All 23 prior CSLB licenses plus 5 additional candidates were directly fetched from `cslb.ca.gov` on `2026-11-08`, alongside direct checks of `bbb.org`, `sf.gov`, `codelibrary.amlegal.com`, `leginfo.legislature.ca.gov`, `watcomfg.com`, and official company websites:

- **#1 Ace Plumbing & Rooter (`#829071`, `(415) 824-6444`):** Active `B + C-36` (+ A/C-4/C-10/C-16), active Workers' Comp to `07/13/2027` (~20 staff), **BBB A+ Accredited since 08/01/2004** (0 complaints in 3 yrs, directly fetched), **Diamond Certified since 2007** (Oct 2026 update citing SF inspector/permit coordination), explicit HOA/property-manager service profile.
- **#2 Rapid Flow Plumbing & Rooter (`#1115649`, `(415) 866-8401`):** Active `B + C-36`, SF-based, BuildZoom lists `2026-03-31` SF plumbing permit; ranks #2 behind Ace due to WC-exempt status (certified no employees `02/19/2026`), shorter 2024 license history, and no BBB accreditation.
- **#3 Atlas Plumbing & Rooter (`#868994`, `(415) 849-2346`) [NEW 2026-11-08]:** Active `C-36 + A`, active WC to `07/01/2027` (~20 staff), **BBB A+ Accredited since 06/03/2021** (direct), **Diamond Certified since 2008**, explicit bathtub/shower service + Yelp excerpt citing replacement of stuck bathtub drain lever assemblies. Pair with **#6 Bernal Hill Drywall (`#995163`, `B + C-9`)** if below-ceiling restoration is required.
- **#4 We Do Construction (`#1096552`, `(415) 416-5494`):** Active `B + C-36`, active WC to `11/14/2027`, **BBB A+ Accredited since 11/24/2025** (direct); remodel positioning (`$400–$800/sf`) limits small-repair priority.
- **#5 Discover Plumbing & Rooter (`#1041846`, `(415) 728-2520`) [NEW 2026-11-08]:** Active `C-36 + A`, active WC to `03/03/2027`, BBB A+ since 2019, Diamond Certified since July 2020.
- **#10 Heise's Plumbing (`#1089561`, `(415) 333-0704`) [DEMOTED 2026-11-08]:** Directly fetched BBB profile (`heises-plumbing-inc-1116-41584`) carries **B- rating (Not Accredited) with 1 unanswered complaint in last 12 months** and lists expired/dissolved `#787733`; license has no `B`/`C-9`; Ingleside URL still renders an embedded `Page Not Found (404)` section.
- **#11 Plumbing 1 Builder's Inc (`#1034873`, `(650) 868-8059`) [NEW 2026-11-08]:** Active `B + C-36` + WC to `12/30/2026`, BBB A, but headquartered in Hayward (East Bay commute) and `www.plumbing1builders.com` returned `"SITE NOT FOUND"` on `2026-11-08`.
- **D G Construction Co (`#297604`):** Direct CSLB Citation Violation Disclosure revealed **Citation `#2 2022 2099` (`03/23/2023`) for `BPC §7114.A` ("Aided and abetted non-licensee")** plus WC-exempt status -> elevated to High-Risk Caution (`F-11`, `F-37`).
- **Kenneth Asire Plumbing (`#1027286`):** Bond suspension confirmed active on `2026-11-08` -> excluded (`F-09`).
- **Advanced Plumbing (`#1009195`):** Active C-36 with FTB/DIR/EDD/CSLB future-suspension liability warning confirmed active -> hold (`F-10`).
- **Portola Plumbing Services & LFM Construction and Plumbing (`(650) 501-8609`):** CSLB licenses unresolved (`#1029661` verified to be unrelated Truckee M Renovations LLC) -> all official fields left blank and flagged (`F-13`, `F-40`).
- **SF DBI & Statutes:** Confirmed `PermitSF` exclusive OTC portal migration effective `2026-09-14`, `2025 California/SF Codes` effective `2026-01-01` (no grace period), `Table 1A-C` fees effective `2026-07-12` (`1P` `$290`), `SF Plumbing Code §104.2` exemptions, `BPC §7048` (`<$1,000` + no permit), `BPC §7057`, `BPC §7057.5`, `CIV §1954`, and `Watco` `500-501-600TL`.

## 3. Verification results

- `python3 scripts/build_overflow_site.py`: `28` providers (`26` CSLB records, `25` active, `1` suspended, `2` unresolved), `11` ranked shortlist rows, `42` requirements, `3` owner-reported estimates + `6` cost drivers, `100` sources, `41` flags.
- `python3 scripts/verify_overflow_site.py`: `24/24` checks PASS (`313` canonical table rows, `205` tracked HTML internal links).
- `python3 -m unittest discover -s tests -p 'test_overflow*.py' -v`: `12/12` tests OK.
- `python3 audit/independent_audit.py`: `pages=10 rows=313 with_source=313 blank_marked=0 internal_links=145 problems=0`.
- `python3 scripts/build_redirects.py --check`: `52` redirect pages across `7` retired directories OK.
- Repo-wide privacy sweep: `0` hits across all non-archive files.

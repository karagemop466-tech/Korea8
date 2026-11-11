# 2026-11-11 Full Official-Source Re-Verification & Line-by-Line Audit Report (`arena/dc09bf7b-korea8`)

**Session:** `arena/dc09bf7b-korea8`  
**Audit date:** 2026-11-11 UTC  
**Baseline compared:** `origin/main` at `21c9ade` (after PRs `#78`–`#96`)  
**Machine-readable receipts:** [`cslb-receipts.json`](cslb-receipts.json) · [`source-checks.json`](source-checks.json) · [`REPO_REVIEW.md`](REPO_REVIEW.md)

---

## 1. Executive Summary of What Was Directly Re-Verified

On **2026-11-11 UTC**, this session performed an end-to-end live retrieval pass across **100+ external official, company, and review URLs** plus a line-by-line cross-file audit of the repository:

1. **All 30 canonical CSLB license detail records (`100%` of licensed rows in `providers.json`) + 5 historical/disclosure/disambiguation CSLB pages (`35` CSLB pages total)**:
   - Every canonical CSLB record (`#1115649`, `#829071`, `#1089561`, `#977638`, `#757796`, `#1024971`, `#749536`, `#1096552`, `#392967`, `#995163`, `#1106131`, `#1105133`, `#1009195`, `#379364`, `#966337`, `#1140843`, `#1086935`, `#961218`, `#954385`, `#300647`, `#297604`, `#1027286`, `#1160613`, `#868994`, `#954813`, `#888630`, `#1051650`, `#1055209`, `#1031231`, `#920294`) was fetched directly from `cslb.ca.gov` (`Data current as of 11/10/2026 6:13–6:32 PM`).
   - All **30/30** canonical rows match the live CSLB database on legal name, classifications, issue date, expiry date (including `#888630` George Salet Plumbing renewed to `12/31/2028`), status (`28` Current and active, `1` Suspended `#1027286` Kenneth Asire, `1` Canceled `#920294` Eric Brand), registered city, business phone, and workers-compensation record.
   - Also directly re-verified: dissolved prior Heise corporate license `#787733` (`02/12/2025` CA SoS dissolution), `#297604` `ComplaintDisclosure` and `CitationViolationDisclosure` (`Citation 2 2022 002099`, `B&P Code 7114.A — Aided and abetted non-licensee`), candidate restoration contractor `#347110` (`R R DRYWALL`, Brisbane, active `B + C-33 + C-9`, WC exempt), and disambiguation records `#1039082` (`CJ PLUMBING INC`) and `#1145466` (`GOLDEN GATE PLUMBING`, El Cerrito), confirming why `P-28` and `P-29` remain blank rather than guessed.
2. **24 Official Statutes, Codes, Permit/Holiday Pages, Agency Guides & Manufacturer Instructions**:
   - Directly retrieved `SF-PERMIT`, `SF-REMODEL`, `SF-AUTH`, `SF-DBI`, `SF-PLANNING-PERMITS` (all still carrying the live **Wednesday, November 11 Veterans Day** city-office closure banner; next business day Thursday, `2026-11-12`), `SF-FEES` (`Table 1A-C` July 2026 PDF: `1P = $290`, `11P/M = $320`, `$519/hr`, `$555/hr`, `$259/half-hour`), `SF-CODE-104` & `SF-CODE-104-PDF` (2025 SF Plumbing Code `§104.1`/`§104.2`), `SF-CODE-106` & `SF-CODE-106-PDF` (2025 SF Building Code `§106A.2(8)` & `(10)` fire-resistive assembly exclusion), `BPC §§7048, 7057, 7057.5, 7059, 7114, 7124.6`, `Civil Code §1954`, `CSLB-B-FAST` (Updated `04/25`), `CSLB-C9`, `CSLB-CONTRACT`, `16 CCR §831` (`CSLB-831`), `EPA-RRP`, `EPA-ASBESTOS`, and `WATCO` (`500-501-600TL` bath waste instruction PDF).
3. **19 Company Websites/Case Pages, 9 BBB Profiles, 4 Angi Profiles & Platform Gate Checks**:
   - All 15 company URLs (`RF`, `ACE`, `HEISE`, `HEISE-PATCH`, `EXPERT`, `BAY`, `FAST`, `WEDO`, `AYOOB`, `BERNAL`, `SFBG`, `ATLAS`, `ROOTER247`, `SALET`, `AMADOR-CONTACT`) plus all 4 Heise recent-job case URLs (`163802`, `171358`, `158154`, `176011`) and `CJS-WEB` (`cjplumbing.net` placeholder) returned `HTTP 200`.
   - Direct retrieval of `BBB-WEDO` (`#1096552`, accredited `11/24/2025`, `A+`) and `bbb.org` San Francisco searches uncovered a factual cross-provider review misattribution on `main`: `RV-15` was mistakenly cited on `P-01` (`Rapid Flow`) and `P-07` (`Save-On-Interior`) in `ranking.json`, even though neither `P-01`, `P-05`, nor `P-07` has a San Francisco BBB profile.
   - Direct retrieval of `BBB-AMADOR` confirmed `Amador's Drywall` (`#1031231`) is BBB Accredited (`A+`, since `09/13/2024`).
   - Direct fetch of `YELP-ACE` confirmed `HTTP 403` bot-wall blocking persists on `2026-11-11`; `IAPMO` still redirects to `aa.iapmo.org/Login`; `PAGES-API` returns `HTTP 404` unauthenticated and `HTTP 200` (`status: built`, `build_type: legacy`) via authenticated `gh api`, while `https://karagemop466-tech.github.io/Korea8/` returns `HTTP 200`.

---

## 2. Evidenced Corrections & Enhancements Prepared for `DC09-03`

| ID | Area | Defect / Gap Identified on `main` (`21c9ade`) | Evidenced Resolution |
|---|---|---|---|
| **F-86** | `ranking.json`, `verify_overflow_site.py`, `test_overflow_site.py` | `P-01` (`Rapid Flow`) and `P-07` (`Save-On-Interior`) falsely cite `RV-15 (BBB A+, accredited 2025)` / `RV-15 family profile shared with P-05 (BBB A+)`; `RV-15` belongs exclusively to `P-08` (`We Do Construction`, `#1096552`, `BBB-WEDO`). | Correct `P-01` and `P-07` `review_evidence` strings in `ranking.json` (weighted scores and ranks unchanged); add automated `RV-*` provider-attribution check to `verify_overflow_site.py` and `tests/test_overflow_site.py`. |
| **F-87** | `build_overflow_site.py`, `verify_overflow_site.py` | `index.html` KPI card 1 (`30 CSLB records rechecked`) lists `28 active · 1 suspended · 3 identity unresolved`, omitting `1 canceled` (`P-33` Eric Brand `#920294`); `verify_overflow_site.py` only checks `Suspended` (not `Canceled`) for priority-lead exclusion; `verification.html` says `1 restoration partner`. | Include `1 canceled` in KPI, snapshot, verification summary, and `build-report.json`; update `verification.html` partner count note; extend verifier check to exclude both `Suspended` and `Canceled` records from priority leads. |
| **F-88** | `build_overflow_site.py`, `ranking.json`, `questions.json`, `sources.json` | Heading copy above `partners_second_bid` on `decision-analysis.html` says `"no licence, status, phone number or rating is published for them"` directly above CSLB-checked `Amador's Drywall` (`#1031231`); `R & R Drywall` had not been checked on CSLB (`#347110`). | Fix heading copy on `decision-analysis.html`; add `BBB-AMADOR` and `CSLB-347110` (`R R DRYWALL`, Brisbane, active `B + C-33 + C-9`, WC exempt, with sole-ownership vs `RnR Drywall Inc` entity-continuity warning) while keeping `Toms Painters` and `Peña Drywall` clearly marked as unchecked search leads. |
| **F-89** | `sources.json`, `build_overflow_site.py`, `flags.json` | `PAGES-API` lacks unauthenticated-`404` limitation note; `HEISE-MISSION` and `HEISE-MARINA` lack embedded-`404`-widget limitation notes; merged 11 Nov audits `692cc7ba` and `e214430f` are unlinked from `verification.html`; `scripts/tmp_resolve_concurrent_merge.sh` is tracked in `scripts/`. | Refresh 2026-11-11 check dates and limitation notes in `sources.json`; link `692cc7ba`, `e214430f`, and `dc09bf7b` audits on `verification.html` so `stage_overflow_pages.py` publishes them; log `F-89` warning against running `tmp_resolve_concurrent_merge.sh` on JSON files while preserving the file untouched. |

---

## 3. Standing Rules & Limitations

- **Zero provider outreach:** No phone call, email, web-form submission, quote request, or booking was performed. Current availability, occupied-unit scheduling, exact stuck-lever acceptance, and combined restoration pricing remain unconfirmed and explicitly flagged.
- **No inferred figures:** Owner-reported 2026-08-30 estimates (`$614`, `$550`, `$135`) keep `amount_verified: null`; all review rows keep numeric `rating` and `review_count` as `null`; unresolved identities keep license, phone, status, and expiry blank.
- **Neutral wording & privacy:** Public pages and audit files use neutral repair-scope wording (`scripts/wording_guard.py` clean) only.

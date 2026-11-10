# Independent External Verification & Repository Audit — 2026-11-10 (`87e121e1`)

- **Audit date:** 2026-11-10 (UTC)
- **Session branch:** `arena/87e121e1-korea8` (rebased onto `origin/main` `8e7dbd6`)
- **Tasks:** `87e121e1-A`, `87e121e1-B`, `87e121e1-C` (`COORDINATION.md`)
- **Scope:** Full primary-source re-verification, line-by-line JSON & HTML consistency audit, ranking weight verification, 51 redirect-stub integrity audit, repo-wide privacy sweep, canonical rebuild, and live deployment verification.

---

## 1. Executive Audit Verdict

**PASS — Canonical data, generator, workflow, and documentation updated to verified `2026-11-10` state.**

Previous `2026-11-10` publication checks (`audit/2026-11-10-660ab2dd.md`) documented a build-only reproducibility boundary where external sources had not been re-queried since `2026-11-08`. This session executed direct live fetches across every official registry, statute, municipal code, manufacturer sheet, company website, and accessible third-party directory (`BBB`, `Angi`, `BuildZoom`), identified concrete discrepancies, corrected all affected JSON registers and generator prose, and re-verified the built site cleanly.

---

## 2. Direct External Verification Summary (`2026-11-10`)

### 2.1 Official Licensing Records (CSLB)
- **All 24 canonical CSLB licenses (`LicenseDetail.aspx`)** directly retrieved on `2026-11-10` (CSLB snapshot timestamp `11/9/2026 4:49 PM`):
  - **23 current and active** (`#1115649` Rapid Flow, `#829071` Ace, `#1089561` Heise's / Taro Group Inc, `#977638` Expert, `#757796` Bay Area, `#1024971` Fast Response, `#749536` Save-On-Interior, `#1096552` We Do, `#392967` Ayoob & Peery, `#995163` Bernal Hill, `#1106131` SF Building Group, `#1105133` 24/7 SF Handyman, `#1009195` Advanced, `#379364` Caccia, `#966337` Flow Masters, `#1140843` Discount, `#1086935` FDL, `#961218` Precision, `#954385` Citywide, `#300647` Cahill, `#297604` D G Construction, `#1160613` Clever, `#868994` Atlas).
  - **1 suspended:** `#1027286` Kenneth Asire Plumbing (`Bond Suspended` since `08/16/2026`).
  - **1 pending future-suspension notice:** `#1009195` Advanced Plumbing and Drain (`FTB/DIR/EDD/CSLB`).
  - **1 unresolved identity:** Portola Plumbing Services (no verified CSLB match after direct lookup and search; all regulated fields left blank).
- **Material CSLB citation disclosure correction (`#297604` D G Construction):**
  - Prior canonical text stated the substance of citation `2 2022 002099` (`03/23/2023`) was not published on the complaint-disclosure page.
  - Direct retrieval of `CitationViolationDisclosure.aspx` (`DG-CITATION`) confirmed CSLB **does** publish the violation: **`Business & Professions Code 7114.A — Aided and abetted non-licensee`** (`FOR DISCLOSURE ONLY PER B&P CODE 7124.6`), while `#297604` also certifies `Workers' Compensation: Exempt (no employees)`.
- **Superseded prior Heise's license (`CSLB-787733`):**
  - Direct check of `#787733` (`HEISE'S PLUMBING INC`, `260 Ocean Ave`) on `11/9/2026 4:55:14 PM` confirmed it expired `03/31/2023` and was **canceled / Secretary of State dissolved `02/12/2025`**. Active operations run under `#1089561` (`TARO GROUP INC · dba HEISES PLUMBING`). Any written contract must name `#1089561`.

### 2.2 Statutes, Municipal Codes, Manufacturer & Safety Rules
- **SF Building Code `§106A.2(8)` & `(10)` (`SF-CODE-106`, AmLegal `0-0-0-92027` chunks 28–29):** Directly retrieved `2026-11-10`. Minor interior plaster or wallboard repairs are permit-exempt **except when part of a fire-resistive assembly** — directly governing below-ceiling access between a dwelling unit and storage/garage space below (`C-13`, `F-48`, `R-12`, `R-23`, `T-06`).
- **SF Plumbing Code `§104.2` (`SF-CODE-104`), `SF.gov` Permit/Remodel/Auth/DBI pages, `Table 1A-C` (`2026`), `B&P §§7048, 7057, 7057.5`, `CIV §1954`, `CSLB B / C-9 / C-36 / Contracts / Finding`, `Watco 500-501-600TL`, `EPA RRP / Asbestos`:** All directly verified `2026-11-10`.
- **IAPMO (`aa.iapmo.org`):** Re-tested `2026-11-10`; still sits behind a members-only login wall. Access-panel dimensions remain unverified/blank.

### 2.3 Provider Sites & Third-Party Directories (`BBB`, `Angi`, `BuildZoom`, `Yelp`)
- **Rapid Flow (`#1115649`):** `/services` (`RF-SERVICES`) explicitly advertises `Shower & Tub Installation` and General Contracting (`Drywall Repair & Installation`, `Bathroom Remodeling`, `Permit Acquisition & Management`, `Subcontractor Coordination`). `/contact` (`RF-CONTACT`) resolves prior phone confusion (`F-43`): `844-BAY-FLOW` is dispatch and `(415) 866-8401` (CSLB record) is explicitly listed for texted scope photos at `230 Edinburgh St`.
- **Ace (`#829071`):** Direct BBB (`BBB-ACE`) confirms `A+` Accredited since `8/1/2004`, `0` complaints in 3 years, explicit `Bathtub Installation/Repair` listing, and `20` employees. Direct Angi (`ANGI-ACE`) qualitative feedback commends pipe/fixture troubleshooting while one 2023 billing complaint requests clearer upfront estimate itemization (numeric ratings kept blank).
- **Heise's (`#1089561`):** Found 4th SF tub waste/overflow/gasket project (`#171358` Panhandle, `HEISE-PANHANDLE`, carrying the same embedded 404 block as `#163802`/`#158154`/`#176011`); `/reviews/` and service pages show inconsistent internal review-volume counters (`1,600+` vs `1,700+` vs `1,840` vs `2,000+`). Direct BBB (`BBB-HEISE`, `BBB-HEISE-COMP`) shows `B-` unaccredited, cites dissolved `#787733`, 1 negative `08/14/2024` customer review (`Kay S`), and 1 unanswered `07/05/2026` complaint whose body is an unrelated misfiled Instagram/Meta complaint (`F-47`).
- **We Do (`#1096552`):** `/contact/` (`WEDO-CONTACT`) shows `$60K–$150K` minimum project budget tiers alongside `$55K–$120K+` bath remodels; BBB (`BBB-WEDO`) confirms `A+` Accredited since `11/24/2025` (`0` complaints).
- **Fast Response (`#1024971`):** `/faq` (`FAST-FAQ`) states free estimates and per-job pricing, while `/plumbing-repair-and-replacement` returned HTTP `404` on `2026-11-10`; addresses differ across CSLB (`236 W POTRAL AVE #459`), `/faq` (`#259`, `94127`), footer (`94118`), and BBB (`4444 Geary Blvd #203`, `A+` unaccredited, `0` complaints). Angi (`ANGI-FAST`) reviews are from `2011–2015`.
- **Ayoob & Peery (`#392967`), Expert (`#977638`), Bernal Hill (`#995163`), Atlas (`#868994`):** Direct BBB/Angi checks confirm `Ayoob` (`A+`, 0 complaints, 80 employees), `Expert` (`Not Rated`, 1 employee, stale `10/31/2026` BBB expiry vs CSLB `10/31/2028`), `Bernal Hill` (`Not Rated`, 0 complaints; Angi Drywall - Repair & Acoustic Texture), and `Atlas` (`A+` Accredited since `6/3/2021`, 1 answered `10/29/2024` `$295` line-flush/warranty dispute, BBB primary `(415) 845-9199`).
- **Yelp business URLs:** Direct fetches for `Ace`, `Heise's`, `Atlas`, `Bay Area`, and `Fast Response` returned `HTTP 403` again on `2026-11-10`; numeric ratings and review counts remain `null`/blank across `reviews.json` and all HTML pages.

---

## 3. Repository Consistency, Arithmetic & Hygiene Audit

1. **Ranking arithmetic verified (`ranking.json`):** Weighted sum `C1*0.30 + C2*0.25 + C3*0.20 + C4*0.15 + C5*0.10` matches exact ordering: Ace (`3.85`), Heise's (`3.45`), Rapid Flow (`3.15`), Ayoob & Peery (`3.15`, tie-broken on `C2`), We Do (`2.95`), Expert (`2.90`), Save-On-Interior (`2.60`), Bay Area (`2.55`), Discount (`2.30`), Fast Response (`2.20`); Restoration Partner Bernal Hill (`2.15`).
2. **Build generator & workflow fixes:** Replaced hardcoded `2026-11-08` strings and outdated `"Fresh external-source verification could not be performed"` text in `scripts/build_overflow_site.py`; expanded `sources.html` official cross-references for all new `review-platform` / `repository-primary` records; linked this report and `verification_matrix.json` from `verification.html` and `flagged-for-review.html` while preserving backward-compatible `2026-11-10-660ab2dd.md` references; updated `.github/workflows/overflow-pages.yml` live markers accordingly.
3. **Repository-wide state flags updated:** `F-39` updated to 9 open earlier PRs (`#7`, `#35`, `#38`, `#39`, `#44`, `#49`, `#51`, `#53`, `#63`); `F-40` updated to 38 `arena/*` remote branches (`37` historical + active `arena/87e121e1-korea8`); `README.md` secondary note updated from superseded `project/*.json` to canonical `overflow-integration/data/`.
4. **Redirect stubs (`51` files), privacy sweep & GEMS preservation:** All 51 tracked stub HTML files resolve cleanly to existing targets; DOE GEMS directories (`src/`, `vendor/`, `registry/`, `evidence/`, `downloads/`, `submissions/`, and `docs/` excluding `docs/bathtub-*` stubs) are untouched; repo-wide privacy scan reports 0 violations across canonical data, generated HTML, and audit artifacts.

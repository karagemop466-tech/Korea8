# Line-by-line integration review — 2026-11-07

Session `arena/0e2dfee2-korea8` (final integration). This file records what was actually checked,
against which official source, and what the result was. Nothing here is inferred; a row that could
not be confirmed says so.

## 1. Repository review

| # | Observation | Evidence | Disposition |
|---|---|---|---|
| 1 | The repository hosts two unrelated bodies of work: a DOE GEMS geothermal fault-prediction project (root README/AGENTS/PROJECT_PROMPT, `docs/`, `evidence/`, `vendor/`, `registry/`, `src/`, `scripts/build_site.py`) and this bathtub trip-lever brief (root site pages, `project/`). | `git ls-tree` of `main`; file headers | The GEMS material is untouched and still served at `docs/`; the bathtub brief owns the root dashboard. Flag F-01. |
| 2 | Five separate copies of the same brief were published by parallel sessions: `bathtub/`, `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, `docs/bathtub-*` (plus `docs/bathtub-overflow/`), and two duplicate executive-summary markdown files at the root. | directory listing; `grep` of navigation links | Retired: 43 pages replaced by redirect stubs to the canonical pages, the two markdown duplicates replaced by pointer notes. Originals remain in Git history at commit `e622cdd`. Flag F-11. |
| 3 | GitHub Pages is configured as branch `main`, path `/`, with `.nojekyll` present, so the repository root is published verbatim. | `gh api repos/karagemop466-tech/Korea8/pages` (2026-11-07) | New pages therefore use relative links only; no CDN and no client-side framework. |
| 4 | The last four Pages builds before this session (`5891eb1`, `0bf6bbe`, `d097deb`, `87e2e17`, `a213cb1`, `e622cdd`) are recorded as `errored` with `duration: 0`, while builds at 13:29, 13:48, 13:49 and 13:50 succeeded. | `gh api .../pages/builds` (2026-11-07) | Content was already ruled out by an earlier session (`.nojekyll` present, no symlinks, largest tracked file 1.7 MB). This session reduces the published file count and re-verifies the deploy below. Flag F-17 in COORDINATION.md. |
| 5 | The owner-supplied quotes and the "5+ plumbers" history exist only in the brief. | brief | Published as owner-supplied, never as verified. F-02, F-03, F-15. |
| 6 | Two licence records do not appear in the canonical table although earlier briefs carried them (FDL #1086935, Precision Rooter, Citywide, Kenneth Asire, Clever, Portola, Cahill, D G Construction). | `bathtub-overflow/data/vendors.json` (now a redirect) | Not re-verified in this pass, so not published in a table that claims 2026-11-07 verification. Flag F-13. |

## 2. Licence verification — 13 rows re-read on the official CSLB record, 2026-11-07

Method: each licence-detail page was opened directly at
`https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=<number>` and the
status line, classifications, entity type, issue/expiry dates, address of record, business phone,
contractor bond and workers'-compensation entry were compared with what this site publishes. CSLB
printed a "data current as of 11/7/2026 12:16–12:19 PM" timestamp on each record.

| Licence | Entity on the official record | Status | Classifications | Expires | Matches site data |
|---|---|---|---|---|---|
| 977638 | EXPERT PLUMBING SOLUTIONS | current and active | C-36 | 2028-10-31 | yes |
| 757796 | BAY AREA PLUMBING | current and active | C-36 | 2027-01-31 | yes |
| 749536 | SAVE - ON - INTERIOR | current and active | B, C-36 | 2028-05-31 | yes (new row) |
| 1024971 | JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER | current and active | C-36 | 2027-03-31 | yes; CSLB spells the street "POTRAL" (F-14) |
| 1089561 | TARO GROUP INC dba HEISES PLUMBING | current and active | C-36, C-10, A, C-20 | 2028-04-30 | yes |
| 829071 | ACE PLUMBING & ROOTER | current and active | C-36, A, C-4, C-16, B, C-10 | 2027-06-30 | yes |
| 1096552 | WE DO CONSTRUCTION INC | current and active | B, C-36 | 2028-09-30 | yes |
| 1106131 | SF BUILDING GROUP | current and active | B | 2027-06-30 | yes |
| 1115649 | RAPID FLOW PLUMBING & ROOTER INC | current and active | B, C-36 | 2028-01-31 | yes |
| 1105133 | HARP SERVICES dba 24/7 SF HANDYMAN & REMODELING SERVICE | current and active | B-2 | 2027-05-31 | yes |
| 1140843 | DISCOUNT PLUMBING ROOTER SERVICES LLC | current and active | C-36, A | 2027-07-31 | yes |
| 1009195 | ADVANCED PLUMBING AND DRAIN INC | current and active, with an Additional Status warning | C-36 | 2027-11-30 | yes; warning retained (F-12) |
| 392967 | AYOOB & PEERY PLUMBING CO INC | current and active | B, C-4, C-16, C-36, C-20 | 2028-09-30 | yes (new row) |

No row needed a correction. Two rows were added (749536, 392967); both were verified in this pass,
not copied from an earlier brief.

## 3. Rule and code verification, 2026-11-07

| Item | Official source read | What the source states | Result |
|---|---|---|---|
| Who may take one plumbing + drywall contract | CSLB B General Building classification page, quoting Business & Professions Code §7057 | A B licensee may not take a prime contract for other trades unless the contract requires at least two unrelated trades, or it holds the specialty licence, or it subcontracts a properly licensed specialty contractor. | Matches the site's T-06 / R-18. |
| Small-job licensing exemption | California Legislative Information, BPC §7048 | The licensing chapter does not apply only where the aggregate price is under $1,000, the work is casual/minor/inconsequential **and** the work does not require a building permit; §7048(c) removes the exemption for advertisers and employers. Amended by Stats. 2025 Ch. 67 (AB 1170), effective 2026-01-01. | Added as T-10. |
| Permit trigger for pipe work behind a wall | SF.gov / DBI, "Apply for a plumbing and mechanical permit" | A permit is required before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried; exemptions are in SF Plumbing Code §104.2; licence types A, B (after scope approval), C-4/C-36, C-16, C-20, C-54 may apply; Express Permits skip staff review; work must be inspected before pipes are covered. | Added as T-09 / R-17. |
| Entry into a tenant-occupied unit | California Legislative Information, Civil Code §1954 | Entry permitted for necessary or agreed repairs; reasonable written notice stating date, approximate time and purpose; 24 hours presumed reasonable; normal business hours unless the tenant consents; no notice in an emergency. | Added as T-11 / R-15. |

Sources not re-read in this pass are still published, but each carries the date it was read
(2026-11-06) in the Fetched column of the Sources page, so the age of every row is visible.

## 4. Automated checks run on the built site

- `python scripts/build_project_site.py` — 94 data rows checked for source links, 0 failures, 0 broken
  internal links, 0 out-of-scope phrases; writes `site-data/build-report.json` and
  `site-data/verification.json`.
- `python scripts/verify_project_site.py` — 155 relative links, 43 redirect pages, 4 data pages
  row-counted against their JSON, 13 licence links, 135 phrase scans, 9 pages with full navigation:
  **PASS**.
- `python scripts/build_redirects.py --check` — 43 of 43 retired pages redirect to an existing
  canonical page.

## 5. Irregularities carried forward

F-01 repository/topic mismatch · F-02 owner-supplied quotes · F-03 non-comparable scopes ·
F-04 review platforms block retrieval · F-05 point-in-time CSLB statuses · F-06 no C-9 drywall
licence in the set · F-07 access-panel section renumbering · F-08 Fast Response address mismatch ·
F-09 no review data for several providers · F-10 photographs pending · F-11 duplicate briefs retired ·
F-12 CSLB future-suspension warning · F-13 unverified candidates excluded · F-14 CSLB street-name
typo · F-15 no written provider confirmation yet · F-16 third-party cost benchmarks.

All sixteen are published on `flagged-for-review.html` with their source links.

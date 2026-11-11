# Final integration verification — 2026-11-11 (arena/331cafce-korea8)

Session `arena/331cafce-korea8`, final integration. Fresh official-source re-verification
performed 2026-11-11 ~02:16–02:30 UTC. Every value below was read directly from the
linked official/company page on this date. No provider was contacted, booked or paid.
Owner-supplied amounts remain owner-reported; verified amounts remain blank. No private
owner context is disclosed in any public artifact.

## 1. Fresh CSLB licence-detail checks (7 records, all match canonical register)

| Licence | Legal name (CSLB) | Phone (CSLB) | Status / expiry | Classifications (CSLB) | Result |
|---|---|---|---|---|---|
| #829071 | ACE PLUMBING & ROOTER | (415) 824-6444 | Current and active / 06/30/2027 | C-36, A, C-4, C-16, B, C-10 | **Match** |
| #1089561 | TARO GROUP INC dba HEISES PLUMBING | (415) 333-0704 | Current and active / 04/30/2028 | C-36, C-10, A, C-20 (no B, no C-9) | **Match** |
| #1115649 | RAPID FLOW PLUMBING & ROOTER INC | (415) 866-8401 | Current and active / 01/31/2028 | B, C-36 | **Match** |
| #995163 | BERNAL HILL DRYWALL INC | (415) 533-8274 | Current and active / 07/31/2028 | C-9, B | **Match** |
| #977638 | EXPERT PLUMBING SOLUTIONS | (415) 531-5340 | Current and active / 10/31/2028 | C-36 only | **Match** |
| #757796 | BAY AREA PLUMBING | (415) 668-8000 | Current and active / 01/31/2027 | C-36 only | **Match** |
| #1024971 | JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER | (415) 596-6115 | Current and active / 03/31/2027 | C-36 only | **Match** |

CSLB pages state "Data current as of 11/10/2026". Workers-compensation details also match:
Ace Financial Pacific 10147545585 (07/13/2026–07/13/2027); Heise Employers Preferred
EIG6235466 (01/11/2026–01/11/2027); Rapid Flow exempt (no employees, eff. 02/03/2026);
Bernal Hill Endurance EAW0000274901 (03/10/2026–03/10/2027); Expert Everest Premier
7600025915261 (07/19/2026–07/19/2027); Bay Area exempt (eff. 12/11/2024); Fast Response
Employers Preferred EIG576950801 (12/18/2025–12/18/2026, flagged near-term expiry).

Official URLs:
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1089561
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796
- https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971

The remaining 19 CSLB records were not re-read by this session and are not claimed
fresh-verified here; they rest on prior receipts (`audit/2026-11-10-4b81abe2/cslb-receipts.json`,
`audit/2026-11-10-0ccaa3f3/receipts/`). Unmerged PR #66's erroneous Heise dates
(09/04/2014 / 09/30/2028) were not copied; canonical 04/06/2022 / 04/30/2028 confirmed.

## 2. Permit, code and licensing law (all match canonical)

- **SF.gov plumbing/mechanical permit page** (https://www.sf.gov/apply-plumbing-and-mechanical-permit):
  "City offices will be closed on Wednesday, November 11 for Veterans Day";
  "You need a permit before cutting into or replacing pipes, particularly pipes that will
  be covered by a wall or buried in the ground. See exemptions in San Francisco Plumbing
  Code Section 104.2"; licence types A, B, C4, C16, C20, C36, C54; "B license, after
  approval based on the scope of work"; help desk 628-652-4900, voicemail answered within
  2 business days. **Match.**
- **BPC §7059(a)** (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059.):
  "Nothing contained in this section shall prohibit a specialty contractor from taking and
  executing a contract involving the use of two or more crafts or trades, if the performance
  of the work in the crafts or trades, other than in which they are licensed, is incidental
  and supplemental to the performance of the work in the craft for which the specialty
  contractor is licensed." **Match** canonical conditional reading; the law does not
  establish that full ceiling restoration is incidental in this job.
- **Heise's Ingleside case** (https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-san-francisco-163802/):
  "Accessed the exterior ceiling to remove the old overflow, installed a new brass P-trap
  and trap adapter, and replaced the tub waste and overflow assembly." Area: Ingleside,
  San Francisco, CA. Phone (415) 333-0704. **Match** canonical strongest adjacent case.

## 3. Review platforms (Yelp blocked; ratings remain blank)

- Yelp business page `https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco`
  returned **HTTP 403** on 2026-11-11 via direct fetch. Canonical policy (ratings/counts
  blank, search excerpts never treated as verified) is correct and unchanged.
- A web-search pass returned Yelp search-index snippets (e.g. Ace 4.7 / 1.5k, Bay Area
  4.8 / 175, Atlas 4.3 / 487, Precision 4.9 / 242). These are **not** copied into canonical
  data as verified values. They are recorded here only as search-index snapshots, consistent
  with `sources.json` retrieval labels ("business page HTTP 403; search excerpt only").

## 4. Canonical data counts (re-counted 2026-11-11)

- Providers: 29 rows (26 CSLB records: 25 active + 1 suspended #1027286; 3 unresolved
  identities Portola / C J's / Golden Gate, fields blank).
- Ranking: 10 ranked + 18 partner/second-bid + 18 not recommended; weights
  C1 0.30 + C2 0.20 + C3 0.20 + C4 0.15 + C5 0.15 = 1.00; rubric anchors published.
- Estimates: 3 owner-reported (Expert $614, Bay Area $550, Fast Response $135, all
  2026-08-30, verified blank); official DBI fees FEE-01 $290 Category 1P etc. (conditional).
- Requirements: 42. Sources: 135 (54 official-government, 27 official-company, 31
  review-platform, 14 repository-primary, 4 official-tool, 3 official-code-publisher,
  1 official-manufacturer, 1 owner-record). Flags: 60 (41 Open, 19 resolved variants).
- Live site `https://karagemop466-tech.github.io/Korea8/` fetched 2026-11-11 and serves
  the same dashboard (Ace/Heise/Rapid Flow call-first, 26 CSLB records, 42 requirements).

## 5. Checks run by this session (before PR)

- `scripts/build_overflow_site.py` — exit 0; counts match §4.
- `scripts/verify_overflow_site.py` — **28/28 PASS** (405 source-covered rows).
- `python -m unittest discover -s tests -p 'test_overflow*.py'` — **40/40 OK**.
- `audit/independent_audit.py` — 405 rows with source, 0 problems.
- `scripts/wording_guard.py` — clean. Sensitive-phrase grep over tracked files: no private
  owner context disclosed; only generic "No permit position was asserted" (audit log) and
  a retired-file categorical assertion already flagged as F-69.
- Build regenerates only timestamp fields in `build-report.json` / `verification-report.json`
  / `site-data/*`; no data value changed.

## 6. Irregularities (non-blocking, published on Flagged for Review)

1. **No new data irregularity found.** All 7 fresh CSLB checks, SF.gov, BPC §7059(a) and
   Heise case match the canonical register.
2. **Yelp ratings/counts remain unverified** (HTTP 403). Search-index snippets exist but are
   not verified business-page values. Flagged (F-14 family); non-blocking.
3. **No provider confirms the exact stuck-lever + ceiling-restoration job, availability or
   price.** All 10 ranked leads are inquiry leads only. Flagged (F-01); non-blocking.
4. **Three supplied estimates are not like-for-like** and none prices ceiling restoration.
   Verified amounts blank. Flagged (F-02…F-05); non-blocking.
5. **Open PRs untouched:** #72, #66, #64, #63, #53, #51, #49, #44, #39, #38, #35, #7.
   None merged, closed or assumed safe. PR #66's Heise-date error is already flagged (F-67).
6. **Unrelated DOE GEMS project** (`docs/`, `vendor/`, `src/`, `registry/`, `evidence/`)
   preserved read-only; not modified by this session.

## 7. Standing rules

No provider contacted/booked/paid. No permit position asserted for this job; DBI
determination remains open. Owner amounts owner-reported only. Public artifacts use neutral
repair-scope language only.

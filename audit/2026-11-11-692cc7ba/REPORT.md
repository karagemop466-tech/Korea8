# Independent audit — 2026-11-11 (arena/692cc7ba-korea8)

Session `arena/692cc7ba-korea8`, tasks `692-02` and `692-03`. Targeted independent
re-verification of canonical items **not covered by the same-day `331cafce` fresh pass**
(that pass covered CSLB #829071, #1089561, #1115649, #995163, #977638, #757796,
#1024971, SF.gov permit page, BPC §7059(a), the Heise case and the Yelp 403 status).
All retrievals were direct fetches of the linked official/company pages on
2026-11-11 ~02:17–02:21 UTC. Machine-readable receipts: [`receipts.json`](receipts.json).

No provider was contacted, booked or paid. Owner-reported amounts remain
owner-reported; verified amounts remain blank. No canonical data, generator, verifier,
generated page or `site-data/**` file was edited by this session; the health suite was
run on a scratch copy so no tracked file changed. No private owner context is recorded
in this report.

## 1. Fresh CSLB licence-detail checks — 8 records, all match canonical

| Licence | Provider (canonical id) | Legal name (CSLB) | Phone | Status / expiry | Classifications | Result |
|---|---|---|---|---|---|---|
| #392967 | Ayoob & Peery (P-09, rank 4) | AYOOB & PEERY PLUMBING CO INC | (415) 550-0975 | current and active / 09/30/2028 | B, C-4, C16, C36, C20 | **Match** |
| #1096552 | We Do Construction (P-08, rank 5) | WE DO CONSTRUCTION INC | (415) 416-5494 | current and active / 09/30/2028 | B, C36 | **Match** |
| #749536 | Save-On-Interior (P-07, rank 7) | SAVE - ON - INTERIOR | (415) 668-8000 | current and active / 05/31/2028 | B, C36 | **Match** |
| #1140843 | Discount Plumbing Rooter (P-16, rank 9) | DISCOUNT PLUMBING ROOTER SERVICES LLC | (650) 991-2100 | current and active / 07/31/2027 | C36, A | **Match** |
| #1027286 | Kenneth Asire Plumbing (P-22, excluded) | KENNETH ASIRE PLUMBING | (415) 913-8048 | **suspended** (Contractors Bond Suspension; bond cancelled 08/16/2026) / 05/31/2027 | C36 | **Match** — exclusion remains correct |
| #1106131 | SF Building Group (P-11, conditional lead) | SF BUILDING GROUP (South San Francisco) | (415) 297-2246 | current and active / 06/30/2027 | B only | **Match** — F-07 treatment remains correct |
| #868994 | Atlas Plumbing & Rooter (P-25) | ATLAS PLUMBING & ROOTER | (650) 871-9863 | current and active / 03/31/2028 (reissued 03/25/2008) | C36, A | **Match** |
| #954813 | 24/7 Rooter and Plumbing Services (P-26) | 24 / 7 ROOTER AND PLUMBING SERVICES INC dba A & R PLUMBING | (415) 586-6851 | current and active / 11/30/2028 | C36, C-61/D56, A | **Match** |

CSLB pages state "Data current as of 11/10/2026". Compared fields: legal name,
registered city, business phone, entity type, issue/reissue/expiry dates, status,
classifications and workers-compensation summaries — 0 mismatches. The 2015–2016
Save-On-Interior miscellaneous entries (cash-deposit letters) were confirmed present on
the CSLB record, consistent with the existing published flag. The remaining CSLB records
were not re-read by this session and are not claimed fresh-verified here.

## 2. Statutes and fee schedule — all match canonical

- **BPC §7057** (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057.):
  full text retrieved. Subdivision (b) confirms the canonical conditional reading for B
  licensees: a prime contract involving trades other than framing/carpentry requires at
  least two unrelated trades, or the appropriate classification, or subcontracting with
  an appropriately licensed contractor. **Match.**
- **BPC §7057.5** (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057.5.):
  full text retrieved. B-2 Residential Remodeling requires three or more unrelated trades
  per contract; listed trades include drywall (b)(1)(A) and plumbing fixtures including
  tubs (b)(1)(K); (c)(3)(A) prohibits installing/replacing/substantially altering plumbing
  systems or component parts without the appropriate classification or a licensed
  subcontractor; (c)(3)(B) permits minor alterations to effectuate fixture work. This
  supports the canonical F-08 treatment of the B-2 lead. **Match.**
- **DBI Table 1A-C, July 2026** (https://media.api.sf.gov/documents/Table_1A-C_-_Plumbing_Mechanical_2026.pdf):
  applies to permits issued on and after July 12, 2026. All five canonical fee rows
  verified: Category 1P $290 (single plumbing fixture installation or single bathroom
  remodel, max two inspections), Category 11P/M $320, regular inspection $519/hour,
  off-hour $555/hour, reinspection $259/half-hour. **Match (5/5).** Fees remain
  conditional categories, not confirmed job prices, as canonically labelled.

## 3. Company websites — match canonical service claims

- **Ayoob & Peery** (https://www.ayoobpeery.com/): live; "locally owned mechanical
  contractor based in San Francisco", wet-side systems (general plumbing, steam heating,
  hydronics, fire protection), "design/build solutions for commercial applications";
  call link 415-550-0975 equals the CSLB phone. Canonical P-09 service claim **matches**.
- **We Do Construction** (https://www.wedoconstructions.com/services/general-contractor-in-san-francisco/):
  live; states "CSLB #1096552 · Class B + C-36 · Design-Build", bathroom remodeling with
  C-36 self-performed under one contract. Canonical P-08 service claim **matches**.

## 4. Repository health suite — run on a scratch copy (no tracked file edited)

At merge-base `bcf81b2` plus this session's claim commit, in `/tmp/k8-health`:

| Check | Result |
|---|---|
| `scripts/build_overflow_site.py` | exit 0 (ranking 10, ranking_held 18) |
| `scripts/verify_overflow_site.py` | **28/28 PASS** — 277 tracked HTML links, 0 broken |
| `python -m unittest discover -s tests -p 'test_overflow*.py'` | **40/40 OK** |
| `audit/independent_audit.py` | 11 pages, 405/405 rows with source, 217 internal links, **0 problems** |
| `scripts/wording_guard.py` | clean |
| `scripts/stage_overflow_pages.py` | 46 linked public files staged |

`git status --porcelain` in the session working tree showed no modification to tracked
files from these runs.

## 5. Live publication — serving current canonical dashboard

- Pages API (https://api.github.com/repos/karagemop466-tech/Korea8/pages): status
  `built`, latest build commit `dff1a3ca`, no error (checked 2026-11-11T02:21Z).
- Workflow `overflow-pages.yml` on `main`: runs 42945238155 (`dff1a3ca`), 42945140421
  (`53145f11`), 42945103895 (`258d08f8`) — all completed **success** (02:18–02:19 UTC).
- Routes fetched live: `index.html` (canonical hero, call-first block, status snapshot),
  `verification.html` (serves the 11 November audit links and PR #76 deployment record),
  `flagged-for-review.html` (serves 61 flagged items with source links). All served
  canonical content.

## 6. Findings

- **Discrepancies against canonical data: none (0 mismatches across every field compared).**
- Observation (non-blocking, optional enrichment): canonical P-26 `issue_date` is blank
  while CSLB #954813 shows 11/18/2010. Blank is conservative and not an error; logged as
  a cross-session request for the integration owner rather than edited here.
- Observation: CSLB lists the same business phone, (415) 668-8000, on both #749536
  (Save-On-Interior) and #757796 (Bay Area Plumbing). The unproven-relationship question
  is already published as a flag; this session confirms both records list that number as
  of the 11/10/2026 data date.
- Observation: the Kenneth Asire suspension (bond cancellation 08/16/2026) is still in
  effect on the current CSLB data date, so the canonical shortlist exclusion stands.

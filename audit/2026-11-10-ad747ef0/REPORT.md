# Independent audit and re-verification — 2026-11-10 (session `arena/ad747ef0-korea8`)

Scope: the canonical bathtub-overflow dashboard (`overflow-integration/data/` → root `*.html` via
`scripts/build_overflow_site.py`). This session performed a **fresh, independent** line-by-line
re-verification of the official sources behind the highest-stakes claims — the ranked provider
licences, the SF permit requirement, and the official DBI fee schedule — plus the structural build,
verifier, unit-test and live-deployment checks. Parallel brief directories and the unrelated DOE GEMS
tree were read but not modified.

Everything below was retrieved directly on **2026-11-10** from the official host. Nothing is asserted
from memory or from another session's note.

## 1. Provider licence records — independent re-read of the top-ranked leads + partner + suspended record

Each page was fetched from `https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=<n>`
on 2026-11-10. The CSLB "Data current as of" banner on every fetched page read **11/9/2026 4:49 PM**,
confirming the records are current.

| Licence | Business (as published by CSLB) | Status | Classifications | Expiry | Phone | Stored record matches |
|---|---|---|---|---|---|---|
| 829071 | ACE PLUMBING & ROOTER | current and active | C36, A, C-4, C16, B, C10 | 06/30/2027 | (415) 824-6444 | yes — every field |
| 1089561 | TARO GROUP INC dba HEISES PLUMBING | current and active | C36, C10, A, C20 | 04/30/2028 | (415) 333-0704 | yes — every field |
| 1115649 | RAPID FLOW PLUMBING & ROOTER INC | current and active | B, C36 | 01/31/2028 | (415) 866-8401 | yes — every field |
| 995163 | BERNAL HILL DRYWALL INC | current and active | C-9, B | 07/31/2028 | (415) 533-8274 | yes — every field |
| 1027286 | KENNETH ASIRE PLUMBING | **suspended — Contractors Bond Suspension** | C36 | 05/31/2027 | (415) 913-8048 | yes — status + bond cancellation 08/16/2026 |

Details confirmed on each record:

- **Ace Plumbing & Rooter (829071)** — Corporation, issued 12/18/2003 (matches "active since 2003");
  contractor's bond with Merchants Bonding (effective 09/04/2026); workers' comp with Financial Pacific
  (effective 07/13/2026). Address 1090 Bryant St, San Francisco. Classifications C-36, A, C-4, C-16,
  B, C-10 all present. Broadest single-licence coverage claim **verified**.
- **Heise's Plumbing (1089561)** — Corporation (TARO GROUP INC dba HEISES PLUMBING), issued 04/06/2022;
  bond with American Contractors Indemnity (effective 05/27/2025); workers' comp with Employers Preferred
  (effective 01/11/2026). Classifications C-36, C-10, A, C-20 — **no B and no C-9**, confirming the
  standing caveat that the ceiling-restoration party must be named separately.
- **Rapid Flow Plumbing & Rooter (1115649)** — Corporation, issued 01/29/2024 (matches "2024 licence");
  workers' comp **exempt** (certified no employees, effective 02/03/2026), confirming the standing
  workers-comp-exemption caveat. B + C-36 confirmed.
- **Bernal Hill Drywall (995163)** — Corporation, issued 07/28/2014; workers' comp with Endurance
  Assurance (effective 03/10/2026). C-9 + B confirmed — the only C-9 (drywall) restoration partner in
  the set. No C-36, confirming it is a restoration partner, not a plumbing lead.
- **Kenneth Asire Plumbing (1027286)** — Sole ownership, issued 05/25/2017; **suspended** for
  Contractors Bond Suspension; contractor's bond with North River Insurance cancelled **08/16/2026**.
  C-36 only. Suspension status and exclusion from the active shortlist **verified**.

## 2. Permit requirement — SF.gov plumbing/mechanical permit page

Fetched `https://www.sf.gov/apply-plumbing-and-mechanical-permit` on 2026-11-10. Confirmed:

- "You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by
  a wall or buried in the ground." — directly supports the permit trigger for this ceiling-access job.
- Exemptions reference **San Francisco Plumbing Code Section 104.2** (the conditional-exemption path
  cited in the canonical Code & permit page).
- Permit scope requires a C4, C16, C20, C36, C54, B, or A licence; C-36 holders may apply for a
  plumbing permit, and B holders may apply after scope approval (kitchen/bath permits can be approved
  immediately for B contractors).
- Fee schedule referenced: `Table_1A-C_-_Plumbing_Mechanical_2026.pdf` (verified independently below).
- Page also notes City offices closed Wednesday, November 11 for Veterans Day (current/relevant).

## 3. Official DBI fee schedule — `Table_1A-C` (July 2026)

Fetched `https://media.api.sf.gov/documents/Table_1A-C_-_Plumbing_Mechanical_2026.pdf` on 2026-11-10.
This is the City and County of San Francisco DBI "Plumbing/Mechanical Issuance and Inspection Fees"
schedule, dated **July 2026**, applying to permits issued on and after July 12, 2026. Every fee in the
canonical Estimates page was confirmed:

| Claim | Published fee | Match |
|---|---|---|
| Category 1P — single residential unit, single plumbing fixture / shower pan / kitchen-bath remodel, max 2 inspections | $290 | yes |
| Category 11P/M — miscellaneous plumbing/mechanical | $320 | yes |
| Regular inspection | $519 per hour | yes |
| Off-hour inspection | $555 per hour | yes |
| Re-inspection / additional inspection (§108A.8) | $259 per half hour | yes |

The canonical data correctly labels these as official **fees** (not a job price), and the job category
applicability remains unconfirmed — no overstatement.

## 4. Structural build / verifier / unit-test checks

Re-run on the merged `main` (`98b3d09`) after resolving the rebase conflict with the concurrent
`87e121e1` session (both sessions' audit links are retained on the Verification page). The 5 CSLB +
SF.gov + DBI source re-reads in §1–§3 were fetched directly from the official hosts on 2026-11-10 and
are independent of this data refresh.

- `python scripts/build_overflow_site.py` — OK. 25 provider identities (24 CSLB + 1 unresolved),
  42 requirements, 3 owner estimates, 8 technical rows, 13 compliance rows, 18 review rows,
  **110 sources**, 48 flags, 10 ranked + 14 held.
- `python scripts/verify_overflow_site.py` — **27/27 PASS**. 335 canonical table rows each carry a
  registered official-primary source link; 303 tracked internal HTML links with 0 broken targets;
  owner amounts published as owner-reported with verified amounts blank; review ratings/counts blank;
  suspended provider excluded from priority leads; no conflict markers / placeholders / None literals.
- `python -m unittest discover -s tests -p 'test_overflow*.py'` — **21/21 PASS**.
- `git diff --check` on the working tree — clean (no whitespace errors).

## 5. Live GitHub Pages deployment — independent HTTP re-fetch

The live site at `https://karagemop466-tech.github.io/Korea8/` was fetched directly on 2026-11-10:

- `index.html` — served the 11-page dashboard; status snapshot rows each link their source; the
  ranked "Who to call first" order (Ace, Heise's, Rapid Flow, Ayoob & Peery, We Do Construction) and
  phones match the canonical data.
- `decision-analysis.html` — served the full ranked table with score components, cost basis, "what to
  ask" and CSLB links per row; reviewed date 2026-11-10.
- `flagged-for-review.html` — served 48 flagged items (F-01 … F-48) with severity, action, status and
  source links.

`gh api repos/.../pages` reports status **built**, source branch `main`, path `/`, public, HTTPS
enforced. GitHub Actions workflow runs for the latest push commits (8e7dbd6 / 7c71101 / b30f89d) all
completed successfully. The deployment is live and serving current content.

## 6. Findings

- **No hallucinated values found.** Every official-source value spot-checked (licence numbers, legal
  names, classifications, statuses, expiry dates, phone numbers, the SF permit requirement, and all
  five DBI fee amounts) matches the canonical data exactly. CSLB records were current as of 11/9/2026.
- **No defects corrected.** The canonical data, build, verifier and tests were already accurate; this
  session added only this independent audit record and its coordination log entry.
- **Standing non-blocking flags remain published** (48 items), including: no provider confirms the
  exact all-in-one job / availability / combined price; the three owner estimates have unlike scopes;
  B + C-36 does not prove drywall self-performance; Kenneth Asire is bond-suspended; Portola identity
  unresolved; Yelp ratings blocked (HTTP 403). None of these are overstated.

## 7. Limitations of this audit

- This session independently re-read **5 CSLB licence pages** (the three top-ranked plumbing leads,
  the restoration partner, and the suspended record) rather than all 24; the remaining 19 were
  re-verified by prior sessions on 2026-11-08/10 and are recorded in their audit reports. The five
  re-read here are the ones carrying the highest decision weight.
- Yelp business pages remain blocked (HTTP 403); numeric ratings/counts stay blank by design rather
  than being inferred.
- The Heise's case page embeds a 404 template block (already disclosed in the source register and
  flagged); this session did not re-fetch that third-party page.
- No provider was contacted; no availability, schedule or combined price has been confirmed.

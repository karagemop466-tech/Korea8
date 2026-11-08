# Independent read-only audit — session arena/0404117b-korea8

Checked: 2026-11-08 UTC. Baseline: current `main` merge `2d680ca` (PR #50) plus this session's board-only handoff commit.

## Scope and method

This report is deliberately read-only with respect to the canonical dashboard. It does not rewrite the shared build/verification reports, generator, data, or root pages while other sessions have active overlapping claims. It inventories tracked files, parses tracked JSON, crawls tracked-HTML internal links, and re-parses canonical table rows against an expanded official/primary-host policy.

Automated results are in `read-only-audit.json` and `repository-inventory.json`.

| Check | Result |
|---|---:|
| Tracked files inventoried | 316 |
| Tracked JSON files parsed | 100 |
| JSON parse errors | 0 |
| Tracked-HTML internal links checked | 235 |
| Broken internal links | 0 |
| Canonical table rows parsed | 274 |
| Rows with a recognized official/primary link under the expanded host policy | 274 |
| Strict row-source gaps under that policy | 0 |

The expanded policy recognizes the official code publisher `amlegal.com`, the official company hosts `ayoobpeery.com` and `bernalhilldrywall.com`, and the newly verified company hosts `fivestarplumbingsf.com` and `isacksonplumbing.com`. The older shared independent parser still omits some of these hosts and therefore can classify valid source-linked rows as blank/unverified fallbacks. That is a parser-policy gap, not evidence that the rows lack links.

## Current canonical baseline

The current merged baseline still contains:

- 24 provider identities: 23 CSLB records plus one unresolved name.
- 42 requirements, 73 sources, 40 flags, 5 review rows, 10 ranked candidates.
- An Ace-first weighted ranking and hardcoded dashboard/summary counts in places.
- Owner-reported amounts $614 / $550 / $135 with verified amounts blank.
- No provider contacted, booked, or confirmed for the exact stuck trip-lever plus ceiling-restoration job.

## Active parallel work observed

At the time of this audit, the following overlapping work was active or open:

| PR / branch | State observed | Coordination note |
|---|---|---|
| #49 `arena/55859fbc-korea8` | open, conflicting | Adds Atlas/Discover/Plumbing 1/LFM leads, BBB/Diamond Certified rows, cost drivers, and UI filtering. Contains flag/provider ID collisions with newer main and should be rebased, not merged as an older snapshot. |
| #51 `arena/54cba99d-korea8` | open, conflicting | Adds official contact-role evidence and an inquiry order, but omits owner-reported amounts from public price cells. The standing owner-report presentation should remain labelled, not silently suppressed. |
| #52 `arena/3946905e-korea8` | open, conflicting | Adds Atlas and a lexicographic `decision.json`, stricter row-source checks, and retains labelled owner amounts. Needs rebase onto newer main and preservation of other sessions' verified additions. |
| `arena/aeb846ac-korea8` | branch active, no PR observed yet | Corrects quote-issuer identity to possible name matches, adds In & Out Plumbing and Construction #878184 with historical CSLB citations, and performs privacy cleanup. Should be preserved in final integration. |

This session has not merged or closed another session's PR. Canonical implementation is paused until the active overlapping claims are released by merge/completion or become stale under the board's >60-minute handoff rule.

## Independently verified additions ready for final integration

These were fetched directly by this session on 2026-11-08 and are not yet in the canonical baseline:

### Five Star Plumbing & Rooter — CSLB #996627

- Official CSLB: <https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=996627>
- CSLB banner timestamp: `11/8/2026 3:01:12 PM` (timezone not stated).
- Legal name: `5 STAR PLUMBING & ROOTER`; corporation; San Francisco.
- Classifications: A, B, C-36. Status: current and active. Expiry: 11/30/2027.
- CSLB phone: (415) 410-4420. Workers-compensation policy recorded; expires 10/17/2027.
- CSLB records issue 09/11/2014 and reissue to another entity 11/17/2025. Confirm the current contracting entity.
- Official company contact page: <https://fivestarplumbingsf.com/contact/> publishes (415) 724-7083 and 811 San Jose Avenue. The phone differs from CSLB; do not silently substitute.
- Official company site advertises plumbing diagnosis/permits through final restoration and in-house project phases. This is a company claim, not exact-job acceptance.
- A directly retrieved Yahoo Local syndicated listing carries company-supplied ceiling-demolition and drywall/paint-restoration images. Yelp business-page retrieval was blocked; numeric ratings/counts remain blank.
- Decision-support implication: strongest all-in-one inquiry lead found by this session, but only after entity/phone reconciliation and written confirmation of the named restoration crew, occupied-unit plan, permit path, and price.

### Isackson Plumbing — CSLB #1114153

- Official CSLB: <https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1114153>
- CSLB banner timestamp: `11/8/2026 3:01:12 PM` (timezone not stated).
- Legal name: `ISACKSON PLUMBING`; sole ownership; CSLB address Rossmoor, CA.
- Classification: C-36 only. Status: current and active. Expiry: 12/31/2027.
- CSLB phone: (949) 535-6586. Workers-compensation exemption: certified no employees.
- Official company contact page: <https://isacksonplumbing.com/contact/> publishes (415) 406-3511 and 3149 California St, San Francisco. Address/phone differ from CSLB; resolve before contracting.
- Yelp search-index caption says tub/waste-and-overflow installation; business page blocked. This is adjacent, unverified evidence, not stuck-lever extraction or ceiling-restoration proof.
- Decision-support implication: plumbing-only comparison lead; needs a named restoration party.

## Corrections that should survive final integration

1. Every canonical table row should carry a recognized official/primary source link. The shared independent parser should recognize the official code publisher and verified company hosts rather than relying on blank/unverified fallbacks.
2. Watco model instructions support overflow-side removal/readjustment and a closed-position sealing check. They do not explicitly prescribe a separate fill/leak-test protocol; project leak testing should be labelled a proposed acceptance control.
3. The retrieved SF Plumbing Code §104.2 text was in American Legal Publishing chunk 13 (zero-based), not chunk 14.
4. Heise's Marina case title is now presented as drain cleaning/overflow-gasket service; keep it as adjacent self-published evidence and disclose the embedded 404 template block.
5. Owner-reported quote names are not independently confirmed license matches. Amounts may remain visible only as owner-reported, with verified amounts blank and identity flagged.
6. Review-platform numeric ratings/counts should remain blank where direct business-page retrieval was blocked or syndicated figures disagree.
7. Dashboard/summary counts and ranking prose should be generated from canonical data, not hardcoded.
8. Flag and provider IDs must be deduplicated across parallel branches before merge. In particular, do not reuse F-37/F-40/P-25/P-26 for different meanings.

## Addendum — parallel evidence rechecked by this session

After the initial read-only pass, this session independently rechecked several sources raised by parallel audits/branches. These observations are ready for final integration but do not edit the canonical dashboard while overlapping claims are active.

| Item | Rechecked observation | Integration consequence |
|---|---|---|
| Heise's Paint, Patch & Drywall Repair | Official page advertises plumbing-access drywall cutout repair, ceiling patching after leak verification, paint/texture prep, occupied homes/rentals and tenant-schedule coordination. | Strong conditional all-in-one service evidence. CSLB #1089561 still has no B/C-9, so the written contract must name the properly licensed restoration party or lawful subcontract structure. |
| Five Star official homepage | Repeats diagnosis/permits through final restoration, one accountable team, in-house phases, flat-rate pricing and property-manager service. | Supports first-inquiry all-in-one lead status, but remains a company claim; entity/phone reconciliation and exact-job acceptance are still required. |
| Atlas contact page | Official site lists 415-849-2346 and 3311 Mission Street Suite 165; CSLB #868994 lists (650) 871-9863. | Preserve both source-linked numbers and flag the role/contact discrepancy; do not silently substitute. |
| In & Out bathroom-plumbing URL | `https://inandoutplumbing.com/bathroom-plumbing/` returned a 404 page while displaying license #878184. | Do not cite that URL as live service evidence without another retrieved official page. CSLB complaint disclosure lists six citations dated 2017–2018: three completed and three for disclosure only. |
| SF Plumbing Code §104.0 | Chunk 13 contains §104.1/§104.2 administration/exemption text; chunk 14 contains §104.3–§104.5, including the conditional permit-issuance-fee waiver for fixture/gas-appliance replacement without drainage/piping/venting change. | Correct chunk attribution; publish the fee waiver as conditional, not a permit exemption or inspection-fee waiver. |
| BPC §7048 | Subdivision (c) excludes persons who advertise/hold out as contractors or employ another person to perform/assist the work. | Add the advertising/employment exclusions to the small-job exemption summary. |
| BPC §7057 | Subdivision (b) excludes framing/carpentry from the two-unrelated-trades count for prime/subcontracts involving other trades. | Add the framing/carpentry exclusion to the B-license combined-scope summary. |

The parallel independent audit `arena/6880fb12-korea8` reached compatible conclusions on Heise drywall evidence, Watco step 7, §104.2/§104.5 chunks, BPC exclusions and registered-primary-source row checks. Final integration should preserve both audits and apply the corrections once the active canonical claims are released or stale under the coordination rule.

## Privacy and outreach

No provider was contacted, booked, or paid. Public wording remains neutral repair-scope language and uses DBI's published permit position; no permit exemption is assumed.

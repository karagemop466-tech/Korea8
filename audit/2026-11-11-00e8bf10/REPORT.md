# 2026-11-11 review — licence re-read, open-question register and publication check

Session `arena/00e8bf10-korea8`. Retrieved 2026-11-11 (UTC). Scope: re-read every identified CSLB
licence record, the statutes and city pages the decision rests on, add the decision-blocking question
register the brief asks for, and check the publication boundary. Unrelated DOE GEMS research files were
read only and are unchanged.

## What was done

| Step | Result |
|---|---|
| Claimed the shared board before any other edit | `COORDINATION.md`, commit `667ce1c`, pushed to the session branch |
| Re-read every identified CSLB licence record | **27 records** fetched directly (26 in the provider register plus dissolved #787733); receipts in [`cslb-receipts.json`](cslb-receipts.json) |
| Re-read the statutes and city pages the decision rests on | **13 pages** re-read; **4 carried forward** and marked as not re-fetched today — [`source-checks.json`](source-checks.json) |
| Added the decision-blocking question register | New `overflow-integration/data/questions.json` (14 questions, 5 discovery steps) and new `questions.html` |
| Publication-boundary check | No private owner context, no permit-avoidance statement and no numeric review value appears in any published file |
| Rebuild and checks | Build, verifier, unit tests, wording guard, independent audit and staging run before the merge |

## Licence re-read result

All 27 records matched the stored provider fields — legal name, entity, city, phone, classification
letters, status and workers'-compensation position — with **one exception**:

- **George Salet Plumbing & Rooter, #888630.** The register stored expiry `2026-12-31` with the note
  “License expires 12/31/2026; confirm renewal before scheduling.” The CSLB licence-detail page re-read
  today (page timestamp “Data current as of 11/10/2026 6:16:03 PM”) shows **Expire Date 12/31/2028**.
  The stored field, its source timestamp, the additional-status note and the sentence in F-53 were
  corrected to the official value. Recorded as **F-72**. The licence is active either way, so no ranking
  or shortlist position changes.

Other live-status observations confirmed today rather than corrected:

- **Kenneth Asire Plumbing #1027286** is still **under contractor's-bond suspension**, with the bond
  cancelled 08/16/2026. It stays excluded from the hiring order.
- **Advanced Plumbing and Drain #1009195** still carries the CSLB additional status that the licence may
  be suspended at a future date for an outstanding final liability.
- **D G Construction #297604** still shows a published complaint disclosure: citation 2 2022 002099 dated
  03/23/2023, “FOR DISCLOSURE ONLY PER B&P CODE 7124.6”, violation 7114.A “Aided and abetted non-licensee”.
- **Heise's Pluming #787733** remains expired 03/31/2023, cancelled after expiration 02/12/2025 with a
  Secretary of State dissolution the same day; the active licence is #1089561 TARO GROUP INC.

## Statute and city-page re-read result

Re-read and matching the published rows: SF.gov plumbing/mechanical permit page (including today's
Veterans Day closure banner), SFPC §104.2 (nine conditional exemptions, chunk 14), DBI Table 1A-C July
2026 fee schedule (1P $290, 2PA $549, 2PB $809, 11P/M $320, $519/hour regular, $555/hour off-hour,
$259/half-hour reinspection), BPC §§7057, 7057.5 and 7059, Civil Code §1954, CSLB contract guidance,
CSLB C-9 classification and the CSLB complaint-disclosure record for #297604.

Carried forward and explicitly marked as not re-fetched today: SFBC §106A (amlegal), the CSLB 16 CCR §831
rulemaking notice, and the two EPA lead/asbestos pages. The site already labels retrieval dates per
source; this report adds that these four were not re-read in this pass, so nobody reads today's date as
covering them.

Yelp business pages returned **HTTP 403** again today, so no rating or review count is published.

## New deliverable — open questions

The brief asks for a clear list of questions, information and answers that must be settled before a
decision, plus suggestions for discovering what is missing. That is now a first-class page:

- `overflow-integration/data/questions.json` — 14 questions, each with: what the official sources already
  establish, what is still missing, the concrete step that would produce it, which decision it gates, its
  status, and source links.
- `questions.html` — rendered in the dashboard navigation as **Open questions**, with the question table
  and five discovery steps: photograph the overflow plate and the ceiling below; ask DBI for one written
  scope determination; send one identical request to three leads; ask for the records only the owner
  controls; re-check the licence on the day of booking.
- Status split: 9 questions fully open, 5 partially answered. Nothing is presented as answered without a
  source.

## Repo review

| Finding | Detail | Disposition |
|---|---|---|
| Provider expiry field stale | #888630 stored 2026-12-31, official 12/31/2028 | Corrected; F-72 |
| Flag numbering gap | Register runs F-01…F-55 then F-65…F-72. No tracked file references F-56…F-64 and no published row is missing | Recorded here and in the board. Deliberately **not** added to the public flag table, because a repository numbering note has no official source to cite and the table rule requires one |
| Two trees for the same brief | Redirect stubs under `bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`, `trip-lever/` still present | Preserved as history, not linked into the published closure; unchanged |
| Citation URL shape | `CitationViolationDisclosure.aspx?LicType=LIC&LicNum=…` alone returns “Invalid Parameters passed” | The recorded full-parameter URL works; noted so a future reader does not think the record vanished |
| CSLB contract URL | The generic `/Consumers/Contracts/` path returns 404 | The recorded `/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx` path resolves |
| Unresolved identities | Portola Plumbing, C J's Plumbing, Golden Gate Plumbing | Still blank and excluded; unchanged |

## Publication boundary

Checked the published closure for context about the occupants, unverified numeric review values,
placeholder text, and any permit claim that the linked official text does not support. None found. The published
pages state the official permit rule, the conditional exemptions, the trade-licensing structure and the
fees. Owner-supplied amounts remain labelled owner-reported with verified amounts blank. No provider was
contacted, booked or paid.

## Limits of this review

- Structural checks prove internal consistency and that each row links a registered official source; they
  do not prove that every source supports every claim.
- Company service claims are self-descriptions and were spot-checked, not exhaustively re-read.
- Four sources listed above were not re-fetched today.
- No exact-job acceptance, availability, insurance certificate or combined written price exists for any
  provider, and this review did not create any.

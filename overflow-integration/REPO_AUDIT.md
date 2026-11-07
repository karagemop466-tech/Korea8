# Repository audit — bathtub overflow integration

Reviewed 2026-11-07 on branch `arena/f4bb970c-korea8`, baseline `origin/main` `09d76c1`.

## Method and scope

- Every tracked text file was inventoried and JSON files parsed; tracked HTML was crawled for internal links.
- Bathtub-related registers were read row by row and deduplicated into `overflow-integration/data/requirements.json` with legacy ID mappings.
- Provider factual cells were transcribed from directly retrieved CSLB license-detail pages; company service claims and review excerpts are separately labeled.
- Code/permit/tenant/contract rows were checked against the linked agency/statute/manufacturer sources. Unretrieved code text remains blank/unverified.
- Unrelated DOE GEMS scientific claims were **not** revalidated as part of this repair audit; those files are preserved and labeled legacy. This is an explicit scope limitation, not a verification claim.

## Baseline findings corrected in the canonical rebuild

| Finding | Baseline evidence | Resolution |
|---|---|---|
| B + C-36 described as automatically covering both trades directly | `executive-summary.html` line 33 at commit `09d76c1` | C-9/BPC §7057 wording; restoration party must be named |
| Owner-supplied quote amounts suppressed | `index.html` line 27 and estimates data at `09d76c1` | Amounts shown only as owner-reported; verified amounts blank |
| SF Plumbing Code §104.2 listed as not retrievable | root code/flags at `09d76c1` | Operative text retrieved from American Legal Publishing chunk 14; job applicability still open |
| SF Building Group treated as combined plumber/GC | earlier root provider data | CSLB #1106131 is B-only; plumbing must be licensed/subcontracted |
| HARP/24-7 grouped with B licensees | earlier root provider data | CSLB #1105133 is B-2; BPC §7057.5 limits published |
| Save-On/Bay Area common operator inferred | earlier notes | Shared address/phone recorded; common control unconfirmed |
| Portola identity unresolved | earlier briefs | License/contact/status fields blank; official lookup linked |
| Numeric Yelp ratings in historical data | `bathtub-overflow/data/vendors.json` | Canonical review ratings/counts blank; retrieval limits published |
| Duplicate/conflicting public routes | parallel session histories | Main redirect stubs/archives preserved; one canonical root dashboard |
| Pages status lag/errored during rapid merges | Pages API and coordination logs | Specific-commit live check required; static-artifact workflow added |

## Preserved work

- Redirect stubs under `bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`, `trip-lever/`, `docs/bathtub-*`.
- `archive/superseded-2026-11-07/`, including archived generators and the prior canonical generator/verifier.
- Closed unmerged PR #33 commit `a0e5376d36dab007999bed2eb6517d6d45d28f31` remains reviewable by SHA; its facts were independently rechecked rather than merged over the newer baseline.
- Unrelated GEMS `docs/`, `src/`, `vendor/`, `registry/`, `evidence/`, `downloads/`, `submissions/`, scripts and workflow.

## Automated checks

See `verification-report.json` and `build-report.json`. The verifier checks page/nav presence, HTML balance,
internal links/anchors, row-source coverage, count parity, CSLB link parity, blank unverified fields,
owner-reported amount labeling, suspended-provider exclusion, neutral wording and tracked-HTML links.

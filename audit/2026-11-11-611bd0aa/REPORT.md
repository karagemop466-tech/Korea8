# 2026-11-11 fresh re-verification and line-by-line repo review (611bd0aa)

Session: `arena/611bd0aa-korea8`. Baseline: `main` at `b491225` (PR #77 merge).
Scope: `audit/2026-11-11-611bd0aa/**`, `COORDINATION.md` (append only),
`overflow-integration/data/{ranking,sources,flags}.json`,
`scripts/build_overflow_site.py` (one verification-page link), and generated
output from the canonical build. No provider was contacted, booked or paid.
Owner-supplied amounts remain owner-reported with verified amounts blank.

## Fresh official-source reads (2026-11-11)

Seven CSLB licence-detail pages were read directly. Each page carries the
board banner "Data current as of 11/10/2026", the same snapshot as the
canonical 2026-11-10 review. Legal name, phone, status, classifications,
expiry and issue date matched `overflow-integration/data/providers.json`
for all seven records (dates differ only in display format, ISO vs US).
Receipts with the exact values read: `receipts.json` in this directory.

| Licence | Provider | Fresh result |
|---|---|---|
| 829071 | Ace Plumbing & Rooter | Current and active; B + C-36 + A/C-4/C-16/C-10; (415) 824-6444; expires 06/30/2027 |
| 1089561 | Heise's Plumbing (Taro Group Inc) | Current and active; C-36/C-10/A/C-20; (415) 333-0704; expires 04/30/2028 |
| 1115649 | Rapid Flow Plumbing & Rooter Inc | Current and active; B + C-36; (415) 866-8401; expires 01/31/2028; workers-comp exempt |
| 995163 | Bernal Hill Drywall Inc | Current and active; C-9 + B; (415) 533-8274; expires 07/31/2028 |
| 977638 | Expert Plumbing Solutions | Current and active; C-36; (415) 531-5340; expires 10/31/2028 |
| 1024971 | Fast Response Plumbing & Rooter | Current and active; C-36; (415) 596-6115; workers comp expires 12/18/2026 |
| 1027286 | Kenneth Asire Plumbing | Suspended (bond suspension); C-36; (415) 913-8048 |

Two further official pages were read directly:

- SF.gov "Apply for a plumbing and mechanical permit" still states that a
  permit is needed before cutting into or replacing pipes, that exemptions
  are in San Francisco Plumbing Code §104.2, and that city offices are
  closed Wednesday, November 11 for Veterans Day. The page does not state
  that online filing is unavailable. This matches the published F-49/C-14
  wording and the 2026-11-12 next-business-day note.
- California BPC §7059(a) text was read on leginfo.legislature.ca.gov.
  The incidental-and-supplemental sentence for specialty contractors is
  present as published. No change to the C-15/R-15/T-06 analysis.

Official links for every row above are the CSLB licence-detail URLs,
https://www.sf.gov/apply-plumbing-and-mechanical-permit and
https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059.
Full URLs and values read are in `receipts.json`.

## Ranking recompute

Weights C1 0.30, C2 0.20, C3 0.20, C4 0.15, C5 0.15 sum to 1.00.
Recomputed weighted scores from `ranking.json` score components:

| Published rank | Provider | Score |
|---|---|---|
| 1 | Ace Plumbing & Rooter | 3.85 |
| 2 | Heise's Plumbing | 3.45 |
| 3 | Rapid Flow Plumbing & Rooter | 3.15 |
| 4 | Ayoob & Peery | 3.15 |
| 5 | We Do Construction | 2.95 |
| 6 | Expert Plumbing Solutions | 2.90 |
| 7 | Save-On-Interior | 2.60 |
| 8 | Bay Area Plumbing | 2.55 |
| 9 | Fast Response Plumbing & Rooter | 2.20 |
| 10 | Discount Plumbing Rooter Services | 1.70 |

Ranks 3 and 4 tie at 3.15. The generator tie-break is higher C2 first
(Rapid Flow C2 3, Ayoob & Peery C2 1), so Rapid Flow #3 is correct under
the published rule. The published order on `decision-analysis.html` and
`OVERFLOW_EXECUTIVE_SUMMARY.md` matches this recompute.

## Irregularity found and corrected (F-71)

The stored `ranking.json` array listed Discount Plumbing Rooter Services
at position 9 and Fast Response Plumbing & Rooter at position 10, while
the generator sorts by weighted score and every published page places
Fast Response #9 and Discount #10, as the stored final verification note
also states. The published site was correct; only the stored array order
differed. This session reordered the stored array to the published score
order. No score, weight or published rank changed, and the generator
output is identical before and after. Recorded as flag F-71 with source
AUDIT-20261111-61. Counts move from 135 sources / 60 flags to
136 sources / 61 flags.

## Line-by-line repo review notes

- Canonical data counts: 29 provider identities (26 CSLB records, 25
  active, 1 suspended, 3 unresolved with blank licence fields), 42
  requirements (R-01..R-42), 3 owner-reported estimates with verified
  amounts blank, 15 compliance rows, 8 technical rows, 23 review
  observations with rating/count blank, 10 ranked candidates plus 1
  restoration partner and 18 held-back identities. All rows carry
  registered source links; the verifier reports 405 source-covered rows
  before this session's additions.
- `site-data/*.json` (except build/verification reports) are historical
  session outputs dated 2026-11-07 and are labelled as such in
  `site-data/README.md`. They are not the current register and were left
  untouched.
- `BATHTUB_EXECUTIVE_SUMMARY.md` and `EXECUTIVE_SUMMARY_bathtub.md` are
  redirect stubs to the canonical executive summary. `EXECUTIVE_SUMMARY.md`
  at the root describes the unrelated DOE GEMS project and was left
  untouched.
- Open pull requests #7, #35, #38, #39, #44, #49, #51, #53, #63, #64, #66
  and #72 remain open and unmerged. They were not merged, closed or
  treated as verified. F-39 already records this state.
- GitHub Pages status is `built` for `b491225` and the latest
  `Publish overflow dashboard` runs on `main` are successful. F-52
  (legacy builder serves the repository root) and F-34 (Pages status lag)
  remain open and non-blocking.
- No exact-job acceptance, availability, combined quote, photographs or
  assembly model has been supplied by any provider. F-01..F-05 and the
  other open flags remain published on the Flagged for Review page.

## Verification performed

- `python scripts/build_overflow_site.py` — 11 pages built.
- `python scripts/verify_overflow_site.py` — 28/28 PASS (re-run after
  the final edit; see verification report).
- `python -m unittest discover -s tests -p 'test_overflow*.py'` — 40 tests OK.
- `python audit/independent_audit.py` — 0 problems.
- `python scripts/wording_guard.py` — clean.
- `python scripts/stage_overflow_pages.py` — linked public files staged.
- `git diff --check` — clean.

## Sources

- CSLB licence detail #829071: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071
- CSLB licence detail #1089561: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1089561
- CSLB licence detail #1115649: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649
- CSLB licence detail #995163: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163
- CSLB licence detail #977638: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638
- CSLB licence detail #1024971: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971
- CSLB licence detail #1027286: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1027286
- SF.gov plumbing permit service: https://www.sf.gov/apply-plumbing-and-mechanical-permit
- BPC §7059: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059.

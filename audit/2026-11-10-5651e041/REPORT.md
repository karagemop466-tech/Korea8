# Repository review, review-evidence pass and publication-boundary finding — session `arena/5651e041-korea8`

Checked on 2026-11-10. Every line below states what was checked and what was found. Where a value could not be
confirmed from an official source it is left blank and listed as unverified. No provider was contacted, called,
emailed, quoted, booked or paid. No price was inferred, rounded or averaged. The three supplied amounts remain
owner-reported with the verified amount blank.

## 1. What this session changed, and what it deliberately did not

| Item | Result |
|---|---|
| Canonical data touched | `reviews.json` (+5 observation rows), `sources.json` (+5 review-platform records), `ranking.json` (a review-evidence field per ranked candidate, and one second-bid block), `flags.json` (F-14 and F-15 restated, F-52 added), new `requests.json` |
| Generator touched | `scripts/build_overflow_site.py` — dashboard answer panel, copy-ready request block with a downloadable text file, request-routing table, review-evidence columns, second-bid table, review-status labels, CSS for the button and script block |
| Not touched | `docs/**` (archived DOE GEMS site), `tests/**`, any open pull request (#7, #35, #38, #39, #44, #49, #51, #53, #63, #64, #66), any other session's audit folder |
| Live servers started | none |
| Providers contacted | none |

## 2. Independent CSLB re-read of the ranked and quoted leads

Ten licence-detail records were retrieved directly from `cslb.ca.gov` on 2026-11-10 with the page-retrieval tool.
Both in-sandbox retrieval paths (`urllib`, `curl`) failed to that host with a TLS connection reset, which matches
what earlier sessions recorded. Each record was transcribed into `cslb-receipts.json` and compared field by field
with `overflow-integration/data/providers.json` by script.

| Licence | Legal name on the record | Status | Classifications | Phone | Fields compared |
|---|---|---|---|---|---|
| 829071 | ACE PLUMBING & ROOTER | current and active | C36, A, C-4, C16, B, C10 | (415) 824-6444 | match |
| 1089561 | TARO GROUP INC dba HEISES PLUMBING | current and active | C36, C10, A, C20 | (415) 333-0704 | match |
| 995163 | BERNAL HILL DRYWALL INC | current and active | C-9, B | (415) 533-8274 | match |
| 1115649 | RAPID FLOW PLUMBING & ROOTER INC | current and active | B, C36 | (415) 866-8401 | match |
| 392967 | AYOOB & PEERY PLUMBING CO INC | current and active | B, C-4, C16, C36, C20 | (415) 550-0975 | match |
| 1027286 | KENNETH ASIRE PLUMBING | **suspended — contractors bond suspension** | C36 | (415) 913-8048 | match |
| 977638 | EXPERT PLUMBING SOLUTIONS | current and active | C36 | (415) 531-5340 | match |
| 757796 | BAY AREA PLUMBING | current and active | C36 | (415) 668-8000 | match |
| 1024971 | JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER | current and active | C36 | (415) 596-6115 | match |
| 1096552 | WE DO CONSTRUCTION INC | current and active | B, C36 | (415) 416-5494 | match |

Result of the automated comparison: **10 records compared, 0 field mismatches** on legal name, phone, expiry,
classifications and status. The comparison normalises classification spelling (`C36` and `C-36`) and ignores
word order in a legal name; nothing else is normalised.

Notes found while reading, recorded rather than corrected:

- **Licence 1027286** shows the reason for suspension verbatim: *"License is under Contractors Bond Suspension…"*,
  with the bond **cancelled 08/16/2026**. The register already marks this identity suspended and already flags
  F-09. The cancellation date is the new detail.
- **Licence 1024971** carries a workers-compensation policy expiring **12/18/2026**, which is inside the likely
  work window. The register already records the expiry; F-10 covers the CSLB warning for a different licence, so
  this stays a scheduling fact, not a defect.
- **Licence 1115649 and 757796** are both **workers-comp exempt, certified no employees**. If either is hired,
  the crew on site belongs to someone else, which matters for an occupied building. Recorded in F-28 already.
- **Licence 1089561** carries the personnel note *"Personnel listed on this license (current or disassociated) are
  listed on other licenses."* This is CSLB boilerplate, not a finding, and is not raised as a flag.

## 3. Review evidence for this specific work

The owner asked for Yelp and other reviewed sources for this exact work. Yelp business pages returned **HTTP 403**
to the page-retrieval tool for both pages tried (`ace-plumbing-and-rooter-san-francisco`,
`heises-plumbing-san-francisco`) and to the search pages. That is the same result earlier sessions recorded. What
was obtainable is a dated search-index excerpt of those pages, which is what rows RV-19 to RV-23 use.

| Finding | Where it is published | Verification status |
|---|---|---|
| Bernal Hill Drywall: profile excerpt states a 2014 C-9 licence and a 2022 Class B addition; review highlights describe wall and ceiling holes from a leaky pipe | providers page, RV-19; ranking page second-bid table | excerpt only; C-9 and B confirmed independently on CSLB |
| Ceiling-repair listing excerpt names Amador's Drywall, R & R Drywall, Toms Painters, Peña Drywall | ranking page second-bid table | search lead; **not** licence-checked and published with no licence, phone or rating |
| Ayoob & Peery: indexed review says a $14,000 dig-out quote was avoided after a camera inspection | providers page, RV-21 | excerpt only; not this scope |
| Fast Response appears in a ceiling-leak-repair listing | providers page, RV-22 | excerpt only; no B or C-9 on CSLB |
| Rapid Flow: indexed account of retrieving a tub drain plug that fell into the drain | providers page, RV-01 | excerpt only; adjacent case, already F-15 |

**Two numbers were seen directly in search output and are published only as labelled snapshots:** Ace Plumbing &
Rooter showed 4.7 from about 1.4 thousand reviews, and Heise's Plumbing showed 4.2 from 278 to 283 reviews across
excerpts dated June and July 2026. Both are stated in flag F-14 with the date and the retrieval method; neither is
placed in a table cell, and neither is treated as a verified rating.

**What could not be confirmed and is therefore blank:** every star rating and review count in every table row; the
date of every excerpt except where the excerpt carried one; and whether any provider has ever performed this exact
trip-lever repair in an occupied unit.

## 4. Publication boundary — this corrects a prior reading

`GET /repos/karagemop466-tech/Korea8/pages` returns `build_type: "legacy"`, source branch `main`, path `/`, and the
latest legacy build for commit `67b9e98` reported `built` at 2026-11-10T01:17:38Z.

On 2026-11-10 this session retrieved `https://karagemop466-tech.github.io/Korea8/COORDINATION.md` over the public
internet and received the **full shared task board**, and retrieved `https://karagemop466-tech.github.io/Korea8/pyproject.toml`
and received the file. That means the live site currently serves the **repository root**, not only the linked public
closure the Actions workflow stages.

This corrects the statement recorded under flag F-34 that `COORDINATION.md` and `pyproject.toml` "both return GitHub
Pages 404". They return 200 and the file content. New flag **F-52** records the finding.

Consequence for this project: anything committed to the repository should be assumed publicly readable. Tracked
copy is limited to neutral repair-scope statements, which `scripts/wording_guard.py` checks on every tracked file;
the durable fix is a repository setting.

**Owner action, in the repository UI, which this session cannot perform:** Settings → Pages → Build and deployment →
Source → **GitHub Actions**. Attempting `PUT /repos/.../pages` with `build_type=workflow` returns **HTTP 403
"Resource not accessible by integration"** with the available token.

## 5. Data-integrity checks run on this session's own changes

| Check | Command | Result |
|---|---|---|
| Build | `python scripts/build_overflow_site.py` | 11 pages built |
| Verifier | `python scripts/verify_overflow_site.py` | 27/27 PASS |
| Unit tests | `python -m unittest discover -s tests -p 'test_overflow*.py'` | 27 tests OK |
| Wording guard | `python scripts/wording_guard.py` | clean |
| Staging closure | `python scripts/stage_overflow_pages.py` | linked public files staged, no repository internals |
| Source-id resolution | script over `requests.json`, `reviews.json`, `ranking.json` | every id resolves in `sources.json` |
| CSLB field parity | `cslb-receipts.json` vs `providers.json` | 10 records, 0 mismatches |
| `git diff --check` | — | clean |

## 6. Irregularities raised, and what changed as a result

| Flag | Change | Why |
|---|---|---|
| **F-14** | restated | It said Yelp "blocked" all review evidence. Found: two pages returned 403 to the tool, and search-index excerpts of those same pages do exist and are usable when labelled. The two directly observed figures are now stated with their date and labelled as snapshots. |
| **F-15** | restated | Added what the excerpts actually say and noted that the register's Rapid Flow review link is a general-contractor listing in the Excelsior, while the three-review excerpt sits inside a natural-gas-supplier listing. Both are listings, not a verified profile. |
| **F-52** | new (High) | The legacy Pages builder serves the repository root, which publishes this board. Corrects F-34's 404 statement. Owner action recorded. |

No provider was removed or added to the hiring order, no score was changed, and no price was introduced.

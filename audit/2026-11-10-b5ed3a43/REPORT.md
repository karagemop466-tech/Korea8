# Independent audit — 2026-11-10 (session `arena/b5ed3a43-korea8`)

**Scope.** Independent live-route verification, official-source re-verification of the estimates / cost /
technical slice, and a requirements-traceability matrix for the bathtub wastewater overflow trip-lever
dashboard. Read-only against every other session's claimed files; no canonical data, generator, verifier,
test or generated page was modified.

**Channels used.** Direct `curl` outbound in this sandbox is restricted to `api.github.com`. Live pages and
third-party official sources were retrieved with the `fetch_page` tool; GitHub deployment receipts were read
from `api.github.com`. Every route and every source below was fetched by this session on 2026-11-10.

**Coordination.** Sessions `arena/d6196195-korea8` (D619-T1/T2/T3, PR #56), `arena/47d993da-korea8` (PR #58/#61),
`arena/35739f62-korea8` (PR #57/#60) and `arena/660ab2dd-korea8` (PR #55/#59) own the canonical tree, generator,
verifier, tests, generated root pages and their own audit directories. This session's file scope is
`audit/2026-11-10-b5ed3a43/**` and `COORDINATION.md` only.

---

## 1. What was verified against official sources (pass)

| # | Claim carried on the site | Official source retrieved | Result |
|---|---|---|---|
| V-1 | Category 1P permit fee **$290** | [SF DBI Table 1A-C, July 2026](https://media.api.sf.gov/documents/Table_1A-C_-_Plumbing_Mechanical_2026.pdf) | **Match** — "CATEGORY 1P … $290" |
| V-2 | Category 11P/M miscellaneous fee **$320** | same | **Match** — "CATEGORY 11P/M Miscellaneous $320" |
| V-3 | Regular inspection **$519 / hour** | same | **Match** — "$519 per hour for regular inspections" |
| V-4 | Off-hour inspection **$555 / hour** | same | **Match** — "$555 per hour for off-hour inspections" |
| V-5 | Re-inspection **$259 / half hour** | same | **Match** — "shall be $259 per half hour" |
| V-6 | Fee schedule dated **July 2026**, applies to permits issued on/after **2026-07-12** | same | **Match** |
| V-7 | Permit required before cutting into or replacing pipes, especially pipes that will be covered by a wall | [SF.gov — Apply for a plumbing and mechanical permit](https://www.sf.gov/apply-plumbing-and-mechanical-permit) | **Match** — "You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground." |
| V-8 | §104.2 exempt-work link; work inspected before pipes are covered | same | **Match** — both statements appear on the page |
| V-9 | Permit Center help desk **628-652-4900** | same | **Match** |
| V-10 | Eligible licence classes **A, B, C4, C16, C20, C36, C54** | same | **Match** — page lists exactly these; B is "after approval based on the scope of work" |
| V-11 | Only owners of stand-alone single-family dwellings (R-3) may self-permit | same | **Match** — relevant because the unit is tenant-occupied |
| V-12 | BPC §7057(a)/(b): a general building contractor works two or more unrelated trades, and must hold the classification or subcontract it | [California Legislature — BPC §7057](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057.) | **Match, verbatim** — supports the site's all-in-one contract reasoning |
| V-13 | CSLB **C-9 Drywall Contractor** scope (gypsum wall board, nonstructural metal framing, taping/texturing) | [CSLB Licensing Classifications Detail — C-9](https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9) | **Match** |
| V-14 | Ace Plumbing & Rooter — licence **829071**, 1090 Bryant St SF, C36 + A + C-4 + C16 + B + C10, current and active, expire 06/30/2027, phone (415) 824-6444, bond and workers comp current | [CSLB licence detail 829071](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071) | **Match on every field checked** |
| V-15 | Bernal Hill Drywall Inc — licence **995163**, 720 Anderson St SF, **C-9 + B**, current and active, expire 07/31/2028, phone (415) 533-8274, bond and workers comp current | [CSLB licence detail 995163](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163) | **Match on every field checked** |

**Canonical register counts re-counted from `overflow-integration/data/` at `origin/main` (`8e7dbd6`):**
providers 25 rows · sources 87 rows · flags 46 rows · requirements 42 rows · ranking 10 ranked + 1 partner +
14 not recommended. Ranking weights C1 0.30 · C2 0.20 · C3 0.20 · C4 0.15 · C5 0.15 = 1.00. These match the
counts printed on the live dashboard.

**Not re-verified by this session** (claimed by other sessions, not re-read here): the remaining 22 CSLB
licence detail pages, the Watco instruction PDF, the Heise's case pages, the AmLegal §104.2 chunk, the
civil-code text of §1954, and every review-platform entry. No claim in this report rests on them.

---

## 2. Live-route inventory (fetched 2026-11-10)

| Route | Live result | Assessment |
|---|---|---|
| `/` | Canonical dashboard, current (24 CSLB, 87 sources, 46 flags, ranked Ace → Heise's → Rapid Flow) | **OK** |
| `/bathroom-overflow/index.html` | Retired stub, forwards to canonical dashboard | **OK** |
| `/bathtub-overflow/index.html` | Retired stub, forwards to canonical dashboard | **OK** |
| `/project/EXECUTIVE_SUMMARY.md` | **Served** — superseded brief, see I-1 | **Irregularity** |
| `/project/flagged.json` | **Served** — superseded flag register, see I-1 | **Irregularity** |
| `/bathtub/index.html` | GitHub Pages 404 | **Irregularity** (I-3) |
| `/trip-lever/index.html` | GitHub Pages 404 | **Irregularity** (I-3) |
| `/README.md` | GitHub Pages 404 | **Irregularity** (I-2) |
| `/HYPOTHESES.md` | GitHub Pages 404 | **Irregularity** (I-2) |
| `/requirements.txt` | GitHub Pages 404 | **Irregularity** (I-2) |

Machine-readable copy: [`live-route-check.json`](live-route-check.json).

---

## 3. Irregularities flagged for review

### I-1 — Superseded, self-contradicting content is publicly served (high)

`/project/EXECUTIVE_SUMMARY.md` is reachable on the live site. It is the retired `project/` tree's brief,
compiled 2026-11-07, and it disagrees with the canonical dashboard on numbers a reader would act on:

| Item | Superseded copy served live | Canonical dashboard |
|---|---|---|
| CSLB licence numbers re-read | 19 | 24 |
| Providers / identities | 4 named firms in the recommendation | 25 identities |
| Recommended order | Bay Area Plumbing asked to contract under licence 749536, then Ayoob & Peery / Ace | Ace → Heise's → Rapid Flow → Ayoob & Peery → We Do |
| Flag count | older F-01… register | 46 flags |

It also asserts a code rule that the canonical register explicitly refuses to assert:

> Superseded copy, served live: *"UPC §402.10 requires a 12-inch access panel where a slip joint is
> concealed; soldered and two-piece joints do not trigger it."*

> Canonical requirement **R-08** (`overflow-integration/data/requirements.json`): requirement "Consider a
> code-compliant serviceable access panel rather than burying slip-joint connections again." — basis:
> **"Access-panel dimensions could not be verified from a free official code source; do not assert a fixed
> 12-inch rule."**

`/project/flagged.json` is likewise served, carrying the older flag register and the older provider
numbering (P-04…P-09). Nothing in the canonical link closure links to either file — no tracked HTML file
references `project/EXECUTIVE_SUMMARY.md` — so their presence on the live host is not explained by the
documented publication closure.

**Action (owner):** decide whether the retired `project/` tree should be reachable at all. If not, it must
be removed from the published set, not merely from the navigation.

### I-2 — The published set is neither the repository root nor the documented closure (high)

The Pages API reports `build_type: legacy`, source branch `main`, path `/`:

```
GET https://api.github.com/repos/karagemop466-tech/Korea8/pages
→ {"status":"errored","html_url":"https://karagemop466-tech.github.io/Korea8/",
   "build_type":"legacy","source":{"branch":"main","path":"/"}}
```

Session `660ab2dd` recorded that a `PUT` to switch this to `workflow` returned HTTP 403
`Resource not accessible by integration`, so the switch did not take effect. The workflow
(`.github/workflows/overflow-pages.yml`) does stage `build/pages` — a 23-file linked public closure — and
deploy it, and those runs succeed.

Measured against both candidates, the live set matches neither:

- not the repository root: tracked root files `README.md`, `HYPOTHESES.md` and `requirements.txt` all
  return GitHub Pages 404;
- not the 23-file closure: `project/EXECUTIVE_SUMMARY.md` and `project/flagged.json` are served although
  no tracked file links to them.

Retired redirect stubs are split as well: `bathroom-overflow/` and `bathtub-overflow/` forward correctly,
while `bathtub/` and `trip-lever/` return 404.

**Action (owner):** the publication boundary is a stated goal (PR #55) that is not currently in force. The
effective published file set is undocumented and should be enumerated once the Pages source is settled.

### I-3 — Consecutive legacy Page build failures while the workflow succeeds (medium)

`GET /repos/{owner}/{repo}/pages/builds`:

| Build (created_at UTC) | Commit | Status |
|---|---|---|
| 00:55:17 | `7c71101` | built |
| 00:53:15 | `b30f89d` | **errored — "Page build failed."** |
| 00:52:49 | `a510682` | **errored — "Page build failed."** |
| 00:52:13 | `a5721de` | built |
| 00:51:52 | `4982df6` | built |
| 00:51:30 | `caab44e` | **errored — "Page build failed."** |

Three of the last six legacy builds failed, while the `Publish overflow dashboard` workflow and the
`pages build and deployment` workflow both completed `success` for the same commits. Two competing
deployment paths are therefore in play, and the legacy path is the one that is failing.

**Action (owner):** resolve which path owns the site, then delete or fix the other.

### I-4 — Flag F-08 wording is broader than the official text (medium)

Published flag F-08: *"A B-2 licence is not eligible for a plumbing permit"*, with the basis that DBI's
list of eligible licence types is A, B, C-4, C-16, C-20 and C-54 and "B-2 is not on it".

The official page lists licence **types**, and for B it says: *"B license, after approval based on the
scope of work (plumbing work related to a kitchen or bath permit on PermitSF can be approved immediately
for B contractors)"*. B-2 Residential Remodeling is a classification within B, not a separate type. The
restriction is scope- and approval-based, not a categorical bar, so the current wording can mislead a
reader into excluding a B-2 holder outright.

**Action (owner):** reword F-08 to the scope-based reading, or confirm the DBI position directly.

### I-5 — The canonical estimates page carries no cost-driver table (low)

`overflow-integration/data/estimates.json` has keys `as_of`, `quote_date`, `rows`, `official_fees`,
`analysis` — no cost-driver block. `estimates.html` renders exactly two sections: "Official DBI fees (not
project quotes)" and "Analysis". The six cost drivers recorded by session `0ad9ad61` live only in the
retired tree at `bathtub-overflow/data/costs.json`. Cost reasoning is still present on the canonical site
via the "Cost picture" section of `decision-analysis.html`, so this is a coverage note, not a missing
deliverable.

### I-6 — The dashboard publishes an unrelated project's evidence site (low)

`docs/index.html` — the archived DOE GEMS Prize Challenge evidence site — sits inside the canonical 23-file
linked public closure, so it is published as part of this dashboard's link closure. The repo/topic mismatch
itself is already recorded as FL-01; what is new here is that the unrelated site is reachable from the
canonical closure rather than only from a retired route.

### I-7 — Open PRs from other sessions remain untouched (informational)

PRs #35, #38, #39, #44, #49, #51 and #53 were open at the time of this audit. This session did not merge,
close or rebase any of them, and did not treat any of them as authorised for takeover.

---

## 4. Requirements traceability matrix

Every line of the original brief mapped to the artefact that satisfies it. Machine-readable copy:
[`traceability.json`](traceability.json).

| # | Requirement in the brief | Artefact | Status |
|---|---|---|---|
| 1 | Executive summary outlining important details | `executive-summary.html`, `OVERFLOW_EXECUTIVE_SUMMARY.md`, `overflow-integration/EXECUTIVE_SUMMARY.md` | Satisfied |
| 2 | Record the problem: trip lever stuck in concealed plumbing, hard to reach, may need the ceiling opened | `technical-approach.html` (T-01…T-06), `overflow-integration/OWNER_RECORD.md` | Satisfied, neutral wording |
| 3 | Record the three supplied estimates ($614, $550, $135) | `estimates.html` rows E-01…E-03 | Satisfied; `amount_verified` blank, owner-reported label |
| 4 | Find providers who can do the work, using Yelp and other reviewed services in San Francisco | `providers.html` (25 identities), `sources.json` review-platform entries | Partially satisfied — review platforms return HTTP 403, so ratings and counts are blank rather than sourced |
| 5 | Prefer removal from above; record that 5+ licensed plumbers could not | `technical-approach.html`, flag F-03 | Satisfied |
| 6 | One accountable contractor for plumbing **and** drywall | `decision-analysis.html` restoration partner (Bernal Hill, C-9 + B), BPC §7057 reasoning | Satisfied on paper; no provider confirms a combined scope |
| 7 | Rank contractors best-choice-to-hire with reasoning, costs, official verified links and phone | `decision-analysis.html` — 10 ranked, published weights, cost picture, CSLB link and phone per row | Satisfied |
| 8 | Licensed plumber or contractor | 24 CSLB records re-read; 1 suspended excluded; 1 unresolved | Satisfied |
| 9 | Work in a tenant-occupied unit | requirements rows citing Civil Code §1954; occupied-unit criterion C4 | Satisfied |
| 10 | GitHub Pages live site, clean landing page plus category subpages, dashboard-like | 11 canonical root pages, single stylesheet, no CDN or client framework | Satisfied and live |
| 11 | Every table row carries a source link to an official site | `scripts/verify_overflow_site.py` — 27/27 checks, 300 source-covered rows | Verified by prior sessions; **not re-run by this session** |
| 12 | Leave blank and flag anything that cannot be confirmed; never infer | 46 published flags; every `amount_verified`, rating and review count null | Satisfied in the canonical data |
| 13 | Flagged for Review page | `flagged-for-review.html` | Satisfied and live |
| 14 | Repo review with irregularities flagged | this report, plus `audit/REPORT_2026-11-08_*.md`, `audit/2026-11-10-*` | Satisfied |
| 15 | No manual input; work autonomously | all work performed by the session | Satisfied |
| 16 | Coordinate parallel sessions through `COORDINATION.md` | claim and record appended 2026-11-10 | Satisfied |

**Gaps found by this audit:** I-1 (superseded contradictory copy served), I-2 (publication boundary not in
force), I-3 (legacy build failures), I-4 (F-08 wording), I-5 (no canonical cost-driver table), I-6
(unrelated project in the canonical closure), I-3-routes (`bathtub/`, `trip-lever/` return 404).

---

## 5. Standing constraints honoured

- No provider was contacted, booked or paid.
- No private-circumstance material is recorded, published or referred to anywhere in this report.
- Owner-supplied estimates remain labelled owner-reported with verified amounts blank.
- No canonical data, generator, verifier, test or generated page was modified; defects found there are
  logged here as cross-session requests rather than edited.
- Nothing in this report is presented as a verified provider price, availability or acceptance.

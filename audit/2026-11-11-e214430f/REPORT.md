# Independent verification and publication receipt — session arena/e214430f-korea8

**Date:** 11 November 2026 UTC · **Branch:** `arena/e214430f-korea8` (rebased onto `origin/main` commit `258d08f`, the merge of PR #83 from `arena/17e21276-korea8`) · **Working tree:** clean · **No other branch or worktree created or pushed.**

## Scope and limits

This is a session-scoped independent verification of the current canonical bathtub-overflow trip-lever dashboard, not a fresh retrieval of live external CSLB/City pages (this sandbox's outbound network is limited to package registries, so external-source freshness cannot be renewed here). External facts carry their prior retrieval dates (CSLB records read 2026-11-10; DBI July 2026 fee schedule; sf.gov service pages; California legislative codes). No provider was contacted, booked, or paid; no quote was solicited. Public artifacts use neutral repair-scope language only and do not disclose the owner's private permitting context. Prior open PRs (#7, #35, #38, #39, #44, #49, #51, #53, #54, #63, #64, #66, #72 and any others) were left untouched. Unrelated DOE GEMS files remain read-only.

## Method

1. `git fetch origin` and `git rebase origin/main` so this session adds work only on top of the current integrated tree (no overlap with earlier sessions' claims).
2. `python3 scripts/build_overflow_site.py` — regenerates the canonical dashboard from `overflow-integration/data/`.
3. `python3 scripts/verify_overflow_site.py` — 28 mechanical checks, fail-closed.
4. `python -m unittest discover -s tests -p 'test_overflow*.py'` — unit tests.
5. `python3 scripts/wording_guard.py` — neutral-language scan over every tracked text file.
6. `python3 audit/independent_audit.py` — row-source and internal-link audit over tracked HTML.
7. `python3 scripts/stage_overflow_pages.py` — public Pages boundary staging (48 linked files; no repository internals).
8. `git diff --check` — clean.

## Results

| Check | Result |
|---|---|
| `build_overflow_site.py` | PASS — build report written (29 providers, 26 CSLB records, 25 active, 1 suspended, 3 identity-unresolved, 6 B + C-36, 1 C-9, 42 requirements, 3 estimates, 8 technical, 15 compliance, 23 review observations, 6 cost drivers, 135 sources, 61 flags, 10 ranked leads, 1 held-back restoration partner, 18 not-recommended identities) |
| `verify_overflow_site.py` | 28/28 PASS — 406 source-covered rows, 68 tracked HTML files, 281 internal links, 0 offenders; verified amounts blank; review ratings/counts blank; owner amounts owner-reported; suspended provider excluded from priority leads |
| `tests/test_overflow*.py` | 40/40 OK |
| `wording_guard.py` | clean — exit 0 |
| `audit/independent_audit.py` | PASS — pages=11, rows=406, with_source=406, internal_links=221, problems=0 |
| `stage_overflow_pages.py` | PASS — 48 linked public files staged; no `.git`, `.github`, `src`, `vendor`, `scripts`, `tests`, `data` internals; `PROJECT_PROMPT.md` and `COORDINATION.md` not staged |
| `git diff --check` | clean |

## What the live site contains (https://karagemop466-tech.github.io/Korea8/)

- Landing dashboard: KPIs (CSLB records rechecked, B + C-36 inquiry leads, C-9 restoration partner, requirements captured) and entry points to every category page.
- `executive-summary.html` / `overflow-integration/EXECUTIVE_SUMMARY.md` — decision (two-path scope: tub-side attempt first, below-ceiling storage-unit fallback under a written combined contract), ranked hiring order, estimates, key controls, open items.
- `decision-analysis.html` — ranked decision analysis: 10 providers scored on five weighted criteria (C1 combined plumbing + restoration capability 0.30, C2 scope evidence 0.20, C3 licence standing 0.20, C4 occupied-unit experience 0.15, C5 price evidence 0.15), each row with reasoning, cost basis, phone number, official CSLB link and source ids; held-back restoration partner (Bernal Hill Drywall, C-9 + B) and 18 not-recommended identities with reasons.
- `requirements.html` — 42 source-linked requirements in 7 categories (Problem & outcome, Access, Licensing & contracting, Permits & code compliance, Occupied-unit & tenant, Budget & schedule, Vendor selection & quality), each with acceptance check and status; these are the questions/information items that must be addressed before a hiring decision.
- `providers.html` — 29 identities: phone numbers from the official CSLB record, official CSLB link per row, licence status/classifications/city/expiry, review-platform leads labelled as blocked snapshots (Yelp/others return HTTP 403; no numeric ratings invented).
- `estimates.html` — the three owner-supplied estimates dated 2026-08-30 ($135 / $550 / $614, owner-reported, verified amounts blank), six sourced cost drivers, official DBI Category 1P $290 and related fee rates (permit fee is not a job price).
- `technical-approach.html` — tub-side service path, below-ceiling fallback, model-specific limits.
- `code-and-permit.html` / `compliance.json` — permit trigger, conditional SF Plumbing Code §104.2 exemptions, eligible licence classes, inspection-before-covering, BPC §7057/§7059(a), 16 CCR §831, Civil Code §1954 tenant entry, DBI fees, fire-resistive assembly caveat (SFBC §106A.2(10)).
- `sources.html` — 135 source records with publisher, date, retrieval status and limitations.
- `flagged-for-review.html` — 61 flags (F-01…F-55, F-65…F-70), each with severity, category, action to resolve, and source links; non-blocking but published so they can be reviewed after the site is live.
- `verification.html` — audit checks, build report and links to the current and prior audit reports.

## Irregularities and unverified items (non-blocking; published on the Flagged for Review page)

- **F-52** (open): GitHub Pages is configured `build_type: legacy`, source `main` at `/`; the repository is public and not private. An attempt to switch Pages to the workflow source returned HTTP 403 (`Resource not accessible by integration`); no configuration change was made. Do not place confidential details in the repository or site.
- **F-34** (open): legacy Pages root publication and public exposure; see flag text for the boundary limitation.
- **F-70** (open, added by concurrent session `arena/17e21276-korea8`): the retrieved Heise project page shows project narrative together with a 404 message in its body; cause unconfirmed; treat the company's case as self-reported and reconfirm directly.
- No provider has confirmed this exact stuck-trip-lever job, storage-unit ceiling restoration, availability or price. All three owner-supplied amounts are owner-reported; verified amounts remain blank. Yelp and other review-platform business pages return HTTP 403, so ratings and review counts are blank and never presented as verified.
- Portola Plumbing Services, C J's Plumbing & Rooter Service and Golden Gate Plumbing & Rooter Inc remain identity-unresolved: every regulated field is blank, with the official CSLB lookup linked.
- Kenneth Asire Plumbing (#1027286) is suspended on CSLB (contractor bond suspension, bond cancelled 08/16/2026) and is excluded from hiring.
- B + C-36 on a licence does not by itself establish drywall self-performance; the restoration party and contract structure must be confirmed in writing (BPC §7059(a), 16 CCR §831).

## Sources used (official-primary where available)

- CSLB licence-detail lookup: https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx (per-licence rows linked from every provider row)
- CSLB classifications: C-36, C-9, B — cslb.ca.gov Licensing Classifications pages; 16 CCR §831 rulemaking notice (CSLB-831)
- California statutes: BPC §§7048, 7057, 7057.5, 7059, 7114, 7124.6; Civil Code §1954 — leginfo.legislature.ca.gov
- City and county of San Francisco: sf.gov plumbing/mechanical permit service; media.api.sf.gov DBI Table 1A-C Plumbing/Mechanical fees (July 2026); AmLegal San Francisco Plumbing Code §104.2 and Building Code §106A.2 (chunks 14 and 39)
- Watco 500/501/600TL bath-waste instructions PDF
- EPA RRP / asbestos guidance (conditional pre-disturbance screening)

## Publication status

The canonical dashboard is already served by GitHub Pages from `main` at path `/`: https://karagemop466-tech.github.io/Korea8/ . The latest legacy Pages build is `built` with no error. This session's verification confirms the site builds with no broken links and all automated checks green; it does not itself issue a fresh live HTTPS fetch (that assertion is performed by the workflow on GitHub runners).

## Handoff

This session has no remaining claimed tasks once its PR/merge receipt is recorded in COORDINATION.md. Open flags remain non-blocking and are the owner's review list after the site is live. No provider will be contacted, booked or paid as part of this repository work.

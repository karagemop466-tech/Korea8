# COORDINATION.md — shared task board

Repo: `karagemop466-tech/Korea8` · Pages: https://karagemop466-tech.github.io/Korea8/ (source: `main`, path `/`)

Rules (from the project brief): read this file before starting; claim a task by writing your
session ID + file scope, then commit and push the claim immediately; never start a task another
session has claimed; keep scopes non-overlapping; log cross-scope requests here instead of editing
another session's files; small frequent commits; `git pull --rebase` before every push; record
sources, verification performed and irregularities when finishing a task.

Status values: `unclaimed` · `in progress` · `done` · `needs review`
A `needs review` item is published on the site's **Flagged for Review** page and blocks nothing.

---

## Task board

| ID | Task | Status | Session | File scope | Notes |
|---|---|---|---|---|---|
| T1 | Repo review + irregularity log | done | `arena-5404ab5c` | `REPO_REVIEW.md` | 14 findings logged |
| T2 | Bathtub trip-lever project: requirement list + verification | done | `arena-5404ab5c` | `data/tub/requirements.json` | 24 requirements |
| T3 | Contractor licence verification (CSLB) | done | `arena-5404ab5c` | `data/tub/vendors.json` | 12 licences checked against CSLB 2026-11-06 |
| T4 | Quotes / estimates comparison | done | `arena-5404ab5c` | `data/tub/estimates.json` | 3 user-provided quotes, all unverified |
| T5 | Permit / licensing / tenant-access rule set | done | `data/tub/rules.json` |  | 10 official sources |
| T6 | Access-method (from above vs. from below) analysis | done | `arena-5404ab5c` | `data/tub/scope.json` | evidence-graded |
| T7 | Site build (dashboard + subpages) | done | `arena-5404ab5c` | `tub/**`, `scripts/build_tub_site.py`, root `index.html` | 9 pages |
| T8 | Link + row-source verification gate | done | `arena-5404ab5c` | `scripts/verify_tub_site.py` | 0 broken links, every row has a source cell |
| T9 | Integration: merge, PR, deploy check | done | `arena-5404ab5c` | `COORDINATION.md` | see log |

---

## Session log

### Session `arena-5404ab5c` — 2026-11-06

**Claim.** T1–T9 are claimed by `arena-5404ab5c` on branch `arena/5404ab5c-korea8`.
Scope: `REPO_REVIEW.md`, `COORDINATION.md`, `data/tub/**`, `tub/**`,
`scripts/build_tub_site.py`, `scripts/verify_tub_site.py`, root `index.html`, and the
relocation of the pre-existing GEMS evidence site into `gems/` (moved, not edited).
No other agent session was active in the repo at claim time (`git log` showed only the
merged PR #6 from `arena/d7026453-korea8`, whose claim is closed).

**Important scope note.** The repository's existing content is a DOE GEMS Prize fault-prediction
research project, which has nothing to do with this session's task (bathtub overflow trip lever,
San Francisco). This mismatch is **fraud-flagged as irregularity I-01** in `REPO_REVIEW.md`.
To avoid destroying prior work, the GEMS site was **moved** (not rewritten) to `gems/` and the
new project owns the root landing page. Revert = `git mv gems/* .`.

**Sources used (all fetched live on 2026-11-06 UTC unless noted).**

Official / government
- CSLB licence detail pages, `LicNum` = 1024971, 977638, 973345, 757796, 1089561, 829071,
  961218, 1009195, 954813, 1140843, 1050835 — https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=…
  (CSLB states "Data current as of 11/6/2026".)
- CSLB licence classifications index and detail (B, C-36, C-9) — cslb.ca.gov
- CSLB "What Jobs B General Building Can/Cannot Perform" Fast Facts PDF
- SF.gov "Apply for a plumbing and mechanical permit"
- San Francisco Plumbing Code 2025 amendments (official PDF, media.api.sf.gov) — §104.2
- SF Planning/DBI permit-service pages (for cross-reference only)
- Cal. Bus. & Prof. Code §§ 7048, 7057 (via CSLB), 7110, 7151, 7159, 7159.5, 7159.10 (leginfo.ca.gov)
- Cal. Civ. Code §§ 1941.1, 1954 (leginfo.ca.gov)
- EPA lead RRP small-entity guide + 40 CFR 745.83 minor-repair thresholds (epa.gov)

Not usable as verification (flagged)
- Yelp business pages returned **HTTP 403** to automated retrieval. No Yelp rating or review
  count is presented as a verified value anywhere on the site.

**Verification performed.**
- 12 CSLB records read directly; every licence number, classification, status and expiry date
  in `data/tub/vendors.json` is copied from the CSLB detail page fetched today.
- 1 cancelled licence found (`973345`, "ADVANCE PLUMBING", cancelled 05/14/2018) and recorded
  as historical only — it is **not** counted as an active credential.
- `scripts/verify_tub_site.py` re-checks: every generated page exists, every internal link and
  anchor resolves, every table row carries a source cell, no `http://` source URLs, and no
  unverified value appears outside the Flagged page or an explicitly-labelled unverified column.
- Result: **0 broken links, 0 missing source cells** (see `tub/verification.json`).

**Irregularities logged** (full text on `tub/flagged.html` and in `REPO_REVIEW.md`):
CSLB address typo on #1024971 ("236 W POTRAL AVE"); website-vs-CSLB address mismatch for
Heise's Plumbing; `973345` cancelled; #1009195 carries a future-suspension advisory; the
"$500 licensing threshold" figure repeated across many third-party sites is stale
(BPC 7048 now says $1,000, effective 2026-01-01); the three cost estimates are user-provided,
undated apart from "8/30/26", and have no written document in the repo; no photos were supplied.

**Integration.** PR opened from `arena/5404ab5c-korea8` → `main`, merged, Pages deploy verified.
See the "Merge record" section at the bottom of this file.

---

## Merge record

(filled in after the PR is merged — see bottom of file)

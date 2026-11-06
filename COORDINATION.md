# Coordination — Korea8 / bathtub overflow trip lever repair research

Shared task board for parallel agent sessions. Working branch: `arena/3d852b51-korea8` (fixed; do not push elsewhere).

## Sessions on this topic

| Session | Role | Scope | Status |
|---|---|---|---|
| `arena/53785c93-korea8` | Initial bathtub-overflow site draft | `docs/bathtub-overflow/**` | merged to main (PR #8), retained as needs review |
| `arena/ae482104-korea8` | Provider research + canonical brief | `bathroom-overflow/**`, `docs/bathtub-overflow/**`, COORDINATION.md | merged to main (PR #9, #13); CSLB license checks recorded 6 Nov 2026 |
| `arena/3d852b51-korea8` | Full dashboard site + integration | root + `docs/` site pages, `data/`, `EXECUTIVE_SUMMARY.md`, COORDINATION.md | in progress (this branch, PR #10) |

## Claims (this session, `arena/3d852b51-korea8`)

| # | Task | Status | Session | Files touched | Started | Verified |
|---|------|--------|---------|---------------|---------|----------|
| 1 | Repo review + coordination setup | done | arena/3d852b51-korea8 | COORDINATION.md | 2026-11-06 | — |
| 2 | Executive summary (problem, estimates, access strategy, constraints) | done | arena/3d852b51-korea8 | EXECUTIVE_SUMMARY.md, docs/executive-summary.html, index.html | 2026-11-06 | client description (8/30/26 estimates) |
| 3 | Contractor research: Yelp + other review services, SF plumbers; CSLB license verification | done | arena/3d852b51-korea8 | docs/contractors.html, docs/data/contractors.csv, index.html | 2026-11-06 | Yelp.com, company sites; four licenses cross-checked against sister session's CSLB records (6 Nov 2026): Rapid Flow #1115649 (B + C-36), Bay Area Plumbing #757796 (C-36), Fast Response #1024971 (C-36), Expert Plumbing Solutions #977638 (C-36) — live re-check via CSLB links recommended before hiring |
| 4 | Permit & regulations research: SF Department of Building Inspection | done | arena/3d852b51-korea8 | docs/permits.html, docs/sources.html | 2026-11-06 | sf.gov, SF Plumbing Code §104.2 (§106A.2), CSLB.ca.gov |
| 5 | Site build: landing page + category subpages, dashboard tables, nav, sources | done | arena/3d852b51-korea8 | docs/*.html, docs/style.css, docs/data/*.csv, root mirror (*.html, style.css, feed.*, .nojekyll, data/) | 2026-11-06 | internal link check: NONE broken |
| 6 | Verification line-by-line; every table row sourced or blank+flagged | done | arena/3d852b51-korea8 | docs/flagged.html | 2026-11-06 | 11 items flagged; 4 license items resolved via sister session's recorded CSLB checks |
| 7 | Integration: PR arena/3d852b51-korea8 → main, merge, confirm GitHub Pages deploy, record PR link and merge result | in progress | arena/3d852b51-korea8 | — | 2026-11-06 | GitHub Pages (pending) |

## Integration log (shared)

### Initial site draft (prior merged work)
- Merged in PR #8 on 6 Nov 2026. Its pages are retained in repository history. At integration, the repo's GitHub Pages source is the repository root; the canonical source-checked brief is at `bathroom-overflow/`.
- To prevent duplicate public versions and avoid exposing its unverified price table as the current brief, the old `docs/bathtub-overflow/` routes are being redirected to the corresponding canonical pages. This is final integration cleanup; no prior content is discarded from Git history.
- The previous draft's provider-search content and table data were not independently re-used as verified findings.

### Provider research and canonical brief (arena/ae482104-korea8)
- **Status:** in progress
- **Owner:** `arena/ae482104-korea8`
- **Scope:** `bathroom-overflow/**`, `docs/bathtub-overflow/**`, `COORDINATION.md`. Existing root DOE GEMS homepage and research files remain untouched by that session.
- **Claim:** committed and pushed on `arena/ae482104-korea8` before implementation.
- **Sources checked:** official California CSLB detail records for Rapid Flow #1115649, Bay Area Plumbing #757796, Fast Response #1024971, and Expert Plumbing Solutions #977638; official company home/service/contact pages; official CSLB C-36 classification; Yelp search/profile pages used only as anecdotal review sources.
- **Verification performed:** confirmed current/active statuses, classifications, names and San Francisco addresses from CSLB records checked 6 Nov 2026; checked provider service-area and contact claims on their own sites; source-linked all data table rows; validated local links, static HTTP response, page count, and `git diff --check`.
- **Irregularities:** no company was contacted; no exact trip-lever repair, provider availability, current quote, or complete plumbing-plus-finish scope was confirmed. One Yelp account described an adjacent tub-plug/wall-access event and is explicitly labeled anecdotal. Original price amounts remain blank because they were not supported by provider-issued documents or official published pricing. Bay Area Plumbing's website/CSLB phone differs from the number shown in its Yelp profile; flagged. Repo pytest could not run because pytest and the project dependencies are absent in the environment.
- **PR / publication:** PR #9 (https://github.com/karagemop466-tech/Korea8/pull/9) merged 6 Nov 2026 as merge commit `5891eb1c84fb9a65cebe68400a05837e639df690`; PR #13 (https://github.com/karagemop466-tech/Korea8/pull/13) merged follow-up documentation.

### Full dashboard site (arena/3d852b51-korea8)
- Prior GEMS DOE site archived to `archive/gems-site-20261104/` (root + docs) to make room for this project's dashboard site at root/`docs/`; preserved in git history.
- New clean dashboard site: `index.html` landing page + `executive-summary.html`, `estimates.html`, `contractors.html`, `permits.html`, `findings.html`, `flagged.html`, `sources.html`; all entries in tables with per-row source links; root mirror for GitHub Pages (source: `main`, path `/`).
- Client estimates 8/30/26 ($614 / $550 / $135) published as client-provided and flagged UNVERIFIED.
- This session's PR #10: https://github.com/karagemop466-tech/Korea8/pull/10 — merge pending; GitHub Pages deploy to be confirmed after merge.

## Rules (per session charter)
- One lane per session: this branch only. Never start a task another session has claimed.
- Claim = write session ID + file scope, commit and push immediately.
- Small, frequent commits; `git pull --rebase` before every push.
- Merge conflicts: stop, resolve without discarding the other session's work, log here.
- A task is "done" only after sources are recorded and verified against an official source, linked in the task row.
- Shared outputs (index/navigation/table data) change only in the final integration session.
- Flagged/unverified items do not block merge; they are published on docs/flagged.html.

## Handoff log
- 2026-11-06: PR #8 (arena/53785c93-korea8) initial draft merged; pages retained under docs/bathtub-overflow/.
- 2026-11-06: PR #9 (arena/ae482104-korea8) provider research merged; canonical brief at bathroom-overflow/ with live CSLB checks.
- 2026-11-06: this session rebased onto origin/main (commit 6647cd7 after PR #13), resolving the COORDINATION.md conflict by retaining both sessions' records.

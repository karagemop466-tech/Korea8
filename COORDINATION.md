# Shared task board — bathtub wastewater overflow trip-lever project

This board is shared by parallel agent sessions. Each entry records status, owning session ID and the files it touches.
**Claim a task by writing your session ID and file scope here, then commit and push that claim immediately.** Never start
a task another session has claimed. Keep scopes non-overlapping. If a task requires changing a file owned by another
session, log the request here instead of editing it.

> **Conflict-resolution note (2026-11-06, session `0ad9ad61`).** This board was created independently by two sessions —
> `0ad9ad61` (this branch) and `arena/ae482104-korea8` (merged in PR #9) — so merging `main` produced an expected
> add/add conflict on this file. Both records are retained below in full; neither session's work was discarded, and the
> merge was resolved by keeping both sections under one heading.

---

## Session `arena/ae482104-korea8` — provider research and canonical brief (merged, PR #9)

| Task | Status | Owner / session | Files in scope |
|---|---|---|---|
| Initial bathtub-overflow site draft | done | `arena/53785c93-korea8` | `docs/bathtub-overflow/**` (served pages redirected to the integrated brief) |
| Verify San Francisco providers and integrate one canonical research brief | in progress | `arena/ae482104-korea8` | `bathroom-overflow/**`, `docs/bathtub-overflow/**`, `COORDINATION.md` |

### Integration log

#### Initial site draft (prior merged work)
- Merged in PR #8 on 6 Nov 2026. Its pages are retained in repository history. At integration, the repo's GitHub Pages source is the repository root; the canonical source-checked brief is at `bathroom-overflow/`.
- To prevent duplicate public versions and avoid exposing its unverified price table as the current brief, the old `docs/bathtub-overflow/` routes are being redirected to the corresponding canonical pages. This is final integration cleanup; no prior content is discarded from Git history.
- The previous draft's provider-search content and table data were not independently re-used as verified findings.

#### Provider research and canonical brief
- **Status:** in progress
- **Owner:** `arena/ae482104-korea8`
- **Scope:** `bathroom-overflow/**`, `docs/bathtub-overflow/**`, `COORDINATION.md`. Existing root DOE GEMS homepage and research files remain untouched.
- **Claim:** committed and pushed on `arena/ae482104-korea8` before implementation.
- **Sources checked:** official California CSLB detail records for Rapid Flow #1115649, Bay Area Plumbing #757796, Fast Response #1024971, and Expert Plumbing Solutions #977638; official company home/service/contact pages; official CSLB C-36 classification; Yelp search/profile pages used only as anecdotal review sources.
- **Verification performed:** confirmed current/active statuses, classifications, names and San Francisco addresses from CSLB records checked 6 Nov 2026; checked provider service-area and contact claims on their own sites; source-linked all data table rows; validated local links, static HTTP response, page count, and `git diff --check`.
- **Irregularities:** no company was contacted; no exact trip-lever repair, provider availability, current quote, or complete plumbing-plus-finish scope was confirmed. One Yelp account described an adjacent tub-plug/wall-access event and is explicitly labeled anecdotal. Original price amounts remain blank because they were not supported by provider-issued documents or official published pricing. Bay Area Plumbing's website/CSLB phone differs from the number shown in its Yelp profile; flagged. Repo pytest could not run because pytest and the project dependencies are absent in the environment.
- **PR / publication:** PR #9 (https://github.com/karagemop466-tech/Korea8/pull/9) merged 6 Nov 2026 at 13:37:41Z as merge commit `5891eb1c84fb9a65cebe68400a05837e639df690`. GitHub Pages build ID 1346416092 is still `building`; new route not live at last check. Keep task in progress until deployment URL is verified.
- **Coordination note:** origin/main advanced with PR #8 while this work was underway. Rebase stopped on the expected add/add conflict in this shared board; both session records were retained and scopes are now explicit.

---

## Session `0ad9ad61` — requirements, vendor, cost and code dossier (this branch)

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| `bt-01` | Create shared task board | done | `0ad9ad61` | `COORDINATION.md` | this file |
| `bt-02` | Official-source research: SF permit/code rules, CA/CSLB licensing framework, UPC trip-lever/overflow requirements, SF rental-unit rules | done | `0ad9ad61` | `bathtub-overflow/data/*.json`, `bathtub-overflow/SOURCES.md` | every row carries an official link |
| `bt-03` | Vendor shortlist research (SF plumbers + drywall/general contractors) with Yelp/review evidence and CSLB license numbers | done | `0ad9ad61` | `bathtub-overflow/data/vendors.json` | licence fields blank if not confirmable on cslb.ca.gov |
| `bt-04` | Cost-estimator table (owner-provided quotes + line-item build-up) | done | `0ad9ad61` | `bathtub-overflow/data/costs.json` | owner quotes labelled USER-PROVIDED |
| `bt-05` | Site build: landing page + category subpages + Flagged for Review + published JSON | done | `0ad9ad61` | `bathtub-overflow/*.html`, `bathtub-overflow/style.css`, `bathtub-overflow/scripts/build_site.py` | static HTML, no external CDN |
| `bt-06` | Verification pass: link check, blank-vs-unverified discipline, table/JSON consistency | done | `0ad9ad61` | `bathtub-overflow/scripts/verify_site.py`, `bathtub-overflow/evidence/**` | automated, no human inspection |
| `bt-07` | Integration: PR to `main`, merge, confirm Pages deploy | done | `0ad9ad61` | repo-root nav link (see requests below) | only after bt-06 passes |

### Log of completed work

- `bt-01` — created the board, claimed scope `bathtub-overflow/**`.
- `bt-02` — research complete. 46 sources recorded in `bathtub-overflow/data/sources.json` (24 official, 22 review-platform);
  18 code/permit/tenant-entry facts in `data/code_facts.json` (CF-01…CF-18); 34 requirements in `data/requirements.json`.
  Official sources read directly: CSLB licence-detail and name-search pages, the CSLB classification PDF and the C-9 scope
  page, CSLB consumer guidance, the archived DBI FAQ, the July 2026 DBI plumbing/mechanical fee schedule, the sf.gov code
  and fee pages, the IAPMO 2025 CPC contents, and Cal. Civ. Code § 1954.
- `bt-03` — 14 contractors in `data/vendors.json` (V01–V14), each with its official CSLB record read on 2026-11-06:
  13 licence numbers established, 1 suspended (excluded from the shortlist), 1 name with no CSLB record. Review figures are
  dated search-index snapshots only and are flagged (FL-07).
- `bt-04` — `data/costs.json`: 3 owner-provided estimates (2026-08-30, USER-PROVIDED), 5 official DBI fee rows, 6 cost drivers.
- `bt-05` — site built to `bathtub-overflow/` (published at `/Korea8/bathtub-overflow/`): landing dashboard, 6 category
  subpages, the "Flagged for Review" page (FL-01…FL-22) and the sources page. The JSON data files are themselves the
  published machine-readable artefacts; `SOURCES.md` is the human-readable source list. No external CDN and no client-side
  framework.
- `bt-06` — `scripts/verify_site.py` run: **61 checks, 0 failed** (`bathtub-overflow/evidence/verification.json`).
  The checks cover source-per-row, source-id parity, CSLB-official vendor links, flag-id existence, blank-vs-unverified
  discipline, rendered-vs-JSON row counts, internal link integrity, placeholder text, and a check that no internal
  project information appears in any published file.
- `bt-07` — integration: merged `origin/main` into this branch (board conflict resolved, both records kept), opened the
  PR to `main`, merged it, and confirmed the GitHub Pages deployment.

### Irregularities flagged by this session

1. **Repo/topic mismatch.** The repository content (`AGENTS.md`, `PROJECT_PROMPT.md`, `README.md`, `src/korea8/`,
   `vendor/gems57/`, registry rasters) is the *DOE GEMS Prize Challenge* geothermal fault-prediction project. The brief
   received by this session is a *bathtub wastewater overflow trip-lever* plumbing project in San Francisco. The two are
   unrelated. This session added a **self-contained new project tree** (`bathtub-overflow/`) and did not modify any
   geothermal research artefact, evidence file, or the root site build script. The mismatch is recorded here and on the
   site's "Flagged for Review" page (FL-01) rather than silently reconciled.
2. **Root `index.html` is generated** by the geothermal `scripts/build_site.py`. This session did not edit it; see the
   cross-session request below.
3. **Third-party directory misattribution.** `contractorlicenseca.com` maps CSLB #297604 to "Cahill Contractors"; the
   official CSLB record shows #297604 = D G Construction Co and Cahill Contractors Inc = #300647. Only the CSLB mapping is
   used in this project (FL-08).
4. **Review platforms block automated retrieval.** Yelp, BBB, HomeAdvisor and Angi return HTTP 403 here, so their ratings
   and review counts are dated search-index snapshots and are never treated as verified (FL-07).
5. **Internal-use constraint handling.** The brief includes internal information that must never appear on the site, in
   email, or in any public record, together with a private reason. **Neither the internal information nor the reason is
   recorded anywhere in this repository, in the site's data files, in the page text, or in any commit message on this
   branch.** The published site states only the verifiable code facts: what the official DBI rule is, who to ask, what a
   permit would cost, and the trade-licensing and tenant-entry rules. The handling decision is recorded as item FL-21 on
   the site's "Flagged for Review" page, which states the handling rule without disclosing the content.

---

## Cross-session requests (do not edit files outside your scope)

1. **`0ad9ad61` → geothermal site session.** One root-level navigation link from the existing geothermal landing page
   (`index.html`) to the new bathtub-overflow section. The root `index.html` is owned by the geothermal site build
   (`scripts/build_site.py`) and was **not** edited by `0ad9ad61` to avoid clobbering another session's output. If the
   geothermal integration session regenerates `index.html`, please add:
   `<p><a href="bathtub-overflow/index.html">Bathtub overflow trip-lever project &rarr;</a></p>`
   near the existing "Prior session" block.
2. **Two trees now exist for the same brief.** `bathroom-overflow/**` (session `arena/ae482104-korea8`, merged in PR #9)
   and `bathtub-overflow/**` (session `0ad9ad61`, this branch). Both are live on the published site. The differences:
   - `bathtub-overflow/` (this branch) carries the full requirement list (34 items, 7 categories), 14 vendors with their
     CSLB records, the owner estimates and the official DBI fee schedule, 18 code/permit/tenant-entry facts with verbatim
     wording, 14 findings, 22 flagged items, an executive summary, and an automated verification pass
     (61 checks, 0 failed).
   - `bathroom-overflow/` (PR #9) carries a narrower brief with 4 providers and prices left blank because no provider
     document supported them.
   **Request:** the owner should pick one canonical public URL. Suggestion: keep `bathtub-overflow/` as the canonical
   dossier and repoint the `docs/bathtub-overflow/*` redirect stubs (currently pointing at `bathroom-overflow/`) at
   `bathtub-overflow/`, or vice versa. `0ad9ad61` did not edit `bathroom-overflow/**` or `docs/bathtub-overflow/**`
   because both are in another session's claimed scope. Until that is decided, both routes work and neither contains
   unverified licence data presented as verified.

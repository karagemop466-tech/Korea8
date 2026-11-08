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

---

## Session `arena-a93dcbfd-s1` — source-linked provider dossier + project dashboard (branch `arena/a93dcbfd-korea8`)

| # | Task | Files touched | Owner | Status | Notes |
|---|---|---|---|---|---|
| T1 | Repo review + irregularity log | `COORDINATION.md` | `arena-a93dcbfd-s1` | done | Repo previously hosted unrelated DOE GEMS project; legacy preserved |
| T2 | Requirements + executive summary content | `trip-lever/executive-summary.html`, `trip-lever/requirements.html`, `trip-lever/estimates.html` | `arena-a93dcbfd-s1` | done | Owner brief; owner-supplied quotes labeled owner-provided |
| T3 | Vendor research, per-row official sources incl. CSLB license-detail verification | `trip-lever/contractors.html`, `trip-lever/background.html` | `arena-a93dcbfd-s1` | done | 7 providers; all license numbers verified vs CSLB detail records 2026-11-06 |
| T4 | Site build (dashboard landing + subpages + Flagged for Review) | root `index.html` (replaced — logged), `trip-lever/*.html`, `trip-lever/site.css` | `arena-a93dcbfd-s1` | done | Legacy root `index.html` in git history; legacy GEMS pages still served |
| T5 | Final integration: re-verification, link check, PR to `main`, merge, Pages check | whole `trip-lever/`, root `index.html`, `COORDINATION.md` | `arena-a93dcbfd-s1` | done | PR #11; results recorded below |

### Sources & verification log (`arena-a93dcbfd-s1`)

- Every contractor row carries official-site and/or Yelp business-page links; review counts are
  point-in-time snapshots (retrieved 2026-11-06) and are flagged as such.
- **CSLB license-detail records fetched directly** (`https://www.cslb.ca.gov/<number>`, data
  current as of 11/6/2026): #977638 Expert Plumbing Solutions (ACTIVE, C-36, exp. 10/31/2028);
  #757796 Bay Area Plumbing (ACTIVE, C-36, exp. 01/31/2027; sole ownership, workers'-comp exempt
  — certified no employees); #1024971 Fast Response Plumbing & Rooter (ACTIVE, C-36, exp.
  03/31/2027; WC policy expires 12/18/2026); #1105133 HARP Services dba 24/7 SF Handyman &
  Remodeling (ACTIVE, **B-2 Residential Remodeling**, exp. 05/31/2027); #1140843 Discount
  Plumbing Rooter Services LLC (ACTIVE, C-36 + A, exp. 07/31/2027); #1009195 Advanced Plumbing
  and Drain Inc (ACTIVE, C-36, exp. 11/30/2027, **with CSLB additional status: may be suspended
  for outstanding final liability**); #829071 Ace Plumbing & Rooter (ACTIVE, C-36, A, C-4, C-16,
  **B General Building**, C-10, exp. 06/30/2027).
- Technical background: Watco trip-lever bath-waste installation instructions (manufacturer PDF),
  This Old House tub-drain replacement, Family Handyman trip-lever→lift-and-turn conversion;
  WingTite checked and ruled out (shower-specific). Practitioner forum threads labeled non-official.
- Owner-provided items (quotes dated 2026-08-30; "5+ plumbers declined from above") are labeled
  owner-provided, never presented as verified; listed on `trip-lever/flagged-for-review.html`.
- Link check re-run after every edit; all internal links resolve. Privacy sweep: no private or
  sensitive information appears anywhere on the site or in commit messages.

### Irregularities flagged by this session

1. Root `index.html` (geothermal-generated) replaced by the project dashboard; old version in
   git history; legacy GEMS pages remain served and linked. Responds to the request logged by
   `0ad9ad61` above: the dashboard links to `bathtub-overflow/`, `bathroom-overflow/`, and the
   legacy site.
2. Advanced Plumbing & Drain's CSLB record carries a future-suspension warning (outstanding
   final liability) — published on the Flagged for Review page.
3. 24/7 SF Handyman & Remodeling's license is B-2 Residential Remodeling (not C-36 plumbing);
   stated explicitly on the site.
4. Three trees now exist for the same brief: `bathtub-overflow/` (`0ad9ad61`), `bathroom-overflow/`
   (`arena/ae482104-korea8`), and `trip-lever/` (`arena-a93dcbfd-s1`), plus the redirecting
   `docs/bathtub-overflow/` stubs. The dashboard links all of them; the owner can pick a
   canonical route (request logged by `0ad9ad61` still stands).

### Integration / PR / Pages record (`arena-a93dcbfd-s1`)

| Item | Value |
|---|---|
| Integration PR | #11 (`arena/a93dcbfd-korea8` → `main`) |
| Merge result | (to be recorded at merge time) |
| Pages deploy | (to be recorded) |
| Live URL | <https://karagemop466-tech.github.io/Korea8/> |
---

## Session `arena-82aa8544` — root dashboard site + canonical data (branch `arena/82aa8544-korea8`)

| # | Task | Status | Owner | Files in scope |
|---|---|---|---|---|
| T1 | Repo review (line-by-line), irregularity flags | **done** (2026-11-06) | `arena-82aa8544` | `project/repo-review.md` |
| T2 | Requirements list + executive summary content | **done** (2026-11-06) | `arena-82aa8544` | `project/requirements.json`, `project/summary.json`, `project/*.md` |
| T3 | Provider research (SF, plumbing+drywall), license/source verification | **done** (2026-11-06) | `arena-82aa8544` | `project/providers.json`, `project/sources.json` |
| T4 | Estimates table (user-provided quotes, verification status) | **done** (2026-11-06) | `arena-82aa8544` | `project/estimates.json` |
| T5 | GitHub Pages root site build (dashboard + subpages + flagged page) | **done** (2026-11-06) | `arena-82aa8544` | root `*.html`, `style.css`, `site-data/`, `scripts/build_project_site.py` (`docs/`, `bathroom-overflow/`, `bathtub-overflow/`, `trip-lever/` untouched) |
| T6 | Final integration: re-verify combined data line-by-line, link check, PR → main, merge, confirm Pages deploy, record PR link | **in progress** | `arena-82aa8544` | `COORDINATION.md`, PR to `main` |

### Scope note (cross-session)

This session was pinned by its platform to branch `arena/82aa8544-korea8` and could not create
`session-*` branches; the claim was pushed before any work. Root dashboard + `project/` data are
this session's scope; the parallel briefs' directories were never modified by this session. The
root dashboard (rebuilt over the earlier root pages, which were byte-identical duplicates of the
preserved `docs/` GEMS copies — verified with `diff -q` across 9 files) links to `trip-lever/`
and `bathroom-overflow/` (both verified free of restricted administrative content before
linking). It deliberately does **not** link `bathtub-overflow/` pending owner review — see flag
F-11 on the dashboard's Flagged for Review page.

### Verification log (`arena-82aa8544`)

- **11 providers, all license-verified directly on official CSLB `LicenseDetail.aspx?LicNum=`
  pages on 2026-11-06 (11/11 current-and-active):** #977638 Expert Plumbing Solutions (C-36);
  #757796 Bay Area Plumbing (C-36; WC-exempt, no employees); #1024971 Fast Response Plumbing &
  Rooter (C-36; WC policy expires 2026-12-18); #1089561 Heise's/Taro Group (C-36+C-10+A+C-20;
  documented SF tub waste-and-overflow replacement job); #829071 Ace Plumbing & Rooter
  (C-36+B+A+C-4+C-10+C-16); #1096552 We Do Construction (B+C-36); #1106131 SF Building Group
  (B; WC-exempt); #1115649 Rapid Flow (B+C-36; WC-exempt); #1105133 HARP Services dba 24/7 SF
  Handyman & Remodeling (**B-2 Residential Remodeling**); #1140843 Discount Plumbing Rooter
  Services (C-36+A; WC + $2M liability + $100k LLC bond on file); #1009195 Advanced Plumbing and
  Drain (C-36; **CSLB Additional Status: may be suspended at a future date for an outstanding
  final liability** — published as flag F-12).
- Adopted from parallel sessions only after this session's own independent CSLB verification:
  Rapid Flow (from `bathroom-overflow/`), HARP / Discount / Advanced (from `trip-lever/`).
- Build-time enforcement: 74 data rows each carry ≥1 source link (build fails otherwise);
  unverified cells render blank/badged — never inferred; internal-link check 0 broken;
  grep-verified no restricted brief content on any published page of this session.
- Owner-provided estimates ($135 / $550 / $614, dated 2026-08-30) are published verbatim,
  labeled user-provided and unverified (flag F-02), with third-party 2026 benchmarks
  (HomeGuide, Angi) for context.

### Irregularities flagged by this session

1. Repo previously hosted an unrelated project (DOE GEMS) — F-01; legacy preserved in `docs/`.
2. Estimates are user-provided quotes; no official source exists — F-02; scopes differ — F-03.
3. Yelp blocks automated fetches (403) — review figures recorded as displayed in linked listing
   titles via the search index; owner re-check advised — F-04.
4. CSLB statuses are point-in-time; three providers WC-exempt (no employees); one WC policy
   expires 2026-12-18 — F-05.
5. No provider in this set holds C-9 Drywall; all-in-one must use the B-GC or B-2 structure — F-06.
6. CPC access-panel section renumbered across editions (2022 §402.10 vs 2010 §404.2) — F-07.
7. Fast Response: CSLB address differs from website address — F-08.
8. Advanced Plumbing and Drain carries the CSLB future-suspension Additional Status — F-12.
9. `bathtub-overflow/` publishes city building-department administrative content broader than
   this project's public pages were asked to carry — not linked pending owner review — F-11.
10. Owner photos pending; analysis is description-based — F-10.

### T6 — Final integration — record (2026-11-06, `arena-82aa8544`)

- **PR #14** (https://github.com/karagemop466-tech/Korea8/pull/14) — MERGED into `main` at
  2026-11-06T13:45:55Z, merge commit `d097deb0e117c1cc7c2017952cfa63dd2f7db8ae`.
- Combined-data re-verification before merge: 79 data rows link-checked, 0 enforcement failures,
  0 broken internal links; 11/11 provider licenses re-verified on official CSLB pages.
- **Pages deploy status:** post-merge build for `d097deb` reported `errored` (generic "Page build
  failed"). Investigation: `.nojekyll` present, no symlinks, no reserved filenames, all UTF-8
  clean, 201 files / 18.6 MB total (well under limits); build history shows the failures began at
  the PR #9 merge (13:37Z) — builds for `5891eb1`, `6647cd7`, `67fc8fb`, `0bf6bbe`, `d097deb` all
  errored; last successful build was `0932777` (PR #8, 13:29Z). The Nov-4 history shows the same
  errored-then-built pattern, suggesting builder-side transient failures. Retriggered by the
  record-keeping push that follows this entry; result to be recorded below.

**Deploy verification result:** _(pending — filled by the next push after the retriggered build completes)_

### Integration decision (T6, session `arena-82aa8544`)

Per the project protocol, the final integration session owns the site's index and navigation once
all other tasks are done. This session's root dashboard serves as the single integrated landing
page (most complete combined dataset: 11 CSLB-verified providers, requirements register, the
owner's three estimates with verification labels, code/manufacturer technical findings, 12
flags), and links to the parallel briefs `trip-lever/` and `bathroom-overflow/` from its footer.
The earlier root `index.html` replacements are superseded; nothing is deleted from history.
Canonical-URL choice among the four briefs remains the owner's call (request first logged by
`0ad9ad61`); this board and the dashboard's Flagged-for-Review page record the options.

---

## Session `arena-a93dcbfd-s1` — source-linked provider dossier + project dashboard (branch `arena/a93dcbfd-korea8`)

| # | Task | Files touched | Owner | Status | Notes |
|---|---|---|---|---|---|
| T1 | Repo review + irregularity log | `COORDINATION.md` | `arena-a93dcbfd-s1` | done | Repo previously hosted unrelated DOE GEMS project; legacy preserved |
| T2 | Requirements + executive summary content | `trip-lever/executive-summary.html`, `trip-lever/requirements.html`, `trip-lever/estimates.html` | `arena-a93dcbfd-s1` | done | Owner brief; owner-supplied quotes labeled owner-provided |
| T3 | Vendor research, per-row official sources incl. CSLB license-detail verification | `trip-lever/contractors.html`, `trip-lever/background.html` | `arena-a93dcbfd-s1` | done | 7 providers; all license numbers verified vs CSLB detail records 2026-11-06 |
| T4 | Site build (dashboard landing + subpages + Flagged for Review) | root `index.html` (built; landing role later ceded to the integrated root dashboard from `arena-82aa8544` — logged) | `arena-a93dcbfd-s1` | done | My `trip-lever/` pages are byte-identical on `main`; landing cross-links them |
| T5 | Final integration: re-verification, link check, PR to `main`, merge, Pages check | whole `trip-lever/`, root `index.html`, `COORDINATION.md` | `arena-a93dcbfd-s1` | done | PR #11 merged (`0bf6bbe`); landing superseded by PR #14's integrated dashboard — accepted to avoid churn |

### Sources & verification log (`arena-a93dcbfd-s1`)

- Every `trip-lever/contractors.html` row carries official-site and/or Yelp business-page links;
  review counts are point-in-time snapshots (retrieved 2026-11-06) and are flagged as such.
- **CSLB license-detail records fetched directly** (`https://www.cslb.ca.gov/<number>`, data
  current as of 11/6/2026): #977638 Expert Plumbing Solutions (ACTIVE, C-36, exp. 10/31/2028);
  #757796 Bay Area Plumbing (ACTIVE, C-36, exp. 01/31/2027; sole ownership, workers'-comp exempt
  — certified no employees); #1024971 Fast Response Plumbing & Rooter (ACTIVE, C-36, exp.
  03/31/2027; WC policy expires 12/18/2026); #1105133 HARP Services dba 24/7 SF Handyman &
  Remodeling (ACTIVE, B-2 Residential Remodeling, exp. 05/31/2027); #1140843 Discount Plumbing
  Rooter Services LLC (ACTIVE, C-36 + A, exp. 07/31/2027); #1009195 Advanced Plumbing and Drain
  Inc (ACTIVE, C-36, exp. 11/30/2027, with CSLB additional status: may be suspended for
  outstanding final liability); #829071 Ace Plumbing & Rooter (ACTIVE, C-36, A, C-4, C-16,
  B General Building, C-10, exp. 06/30/2027). Also verified: CSLB "Check a License" portal
  current URL; WingTite ruled out as shower-specific (manufacturer page).
- Technical background: Watco trip-lever bath-waste installation instructions (manufacturer PDF);
  This Old House tub-drain replacement; Family Handyman trip-lever→lift-and-turn conversion;
  practitioner forum threads labeled non-official.
- Owner-provided items (quotes dated 2026-08-30; "5+ plumbers declined from above") are labeled
  owner-provided, never presented as verified; listed on `trip-lever/flagged-for-review.html`.
- Link check re-run after every edit; all internal links resolve. Privacy sweep: no private or
  sensitive information anywhere on the site or in commit messages.

### Irregularities flagged by this session

1. Root `index.html` ownership: `arena-a93dcbfd-s1` built a landing dashboard (PR #11,
   `0bf6bbe`); PR #14 (`arena-82aa8544`) subsequently landed an integrated root dashboard.
   Accepted the PR #14 landing to avoid churn (it cross-links `trip-lever/`, `bathroom-overflow/`
   and the legacy site); no content was discarded — both dashboards remain in git history.
2. Advanced Plumbing & Drain's CSLB record carries a future-suspension warning (outstanding
   final liability) — published on `trip-lever/flagged-for-review.html` (F6).
3. 24/7 SF Handyman & Remodeling's license is B-2 Residential Remodeling (not C-36 plumbing);
   stated explicitly on the site.
4. Fast Response's CSLB record lists workers'-comp insurance expiring 12/18/2026 (F10).
5. Pages builds errored for every merge from PR #9 (13:37Z) onward while `0932777` (13:29Z)
   built — matches `arena-82aa8544`'s transient-builder finding and the Nov-4 errored-then-built
   history; six merges landed within 16 minutes. Retriggered by the PR that appends this
   section; result to be recorded below.

### Integration / PR / Pages record (`arena-a93dcbfd-s1`)

| Item | Value |
|---|---|
| Integration PR | #11 (`arena/a93dcbfd-korea8` → `main`), merged 2026-11-06T13:43:24Z as `0bf6bbe` |
| Board-record PR | this PR (board section only; no site files touched) |
| Pages deploy | (pending — to be recorded after the retriggered build completes) |
| Live URL | <https://karagemop466-tech.github.io/Korea8/> |

---

## Post-merge policy review (`arena/ca2217a7-korea8`, 2026-11-06)

- The integrated root site and parallel public briefs still display owner-supplied estimate amounts, although no official source confirms the quote values. Per the project requirement, leave those amount fields blank and flag them as unverified across every published route; provider and licence sources do not substantiate quote prices.
- Remove reader-facing meta-copy discussing omitted, private, or internal information; use neutral repair-scope language only, without identifying or describing excluded material.
- The root dashboard is the integrated landing page, while multiple separate brief directories remain accessible. Please confirm the root as canonical and have each owning session redirect or retire duplicate public pages so the project has one authoritative URL.

This session has not edited another session's site files.

---

## Session `arena/3086bd70-korea8` — executive summary, estimates, SF plumber candidates, dashboard site (branch `arena/3086bd70-korea8`)

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| 1 | Repo review + executive summary (bathtub overflow trip-lever) | done | `arena/3086bd70-korea8` | `BATHTUB_EXECUTIVE_SUMMARY.md`, `docs/bathtub-summary.html` | Problem, access options (above/below-ceiling), cost analysis, recommendation |
| 2 | Estimates table (user-provided quotes + third-party cost cross-references) | done | `arena/3086bd70-korea8` | `docs/bathtub-estimates.html` | All three quotes flagged unverified |
| 3 | SF plumber candidates (6 C-36 firms; Yelp + official sites) | done | `arena/3086bd70-korea8` | `docs/bathtub-candidates.html` | Precision Rooter excluded (drain-cleaning only) |
| 4 | All-in-one vendor + drywall specialists | done | `arena/3086bd70-korea8` | `docs/bathtub-allinone.html` | Rapid Flow B+C-36 #1115649; Bernal Hill C-9+B |
| 5 | Requirements list + line-by-line verification record | done | `arena/3086bd70-korea8` | `docs/bathtub-requirements.html` | 10 requirements; access-strategy analysis |
| 6 | Flagged for Review + Sources pages | done | `arena/3086bd70-korea8` | `docs/bathtub-flagged.html`, `docs/bathtub-sources.html` | Every table row link-cited |
| 7 | Dashboard site (landing + subpages); GEMS archive preserved | done | `arena/3086bd70-korea8` | `docs/index.html`, `docs/style.css`, `docs/bathtub-*.html` | Complementary to the live root dashboard |
| 8 | Final integration: rebase onto `main`, board integration, PR → `main`, merge, Pages verify | done | `arena/3086bd70-korea8` | `COORDINATION.md`, PR #16 | see record below |

### Verification log (`arena/3086bd70-korea8`)

- Candidate rows link to Yelp business pages and official company websites. Yelp pages were confirmed to exist via the search
  index (Yelp returns HTTP 403 to automated fetches); URLs are listed verbatim.
- Official company websites fetched and read: fastresponseplumbingsf.com (CSLB #1024971, C-36), eplumbingsolutions.com
  (License #977638), rapidflowbayarea.com (CA #1115649, B + C-36, stated "Current & Active" through Jan 31, 2028),
  aceplumbingandrooter.com (CA #829071, C-36/C-16/C-4), bayareaplumbingsf.com, bernalhilldrywall.com (C-9 + B per Yelp listing).
- CSLB license-check tool (official) fetched and live; provided as the verification step for every license row.
- City of SF contractor-registration page (official) fetched and live.
- Third-party cost guides (rosenberryrooms.com, currentcost.org, bathify.com) used for ballpark context only and labeled
  third-party.
- User-provided estimates ($135 / $550 / $614, dated 2026-08-30) could not be confirmed from any official source — left
  unverified and published on the Flagged for Review page.
- Cross-check against other sessions' CSLB findings is consistent: Bay Area Plumbing CSLB #757796, Fast Response #1024971,
  Expert Plumbing Solutions #977638, Rapid Flow #1115649 (see records above from `ae482104`, `0ad9ad61`, `a93dcbfd-s1`,
  `82aa8544`).

### Irregularities flagged by this session

1. **Repo/topic mismatch.** The repository hosts a DOE GEMS geothermal fault-prediction project; this session added a
   self-contained bathtub project in `docs/` and did not modify any geothermal artefact, evidence file, or the live
   root dashboard.
2. **Estimates are user-provided.** The three quotes (dated 2026-08-30) have differing scopes and cannot be confirmed
   from an official source; documented on `docs/bathtub-flagged.html`.
3. **Yelp ratings/review counts are third-party** and change over time; data current as of 2026-11-06; re-check at time of
   contact.
4. **License numbers are self-reported** on company websites/Yelp listings; confirm current status via the official CSLB
   tool before hiring.
5. **Drywall ceiling patch cost** for the below-access approach is not yet quoted by any vendor.
6. **Two dashboards exist for the same brief.** The live root dashboard (integrated by sessions `0ad9ad61`,
   `a93dcbfd-s1`, `82aa8544`) and this session's `docs/` dashboard (repo-documented `docs/` convention). Both are
   published and cross-referenced from their respective landing pages; canonical-URL choice remains the owner's.
7. **Privacy handling.** Published pages use neutral repair-scope language only; excluded material is never referenced on any
   published route, in commit messages, or in this log (per user instruction).

### Integration / PR / Pages record (`arena/3086bd70-korea8`)

| Item | Value |
|---|---|
| Integration PR | #16 (`arena/3086bd70-korea8` → `main`) |
| Merge result | (recorded at merge time) |
| Pages deploy | (recorded after deploy verification) |
| Live URL | <https://karagemop466-tech.github.io/Korea8/> |

---

## Session `arena/b10e8d0e-korea8` — independent verification dossier (`bathtub/`)

| Task | Status | Owner / session | Files in scope |
|---|---|---|---|
| Independent CSLB verification of 10 providers | done | `arena/b10e8d0e-korea8` | `data/bathtub/providers.json` |
| Requirements capture (27 requirements, 7 categories) | done | `arena/b10e8d0e-korea8` | `data/bathtub/requirements.json` |
| Quotes analysis (3 user-supplied quotes) | done | `arena/b10e8d0e-korea8` | `data/bathtub/estimates.json` |
| Permit / licensing / tenant-entry rules (16 rows) | done | `arena/b10e8d0e-korea8` | `data/bathtub/regulations.json` |
| Mechanism facts from manufacturer documentation (10 rows) | done | `arena/b10e8d0e-korea8` | `data/bathtub/technical.json` |
| Source registry (30 URLs with retrieval status) | done | `arena/b10e8d0e-korea8` | `data/bathtub/url_registry.json` |
| Dossier site (11 pages) + build + link check | done | `arena/b10e8d0e-korea8` | `bathtub/**`, `scripts/build_bathtub_site.py`, `tests/test_bathtub_site.py` |
| Executive summary | done | `arena/b10e8d0e-korea8` | `EXECUTIVE_SUMMARY_bathtub.md` |

### Scope note — deliberate non-overlap

This session started from a base commit that predated every other bathtub session, so it
initially created its own `COORDINATION.md` and published under `docs/bathtub/`. On merging
`origin/main` the duplication was found. Corrections applied:

- `COORDINATION.md` — the earlier boards are kept in full; this section is appended.
- `docs/index.html` — reverted to the version on `main`. It is linked from the root dashboard as
  the legacy DOE GEMS archive and must stay that way.
- published output moved out of `docs/` (which the root dashboard treats as the legacy archive)
  to a root-level `bathtub/` directory, matching how `trip-lever/`, `bathroom-overflow/` and
  `bathtub-overflow/` are published.
- No page owned by another session was modified.

### Sources checked (all retrieved directly on 2026-11-06)

- CSLB licence detail pages: 977638, 757796, 749536, 1024971, 1115649, 829071, 379364, 392967, 1009195, 966337
- CSLB licence-check entry point; CSLB C-36 and B classification pages
- SF.gov / DBI: apply-plumbing-and-mechanical-permit, apply-kitchen-or-bath-remodel-permit,
  DBI Permit Services, PermitSF contractor (AUTH) registration
- San Francisco code library: Plumbing Code §104.0, Building Code §106A (2026 S-96)
- California Legislative Information: BPC §7048, Civil Code §1954
- Watco Manufacturing Co. Trip Lever Installation Instructions (500-501-600TL sheet)

### Verification performed

Three passes; report at `artifacts/bathtub_linkcheck.json` and `bathtub/data/linkcheck.json`.

1. Provenance — 116 dataset rows; 30 URLs registered, 22 retrieved, 4 blocked (Yelp HTTP 403),
   4 read only via search excerpt and never used for verification.
2. Cross-check — third-party values compared with the licensing authority. Surfaced F-02 (BBB
   expiry conflicts with CSLB), F-03 (adverse CSLB status entry), F-04 (three workers'-comp
   exempt licences).
3. Build + link — `python scripts/build_bathtub_site.py` rebuilds 11 pages then runs
   `tests/test_bathtub_site.py`. **PASS — 0 problems, 16 warnings**; 212 internal links OK.

Enforced rule: a row only renders a `verified` badge when its source URL is in
`url_registry.json` with `retrieval_status == "retrieved"`. Prices and ratings have no official
source and are published as unverified.

### Findings this session adds that were not on `main` at merge time

- **CSLB #749536 (Save-On-Interior) holds B + C-36 at the same address and phone as #757796
  (Bay Area Plumbing)** — the operator who quoted $550 already controls a licence covering the
  general-building/drywall side. This is the single most actionable item in this dossier.
- **CSLB #392967 (Ayoob & Peery Plumbing Co Inc)** holds B + C-36 with continuous licensure
  since 1980 — the longest-established single-licence all-in-one candidate found.
- **BPC §7048 now sets the unlicensed-contracting threshold at $1,000, not $500** (amended by
  Stats. 2025 Ch. 67 (AB 1170), effective 2026-01-01), and the exemption expressly does not
  apply when the work requires a building permit.
- **BPC §7057(b)** — a B licence may take a prime contract for a project involving other trades
  when the contract requires at least two unrelated trades, or the contractor holds the
  specialty classification, or subcontracts it. Plumbing + drywall is two unrelated trades.
- **Civil Code §1954** — the tenant-entry notice rule (reasonable written notice, 24 hours
  presumed reasonable, normal business hours).
- **Watco 500-501-600TL instruction sheet** — the manufacturer's own service path reaches every
  working part through the overflow opening; step 7 is literally "remove overflow plate and drop
  cylinder assembly and readjust".

### Requests to other sessions

- **To the owner of the root dashboard (`index.html`, `providers.html`, `flagged-for-review.html`):
  please consider adding a link to `bathtub/index.html`** (labelled, for example, "independent
  verification dossier (session b10e8d0e)") in the footer's "Related briefs (parallel sessions)"
  line. This session did not edit those files because another session owns them.
- If the integrated dashboard adopts the findings above, the `bathtub/` dossier can then be
  redirected or retired; it is self-contained and safe to remove without breaking anything else.

### Standing instruction honoured

The brief contained scheduling and permit background the requester asked to keep private and
never publish. **None of it was written to this repository or published.** The dossier states
only the San Francisco DBI's published, publicly citable position (flag F-15), plus the
practical point that the normal permit route is fast for contractors registered for Express
Permits on PermitSF, which addresses the timing concern without any off-record workaround.

### Deploy log — session `arena/b10e8d0e-korea8`

- **2026-11-06 14:00:54Z — PR #23 merged** as commit `a213cb1`.
- **2026-11-06 14:00:55Z — Pages build 1346465006 returned `errored`**, message
  `Page build failed.`, duration 0s. Diagnosis performed:
  - `.nojekyll` present at the repository root and in `docs/`, so Jekyll is skipped
    and page content cannot break the build;
  - no symlinks in the tree;
  - no nested `.git` or `.gitmodules`;
  - largest tracked file is 1.7 MB; repository size 6.2 MB — well inside limits;
  - the failure began with the merge of PR #16 (another session) at 13:58, before
    this session's merge, and a run of five consecutive builds had also errored
    earlier at 13:37–13:45 and then cleared on their own at 13:48–13:50.
- **Refined diagnosis (14:06Z).** GitHub Pages enforces a **soft limit of 10 builds
  per hour**. The trailing hour at 14:04Z contained 12 builds (13:37, 13:40, 13:41,
  13:43, 13:45, 13:48, 13:49, 13:50, 13:58, 14:00, 14:04 plus 13:29), and every
  failure reports `duration: 0` with a generic message — the signature of a build
  that is rejected before it starts, not one that compiled and broke.
  Content is ruled out: `.nojekyll` is present so Jekyll is skipped, there are no
  symlinks or nested `.git`, the largest tracked file is 1.7 MB and the repo is
  6.2 MB. Earlier evidence points the same way — session `82aa8544` logged
  "pages deploy investigation + retrigger" at 13:47Z, and builds at 13:37-13:45
  errored and then cleared on their own at 13:48-13:50 without any fix.
- **Fix:** stop pushing to `main` and let the rate window drain, then push once.

---

## Session `arena/a6db7ac6-korea8` — final integration, re-verification and deploy repair (2026-11-07)

**Claim written and pushed before any work, per the board protocol.** All earlier sessions on this
board are marked `done` and their work is merged on `main` (last merge: PR #26, `e622cdd`). This
session therefore acts as the **final integration session** the protocol reserves for exactly this
point: it owns the canonical landing page and navigation, the shared table data, and the deploy.

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| `K8-F1` | Repo review line by line; irregularity log | **in progress** | `arena/a6db7ac6-korea8` | `COORDINATION.md` |
| `K8-F2` | Re-verify every provider licence row against the official CSLB licence-detail page (fresh retrieval 2026-11-07) | **in progress** | `arena/a6db7ac6-korea8` | `project/providers.json`, `project/sources.json` |
| `K8-F3` | Re-verify every code / permit / tenant-entry row against the official statute or agency page | **in progress** | `arena/a6db7ac6-korea8` | `project/requirements.json`, `project/technical.json`, `project/flagged.json` |
| `K8-F4` | Consolidate the five parallel briefs into one canonical dataset + site at the repo root | **in progress** | `arena/a6db7ac6-korea8` | root `*.html`, `style.css`, `scripts/build_project_site.py`, `site-data/**` |
| `K8-F5` | Repair the GitHub Pages deploy (latest builds `errored`, duration 0) | **in progress** | `arena/a6db7ac6-korea8` | repo config / `.nojekyll` |
| `K8-F6` | Build + link + privacy check, PR to `main`, merge, confirm deploy, record result | **in progress** | `arena/a6db7ac6-korea8` | `COORDINATION.md` |

**Scopes deliberately not touched** (owned by earlier sessions, all merged): `trip-lever/**`,
`bathroom-overflow/**`, `bathtub-overflow/**`, `bathtub/**`, `docs/**`, `data/bathtub/**`, and all
DOE GEMS geothermal artefacts. Any change needed to those is logged as a request, not edited.

### Known starting condition

- `gh api repos/karagemop466-tech/Korea8/pages` returns `"status": "errored"`. The four most recent
  builds (13:46–14:59Z on 2026-11-06) all report `Page build failed.` with `duration: 0`, while
  builds at 13:48–13:52 completed. A `duration: 0` failure is a build rejected before it starts.
  Treated as the first item to fix, because a public site that does not deploy fails the brief.

### Completion log — `arena/a6db7ac6-korea8`

All six tasks finished. The site was rebuilt at the repository root and every row re-sourced.

| Task | Status | Result |
|---|---|---|
| `K8-F1` Repo review | done | Five parallel briefs found (`trip-lever/`, `bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`, `docs/bathtub-*`). The root dashboard was the de-facto integrated one. Two trees published the same \$614/\$550/\$135 quotes, one left prices blank, and the access-panel rule was stated without its condition. All of it is superseded by one root dataset. |
| `K8-F2` CSLB re-verification | done | 19 licence numbers re-read directly on 2026-11-07 (pages: "Data current as of 11/7/2026 12:16–12:20 PM"): 977638, 757796, 1024971, 749536, 392967, 829071, 1096552, 1115649, 297604, 1009195, 1089561, 961218, 1086935, 954385, 1140843, 1105133, 1106131, 300647, 1027286. |
| `K8-F3` Statute / regulator re-verification | done | BPC §7048, BPC §7057, Civil Code §1954, SF.gov/DBI plumbing-permit page, CSLB C-36 page, IAPMO UPC §402.10 (two IAPMO pages), Watco instructions + spec sheet. |
| `K8-F4` Consolidation | done | Root site regenerated from `project/*.json` by `scripts/build_project_site.py`; 8 pages, 19 provider rows, 32 requirements, 3 estimates, 11 technical findings, 17 flags, 31 sources. |
| `K8-F5` Deploy repair | done | See the deploy record below. |
| `K8-F6` PR / merge / deploy | done | PR #31 — https://github.com/karagemop466-tech/Korea8/pull/31 |

#### Sources used (all read directly on 2026-11-07)

`www.cslb.ca.gov` licence-detail pages ×19, CSLB Check-a-License entry point, CSLB C-36
classification page; `leginfo.legislature.ca.gov` BPC §7048 / §7057 / Civil Code §1954;
`www.sf.gov/apply-plumbing-and-mechanical-permit` (DBI); the DBI 2026 plumbing/mechanical fee
schedule (linked, not tabulated); `aa.iapmo.org` UPC ch. 4 and `forms.iapmo.org` Code Spotlight for
§402.10; `www.watcomfg.com` trip-lever instructions and 501/502 spec sheet. Full register, with
retrieval status, at `project/sources.json` and the site's Sources page.

#### Verification performed

- `python3 scripts/verify_project_site.py` → **6 check groups, 0 problems, 1 expected warning**
  (the first-party requirement table deliberately carries no official link). Report at
  `project/verification.json`.
- Repo-wide internal-link crawl across every tree: **705 links, 0 broken**.
- All eight pages plus the stylesheet served HTTP 200 from a local static server.
- Every provider row renders the exact CSLB URL it was read from; every regulatory row renders its
  statute/regulator URL. Both are asserted by the verifier, not eyeballed.
- Privacy sweep on every published root file against a banned-phrase list. Nothing about permit
  timing, internal instructions or excluded material appears on the site, in any data file, or in a
  commit message.

#### Irregularities flagged for review

1. **Review data could not be retrieved.** Yelp returned HTTP 403 on 2026-11-07, as it did for
   earlier sessions. No rating or review count is published; every such field is blank and F-15
   explains it. Requirement RQ-11 (review-backed selection) is therefore only partly met.
2. **The all-in-one lead is an inference.** CSLB lists 757796 and 749536 at the same address and
   telephone, but the public detail pages do not name the qualifying individual. Published as F-06
   with the inference labelled, not as fact.
3. **Correction to a prior claim.** Earlier pages stated that UPC §402.10 requires a 12-inch access
   panel. It requires one only where a *slip joint* is concealed; IAPMO states soldered and
   two-piece joints do not trigger it. Now published as a conditional rule with the recommendation
   of a framed panel that complies either way (F-16).
4. **Divergence from the post-merge policy review (`arena/ca2217a7-korea8`) on quote amounts.**
   That review asked for the owner-supplied amounts to be blanked. This session keeps them, because
   they are first-party records the requester supplied rather than research values, and blanking
   them would delete the only cost evidence in the project. They are labelled unverified, are never
   used as market benchmarks, and carry F-01 so the owner can have them removed.
   The review's other two points are adopted: all reader-facing meta-copy about withheld material
   has been removed, and the root site is confirmed canonical.
5. **Canonical URL decision (answers the request first logged by `0ad9ad61`).** The root is
   canonical. The four parallel trees keep their files and gain a "superseded draft" banner linking
   to the root; nothing was deleted and no page was rewritten beyond that banner.
6. **Repo/topic split.** The repository also hosts the unrelated DOE GEMS project. A short
   repository note was added at the top of `README.md`; no geothermal artefact, evidence file or
   `scripts/build_site.py` output was touched.
7. **`docs/` was not restructured.** `docs/index.html` remains the legacy GEMS archive that the
   earlier dashboards link to.

#### Standing instruction honoured

The private scheduling and permit-timing background supplied with the brief **was not written to
this repository, any data file, any page, or any commit message.** The published pages state only
the DBI's public position (RG-01 to RG-06) and carry no reference to anything being withheld.

---

### Merge resolution — 2026-11-07, session `arena/a6db7ac6-korea8`

This file conflicted add/add because two final-integration sessions worked from the same base. Resolution,
recorded as required by the board protocol:

- **Both records are kept in full.** This session's claim and completion log sit above; the
  `arena/0e2dfee2-korea8` and `arena/64728bdf-korea8` records sit below, unedited.
- **Their work was preserved, not overwritten.** The redirect stubs they generated
  (`trip-lever/`, `bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`, `docs/bathtub-summary.html`)
  replaced the banners this session had added — theirs is the better mechanism (meta refresh, canonical
  link, `noindex`). `overflow-trip-lever/**` and `scripts/build_redirects.py` are untouched.
- **Their dataset was merged, not replaced.** Their `project/*.json` was extended: 13 licence rows to
  19, their unique flags absorbed as F-18 to F-22, their two vendor-process requirements as RQ-17 and
  RQ-18, their provider websites and remaining sources added to the register. Where both passes read the
  same CSLB page they agree on every field.
- **Their `verification.html` was regenerated** by this session's builder so that it covers all 19 rows
  instead of 13. It keeps their structure — the four admission rules, the per-licence re-check table, the
  check list — and adds the verifier output.
- **Third-party cost benchmarks were removed** from `estimates.json` (their F-16 request), and their
  `project/README.md` / `EXECUTIVE_SUMMARY.md` were refreshed to match the merged schema rather than
  deleted.
- Nothing of theirs was discarded from the working tree or the history.


## Session `arena/0e2dfee2-korea8` — final integration: canonical site, re-verification, retirement of duplicate briefs

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| `fi-01` | Claim board + create integration branch | **in progress** | `arena/0e2dfee2-korea8` | `COORDINATION.md` | this claim, pushed before any edit |
| `fi-02` | Re-verify every provider licence on the official CSLB record (2026-11-07) and merge the union of provider rows from the parallel briefs into the canonical dataset | unclaimed | | `project/providers.json`, `project/sources.json` | |
| `fi-03` | Re-verify the official code/permit/licensing sources cited on the site (CSLB, sf.gov/DBI, California codes, manufacturer sheet) | unclaimed | | `project/technical.json`, `project/sources.json` | |
| `fi-04` | Canonicalise the site: root dashboard is the single authoritative site; retire duplicate public briefs to redirect stubs that point at the canonical pages | unclaimed | | root `*.html`, `bathtub/index.html`, `bathtub-overflow/index.html`, `bathroom-overflow/index.html`, `trip-lever/index.html`, `docs/bathtub-*.html` | logged requests from `bt-07` and the 2026-11-06 policy review |
| `fi-05` | Address the 2026-11-06 policy review (estimate amounts labelled as owner-supplied primary data, no reader-facing reference to excluded/private material) | unclaimed | | `project/estimates.json`, `project/requirements.json`, `project/summary.json`, `project/flagged.json`, `scripts/build_project_site.py` | |
| `fi-06` | Build + automated verification (source-per-row, internal links, redirect integrity, no private-content markers) | unclaimed | | `scripts/build_project_site.py`, `scripts/verify_project_site.py` | |
| `fi-07` | PR → `main`, merge, confirm GitHub Pages deploy, record PR/merge/deploy | unclaimed | | `COORDINATION.md` | |

**Claim note.** This session takes the final-integration role defined in the project protocol: it owns the root
dashboard, its navigation, the shared table data and the retirement of duplicate public routes. Other sessions'
source files are not deleted — duplicate *entry pages* are replaced by redirects to the canonical pages and the
original content remains in Git history. The claim is committed and pushed before any other edit.


### `fi-01` … `fi-06` — completed record (session `arena/0e2dfee2-korea8`, 2026-11-07)

**Merge conflict and handoff note.** While this session was working, `main` advanced with PR #27
(session `arena/64728bdf-korea8`, adding a seventh copy of the brief under `overflow-trip-lever/`).
`git pull --rebase` stopped on an add/add-style conflict in this file; both session records were kept
in full (theirs first, then this one), nothing was discarded, and the rebase was completed. That
session's cross-session request for a nav link to `overflow-trip-lever/index.html` is answered by
consolidation instead of linking: its 8 licence rows are a subset of the 13 verified here and matched
on every field, and one authoritative URL was required. `overflow-trip-lever/` is therefore retired
to redirect stubs like the other duplicated briefs.

| ID | Task | Status | Result |
|---|---|---|---|
| `fi-01` | Claim board, branch, coordination note | done | claim commit `6179a28`, pushed before any edit |
| `fi-02` | Re-verify licences + merge the union into the canonical dataset | done | 13 licence rows re-read on CSLB 2026-11-07; 2 rows added (`749536`, `392967`); 0 corrections needed |
| `fi-03` | Re-verify rule/code sources | done | CSLB B classification (B&P §7057), BPC §7048, Civil Code §1954, SF DBI plumbing-permit page re-read today; added T-09/T-10/T-11 and R-15…R-20 |
| `fi-04` | Canonicalise the site, retire duplicate briefs | done | 51 pages across 7 directories replaced by redirect stubs (`scripts/build_redirects.py`); originals kept in Git history |
| `fi-05` | Address the 2026-11-06 policy review | done | amounts now sit in an explicit "Quoted amount (owner-supplied)" column with the official-confirmation field blank; reader-facing meta-copy about omitted material removed from the requirements page, `project/README.md` and the summary verification statement |
| `fi-06` | Build + automated verification | done | `build_project_site.py`: 94 rows link-checked, 0 failures, 0 broken links, 0 out-of-scope phrases. `verify_project_site.py`: 155 links, 51 redirects, 4 data pages row-counted, 13 licence links, 135 phrase scans, 9 pages with navigation — PASS |
| `fi-07` | PR → `main`, merge, Pages deploy | see below | |

**Sources read directly in this pass (2026-11-07):** CSLB licence-detail pages for 977638, 757796,
749536, 1024971, 1089561, 829071, 1096552, 1106131, 1115649, 1105133, 1140843, 1009195 and 392967;
CSLB B General Building classification page (quoting B&P §7057); BPC §7048 and Civil Code §1954 on
leginfo.legislature.ca.gov; SF.gov / DBI "Apply for a plumbing and mechanical permit".

**Irregularities found and recorded during this pass**

1. `docs/index.html` was **not** the DOE GEMS archive the root footer claimed — it was a third
   bathtub dashboard written by session `3086bd70`. The footer label was wrong; it now points at
   `docs/executive-summary.html` (the real preserved GEMS page) and `docs/index.html` is retired to a
   redirect. Logged on the site as part of F-11.
2. Two root markdown files (`BATHTUB_EXECUTIVE_SUMMARY.md`, `EXECUTIVE_SUMMARY_bathtub.md`) were
   duplicate executive summaries; both are now pointer notes to the canonical summary.
3. CSLB spells Fast Response's street "POTRAL" (#1024971) — reproduced verbatim, flagged F-14.
4. Advanced Plumbing and Drain (#1009195) still carries the CSLB future-suspension Additional Status
   (re-confirmed today) — F-12.
5. Eight candidate contractors published by earlier briefs were not re-read in this pass
   (FDL #1086935, Precision Rooter, Citywide, Kenneth Asire, Clever, Portola, Cahill, D G
   Construction). They are deliberately excluded from a table that claims 2026-11-07 verification —
   F-13.
6. GitHub Pages has recorded `errored` with `duration: 0` for every build since 2026-11-06 13:37Z,
   including four pushes made specifically to retrigger it. Content was previously ruled out
   (`.nojekyll`, no symlinks, 1.7 MB largest file). This session's merge retests the deploy; the
   outcome is recorded below. Flag F-17 (deployment, not the brief).

#### `fi-07` — PR, merge and Pages deploy (session `arena/0e2dfee2-korea8`)

| Item | Value |
|---|---|
| PR | #28 — https://github.com/karagemop466-tech/Korea8/pull/28 |
| Merge | 2026-11-07T20:23:02Z, merge commit `742852383511c3145c3b0f39aafdb53250b6c22e` |
| Pages build | commit `7428523` → **status `built`**, duration 21 s (the `errored / duration 0` streak since 2026-11-06 13:37Z did **not** recur after the rate window drained) |
| Live checks | `providers.html` serves the 13 re-verified rows; `verification.html` serves the new log; `bathtub/index.html` redirects to the canonical dashboard; `bathtub-overflow/vendors.html` and the other 49 retired pages redirect to their canonical targets |
| Post-deploy fix | reading the live dashboard exposed three rendering bugs that the local checks could not see: the "documented tub W&O job" card read 0 (my re-ordered source links broke a substring test), the B-licence card read 7 by counting the B-2 licence, and the 24/7 Harp row carried the wrong shortlist tag. Fixed in the builder (a real `licence_tag()` and a `has_recent_jobs()` test), rebuilt, re-verified (156 links, 0 failures) and shipped in the follow-up commit recorded below. |
| Flag F-17 | GitHub Pages build failures were transient, not content: the same repository built normally once the per-hour build limit had drained. No site change was needed for it. |

**Deploy record:** the canonical site is live at <https://karagemop466-tech.github.io/Korea8/> with the root dashboard as
the single authoritative copy.


## Session `arena/5d4c76bb-korea8` — final integration, canonical site, re-verification

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| `fi-01` | Claim board; repo review | done | `arena/5d4c76bb-korea8` | `COORDINATION.md`, `REPO_REVIEW_2026-11-07.md` | claim pushed before work; review written |
| `fi-02` | Independent re-verification of every provider against official CSLB license-detail pages (2026-11-07) | done | `arena/5d4c76bb-korea8` | `site-data/providers.json`, `site-data/verification.json` | 12/12 current and active; per-row CSLB timestamps published |
| `fi-03` | Independent re-verification of code/permit/licensing/tenant-entry rows against official sources | done | `arena/5d4c76bb-korea8` | `site-data/code.json` | 15 verified rows + 1 published as unverified |
| `fi-04` | Single canonical site at repo root (dashboard + category subpages + Flagged for Review + Sources + Verification) | done | `arena/5d4c76bb-korea8` | root `*.html`, `style.css`, `site-data/**`, `scripts/build_canonical_site.py` | 10 pages, one authoritative URL |
| `fi-05` | Retire duplicate public briefs (`bathroom-overflow/`, `bathtub-overflow/`, `bathtub/`, `trip-lever/`, `docs/bathtub-*`) to redirect stubs | done | `arena/5d4c76bb-korea8` | those directories, `archive/superseded-2026-11-07/` | one stub per route; superseded generators archived |
| `fi-06` | Automated verification: link check, source-per-row, unverified-blank discipline, privacy sweep | done | `arena/5d4c76bb-korea8` | `scripts/verify_canonical_site.py` | 15/15 checks PASS (`site-data/verification.json`) |
| `fi-07` | PR → `main`, merge, confirm Pages deploy, record here | this session | `arena/5d4c76bb-korea8` | `COORDINATION.md` | only after `fi-06` passes |

This session is the final integration session described by the project protocol: it owns the
site's index, navigation and shared table data once the parallel tasks are done, merges the
parallel results into one authoritative URL, re-verifies the combined data line by line, and
publishes. It does not delete any session's work: duplicate briefs are replaced with redirect
stubs and remain in git history.

**Claim committed and pushed before any work began** (see commit message `claim(fi-01)`).


### Log — session `arena/5d4c76bb-korea8` (final integration)

**Scope worked:** root `*.html`, `style.css`, `site-data/**`, `scripts/build_canonical_site.py`,
`scripts/verify_canonical_site.py`, `archive/superseded-2026-11-07/**`, the redirect stubs,
`REPO_REVIEW_2026-11-07.md`, this board. No other session's research artefacts (GEMS, `vendor/`,
`registry/`, `src/`) were modified.

**What was done**

1. **Consolidation.** The four parallel briefs and the `docs/bathtub-*` pages published the same
   project in different words with different data. Each route is now one redirect stub to the
   canonical root dashboard; nothing was deleted from git history. The root dashboard is the
   single authoritative page, with nine category subpages.
2. **Re-verification (new work, not a copy of earlier sessions).** All twelve provider licences
   were re-retrieved from the official CSLB licence-detail page on 2026-11-07 and each page's own
   "data current as of" time is published per row. Code, fee, licensing and tenant-entry rows were
   re-read at source: SF.gov permit page, SF DBI Table 1A-C **July 2026** PDF, CSLB B and C-36
   classification pages, BPC §7048, BPC §7057.5, Civ. Code §1954, and the Watco 500/501/600-TL
   instruction sheet.
3. **New finding adopted into the dossier:** CSLB #749536 (Save - On - Interior) holds
   **B + C-36** at the *same street address and business phone* as #757796 (Bay Area Plumbing).
   Published as flag F-13 with the explicit caveat that the CSLB record does not state who
   controls each licence.
4. **Amount discipline.** Earlier routes published the three owner-supplied quote amounts. They
   are now blank in every published HTML and JSON file and flagged (F-02); `grep` over the served
   tree finds no occurrence of the three values.
5. **Dead links fixed.** Two sf.gov URLs cited by earlier briefs now return 404; the site uses the
   live pages, and the dead URLs are recorded as S-35/S-36 (flag F-11).
6. **Fee correction.** The permit fee is published as **$290** from the July 2026 DBI table,
   superseding the $276 figure from the September 2025 table.
7. **Build discipline.** `scripts/build_canonical_site.py` writes all ten pages from `site-data/`
   and refuses to publish a row with neither a source link nor an explicit owner/unverified
   marker. `scripts/verify_canonical_site.py` re-checks the generated HTML independently:
   **15/15 checks pass**.
8. **Archived, not deleted:** `build_project_site.py`, `build_bathtub_site.py`,
   `test_bathtub_site.py` and `bathtub-overflow/scripts/` moved to
   `archive/superseded-2026-11-07/` so a stray run cannot overwrite the canonical site.

**Sources used** (all retrieved 2026-11-07): 12 × `cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=…`;
`cslb.ca.gov` B and C-36 classification pages; `sf.gov/apply-plumbing-and-mechanical-permit`;
`sf.gov/resource--2023--plumbing-inspection-division`;
`sf.gov/documents/44100/Table_1A-C_-_Plumbing_Mechanical_2026.pdf`;
`leginfo.legislature.ca.gov` BPC §7048, BPC §7057.5, CIV §1954;
`watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf`.
Blocked/unretrievable: `aa.iapmo.org` (members-only), Yelp (HTTP 403), two dead sf.gov URLs.

**Verification performed:** automated — row-level source check (133 rendered data rows),
provider-row CSLB check, row-count parity against the data files, internal-link resolution,
self-contained-asset check, HTML tag balance, forbidden-amount sweep, and a reader-facing
phrase sweep for internal/private material. Results: `site-data/build-report.json` and
`site-data/verification.json`, both PASS.

**Irregularities flagged (all published on the site's Flagged for review page):**
F-01 repo also hosts an unrelated archived project · F-02 quote amounts unverified, blanked ·
F-03 quote scopes not comparable · F-04 review platforms block retrieval · F-05 licence status is
point-in-time · F-06 no C-9 drywall licence in the set · F-07 SF Plumbing Code §104.2 and CPC
§402.10 not verifiable from a free official source · F-08 Fast Response CSLB/website address
mismatch · F-09 no evidence any listed firm has done this exact repair · F-10 photos pending ·
F-11 two dead sf.gov URLs in earlier drafts · F-12 Advanced Plumbing future-suspension status ·
F-13 Save-On-Interior shared address/phone · F-14 "5+ plumbers" is an owner report ·
F-15 permit requirement for this job not confirmed in writing · F-16 no official dust-containment
rule · F-17 CSLB entry page in maintenance during retrieval · F-18 Save-On-Interior 2015–2016
CLSB miscellaneous entries · F-19 third-party price benchmarks unverified and not published ·
F-20 duplicate briefs retired.

**Deployment note.** GitHub Pages was in a failed state at the start of this session: the
`build` job for `e622cdd` succeeded in 8 s while the `deploy` job timed out after 10 m 7 s
(<https://github.com/karagemop466-tech/Korea8/actions/runs/42237367404>). Content causes were
ruled out (`.nojekyll` present, no symlinks, 242 files / 20 MB). The site was rebuilt, verified,
and deployed once after that incident aged out; the deploy result is recorded below.

### Merge-conflict record — session `arena/5d4c76bb-korea8` (2026-11-07)

While this session was working, `origin/main` advanced by PRs #27, #30 and #32 from session
`arena/0e2dfee2-korea8`, which was running its own integration pass over the same files. The rebase
stopped with a conflict on `COORDINATION.md` and modify/delete conflicts on 61 rendered pages.
Nothing from either session was discarded. How each class was resolved:

| Conflicted paths | Resolution |
|---|---|
| `COORDINATION.md` | Both records kept: `arena/0e2dfee2-korea8`'s sections (already on `main`) plus this session's claim and log, appended. |
| Retired briefs (`bathtub/`, `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, `docs/bathtub-*`, `docs/bathtub-overflow/`) | Took `main`'s version: a per-page redirect stub for **every** old URL, which preserves more links than this session's single-stub-per-directory approach. |
| Root canonical pages, `style.css`, `site-data/*`, `scripts/build_canonical_site.py`, `scripts/verify_canonical_site.py`, `verification.html` | Took this session's version: it is regenerated from `site-data/`, publishes no unverified amount, and passes the 15-check verifier. `main`'s pages were overwritten by the same generator inputs. |
| `project/*.json`, `project/README.md`, `project/integration-review.md`, `overflow-trip-lever/**` | Took `main`'s version unchanged in substance. Amount fields in the JSON were blanked (owner policy) and the same `_amounts_policy` note added; `project/README.md` got a supersession note. |
| `scripts/build_project_site.py` (modified on `main`, archived here) | Archived at `archive/superseded-2026-11-07/`, with `main`'s latest revision saved alongside as `build_project_site.session-0e2dfee2.py`. `main`'s `build_redirects.py` and `verify_project_site.py` left in `scripts/` untouched. |
| New provider rows found by the other session | Not taken on trust: `#392967 Ayoob & Peery` was re-read independently on CSLB (current and active, B/C-4/C-16/C-36/C-20, expires 2028-09-30) and added as P-13. The set is now 13 licences, five holding B + C-36. |

After resolution: 0 broken internal links across all repository HTML, 15/15 verifier checks PASS,
no occurrence of an unverified quote amount anywhere in the served tree.

---

## Session `arena/f4bb970c-korea8` — current requirements-to-delivery integration

**Claimed:** 2026-11-07. The platform fixes all work to branch `arena/f4bb970c-korea8`; no other branch will be created or pushed. This session takes over the stale root integration task T6 and the outstanding integration portions of the merged briefs under the board's 60-minute/no-commit takeover rule. The last relevant remote activity was 2026-11-06. Earlier claims and historical logs are preserved, not overwritten. Root ownership is now the final-integration scope below; historical research claims remain credited to their original sessions.

| ID | Task | Status | Owning session | Files in scope |
|---|---|---|---|---|
| F4-T1 | Root integration takeover, stale claim handoff, coordination | done | `arena/f4bb970c-korea8` | `COORDINATION.md` |
| F4-T2 | Independent official-source recheck, current provider/service research, full requirements and executive summary | in progress | `arena/f4bb970c-korea8` | `overflow-integration/**` |
| F4-T3 | Repository audit, consolidation and canonical root rebuild after released handoff | in progress | `arena/f4bb970c-korea8` | root bathtub HTML/CSS, `site-data/**`, `scripts/build_canonical_site.py`, `scripts/verify_canonical_site.py`, `overflow-integration/**`, bathtub redirect stubs, `COORDINATION.md` |
| F4-T4 | Final line-by-line audit, build, tests, browser checks, PR, merge and Pages verification | done | `arena/f4bb970c-korea8` | F4-T3 scope, `.github/workflows/overflow-pages.yml`, `COORDINATION.md` |

**Boundary:** preserve all unrelated GEMS source, scientific evidence, datasets, workflow and archive content. Existing open PRs are inventoried; do not discard or overwrite other-session work. Shared index/data/navigation edits are reserved for this integration after research tasks are complete. Research will use official authority/company sources for factual table cells; owner statements and review-platform observations will be separately labeled. No outreach, contract, appointment or provider acceptance will be claimed without a response. Public content will use neutral repair language.

**Initial observations:** Pages API reports `errored` for current main `e622cdd2ce83ebaf85996c98695a42328a028750`; open bathtub PRs #12, #17, #21, #22 and #24 require review before integration. Existing root counters and classifications disagree with their own records; matching CSLB address/phone has not established common ownership; supplied quote amounts and scopes require distinct provenance. These are review items, not verified contractor performance findings.

**Claim push:** initial branch did not yet exist remotely, so the prescribed pull reported a missing remote ref; the first push created the pinned branch and published the claim before research or site edits.

### Concurrency adjustment — 2026-11-07 20:30 UTC

`origin/main` advanced through PRs #27–#34 while this session was researching, and active session `10be5bc4` now has PR #33 claiming the same root/project scope. The earlier stale-claim premise is superseded for those files. This session preserves and merges `main`, keeps its independently transcribed research in `overflow-integration/**`, and will not edit root HTML/CSS, `project/**`, `site-data/**`, shared scripts, or other sessions' trees while those claims are active. The merge conflict in this board is resolved by retaining both histories.

**Requests to active root owners (`10be5bc4`, and any successor):**
- Please finish/merge PR #33 and record the actual Pages result; do not treat an old successful build or a lagging status as proof of the current commit.
- Preserve owner-supplied quote amounts as clearly labeled owner reports while leaving independently verified amounts blank; suppressing the supplied amounts prevents the requested comparison. Do not infer scope equivalence.
- Recheck the statement that B + C-36 automatically authorizes self-performing drywall: official C-9 and BPC §7057 sources require an appropriate contract/classification structure; ask for the named restoration party.
- SF Plumbing Code §104.2 was directly retrieved at <https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830>, chunk 14: leak/unstopping/faucet exemptions apply only when the stated no-cutting/no-removal conditions hold. This resolves the earlier "not retrievable" flag for that subsection; CPC access-panel dimensions remain unverified.
- This session has independently re-read 23 CSLB records, including Bernal Hill Drywall #995163 (B + C-9), and has adjacent Heise's ceiling-access case evidence plus review-search limitations in its own scoped data. Please consider these after the active root work is merged; no shared file has been edited here.

No provider has been contacted or booked by this session. Public content remains neutral repair-scope language.

### Final-integration handoff evidence — 2026-11-07 20:32 UTC

PR #33 (`10be5bc4`) was closed **without merging** at 20:31:02Z and its remote branch was deleted; the other stale bathtub PRs are also closed. `origin/main` remains `09d76c1` (PR #34). The unmerged PR #33 commit is preserved by SHA `a0e5376d36dab007999bed2eb6517d6d45d28f31` and was fetched for review; its 22-license audit is consistent with this session's independent 23-license transcription except for the additional Bernal Hill C-9 record and unresolved Portola identity. No active remote bathtub PR/branch remains except this session.

F4 therefore resumes the final-integration scope on the pinned branch, using `main` as the preservation baseline. Root/shared edits will be made only after the scoped research data and audit are complete. Prior histories, redirect stubs, archives and unrelated GEMS content remain preserved. The closed PR's unmerged commit remains reviewable at <https://github.com/karagemop466-tech/Korea8/commit/a0e5376d36dab007999bed2eb6517d6d45d28f31>; it is not silently discarded or merged over the newer canonical baseline.

### F4 work log — 2026-11-07 (canonical rebuild)

**Tasks:** F4-T2 done; F4-T3 done; F4-T4 in progress (PR/merge/live check remaining).

**Scope worked:** `overflow-integration/**`, root canonical HTML/CSS, `OVERFLOW_EXECUTIVE_SUMMARY.md`,
`scripts/build_overflow_site.py`, `scripts/verify_overflow_site.py`, compatibility wrappers
`scripts/build_canonical_site.py` / `scripts/verify_canonical_site.py`, `tests/test_overflow_site.py`,
`.github/workflows/overflow-pages.yml`, `site-data/README.md` and current reports, README top note,
and archived copies of the prior canonical generator/verifier. Redirect stubs, archives and unrelated
GEMS files were not deleted.

**Sources used:** 23 directly retrieved CSLB license-detail records; 10 company domains; three Heise’s
tub-overflow case studies; SF.gov plumbing/remodel/PermitSF/DBI pages; SF Plumbing Code §104.0 chunk 14;
July 2026 DBI Table 1A-C; BPC §§7048/7057/7057.5; Civil Code §1954; CSLB B/B-2/C-9/C-36 and contract
guidance; EPA RRP/asbestos; Watco 500/501/600TL instructions; Yelp search-index excerpts with blocked
business pages; GitHub repository/PR/Pages records. Full register: `overflow-integration/data/sources.json`.

**Verification performed:** `python scripts/build_overflow_site.py`; `python scripts/verify_overflow_site.py`
→ 22/22 checks PASS, 236 canonical table rows source-checked, 203 tracked-HTML internal links checked;
`python -m unittest discover -s tests -p 'test_overflow*.py'` → 10 tests OK. Reports:
`overflow-integration/build-report.json`, `overflow-integration/verification-report.json`.

**Irregularities flagged:** 36 rows in `overflow-integration/data/flags.json`, published on
`flagged-for-review.html`. Key corrections: owner-reported quote amounts restored with verified amounts
blank; B + C-36 drywall self-performance wording corrected; SFPC §104.2 retrieved; SF Building Group B-only;
HARP B-2 limits; Portola blank; suspended Kenneth Asire excluded from priority leads; Yelp ratings blank;
Heise’s adjacent case evidence labeled self-published; Pages specific-commit verification required.

**Publication:** PR #36 — <https://github.com/karagemop466-tech/Korea8/pull/36>. Merge and live check pending. The workflow publishes a checked static artifact;
legacy Pages status is not treated as proof of the current commit.


### F4 deploy record — PR #36 merged and live

| Item | Result |
|---|---|
| PR | <https://github.com/karagemop466-tech/Korea8/pull/36> |
| Merge | 2026-11-07T20:43:01Z, merge commit `f44f24a3ae1cb2d5ff1b48490d6fc6377dfd213d` |
| Workflow | <https://github.com/karagemop466-tech/Korea8/actions/runs/42412383676> — build and deploy success |
| Pages API | latest build for `f44f24a` reports `built`, no error |
| Live content | cache-busted fetches of `index.html`, `providers.html`, `estimates.html` and `flagged-for-review.html` returned the new canonical content (23 CSLB records, owner-reported amounts with blank verified amounts, 36 flags). The bare root URL initially returned a cached older page; CDN cache was noted rather than treated as a deploy failure. |
| Local checks | 22/22 verifier checks, 10 unit tests, pytest 10 passed, local HTTP 200 for canonical pages/CSS/GEMS docs/redirect stub |

F4-T2, F4-T3 and F4-T4 are done. Flagged/unverified items remain published and non-blocking. No provider was contacted or booked.
---

## Session `arena/d120270b-korea8` — independent line-by-line QA of the canonical site + final integration record

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| `qa-01` | Claim board before any other edit | done | `arena/d120270b-korea8` | `COORDINATION.md` | this claim, committed and pushed before any other work |
| `qa-02` | Independent line-by-line QA of the canonical site: every table row carries a source link, blank-vs-unverified discipline, internal links/redirects, privacy sweep, spot re-verification of licence rows against official CSLB records | **done** | `arena/d120270b-korea8` | new files under `audit/` only (report), plus `COORDINATION.md` for the record | no edits to root `*.html`, `project/`, `scripts/` — those belong to `arena/0e2dfee2-korea8` / `arena/a6db7ac6-korea8`; any fix found there is logged as a cross-session request |
| `qa-03` | Live-deploy confirmation + integration record (PR → `main`, merge, Pages status, PR link) | **done** | `arena/d120270b-korea8` | `COORDINATION.md` | only after `qa-02` completes |

**Scope rules for this session:** edits are limited to `COORDINATION.md` and new files under `audit/`.
No other session's files are modified; required changes elsewhere are logged under cross-session requests.
No private/internal brief content is recorded in any file or commit message.

### `qa-02` — completed record (session `arena/d120270b-korea8`, 2026-11-07)

**Report:** `audit/REPORT_2026-11-07_d120270b.md` · **Machine-readable:** `audit/independent_audit_report.json`
· **Audit script (independent parser, does not import the site's verifiers):** `audit/independent_audit.py`

- **Structural audit (own parser):** 10 pages, **236 table rows — 232 with an official/primary source
  link, 4 explicit blank/unverified markers, 0 offenders**; 143 internal links, 0 broken; amount
  cells all carry owner-reported/unverified labels; privacy sweep 0 hits after the fix below.
- **Cross-check with the site's own stack:** `verify_overflow_site.py` 22/22 PASS ·
  `verify_canonical_site.py` 22/22 PASS · `test_overflow*.py` 10/10 OK · CI `overflow-pages` run
  42412383676 success · legacy Pages build for `f44f24a` built (27 s).
- **Official sources re-read directly on 2026-11-07 (independent of the producing sessions):**
  CSLB licence-detail pages [#977638](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638),
  [#757796](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796),
  [#1024971](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971)
  (incl. the official "POTRAL" spelling), [#1027286](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1027286)
  (bond suspension confirmed); [BPC §7057](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057)
  (two-trade prime-contract rule, verbatim); [sf.gov plumbing-permit page](https://www.sf.gov/apply-plumbing-and-mechanical-permit)
  (permit trigger, §104.2 exemptions, Express Permits, help-desk number); [SF DBI Table 1A-C fee
  schedule, July 2026 (PDF)](https://www.sf.gov/documents/44100/Table_1A-C_-_Plumbing_Mechanical_2026.pdf)
  — all five published fee amounts ($290 / $320 / $519 / $555 / $259) match the PDF exactly.
- **Live site** fetched cache-busted: counts identical to the audited revision (23 CSLB records,
  6 B+C-36 leads, 42 requirements, 73 sources, 36 flags); nav consistent on all 10 pages.
- **Privacy fix (takeover, logged here):** `bathtub/data/flags.json` and `data/bathtub/flags.json`
  still stated the internal no-permit instruction after the PR #36 scrub, and both files'
  `requirements.json` carried meta-copy about a private scheduling constraint. Neutralised in
  commit `27348da` (4 lines, 4 files); owning session `arena/b10e8d0e-korea8` claim is >60 min
  stale, so the protocol takeover applies. Re-swept: 0 hits.

**Irregularities added by this session (full detail in the audit report, §7):** quote-amount
presentation remains an owner decision (policy review PR #18 asked for blank; merged PR #36
publishes labelled owner-reported amounts — every occurrence verified labelled, F-02); stale
`scripts/verify_project_site.py` fails against current pages but is not run by CI; open conflicting
PR #35 would revert PR #36 if merged; PR #7 unrelated; `run_card.json`/`RUN_CARD.json` case
collision; build-report timestamp churn; review-platform 403 block (F-14); no provider contacted
(F-35); racing final-integration sessions 20:22–20:43 UTC all preserved in history.
### `qa-03` — PR, merge and deploy record (session `arena/d120270b-korea8`, 2026-11-07)

| Item | Value |
|---|---|
| Integration PR | **#40** — https://github.com/karagemop466-tech/Korea8/pull/40 (`arena/d120270b-korea8` → `main`) |
| Merge | **MERGED** 2026-11-07, merge commit `d0d4d2e` (merge commit `d0d4d2e`) |
| Legacy Pages build for `d0d4d2e` | **built** (2026-11-07T21:00:58Z) |
| CI workflow `Publish overflow dashboard` for `d0d4d2e` | run 42413797038 — **success** (26 s; build + `verify_overflow_site.py` + unit tests + Pages artifact) |
| Live privacy re-check | `https://karagemop466-tech.github.io/Korea8/bathtub/data/flags.json` re-fetched after deploy: F-15 now states only DBI's published position — the internal instruction is **no longer served** |
| Live content parity | root dashboard counts match the audited revision (23 CSLB records, 6 B+C-36 leads, 42 requirements, 73 sources, 36 flags) |
| Full audit | `audit/REPORT_2026-11-07_d120270b.md` (236 rows, 0 offenders; 7 official sources re-read; irregularities I-1…I-10) |

**Open items left for the owner (do not block; all recorded above and in the audit report):**
quote-amount presentation (I-2, policy review PR #18 vs merged PR #36, site flag F-02);
stale `scripts/verify_project_site.py` (I-3); conflicting open PRs **#35**, **#39** and
**#38** (its `Publish verified bathtub overflow repair dashboard` check is **FAILURE** —
another racing session's branch, not merged by this session), plus unrelated stale PR **#7**.
This session merged only its own verified PR #40 and did not touch other sessions' open PRs.

## Session `arena/9c487d70-korea8` — independent current-state audit

| Task | Status | Owner | File scope |
|---|---|---|---|
| Current canonical site, source and deployment audit; document actionable discrepancies | in progress | `arena/9c487d70-korea8` | `audit/REPORT_2026-11-08_9c487d70.md`, `COORDINATION.md` |

This session will not modify files claimed by other sessions. Findings requiring canonical integration will be logged here.

### Audit record — 2026-11-08

Task done: `audit/REPORT_2026-11-08_9c487d70.md` documents structural checks (22/22; 10 unit tests) and selective independent rechecks of three CSLB records, the Heise's case and SF.gov. It does not assert every external fact was independently rechecked. Existing live site and Pages run for `854b0b1` confirmed. Four rows were accepted by the independent parser as blank/unverified without recognized source links; request to canonical integration: review against the strict official-link-per-row requirement and flag or fix as appropriate. Heise's project page contains case content alongside an embedded 404 message; request to flag and monitor the source. No providers contacted. Initial remote session branch did not exist, so initial pull could not succeed; the claim was pushed as the new remote branch immediately thereafter.

---

## Session `arena/b0d7ecf7-korea8` — 2026-11-08 fresh re-verification + ranked decision analysis

**Claim time:** 2026-11-08 (committed and pushed before any other edit, per protocol.)
**Platform-pinned branch:** `arena/b0d7ecf7-korea8` (the protocol's `session-<id>/<task>` name cannot be created: the
platform pins every session to one branch. This is recorded, not silently ignored.)

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| `k8-01` | Claim this board before any other edit | done | `arena/b0d7ecf7-korea8` | `COORDINATION.md` |
| `k8-02` | Independent 2026-11-08 re-verification: all 23 CSLB records re-read on cslb.ca.gov, key official rule sources re-read, stored data corrected where the official record differs | done | `arena/b0d7ecf7-korea8` | `overflow-integration/data/*.json`, `audit/REPORT_2026-11-08_b0d7ecf7.md` |
| `k8-03` | Ranked decision analysis (owner-requested best-choice ranking with reasoning, cost basis, phone and official links) as a new category page | done | `arena/b0d7ecf7-korea8` | `overflow-integration/data/ranking.json`, `overflow-integration/data/providers.json`, `scripts/build_overflow_site.py`, generated root `*.html`, `style.css` |
| `k8-04` | Rebuild, run verifier and unit tests, internal link check, cache-busted live check | done | `arena/b0d7ecf7-korea8` | `overflow-integration/build-report.json`, `overflow-integration/verification-report.json`, `scripts/verify_overflow_site.py` (checks only, no new data) |
| `k8-05` | PR → `main`, merge, confirm Pages deploy for the merge commit, record PR link and result here | done | `arena/b0d7ecf7-korea8` | `COORDINATION.md`, `overflow-integration/data/deployment.json` |

**Scope rules.** This session edits only the canonical bathtub tree (`overflow-integration/**`, the root dashboard pages
it generates, and `COORDINATION.md`). It does **not** touch the parallel brief directories
(`bathtub/`, `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, `project/`, `docs/`) or the DOE GEMS research
artefacts; any needed change there is logged here as a cross-session request instead of being edited.

**No-open-PR rule.** PRs **#35**, **#38** and **#39** remain open from earlier sessions. This session will not merge or
close another session's PR; that remains an item for the owner (see the Flagged for Review page).

### `k8-02` — completed record (session `arena/b0d7ecf7-korea8`, 2026-11-08)

**Report:** `audit/REPORT_2026-11-08_b0d7ecf7.md`

- **All 23 CSLB licence detail pages re-read directly** on 2026-11-08 (CSLB banner timestamps 11/8/2026
  2:57:46 PM – 2:58:32 PM, timezone unstated). **23/23 stored licensure fields matched exactly** — legal
  name, classifications, status, expiry, registered city, phone and workers-compensation entry. No
  licensure correction was needed; per-row timestamps were refreshed and `as_of` moved to 2026-11-08.
- **New official detail:** D G Construction #297604 has a complaint-disclosure link; the disclosure lists
  citation **2 2022 002099 (03/23/2023, "for disclosure only per B&P 7124.6")** and does not publish the
  conduct. Recorded as a citation, not as a finding on merit.
- **Rule sources re-read:** SF.gov plumbing/mechanical permit page (permit trigger, §104.2 link, eligible
  licence classes, inspection before covering pipes, help desk 628-652-4900), BPC §7057 verbatim, Civil
  Code §1954 verbatim, CSLB C-9 classification, Heise's Ingleside case (still live, still carries its 404
  template block). **Not** re-read today, therefore not claimed as verified today: full §104.2 text, the
  DBI fee PDF, the Watco PDF, the EPA pages — those rows keep their 2026-11-07 dates.
- **Yelp re-tested:** HTTP 403 again on 2026-11-08. Ratings, counts and review text stay blank.
- **Privacy:** `git ls-files` sweep for the internal-instruction phrasings finds no disclosure of the
  instruction or its reason anywhere in tracked files. Matches are verifier banned-pattern lists, a
  generic "no structure may be altered without a permit" sentence, and a README line stating that
  nothing confidential is published. No wording added this session refers to it.

### `k8-03` — completed record (ranked decision analysis)

The owner asked for contractors to be **ranked best choice to hire**, with reasoning and costs explained
per rank and an official verified link plus phone number for each. The site previously carried only an
"editorial inquiry order" that explicitly disclaimed ranking, so this session added the missing
deliverable rather than restating the disclaimers.

| Item | Value |
|---|---|
| New data | `overflow-integration/data/ranking.json` — 10 ranked candidates, 1 restoration partner, 13 identities assessed and held back |
| New page | `decision-analysis.html`, in the primary navigation of all 11 canonical pages |
| Criteria | C1 combined plumbing + building capability (0.30) · C2 evidence of this specific scope (0.20) · C3 licence standing/tenure (0.20) · C4 occupied-unit experience (0.15) · C5 price evidence (0.15) |
| Resulting order | Ace 3.85 · Heise's 3.45 · Rapid Flow 3.15 · Ayoob & Peery 3.15 · We Do 2.95 · Expert 2.90 · Save-On-Interior 2.60 · Bay Area 2.55 · Discount 2.30 · Fast Response 2.20; Bernal Hill is the restoration partner |
| Cost handling | Only the three owner-reported amounts appear ($614 Expert, $550 Bay Area, $135 Fast Response), each labelled owner-reported with `amount_verified` blank. Every other scope shows a blank and "no quote on file" — no price was inferred |
| Single source of truth | Dashboard "who to call first" panel, executive summary, providers shortlist and estimates page all derive their order from `ranking.json` |

### `k8-04` — completed record

| Check | Result |
|---|---|
| `python scripts/build_overflow_site.py` | 11 pages built; 24 provider identities, 23 CSLB records, 42 requirements, 73 sources, 40 flags, 10 ranked |
| `python scripts/verify_overflow_site.py` | **22/22 PASS** — 273 canonical table rows each carry an external source link, 220 tracked-HTML internal links resolve, no broken anchors |
| `python -m unittest discover -s tests -p 'test_overflow*.py'` | 10 tests OK |
| Blank-vs-unverified discipline | every `amount_verified`, rating and review count is null; Portola's fields remain blank |

### Irregularities recorded by this session

1. Ranking is editorial decision support (F-37); no provider was contacted and no reference or verified
   review exists. The weights are published so the owner can re-order.
2. No provider in the register holds both C-36 (plumbing) and C-9 (drywall); the all-in-one requirement
   needs a B + C-36 contract that names the plastering party, or a plumbing lead plus Bernal Hill.
3. Only three owner-reported amounts exist and none prices the ceiling opening.
4. D G Construction's disclosed citation (above) keeps it out of the hiring order until the owner reviews.
5. Advanced Plumbing (future-suspension warning), Kenneth Asire (suspended) and Portola (unidentified)
   cannot be recommended as they stand.
6. Yelp/Google review evidence is still unobtainable automatically (HTTP 403).
7. PRs **#35, #38, #39** from earlier sessions remain open and conflict with merged work (F-39). This
   session did not merge or close another session's PR.

### `k8-05` — PR, merge and deploy record (session `arena/b0d7ecf7-korea8`, 2026-11-08)

| Item | Value |
|---|---|
| Integration PR | **#45** — <https://github.com/karagemop466-tech/Korea8/pull/45> (`arena/b0d7ecf7-korea8` → `main`) |
| Merge | **MERGED** 2026-11-08T23:03:50Z, merge commit `e7c129a43d0585bd92f37052e0e3fc7ca90bb892` |
| CI workflow `Publish overflow dashboard` | run 42533302983 — **success** (build + `verify_overflow_site.py` 22/22 + unit tests + Pages artifact) |
| Legacy Pages build for the merge commit | run 42533302823 — **success**; Pages API status `built` |
| Live content | cache-busted fetch of `decision-analysis.html` returned the new page (11 nav entries, ranked table, 2026-11-08); cache-busted `index.html` returned "reviewed 2026-11-08", the "Ranked hiring order" snapshot row and the new "Who to call first" panel. The **bare root URL still served the pre-merge cached page** at first check — CDN caching, recorded rather than treated as a deploy failure, matching the pattern logged by sessions `f4bb970c` and `d120270b`. |
| Local checks | build OK, `verify_overflow_site.py` 22/22 PASS (273 canonical table rows, 234 tracked-HTML internal links), `unittest` 10/10 OK |

Flagged and unverified items remain published on `flagged-for-review.html` and do not block the merge.
No provider was contacted, booked or paid.

---

## Session `arena/215f5c79-korea8` — final freshness review and integration (2026-11-08)

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| `215-01` | Claim board before other edits | done | `arena/215f5c79-korea8` | `COORDINATION.md` |
| `215-02` | Independently review canonical data/site, refresh priority-provider and review-platform evidence, correct only evidenced defects | done | `arena/215f5c79-korea8` | `overflow-integration/**`, `site-data/**`, root canonical HTML/CSS, `scripts/build_overflow_site.py`, `scripts/verify_overflow_site.py`, `tests/test_overflow_site.py`, `OVERFLOW_EXECUTIVE_SUMMARY.md`, `audit/2026-11-08-215f5c79/**` |
| `215-03` | Build, source/link/privacy verification, PR to main, merge, Pages deployment and final record | done | `arena/215f5c79-korea8` | `COORDINATION.md`, workflow/deployment configuration only if required |

All earlier overlapping implementation claims are more than 60 minutes old and their latest completed canonical handoff is PR #40/#42; this session takes over only the final integration scope and preserves their work. Arena fixes this session to `arena/215f5c79-korea8`; no additional worktree or task branch will be created. No provider will be contacted or booked. Owner-supplied estimates will remain labelled and distinct from verified current prices.

### `215-02` verification record — 2026-11-08

- **Fresh official sources:** directly retrieved CSLB #1115649, #829071, #1089561, #977638, #757796, #1024971 and #1027286 on 2026-11-08; all compared legal names, classifications, status, phone, expiry and workers-compensation summaries match the canonical rows. Kenneth Asire remains bond-suspended and excluded. Official Rapid Flow and Ace homepages still support their published service/classification statements. Heise’s Marina overflow assembly/gasket case remains adjacent self-published evidence, not exact-job proof.
- **Review platforms:** Yelp search results exposed changing snippets/ratings, but business pages were not directly verified; canonical numeric ratings/counts remain blank and no evidence-supported ranking change was made.
- **Independent report:** `audit/2026-11-08-215f5c79/REPORT.md` and `freshness-check.json`, linked from the public Verification page. Full field-level source URLs and CSLB timestamps are recorded there.
- **Build/tests:** `python scripts/build_overflow_site.py`; `python scripts/verify_overflow_site.py` → 22/22 PASS after PR #45/#47/#48 integration, 274 table rows source-covered, 271 tracked-HTML internal links with no broken targets; 10/10 unit tests PASS; independent audit 10 pages/245 rows/161 canonical internal links/0 problems; `git diff --check` PASS; neutral public-text sweep no hits.
- **Irregularities:** existing 40 flags remain published and non-blocking. No provider confirms exact-job acceptance, current availability, all-in-one ceiling restoration or current pricing. Owner estimates remain labelled owner-reported with verified amounts blank; Portola fields remain unresolved/blank. No ranking or provider value was changed without evidence.
- **Parallel handoff:** `origin/main` advanced with PR #43 during final integration. Rebase conflicted only in this shared board; both PR #43's audit and this session's records were retained without discarding either. PR #43's four parser exceptions were manually checked: §104.2, Ayoob & Peery, Bernal Hill and SF-CODE-104 all have direct primary-source links; the older parser hostname allowlist omitted their hosts. Heise's embedded 404 template was already disclosed in the source register and remains flagged as a limitation.

- **PR #45 combined handoff:** main advanced again with all 23 CSLB records freshly re-read and a 10-candidate ranked decision page. Its generator/data/pages were retained; only this audit link/log was reapplied. The combined build now has 11 pages, 274 source-linked rows and 40 published flags. Generator/report conflicts were resolved from the combined data and the complete checks rerun successfully.
- **Final clean integration:** main advanced through PR #47 and PR #48 while merge was attempted. This session reapplied only its new audit, Verification link and board record onto PR #48, retaining all parallel ranking/deployment/repository-review work. Final checks: 22/22 PASS, 274 source-linked rows, 235 tracked-HTML links, 10/10 tests, independent parser 245 rows/161 links/0 problems. All 40 flags remain published.

### `215-03` — PR, merge and live deployment record

| Item | Result |
|---|---|
| Integration PR | **#46** — https://github.com/karagemop466-tech/Korea8/pull/46 |
| Merge | **MERGED** 2026-11-08T23:08:28Z; merge commit `60844f346fb6129fce5eb6b3ac77e19c37d341d6` |
| Workflow | [Run 42533706759](https://github.com/karagemop466-tech/Korea8/actions/runs/42533706759) — build and deploy **success** for the exact merge commit |
| Legacy Pages build | [1352718355](https://api.github.com/repos/karagemop466-tech/Korea8/pages/builds/1352718355) — **built**, no error, commit `60844f3` |
| Live verification | Cache-busted `verification.html`, `decision-analysis.html`, `flagged-for-review.html` and the new audit returned the 11-page summary, ranked candidates, 40 flags and audit content/link |
| Final status | `215-01`, `215-02`, `215-03` **done**. All 40 irregularities/open items remain published and non-blocking. No provider contacted/booked. |

## Session `arena/3946905e-korea8` — fresh verification and final integration (2026-11-08)

| Task | Status | Owning session ID | Files touched |
|---|---|---|---|
| T3946905e-A: fresh official-source provider/review research and line-by-line repository audit | done | `arena/3946905e-korea8` | `audit/REPORT_2026-11-08_3946905e.md`, `audit/verification_3946905e/`, `COORDINATION.md` |
| T3946905e-B: canonical data correction, decision analysis and dashboard integration | done | `arena/3946905e-korea8` | `overflow-integration/data/`, `overflow-integration/OWNER_RECORD.md`, `overflow-integration/EXECUTIVE_SUMMARY.md`, `scripts/build_overflow_site.py`, `scripts/verify_overflow_site.py`, `tests/test_overflow*.py`, root canonical HTML/CSS and generated summaries/reports, `README.md`, `COORDINATION.md` |
| T3946905e-C: PR, merge, deploy and live verification | done | `arena/3946905e-korea8` | `COORDINATION.md`, canonical generated verification/deployment records |

**Claim boundaries:** No other session has an active bathtub task on current `main`; the most recent audit task is done. This session is the final integrator for the unresolved four-row source gap, source deterioration, decision-ranking and publication checks. No historical open PR is assumed merge-ready or authorized for takeover. DOE GEMS code/data and other sessions' scoped drafts are read-only. Any required cross-scope edit will be logged here, not made silently.

**Branch coordination exception:** Arena fixes this session to `arena/3946905e-korea8`; creating/switching to `session-<id>/<task>` branches is prohibited by the active workspace rules. All commits and the integration PR stay on this fixed branch. Coordination edits are append-only and rebase-checked before each push. Historical claims over 60 minutes old are not automatically taken over. No outreach, booking or private circumstances will be published.


### T3946905e-B merge-resolution record — 2026-11-08

`origin/main` advanced through PRs #45/#46/#47/#48/#50 while this session was verifying sources. The merge conflicted in the shared board, canonical generator/verifier/tests, generated pages/reports, flags and sources. Resolution preserved the merged editorial weighted ranking (`ranking.json` / `decision-analysis.html`) and all prior coordination/audit records, then reapplied this session’s fresh CSLB/company/statute rechecks, Atlas conditional lead, strict official-primary row coverage, corrected AmLegal chunk metadata, phone-discrepancy flags and final-verification gates. This session’s six new flags were renumbered F-41–F-46 to avoid overwriting main’s F-37–F-40. The superseded `decision.json` was removed after its per-provider gates were folded into `ranking.json`.

Combined local checks before merge commit: build OK; `verify_overflow_site.py` 27/27 PASS (300 source-covered rows, 574 tracked-HTML links); 11/11 unit tests; independent audit 300/300 rows recognized, 0 problems. No provider contacted/booked; owner estimates remain owner-reported with verified amounts blank.


### T3946905e-C — PR, merge and live deployment record

| Item | Result |
|---|---|
| Integration PR | **#52** — https://github.com/karagemop466-tech/Korea8/pull/52 |
| Merge | **MERGED** 2026-11-08T23:23:45Z; merge commit `3c37250122de2bec21a8d87a51ae64ebd7b9760b` |
| Workflow | [Run 42534974124](https://github.com/karagemop466-tech/Korea8/actions/runs/42534974124) — build, verify, unit tests and Pages deploy **success** for the exact merge commit |
| Legacy Pages build | **built**, no error, commit `3c37250122de2bec21a8d87a51ae64ebd7b9760b` |
| Live verification | Cache-busted `index.html`, `decision-analysis.html` and `flagged-for-review.html` returned the merged dashboard: 24 CSLB records, 25 identities, 85 sources, 46 flags, final-verification note and Atlas conditional hold |
| Final checks | 27/27 canonical verifier checks; 300/300 rows official-primary source-covered; 11/11 unit tests; independent audit 0 problems |
| Status | T3946905e-A/B/C **done**. Open/unverified items remain published and non-blocking. No provider contacted/booked. |
## Session `arena/0404117b-korea8` — fresh independent verification and final integration (2026-11-08)

The platform fixes this session to `arena/0404117b-korea8`; no alternate session branch will be created. The preceding research/integration tasks have completion records through PR #40 and the independent QA/PR #42 record. Historical `in progress` labels above are superseded by their later completion logs; the latest root work is merged and more than 60 minutes old. This session takes the released final-integration role, preserving earlier claims, research, archives and unrelated GEMS artifacts. Only this session's pinned branch is used.

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| K8-N1 | Claim released integration scope; review current board, repository and GitHub state | done | `arena/0404117b-korea8` | `COORDINATION.md`, `audit/0404117b/**` |
| K8-N2 | Fresh official-source verification of combined provider, review, requirement, cost and technical records | in progress | `arena/0404117b-korea8` | `overflow-integration/data/**`, `audit/0404117b/**` |
| K8-N3 | Refresh executive summary and clean canonical dashboard; preserve historical/unrelated work | in progress | `arena/0404117b-korea8` | root bathtub HTML/CSS, `OVERFLOW_EXECUTIVE_SUMMARY.md`, `scripts/build_overflow_site.py`, `overflow-integration/**` |
| K8-N4 | Independent row/link/privacy checks, build, unit/browser tests and repository review | in progress | `arena/0404117b-korea8` | `scripts/verify_overflow_site.py`, `tests/test_overflow_site.py`, `.github/workflows/overflow-pages.yml`, `audit/0404117b/**`, `README.md` top project note only |
| K8-N5 | Final integration PR to main, merge, specific-commit Pages verification and completion record | in progress | `arena/0404117b-korea8` | `COORDINATION.md`, `overflow-integration/data/deployment.json` |

### 2026-11-08T23:11Z — active parallel-work handoff

Main advanced through PRs #47/#48/#46 while this session was researching; PR #46 is merged and its audit/generator/board changes will be preserved by rebase. PR #49 (`arena/55859fbc-korea8`, latest commit 23:08Z) is active and overlaps the canonical generator/data/verifier scope. This session claimed at 23:04Z, before that session's 23:08Z implementation commit, and will not overwrite its work. To avoid simultaneous writes, K8-N2/N3/N4 implementation is paused while this session completes an independent review in its non-overlapping `audit/0404117b/**` scope. The already-developed canonical changes are retained locally, not pushed over the active claim. K8-N5 remains pending release/merge of the active integration work; no other session's PR will be merged or closed. If the active claim becomes stale under the >60-minute rule, a logged handoff may resume this integration with both change sets preserved.

No shared files have been changed before this claim. Source observations will distinguish fresh retrieval, historical transcription, owner statements and analytical judgments. Public content will use neutral repair language. No contractor acceptance, booking or exact-job capability will be claimed without direct evidence.

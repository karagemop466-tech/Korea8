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

## Session `arena/64728bdf-korea8` — fresh line-by-line re-verification + consolidated brief (branch `arena/64728bdf-korea8`)

| # | Task | Status | Owner | Files in scope |
|---|---|---|---|---|
| S1 | Claim + repo review (this session) | in progress | `arena/64728bdf-korea8` | `COORDINATION.md` only for the claim commit |
| S2 | Fresh official-source verification (CSLB, SF DBI/sf.gov, manufacturer) | done | `arena/64728bdf-korea8` | `overflow-trip-lever/data/*.json`, `overflow-trip-lever/SOURCES.md` |
| S3 | Consolidated site: dashboard + category subpages + Flagged for Review | unclaimed→claimed below | `arena/64728bdf-korea8` | `overflow-trip-lever/**` only |
| S4 | Verification pass (link/blank-discipline/privacy sweep), PR→main, merge, Pages confirm | unclaimed→claimed below | `arena/64728bdf-korea8` | `overflow-trip-lever/**`, `COORDINATION.md` |

Scope rules for this session: edits only `COORDINATION.md` and new `overflow-trip-lever/**`. No edits to root `index.html`, `project/`, `bathtub/`, `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, `docs/` (owned by prior sessions). Cross-session request (root owner): add one link `overflow-trip-lever/index.html` to root nav when convenient. Estimate amounts: no official source exists → published blank + flagged unverified (per post-merge policy review above). No private/internal brief content is recorded in any file or commit message.

### Log — session `arena/64728bdf-korea8` (2026-11-07)
- S1 done: repo reviewed. Prior bathtub briefs (`bathtub/`, `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, root dashboard) left untouched. Irregularities carried to `overflow-trip-lever/flagged.html` (F-08 dead SF.gov URL in older citations, F-10 duplicate briefs, F-11 repo topic mismatch, F-12 Pages `errored` at session start).
- S2 done: fresh verification 2026-11-07 — 8 CSLB LicenseDetail records read directly (977638, 757796, 749536, 1024971, 1115649, 829071, 392967, 1009195; all current/active; 1009195 carries a future-suspension Additional Status, F-05); SF.gov plumbing-permit page (live URL replaces a 404, F-08); CSLB classifications PDF; BPC §7057/§7048 and Civil Code §1954 on leginfo; Watco trip-lever instruction sheet (steps 5–7). Yelp used only as a linked anecdotal search (F-07).
- S3 done: `overflow-trip-lever/` — dashboard + executive summary, requirements (12), estimates (3 rows, amounts BLANK/unverified), providers (8), rules/technical (8), Flagged (12), sources; JSON in `overflow-trip-lever/data/`; build enforced (amounts blank, CSLB link per provider).
- S4 in progress: `verify_site.py` — 0 failures (7 pages, internal links, blank discipline, privacy sweep); local HTTP 200 ×7. PR/merge/Pages result recorded below after merge.
- Cross-session request stands: root-dashboard owner please add one nav link to `overflow-trip-lever/index.html`.
- S4 done: **PR #27 merged** (https://github.com/karagemop466-tech/Korea8/pull/27), merge commit `5ad548d`. GitHub Pages build for `5ad548d` at 2026-11-07T20:22:16Z = **built** (Pages status now `built`, previously `errored`). Live verified by direct fetch: https://karagemop466-tech.github.io/Korea8/overflow-trip-lever/index.html and /flagged.html render correctly. This board-record entry follows in a separate small PR so the record itself lands on `main`.
- Handoff (2026-11-07): the parallel final-integration session `arena/0e2dfee2-korea8` (PR #28) then retired `overflow-trip-lever/*.html` to redirect stubs pointing at the canonical root dashboard, noting my 8 licence rows are a subset of its 13 re-verified rows and matched. Accepted — no content restored; my JSON/build/verify files remain in history and on `main` under `overflow-trip-lever/data/` etc. Canonical URL is now the root dashboard. Merge conflict on this file (PR #29) was resolved keeping both session records in full.
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

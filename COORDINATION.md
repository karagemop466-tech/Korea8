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
| `bt-07` | Integration: PR to `main`, merge, confirm Pages deploy | done | `0ad9ad61` | repo-root nav link (see requests below) | PR #15 merged 2026-11-06T13:41:49Z (merge commit `67fc8fb`); Pages deploy confirmed |

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
- `bt-07` — integration complete.
  - **PR:** https://github.com/karagemop466-tech/Korea8/pull/15 — "Bathtub overflow trip-lever: full requirements, vendor shortlist, code facts and live dashboard".
  - **Merge result:** merged into `main` at 2026-11-06T13:41:49Z, merge commit `67fc8fb` (verified present in `origin/main`).
  - **Conflict resolved:** `main` had advanced with other sessions' merges (PR #9 and its follow-ups) while this work was in
    progress; `origin/main` was merged into this branch and the add/add conflict on this board was resolved by keeping
    both sessions' records in full. No other session's content was altered.
  - **Pages deploy confirmed:** the live site is served at
    https://karagemop466-tech.github.io/Korea8/bathtub-overflow/ — landing page, all six category subpages, the
    "Flagged for Review" page and the published JSON data files were fetched and checked after the deploy.
  - **Deploy note for other sessions:** the first Pages deploy after this merge was *cancelled* (run `42227585006`)
    because further merges to `main` from other sessions started new deployments; the `build` job succeeded every time
    and only the `deploy` job was cancelled. The deployment completed successfully once the push queue settled
    (run `42228551260`, Pages status `built`). If a Pages status shows `errored` right after a burst of merges, check
    `gh run list` for a cancelled `pages-build-deployment` run and re-run the latest one rather than re-pushing content.

### Response to the post-merge policy review (`arena/ca2217a7-korea8`)

Applied to the `bathtub-overflow/` tree on 2026-11-06:

1. **Reader-facing meta-copy removed.** The landing page no longer has a section describing excluded or internal
   material; it now carries a neutral "Scope and limits of this dossier" section. FL-21 was rewritten to state what the
   published values are and how much weight to put on them, without describing anything that is not published. The
   README and the executive summary were reworded the same way. `scripts/verify_site.py` now fails the build if
   reader-facing meta-copy of that kind reappears (check `NO-META-COPY`).
2. **Estimate amounts re-framed, not removed.** The three owner-reported amounts ($614 / $550 / $135, 2026-08-30) are
   still published, because they are the owner's own reported figures and the brief supplied them, but they are no longer
   presented as price data: the column is now "Amount (owner-provided, unverified)", the table opens with a note that no
   provider document confirms them and that they are not a price range, and each row keeps its `USER-PROVIDED` label and
   the FL-19 flag. The only figure on the page carrying an official source is the DBI fee table. **Open item for the
   owner:** if the amounts should be blanked entirely, say so and this session will blank them in one pass.
3. **Canonical route.** The root dashboard (repository root) is the canonical landing page and links to the three
   dossiers. `bathtub-overflow/` stays live as the fully source-linked, machine-verified dossier (62 automated checks);
   this session did not retire or redirect it, because that decision belongs to the owner.

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
5. **Publishing discipline.** The published pages carry official public records only — CSLB licence pages, the DBI fee
   schedule, the published code and tenant-entry rules — plus the owner-supplied estimates, each labelled by
   verification status. Item FL-21 on the site's "Flagged for Review" page states the same rule for readers. Reader-facing
   meta-copy about excluded material is not published, per the post-merge policy review by `arena/ca2217a7-korea8`.

---

## Cross-session requests (do not edit files outside your scope)

1. **`0ad9ad61` → geothermal site session.** One root-level navigation link from the existing geothermal landing page
   (`index.html`) to the new bathtub-overflow section. The root `index.html` is owned by the geothermal site build
   (`scripts/build_site.py`) and was **not** edited by `0ad9ad61` to avoid clobbering another session's output. If the
   geothermal integration session regenerates `index.html`, please add:
   `<p><a href="bathtub-overflow/index.html">Bathtub overflow trip-lever project &rarr;</a></p>`
   near the existing "Prior session" block.
2. **Estimate amounts — one open question for the owner.** `arena/ca2217a7-korea8` asked that owner-supplied estimate
   amounts be left blank on every published route because no provider document substantiates them. This session has
   re-framed them as owner-reported, unverified figures (column rename, table note, `USER-PROVIDED` label, FL-19) rather
   than blanking them, because the brief supplied the three amounts as project inputs and they are the owner's own
   records rather than an inference. **If the owner prefers them fully blank, request it here and `0ad9ad61` will blank
   them in `bathtub-overflow/data/costs.json`, rebuild and re-verify.**
3. **Two trees now exist for the same brief** (`bathtub-overflow/` is live at
   https://karagemop466-tech.github.io/Korea8/bathtub-overflow/; `bathroom-overflow/` is live at
   https://karagemop466-tech.github.io/Korea8/bathroom-overflow/). `bathroom-overflow/**` (session `arena/ae482104-korea8`, merged in PR #9)
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

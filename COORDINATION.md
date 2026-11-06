# COORDINATION.md — shared task board

Repo: `karagemop466-tech/Korea8` · Pages source: `main` / `/` (root of repo is the site root)

This is the shared task board for parallel agent sessions. Each task lists status, owning
session ID, and the files it touches. **Claim a task by writing your session ID and file
scope here, then commit and push that claim immediately.** Never start a task another
session has claimed. Keep scopes non-overlapping. If a task requires changing a file owned
by another session, log the request here instead of editing it.

Status values: `unclaimed` · `in progress` · `done` · `needs review`

---

## Session IDs in use

| Session ID | Branch | Notes |
|---|---|---|
| `0ad9ad61` | `arena/0ad9ad61-korea8` (fixed by Arena) | Bathtub wastewater overflow trip-lever project (this session) |

> Note: the arena harness fixes this session's branch to `arena/0ad9ad61-korea8` and forbids
> creating/pushing other branches, so the `session-<id>/<task>` branch convention in the brief
> is not used here. Scopes are instead kept non-overlapping by directory, as recorded below.

---

## Task board

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| `bt-01` | Create shared task board | done | `0ad9ad61` | `COORDINATION.md` | this file |
| `bt-02` | Official-source research: SF permit/code rules, CA/CSLB licensing framework, UPC trip-lever/overflow requirements, SF rental-unit rules | done | `0ad9ad61` | `bathtub-overflow/data/*.json`, `bathtub-overflow/SOURCES.md` | every row must carry an official link |
| `bt-03` | Vendor shortlist research (SF plumbers + drywall/general contractors) with Yelp/review evidence and CSLB license numbers | done | `0ad9ad61` | `bathtub-overflow/data/vendors.json` | license fields blank if not confirmable on cslb.ca.gov |
| `bt-04` | Cost-estimator table (user-provided quotes + line-item build-up) | done | `0ad9ad61` | `bathtub-overflow/data/costs.json` | user quotes labelled USER-PROVIDED |
| `bt-05` | Site build: landing page + category subpages + Flagged for Review + JSON/MD data mirrors | done | `0ad9ad61` | `bathtub-overflow/*.html`, `bathtub-overflow/style.css`, `bathtub-overflow/scripts/build_site.py` | static HTML, no external CDN |
| `bt-06` | Verification pass: link check, blank-vs-unverified discipline, table/JSON consistency | done | `0ad9ad61` | `bathtub-overflow/scripts/verify_site.py`, `bathtub-overflow/evidence/**` | automated, no human inspection |
| `bt-07` | Integration: PR to `main`, merge, confirm Pages deploy | in progress | `0ad9ad61` | repo-root nav link (see below) | only after bt-06 passes |

### Cross-session requests (do not edit files outside your scope)

- `0ad9ad61` requests, from the final integration step, one root-level navigation link from the
  existing geothermal landing page (`index.html`) to the new bathtub-overflow section. The root
  `index.html` is owned by the geothermal site build (`scripts/build_site.py`); it was **not**
  edited by `0ad9ad61` to avoid clobbering another session's output. If the geothermal
  integration session regenerates `index.html`, it should add:
  `<p><a href="bathtub-overflow/index.html">Bathtub overflow trip-lever project &rarr;</a></p>`
  near the existing "Prior session" block.

---

## Irregularities flagged (rolling log)

1. **Repo/topic mismatch.** The repository content (`AGENTS.md`, `PROJECT_PROMPT.md`, `README.md`,
   `src/korea8/`, `vendor/gems57/`, registry rasters) is the *DOE GEMS Prize Challenge*
   geothermal fault-prediction project. The brief received by this session is a *bathtub
   wastewater overflow trip-lever* plumbing project in San Francisco. The two are unrelated.
   This session therefore added a **self-contained new project tree** (`bathtub-overflow/`)
   and did not modify any geothermal research artefact, evidence file, or the root site build
   script. The mismatch is recorded here and on the site's "Flagged for Review" page rather than
   silently reconciled.
2. **Root `index.html` is generated** by `scripts/build_site.py` (geothermal). This session did
   not edit it; see the cross-session request above.
3. **Third-party directory misattribution.** `contractorlicenseca.com` maps CSLB #297604 to "Cahill Contractors";
   the official CSLB record shows #297604 = D G Construction Co and Cahill Contractors Inc = #300647. Only the CSLB
   mapping is used in this project (FL-08).
4. **Review platforms block automated retrieval.** Yelp, BBB, HomeAdvisor and Angi return HTTP 403 here, so their
   ratings and review counts are dated search-index snapshots, never treated as verified (FL-07).
5. **Internal-use constraint handling.** The brief includes internal information that must never
   appear on the site, in email, or in any public record, together with a private reason.
   **Neither the internal information nor the reason is recorded anywhere in this repository, in
   the site's data files, in the page text, or in any commit message on this branch.** The
   published site states only the verifiable code facts: what the official DBI rule is, who to
   ask, what a permit would cost, and the trade-licensing and tenant-entry rules. The handling
   decision is recorded as item FL-21 on the site's "Flagged for Review" page, which states the
   handling rule without disclosing the content.

---

## Log of completed work

- `bt-01` — created `COORDINATION.md`, claimed scope `bathtub-overflow/**`.
- `bt-02` — research complete. 46 sources recorded in `data/sources.json` (24 official, 22 review-platform);
  18 code/permit/tenant-entry facts in `data/code_facts.json` (CF-01…CF-18, 13 OFFICIAL-VERIFIED, 5 UNVERIFIED);
  34 requirements in `data/requirements.json`. Official sources read directly: CSLB licence-detail and name-search
  pages, the CSLB classification PDF and C-9 scope page, CSLB consumer guidance, the archived DBI FAQ, the July 2026
  DBI plumbing/mechanical fee schedule, sf.gov code and fee pages, the IAPMO 2025 CPC contents, and Cal. Civ. Code
  § 1954.
- `bt-03` — 14 contractors in `data/vendors.json` (V01–V14), each with its official CSLB record read on 2026-11-06;
  13 licence numbers established, 1 suspended (excluded), 1 name with no CSLB record. Review figures are dated
  search-index snapshots only and are flagged (FL-07).
- `bt-04` — `data/costs.json`: 3 owner-provided estimates (2026-08-30, USER-PROVIDED), 5 official DBI fee rows,
  6 cost drivers.
- `bt-05` — site built to `bathtub-overflow/` (published at `/Korea8/bathtub-overflow/`): landing dashboard,
  6 category subpages, the "Flagged for Review" page (FL-01…FL-22) and the sources page. Data files are the published
  JSON; `SOURCES.md` is the human-readable source list. No external CDN, no client-side framework.
- `bt-06` — `scripts/verify_site.py` run: **61 checks, 0 failed** (`bathtub-overflow/evidence/verification.json`).
  Checks cover source-per-row, source-id parity, CSLB-official vendor links, flag-id existence, blank-vs-unverified
  discipline, rendered-vs-JSON row counts, internal link integrity, placeholder text, and a check that no internal
  project information appears in any published file.
- `bt-07` — integration in progress (PR to `main`, merge, Pages deploy check).
</content>

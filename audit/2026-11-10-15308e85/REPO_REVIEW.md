# Repository review — 10 November 2026

**Session:** `arena/15308e85-korea8`
**Scope:** the whole tracked tree, read one item at a time. This is a review record, not a
rebuild. Nothing outside this session's claimed scope was edited.

**What this session did *not* do.** It did not contact, call, email, quote, book or pay any
provider. It did not re-rank anybody. It did not change an owner-supplied amount, a licence
field, a review value or a source retrieval date. It did not delete a superseded tree.

---

## 1. How the review was run

| Step | Method | Where the receipt is |
|---|---|---|
| Enumerate the tree | `git ls-files`, 341 files before this session's work | this document |
| Read the shared board | Full `COORDINATION.md` read before any edit; claim pushed first | claim commit `0ec0913` |
| Re-read official licence records | 12 CSLB licence-detail pages retrieved live and compared field by field | `cslb-receipts.json` |
| Re-read the fee schedule | July 2026 DBI plumbing/mechanical fee PDF | `estimates-and-ranking-check.json` A-04 |
| Re-run the build and every gate | build, verifier, unit suite, wording guard, independent audit, staging | §6 |
| Check what the live origin serves | Independent fetch of the published URL plus six targeted path probes | §4 |
| Check the arithmetic the owner will act on | Ranking scores, weights, estimate spread | `estimates-and-ranking-check.json` |

**Network note.** In this sandbox `curl` has no outbound network at all (every attempt returns
connection code 000). The `fetch_page` tool does reach the open web, so every live retrieval
recorded here was made with that tool. This matters for anyone re-running the audit: an
in-sandbox `curl` failure is not evidence that a site is down.

---

## 2. Line-by-line findings

Each row states what was checked, what was found, and whether it is a defect, a limitation or
nothing to fix. Severity is this session's own judgement.

| # | Area | What was checked | What was found | Severity | Action taken |
|---|---|---|---|---|---|
| R-01 | Brief vs. repository | The owner brief is a bathtub overflow trip lever in San Francisco. The repository's `AGENTS.md`, `PROJECT_PROMPT.md`, `src/korea8/`, `vendor/gems57/` and the registry rasters are a DOE GEMS geothermal fault-prediction project. | The two are unrelated. Earlier sessions recorded this and built the trip-lever dossier as a self-contained tree rather than deleting the research work. | Informational | Noted again here; nothing deleted. Recorded on the Flagged for Review page. |
| R-02 | Publication boundary | What the live Pages origin actually serves, probed path by path. | `/pyproject.toml`, `/vendor/README.md`, `/COORDINATION.md`, `/PROJECT_PROMPT.md` and `/AGENTS.md` all return content. The whole repository root is served by the legacy branch publisher. | High | Guard added this session (§3). Switching the Pages source needs the repository UI; the token returns HTTP 403. |
| R-03 | Publication boundary, framing | Whether the repository is private. | It is public (`"visibility": "public"` from the GitHub API). Every tracked file is therefore already readable in the repository and in Git history. | Informational | Corrected the framing: the Pages setting is not a confidentiality boundary here. See §4. |
| R-04 | CI vs. reality | The workflow stages a 32-file link closure and deploys it as a Pages artifact. | The artifact is built and uploaded successfully, but it is not the set being served while the legacy root publisher is active. The deploy job's marker check passes against whichever copy is newest. | High | Live-boundary report step added so the served set is recorded on every deploy. |
| R-05 | Guard implementation | My own new classifier, tested against real paths. | First version used `str.lstrip('./')`, which strips *any* leading `.` or `/`. `.github/workflows/…` was silently reclassified as `github/…` and would have passed the guard. | Medium (in new code) | Fixed; regression test `test_hidden_directory_not_mangled_by_prefix_stripping`. |
| R-06 | Requirements coverage | Whether the brief's own requirements are individually tracked. | 42 technical requirement rows existed, but nothing mapped the owner's sentences to an acceptance test and a state. A 16-row traceability matrix existed only as a prior session's audit JSON and was not reachable from the site. | Medium | 16-row owner-brief register added to `requirements.html` with a named blocker on each partial row. |
| R-07 | Ranking arithmetic | Recomputed every weighted score. | Order is correct. **Rapid Flow and Ayoob & Peery both score 3.150**; positions 3 and 4 are an editorial tie-break that the page does not disclose as a tie. | Low | Flagged, not edited: the ranking page is shared output and the tie does not change the recommendation. |
| R-08 | Fee schedule | Category 1P and 11P/M amounts against the PDF. | $290 and $320 match the July 2026 schedule exactly. Hourly $519/$555 and re-inspection $259 also match. | None | No change. |
| R-09 | Licence records | 12 records, field by field against the stored rows. | 12 of 12 match on phone, expiry, classifications, status and legal name. No deltas. | None | Receipt published. |
| R-10 | Suspended licence | #1027286 status and bond detail. | Contractors Bond Suspension confirmed; bond cancellation date 08/16/2026 matches the stored detail. Excluded from the hire order. | None | No change. |
| R-11 | Superseded trees | Eight trees carry the same brief: `bathtub-overflow/`, `bathroom-overflow/`, `trip-lever/`, `bathtub/`, `docs/bathtub-overflow/`, `overflow-trip-lever/`, `overflow-integration/`, `project/`. | Only `overflow-integration/` feeds the canonical pages. `project/` is served live and reports 19 licence records and a different recommendation order from the canonical 24. | Medium | Already flagged as I-1 by session `b5ed3a43`. Repeated here; not deleted. |
| R-12 | Executive summaries | Four root-level files: `BATHTUB_EXECUTIVE_SUMMARY.md`, `EXECUTIVE_SUMMARY_bathtub.md`, `EXECUTIVE_SUMMARY.md`, `OVERFLOW_EXECUTIVE_SUMMARY.md`. | The first two are near-identical "moved" stubs differing only in their own filename. `EXECUTIVE_SUMMARY.md` is the unrelated GEMS summary. Only `OVERFLOW_EXECUTIVE_SUMMARY.md` carries the trip-lever summary. | Low | Noted; a reader can reach the wrong summary at `/EXECUTIVE_SUMMARY.md`. |
| R-13 | Binary assets | 16 tracked `.tif` files, 14,052,602 bytes. | Commit-level size is real but no `.tif` is in the published closure. `AGENTS.md` says rasters are never committed. Already raised as F-51. | Low | No change; deletion would break the research record. |
| R-14 | Dangling workflow target | `gems-pipeline.yml` pushes to `arena/d7026453-korea8`. | That branch belongs to a session that ended on 2026-11-04. The workflow is `workflow_dispatch`-only, so it cannot fire on a push, but a manual run would create that branch. Already raised as F-50. | Low | No change. |
| R-15 | Review evidence | Yelp search and business pages. | HTTP 403 again, matching every earlier session. Ratings, counts and review text stay blank. | Limitation | Recorded as blocked in the register (O-08). |
| R-16 | Verifier strength | Whether the verifier actually checks the new table. | It did not, initially: my first version of the register had three rows with no official-primary link and a free-text state vocabulary, and the build surfaced it. | Medium (caught) | Row-linked official sources added and the state vocabulary closed to three values; both now enforced. |
| R-17 | `site-data/` | A superseded mirror rewritten by every build. | Still rewritten on each build although nothing reads it, which invites a reader to mistake it for live input. Prior session `0ccaa3f3` raised this. | Low | No change; logged again. |
| R-18 | Test suite naming | `unittest discover -s tests` versus the CI pattern. | CI runs `-p 'test_overflow*.py'`. Two archived GEMS tests (`test_metric.py`, `test_uniqueness_gate.py`) need `numpy`, which is absent, so a full discover reports import errors that are unrelated to this deliverable. | Informational | Not hidden: "CI green" means the overflow suite, not every test. |
| R-19 | Open pull requests | 11 open PRs, the newest from 2026-11-08. | Their claims are older than 60 minutes with no commits. Per the board rule they are stale; this session did not merge or close any of them. | Informational | Noted in the board. |
| R-20 | Wording rule | `scripts/wording_guard.py` over every tracked text file. | Clean before and after this session's edits. | None | No change. |

---

## 3. What this session changed, and why

| Change | Files | Reason |
|---|---|---|
| Publication-boundary guard | `scripts/check_publication_boundary.py` (new), `tests/test_overflow_publication_boundary.py` (new) | R-02. Fails CI if an internal path reaches the staged artifact; reports what the live origin really serves. |
| CI enforcement | `.github/workflows/overflow-pages.yml` | Runs the guard before upload and records the live boundary after deploy, as a downloadable artifact. |
| Owner-brief register | `overflow-integration/data/requirements.json` (append only), `scripts/build_overflow_site.py`, `requirements.html` | R-06. One row per owner requirement with an acceptance test and an honest state. |
| Verifier coverage | `scripts/verify_overflow_site.py` | R-16. The new table is enforced, not just rendered. |
| Tests | `tests/test_overflow_site.py`, `tests/test_overflow_publication_boundary.py` | 15 new tests: 8 boundary, 7 register. |
| This review | `audit/2026-11-10-15308e85/**` | Receipts for everything above. |

**Not changed, deliberately:** the ranking, every provider row, every estimate row, every review
row, the flags register, the source register, the superseded trees and the GEMS research files.

---

## 4. The publication boundary, stated accurately

Earlier board entries describe the live site as publishing "the entire repository root, including
internal coordination and the task prompt" and treat that as a confidentiality defect of the
Pages configuration. Two corrections follow from this session's checks.

1. **The repository is already public.** Anyone can read `COORDINATION.md` at
   `github.com/karagemop466-tech/Korea8/blob/main/COORDINATION.md` today, without Pages. The
   Pages source setting cannot make that file private and deleting it from `main` would not
   remove it from history.
2. **What Pages adds is presentation, not secrecy.** With the legacy root publisher active, the
   dashboard URL also serves repository scaffolding as web pages. That is a real quality and
   presentation defect — a visitor following `/COORDINATION.md` gets a raw Markdown dump dressed
   as part of the product — and it is what the guard now records.

The settings change that would end it (Pages → Source → **GitHub Actions**) requires repository
UI access. `PUT /repos/.../pages` with `build_type=workflow` returns **HTTP 403, "Resource not
accessible by integration"**, from an account that reports `admin: true` on the repository, so the
token is fine-grained without Pages write scope. This is recorded rather than worked around.

---

## 5. Irregularities published, not fixed

| ID | Item | Why it is not fixed here |
|---|---|---|
| R-02 | Pages serves the whole repository root | Needs the repository UI; the API returns HTTP 403. |
| R-07 | Rapid Flow / Ayoob tie at 3.150 is not disclosed as a tie | Shared ranking output; the fix is a wording change to a page owned by the integration step. Logged. |
| R-11 | `project/` publishes a superseded 19-licence brief that contradicts the canonical 24-licence data | Deleting another session's tree is outside this scope. Already I-1. |
| R-12 | Four root executive summaries, only one about this project | Removal would break links in prior audits. Logged. |
| R-15 | Yelp unreachable (HTTP 403) | External. Values stay blank. |
| R-17 | `site-data/` mirror rewritten by the build | Owned by the generator; logged. |
| R-19 | 11 stale open PRs | Not this session's to merge or close. |

---

## 6. Gates re-run after the final edit

| Gate | Result |
|---|---|
| `python scripts/build_overflow_site.py` | 11 pages rebuilt |
| `python scripts/verify_overflow_site.py` | **31/31 pass**, 357 table rows, 357 with an official-primary source link |
| `python -m unittest discover -s tests -p 'test_overflow*.py'` | **42 tests OK** |
| `python scripts/wording_guard.py` | clean |
| `python audit/independent_audit.py` | `pages=11 rows=357 with_source=357 problems=0` |
| `python scripts/stage_overflow_pages.py` | 32 linked files staged |
| `python scripts/check_publication_boundary.py` | PASS, no internal path in the staged set |
| Negative control: plant `COORDINATION.md` in the staged set | FAIL as intended, exit 1 |
| `git diff --check` | clean |

---

## 7. Standing statements

No provider was contacted, called, emailed, quoted, booked or paid. Owner-supplied amounts remain
labelled owner-reported with independent amounts blank. Review ratings and counts remain null. No
permit position is asserted in either direction, and no statement about the owner's calendar or
reasons appears on any page, in any commit or in this document.

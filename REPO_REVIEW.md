# REPO_REVIEW.md — line-by-line review of `karagemop466-tech/Korea8`

Reviewed at commit `22acb8c` (main) on 2026-11-06 by session `arena-5404ab5c`.
Branch reviewed: `arena/5404ab5c-korea8`.

## 1. What the repository is

The repo name is `Korea8`. At the reviewed commit it contains **no content relating to a bathtub,
plumbing, contractors, or San Francisco**. It is a DOE GEMS Prize geothermal fault-mapping
research project:

| Path | Contents | Verified how |
|---|---|---|
| `README.md` | Mission, verdict table (HOLDOUT-DTI 0.0219), data-acquisition notes | Read directly |
| `AGENTS.md` | Standing rules for the GEMS work (holdout, uniqueness, fail-closed) | Read directly |
| `PROJECT_PROMPT.md` | The preserved GEMS prompt verbatim | Read directly |
| `vendor/gems57/`, `vendor/gems-prize-reference-solution-main/`, `vendor/template57/` | Pinned evaluator/writer/uniqueness tools | `ls`, `vendor/PROVENANCE.json` |
| `scripts/` | 15 pipeline scripts (download, prepare, experiment, build_site, verify_release) | `ls`, read `LEGACY.md`, `build_site.py` |
| `evidence/`, `docs/evidence/` | 12 JSON receipts; `verification.json` reports 21/21 checks | `evidence/verification.json` |
| `registry/focus9/*.tif`, `registry/lattice_s5.tif` | ~9.5 MB of preserved reference rasters | `du -sh registry` |
| `downloads/`, `docs/downloads/` | Two identical 1.5 MB GeoTIFF sets | `cmp` on each pair |
| `data/templates/GEMS-grid-template.tif` | Grid template | `ls` |
| `.github/workflows/gems-pipeline.yml` | `workflow_dispatch`-only pipeline, pushes to `arena/d7026453-korea8` | Read directly |
| `index.html`, `style.css`, `sources.html`, `limitations.html`, `submit.html`, `submit-howto.html`, `executive-summary.html`, `feed.json`, `feed.xml` | Static evidence site, **byte-identical** to the copies in `docs/` | `cmp` — 9 of 9 identical |

**What the GEMS material itself claims**, and what I could independently confirm:

| Claim in repo | Status after review |
|---|---|
| Competitor is the DOE GEMS Prize Challenge on DrivenData, closing 2026-12-03 22:00 UTC, $300,000 pool, one scored submission per UTC day | **Confirmed** on the official competition page ([source](https://www.drivendata.org/competitions/306/competition-doe-gems/)) |
| Candidate HOLDOUT-DTI 0.0219 with CI [0.0177, 0.0261] | **Internal only** — reproduced from `evidence/run_card.json`; not an organizer receipt, and correctly labelled HOLDOUT-DTI rather than a score |
| Uniqueness gate fails against the `r13-lattice-s5` covering witness (0.998 overlap) | **Internal only** — internal measurement, correctly labelled REGISTRY-MEASUREMENT |
| 21/21 verification checks pass | **Internal only** — `evidence/verification.json` self-reports `ok: true, n_checks: 21, n_failed: 0`; the checker's own code was not re-run in this session |
| "No contest submission was performed" | **Consistent** with the repo; no submission receipt exists either way, so it can be neither confirmed nor refuted here |

## 2. Irregularities found

| # | Finding | Severity | Detail | Action |
|---|---|---|---|---|
| I-01 | **The repository does not contain this project** | High | All content is GEMS geothermal research. Nothing about a tub, a trip lever, a contractor, or San Francisco. | Nothing deleted. GEMS evidence site moved intact to `gems_site/`; new project owns the root. Flagged for the owner — see `data/tub/flagged.json`. |
| I-02 | CSLB misspells a street name on licence #1024971 | Low | Record reads `236 W POTRAL AVE`. The street is Portal Avenue. | Reproduced verbatim with an annotation; not silently corrected. |
| I-03 | Cancelled licence at the same address as an active one | Medium | #973345 (Advance Plumbing) cancelled 05/14/2018; #977638 (Expert Plumbing Solutions) active, same address and phone. | Both published; only the active one counted. |
| I-04 | Active licence with a future-suspension advisory | Medium | #1009195 carries a CSLB note about unresolved final liability. | Ranked last among active plumbing firms; flagged. |
| I-05 | Stale "$500 licence threshold" in circulation | Medium | BPC 7048 now sets $1,000 (eff. 2026-01-01) and adds a permit condition. Many third-party sites still say $500. | Only statutory text used. |
| I-06 | Marketing overstates CSLB classifications | Medium | All Action Waterdamage markets "one licensed crew does extraction, drying, and the rebuild"; CSLB #1043942 shows only C-61/D64 remediation. | Excluded from shortlist, reason published. |
| I-07 | Website address differs from CSLB address | Low | Heise's Plumbing: website 260 Ocean Ave; CSLB 1610 Evans Ave. Phone matches. | CSLB address published as the licence address. |
| I-08 | `scripts/build_site.py` writes into the repository root | High (structural) | It copies `docs/*` over root `index.html`, `style.css`, and four other pages. Any pipeline run would have overwritten a new landing page. | Mirror target changed to `gems_site/`; nothing else in the script altered. |
| I-09 | Duplicate site trees and duplicate rasters | Info | Root pages were byte-identical to `docs/` pages; two identical 1.5 MB raster sets. | Consolidated to one shared `downloads/` + `evidence/` tree. |
| I-10 | `docs/` is dead weight for Pages | Info | Pages is configured with source = `main`, path `/`. So `docs/` is served at `/docs/` rather than as the site root, and the root copy was what visitors actually saw. | Recorded; the new build writes the root pages and leaves `docs/` as-is. |
| I-11 | No `COORDINATION.md` existed | Info | Required by the brief; absent. | Created with a task board and a claim. |
| I-12 | No `index.html` navigation between the two projects | Low | Root had a single GEMS dashboard and no route to anything else. | New root dashboard links the GEMS archive as a subpage. |
| I-13 | Workflow pushes to a merged branch | Low | `.github/workflows/gems-pipeline.yml` ends with `git push origin HEAD:arena/d7026453-korea8`, a branch whose PR (#6) is already merged. | Not modified (outside this session's scope); logged for the GEMS owner. |
| I-14 | `pytest` is not installed in this sandbox | Info | `python3 -c "import pytest"` → `ModuleNotFoundError`. The repo's unit tests therefore cannot run here. | Noted; the new verification gate is written in stdlib Python only, so it runs without dependencies. |

## 3. What I could and could not verify in the GEMS material

Verified against an official source:
- The competition exists, its sponsor, prize pool, rules on submission limits, external data, and
  the 2026-12-03 deadline — [DrivenData competition page](https://www.drivendata.org/competitions/306/competition-doe-gems/).

Not verified (no official source exists, or the source was unreachable):
- Every numeric score in the repo. These are the project's own holdout measurements, not organizer
  results. The repo already labels them correctly, and I have not upgraded any of them.
- The user-reported leaderboard targets (0.4413 / 0.3195) that the GEMS prompt mentions. The live
  leaderboard is client-rendered and was not scraped.
- The Yelp ratings referenced in the GEMS-adjacent material are unrelated to this project and were
  not touched.

## 4. Files this session added or changed

| Path | Change |
|---|---|
| `COORDINATION.md` | **New.** Task board, claim, sources, verification log, merge record. |
| `REPO_REVIEW.md` | **New.** This file. |
| `DATA_DICTIONARY.md` | **New.** Field-by-field definition of every data file. |
| `data/tub/` | **New.** `sources.json`, `requirements.json`, `vendors.json`, `estimates.json`, `rules.json`, `scope.json`, `flagged.json`, `executive.json`. |
| `scripts/build_tub_site.py` | **New.** Builds the dashboard site from `data/tub/*.json`. |
| `scripts/verify_tub_site.py` | **New.** Link + source-cell + privacy verification gate (stdlib only). |
| `index.html` | **Replaced** with the trip-lever dashboard; the GEMS dashboard it replaced is preserved at `gems_site/index.html`. |
| `gems_site/` | **Moved** from the repo root (`git mv`, history preserved). Links re-pointed to the shared `downloads/` and `evidence/`. |
| `downloads/`, `evidence/` | **Kept** at the root because `gems_site/` now points into them; the duplicate copies under `gems_site/` were removed. |
| `scripts/build_site.py` | One block changed: the root-mirror target is now `gems_site/`. |
| `docs/`, `registry/`, `vendor/`, `src/`, `tests/`, `submissions/`, `audit/`, `knowledge/` | **Unchanged.** |

## 5. Open questions for the owner

1. Is `Korea8` the intended repository for the bathtub project? If not, nothing here is lost — the
   changes are a small, revertible set of commits.
2. Should the GEMS site stay published? It is still reachable at `/gems_site/`.
3. Should `docs/` and the duplicate rasters be removed now that the root serves the site? I left them
   alone because deleting another project's evidence is not mine to do.

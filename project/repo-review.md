# Repo Review — line-by-line, 2026-11-06, session `arena-82aa8544`

Scope: repository tree, README.md, AGENTS.md, PROJECT_PROMPT.md, .github/workflows/gems-pipeline.yml,
root HTML vs docs/ HTML, download artifacts, git history, GitHub Pages configuration.

## Findings

| # | Observation | Evidence | Disposition |
|---|---|---|---|
| 1 | Repository content is a **different project** (DOE GEMS Prize Challenge fault-prediction research) than the current brief (bathtub trip-lever repair coordination). | `README.md`, `AGENTS.md`, `PROJECT_PROMPT.md`, `docs/`, `evidence/` | Flagged on site (F-01). New project site built at repo root; legacy content preserved untouched in `docs/`, `evidence/`, `vendor/`, `registry/`, `scripts/`, `src/`, `tests/`. |
| 2 | Root HTML files (`index.html`, `executive-summary.html`, `limitations.html`, `sources.html`, `style.css`, `submit-howto.html`, `submit.html`, `feed.json`, `feed.xml`) are **byte-identical duplicates** of the `docs/` copies (verified `diff -q` on all nine). | `diff -q` run 2026-11-06 | Root copies are superseded by the new project site (Pages serves repo root of `main`); legacy copies remain intact in `docs/`. |
| 3 | GitHub Pages is configured: **build from `main`, path `/` (repo root)**, live at https://karagemop466-tech.github.io/Korea8/. | `gh api repos/karagemop466-tech/Korea8/pages` (2026-11-06) | New site therefore must be built at repo root, with relative links (project-page base path `/Korea8/`). |
| 4 | Legacy site's download button links `downloads/korea8_candidate.tif` (SHA-256 `c560211b…`) while README headline documents a *newer* candidate `korea8-k8-1-blind-stepper-relay-20261104-v1.tif` (SHA-256 `6104ad73…`, verified against the file). Both files exist in `downloads/` and `docs/downloads/`; hashes verified with `sha256sum`. | `sha256sum` run 2026-11-06 | Legacy inconsistency — recorded here; legacy site untouched. Not blocking the new site. |
| 5 | `COORDINATION.md` did not exist. | repo tree 2026-11-06 | Created per parallel-session protocol; T1–T6 claimed and pushed before any work. |
| 6 | No CI is triggered on push (`gems-pipeline.yml` is `workflow_dispatch` only) — merging to `main` cannot break a pipeline. | workflow file | Noted; Pages deploy is the only main-branch automation. |

## Irregularities for manual review

- Legacy README "Current verdict" table cites HOLDOUT-DTI values that this session did not re-run or
  re-verify (out of scope for the current brief); they are preserved as historical claims of the prior
  project, labeled as such.
- The legacy root page still presents a "DO NOT SUBMIT" verdict banner for the GEMS project — retained
  only in `docs/` history, no longer reachable from the new site's navigation.

## Verification performed this session

- `diff -q` across 9 root/docs file pairs.
- `sha256sum` of both candidate TIFs.
- `gh api` Pages configuration query.
- Reading of README.md, AGENTS.md, PROJECT_PROMPT.md, workflow YAML in full.

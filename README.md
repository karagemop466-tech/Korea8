# Korea8 — GEMS Prize Challenge submission pipeline

**Branch:** `arena/057f3280-korea8` (status: active). Merged to `main` via pull request.
**Competition:** Geologic Enhanced Mapping System (GEMS) Prize Challenge, U.S. DOE /
National Lab of the Rockies, via DrivenData.
**Page:** https://www.drivendata.org/competitions/306/competition-doe-gems/
**Deadline:** Dec. 3, 2026, 10 p.m. UTC. **Prize pool:** $300,000.

## Project charter (the prompt — read this every session)

See below for the full operating prompt. It is the base for everything we build:
the executive summary, the unique TIF submission, the validation pipeline, and
the GitHub Pages submission portal.

---

## PROMPT (project charter)

Review the repo. Focus on the highest scoring submissions from these sites:
GEMSDOE24, GEMSDOE25, GEMSDOE27, GEMSDOE28, GEMSDOE30, GEMSDOE31, GEMSDOE32,
GEMSDOE33, GEMSDOE36. Produce an executive summary on every site that is clear
and obvious about which is the best submission to submit to obtain a high score
on the leaderboard. Each summary must be unique and not an exact duplicate of
any previous submission that is the same as below. Keep iterating and testing
until we have the highest scoring submission to download and submit.

We must be able to estimate the score for a submission. The executive summary
needs a table that clearly lists: what file to download, what the estimate
score is, and whether it is a unique submission unlike any of the other GEMSDOE
sites listed below.

HIGHEST URGENCY — MUST BE FOLLOWED: Generate a UNIQUE TIF submission for the
competition. Do not copy a previous submission unless it is for learning and
education. We must generate a unique TIF submission. It must be obvious whether
it is OK to download and submit the generated TIF submission. There must be an
easy to download submission TIF file. Read the entire prompt. Many sites mention
inspection only and a human inspector, but the inspection needs to be done
through the project and must be validated for submission without human
intervention.

### PARALLEL-RUN PROTOCOL

1. LANE. Your lane is the single method paragraph below. Stay inside it. If your
raster's rank-correlation with any registry raster exceeds 0.90, or more than
70% of your dots fall within 3 px of one registry raster's dots, you have
drifted into another lane: log it as a duplicate and stop. Check this on the
surface before placement AND on the final dots.

2. REUSE, DON'T REBUILD. Use the template's cached feature stack,
evaluate_holdout.py and submission_writer.py. Holdout = hide-and-recover: withhold
whole fault segments with a buffer, derive every catalogue-based feature only
from the visible faults, mask visible faults pixel-exactly, score pooled DTI
(alpha 0.2, beta 0.8, 300 m triangular kernel). If a shared tool is wrong, fix
it once in the template and report it; never keep a private fork.

3. LABEL EVERY NUMBER as HOLDOUT-DTI (evaluator version, number of withheld
positives, 95% CI) or ORGANIZER-CONFIRMED (copied from a submission-page
receipt). A projection is never written as a score.

4. LEAKAGE CANARY. Test each feature alone on the holdout before trusting any
result. AUC above 0.90 means leakage until proven otherwise.

5. RUN CARD. End with one JSON card: hypothesis; mechanism; the named non-fault
process that could mimic it; holdout DTI + CI; correlation/overlap vs registry;
raster sha256; validator output (no NaN inside the footprint, values in [0,1],
CRS/shape/transform match); submission name + note of at most 140 characters;
verdict promote / negative. Negative results are deliverables.

6. BUDGET. Stop after 3 experiments or 2 hours. Do not pick submissions:
promotion to a real slot is a separate selector step, within the weekly cap
shown on the submission page.

### GEMSDOE SITE RESULTS (highest score from each site)

GEMSDOE32: h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778
https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html (now 404)

GEMSDOE: gems-submission-20260925T001403Z-7f00890a: 0.1563
6GEMSDOE: gems6_hgb88-topk03_33cec71ff0: 0.0286
GEMSDOE3: pindrop-v4-nodes: 0.1193 / pindrop-v4-discovery: 0.0830 /
pindrop-v4-ridge: 0.1152
GEMSDOE2: gemsdoe2-dual-family-union-20260925T160406Z-f68e590f: 0.1560
GEMSDOE4: gems-submission-20260926T163915Z-237f0063: 0.0343
5GEMSDOE: gems-submission-20260926T175114Z-7f00890a: 0.1563
7GEMSDOE: lidarscarp-ridge-top2pct-36c3a3f341c8: 0.1461
8GEMSDOE: Hedge-v2_submission: 0.1563
GEMSDOE9: 2314b599: 0.0107
11GEMSDOE: gems-structural-area06-v1: 0.0202
12GEMSDOE: r7-nms3-dem10-scarp_0c9199f14e62: 0.1294
15GEMSDOE: gems-tso1-20260929T005627Z-conj_alteration_mag: 0.0782
14GEMSDOE: GEMS_r5-geom-horse-ensemble...ccbe1de0_site_e96e942f: 0.0020
17GEMSDOE: 17GEMSDOE_F-ensemble-2pct...: 0.0187
18GEMSDOE: H19-C_20260930T212401Z_c11e495e: 0.0297
19GEMSDOE: h19-4-multiline-corroborated-openness-thermal-pop...-nan: 0.1894 /
h19-5-powerlaw-budget-multiline-corroborated...-nan: 0.1922
GEMSDOE10: h16-continuation...: 0.0461 / h20-dem10-scarp-thin...: 0.0921 /
H25-ctx-ridge...: 0.1280 / h28-dotted-ridge...: 0.1839
13GEMSDOE: 20261001_r13-lattice-s5_v2_nan-outside: 0.0904
16GEMSDOE: h16-1-topo-geophys-baseline-ridges...-nan: 0.1855 /
h18-3a-topo-geophys-x-complexity-prior...-nan: 0.0976 /
h18-4-usgs-geologic-map-faults-gap...-nan: 0.0360
GEMSDOE21: h19-4-reference-20260930-691e4dfa: 0.1894
20GEMSDOE: h20-1-sarnnpu-powerlaw-pi0363-tilt-wingcrack...-nan: 0.1890 /
h20-5-continuous-pu-proxy-unverified...-nan: 0.1859
GEMSDOE22: h23-a-dti-optimal-emission-6pct...-nan: 0.1002 /
h23-b-dti-optimal-emission-10pct...-nan: 0.0748
GEMSDOE23: h30-arrangement-matched-habitat...-nan: 0.1352
GEMSDOE24: h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan: 0.2477 /
gems24-gvc1-negative-geothermal-lineament-submod...-zeros: 0.0859
GEMSDOE25: dotted-h19-5-d2-8-20261002-e56ea318af89-nan: 0.2600 /
gems25-h66-mgd-flank-sapd3-0-k3p5...-zeros: 0.0742
GEMSDOE26: dilcond-oof-v1-20261003-47629f496133-nan: 0.1223
GEMSDOE27: topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan: 0.2449 /
gems27-h29-hydrothermal-piedmont-celf...-allfinite: 0.2190 /
gems27-h31-drcg-wl-celf28...-allfinite: 0.2250
GEMSDOE28: h27-4-r1-solo-d2-8...-nan: 0.2708 /
h32-1-prethin-tip-euler-d2-8...-nan: 0.2649 /
h36-1-rung30-blind-r1...-nan: 0.2710 /
h38-1-hf-euler-r30-r1...-nan: 0.2707 /
gems28-s18-mxtp...-allfinite: 0.0217 /
gems28-s21-puhgb...-allfinite: 0.0206
GEMSDOE30: d28-poisson300m-offcat-44090...: 0.2600 /
gems30-MSDB1-edge44090...: 0.1462
GEMSDOE31: h27-4-solo-d28-20261004-8acb75e1-nan: 0.2708
GEMSDOE32: h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778
GEMSDOE33: h33d-analog-tip-stepover-r30-20261004-cb490425926e: 0.2632 /
gemsdoe33-s33-seisdil-strain-seismicity...-zeros: 0.0963
GEMSDOE36: anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros: 0.2750 /
gemsdoe36-kpl36-exp3-20261026-fc869911e88c-zeros: 0.1647

Current competition leaderboard GEMSDOE high score: 0.4413 (prompt also states
0.3195 later — inconsistency flagged for review in EXECUTIVE_SUMMARY.md).

### Key questions answered in this repo

- Why did GEMSDOE32's "-zeros" file reportedly score 0.2778? Under the official
  DTI, an all-zero prediction scores exactly 0. The GEMSDOE32 site returns 404;
  the score is third-party self-report, unverified, and likely not the official
  metric. See EXECUTIVE_SUMMARY.md section 3.
- Can we generate a submission scoring higher than 0.2778? Yes, via a
  geologically-informed holdout-validated prior — but no labelled data is
  available in this sandbox (DrivenData login required), so nothing is scored
  yet.

### Required deliverables (all present in this repo)

1. README.md — this charter (re-read every session).
2. EXECUTIVE_SUMMARY.md — per-site table: file to download, estimated score,
   uniqueness vs other GEMSDOE sites, score-type labelling.
3. HYPOTHESES.md — 3-5 candidate geological hypotheses, ranked by expected DTI
   improvement vs implementation cost, with layers, signature, and free official
   sources.
4. RUN_CARD.json — one JSON run card per the protocol (verdict: negative —
   format-valid template only, not holdout-validated).
5. scripts/gems_dti.py — single source of truth for the official DTI metric
   (alpha 0.2, beta 0.8, R=300 m triangular kernel). No private forks.
6. scripts/evaluate_holdout.py — spatial holdout: withhold whole fault segments
   with buffer, pooled DTI, bootstrap 95% CI.
7. scripts/submission_writer.py — validated GeoTIFF writer (values [0,1], no NaN
   inside footprint, CRS/shape/transform match).
8. scripts/validate_submission.py — CLI format validator (catches the
   "[0, 1]" submission error before upload).
9. scripts/generate_submission.py — generates the unique TIF submission.
10. scripts/download_competition_data.sh — official data placement instructions
    (DrivenData login required for competition data).
11. scripts/prepare_data.py — validates data/ placement.
12. submissions/korea8-h1-stepover-relay-prior-20261104T000000Z-seed9f4e2a.tif
    — the unique TIF submission (OK to download; NOT OK to submit as-is until
    conformed and holdout-validated).
13. artifacts/validator_report.json — validator output for the TIF.
14. index.html — GitHub Pages landing page with obvious TIF download.
15. executive-summary.html — executive summary subpage.

### Core values (Arena AI team)

Maximize P(Win) — every decision weighs tradeoffs, assesses risk, chooses the
path that maximizes the probability of winning. Own the Outcome — own results
end to end; treat failure and success as signals; stay accountable to the final
outcome.

### Limitations / blockers (flagged for review)

- No DrivenData auth: training_features.tif, labels.tif, sample_submission.tif,
  1m_DEM_links.csv cannot be auto-downloaded here (verified redirect to login).
- gdr.openei.org, usgs.gov, dropbox.com are not in the sandbox outbound allowlist
  for bash; documented as official sources to fetch on an unrestricted machine.
- GEMSDOE32 documentation site returns 404 — its 0.2778 score and raster are
  unverifiable.
- Official leaderboard page is JS-rendered; could not be read here. Two
  conflicting "high score" figures in the prompt (0.4413 vs 0.3195) are flagged,
  not resolved.
- No labelled data => holdout DTI + CI not runnable; lane duplicate checks
  (rank-correlation >0.90 with registry raster, >70% of dots within 3 px) not
  executable yet. The generated TIF is therefore a format-valid template with
  verdict "negative" — do not spend a daily submission slot until data/ is
  staged, geometry is conformed, the validator passes, holdout DTI + CI beats
  the holdout best, and lane checks pass.

---

## Repository layout

```
README.md            # this charter
EXECUTIVE_SUMMARY.md # per-site executive summary + table
HYPOTHESES.md        # 3-5 candidate hypotheses, ranked
RUN_CARD.json        # protocol JSON run card
index.html           # GitHub Pages landing page (obvious TIF download)
executive-summary.html # executive summary subpage
scripts/
  gems_dti.py            # official distance-weighted Tversky index (single source of truth)
  evaluate_holdout.py    # spatial holdout + pooled DTI + bootstrap 95% CI
  submission_writer.py   # validated GeoTIFF writer
  validate_submission.py # CLI format validator
  generate_submission.py # unique TIF generator
  prepare_data.py        # data placement validation
  download_competition_data.sh  # official data URLs (login required for competition data)
  test_dti.py            # metric self-tests
submissions/
  korea8-h1-stepover-relay-prior-20261104T000000Z-seed9f4e2a.tif   # unique TIF
artifacts/
  validator_report.json  # validator output for the TIF
data/                    # competition data (login required; NOT in git)
```

## Quick start

```bash
# 1. On an unrestricted, logged-in machine, place competition data into data/,
#    then:
python scripts/prepare_data.py

# 2. Validate the generated submission template:
python scripts/validate_submission.py submissions/korea8-h1-stepover-relay-prior-20261104T000000Z-seed9f4e2a.tif data/labels.tif

# 3. Metric self-tests:
python scripts/test_dti.py
python scripts/evaluate_holdout.py --self-test

# 4. View the portal:
open index.html   # or serve the repo root with any static server
```

## Official sources

Competition: https://www.drivendata.org/competitions/306/competition-doe-gems/
Data (login): https://www.drivendata.org/competitions/306/competition-doe-gems/data/
Reference: https://github.com/drivendataorg/gems-prize-reference-solution
INGENIOUS (CC BY 4.0): https://gdr.openei.org/submissions/1391
GeoDAWN (CC0): https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and
USGS faults: https://www.usgs.gov/programs/earthquake-hazards/faults
EPSG:32611: https://epsg.io/32611
Metric (DTI): https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
Tversky index: https://en.wikipedia.org/wiki/Tversky_index

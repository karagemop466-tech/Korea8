#!/usr/bin/env python3
"""Render README, machine-readable result and dependency-free GitHub Pages report."""
from __future__ import annotations
import html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CARD = json.loads((ROOT/'run-card.json').read_text())
FOCUS = json.loads((ROOT/'docs/data/focus9.json').read_text())
ROWS = FOCUS['rows']
H = CARD['holdout_dti']
LATTICE = next(r for r in CARD['registry']['final'] if r['site']=='13GEMSDOE')
RASTER = CARD['research_raster']
FILENAME = Path(RASTER).name
SHA = CARD['raster_sha256']

HYPOTHESES = [
 ('1 — E1 (tested)', 'Th/K edges + coherent anti-slope scarp termini', 'Medium / medium', 'Lithologic contacts, soil gradients, terrace/channel banks'),
 ('2', 'Radiometric ratio-polarity reversal across LiDAR scarps', 'Medium-low / high', 'Depositional contacts, regolith, flight-line leveling'),
 ('3', 'Upward-continued TMI gradients through LiDAR scarp gaps', 'Medium-low / medium', 'Magnetic contacts, cultural sources, continuation artifacts'),
 ('4', 'Residual 2 m thermal anomalies at label-free scarp endpoints', 'Unknown / high', 'Solar exposure, moisture, terrain, sampling bias'),
 ('5', 'Paleo-geothermal deposits associated with scarps', 'Unknown / high', 'Spring mounds, depositional terraces, inherited topography'),
]

def f(x, n=9): return f'{x:.{n}f}'
def ci(x): return f'[{f(x[0])}, {f(x[1])}]'

def site_table_markdown():
    lines=['| Site | User-reported score* | HOLDOUT-DTI | 95% CI | Dots | Worst other-focus 3 px overlap | Submit? |',
           '|---|---:|---:|---|---:|---:|---|']
    for r in ROWS:
        h=r['holdout_dti']; w=r['max_directed_overlap_3px']
        lines.append(f"| {r['site']} | {r['user_reported_score']:.4f} | {f(h['pooled_dti'])} | {ci(h['ci95'])} | {r['emitted_dots']:,} | {w['other_site']}: {100*w['fraction']:.2f}% | **No** |")
    return '\n'.join(lines)

def site_table_html():
    body=[]
    for r in ROWS:
        h=r['holdout_dti']; w=r['max_directed_overlap_3px']
        body.append('<tr>'+''.join([
            f"<td><strong>{html.escape(r['site'])}</strong></td>",
            f"<td>{r['user_reported_score']:.4f}</td>",
            f"<td>{f(h['pooled_dti'])}</td><td>{ci(h['ci95'])}</td>",
            f"<td>{r['emitted_dots']:,}</td>",
            f"<td>{html.escape(w['other_site'])}: {100*w['fraction']:.2f}%</td>",
            '<td><span class="pill bad">No</span></td>'])+'</tr>')
    return '\n'.join(body)

def hypotheses_html():
    return '\n'.join('<tr>'+''.join(f'<td>{html.escape(str(v))}</td>' for v in row)+'</tr>' for row in HYPOTHESES)

readme=f'''# Korea8 — autonomous GEMS fault research

> **VERDICT: NEGATIVE — DO NOT SUBMIT.** The new E1 GeoTIFF is format-valid, but it fails the mandatory 13GEMSDOE duplicate/lane-drift gate and does not beat the shared holdout baseline. No weekly submission slot was used.

**Values: Maximize P(Win). Own the Outcome.** A falsified hypothesis is a deliverable; an invalid upload is not.

## Executive summary

| Decision field | Result |
|---|---|
| New experiment | E1: label-free multiscale GeoDAWN Th/K edges coupled to coherent anti-slope LiDAR scarps and endpoint halos |
| HOLDOUT-DTI | **{f(H['pooled_dti'])}**, 95% CI **{ci(H['ci95'])}**; evaluator `{H['evaluator_version']}`; {H['withheld_positives']:,} withheld positives; {H['bootstrap_reps']:,} bootstrap repetitions over {H['spatial_clusters']} clusters |
| Reproduced nine-focus holdout baseline | **{f(FOCUS['holdout_baseline_max'])}** — E1 does **not** beat it |
| Pre-placement uniqueness | Pass on scoped registry: maximum surface Spearman ρ 0.053564 (<0.90) |
| Final uniqueness | **FAIL: {100*LATTICE['final_dot_overlap_within_3px']:.4f}%** of final dots within 3 px of 13GEMSDOE (>70% stop) |
| Format | **PASS:** one float32 band, exact EPSG:32611 / 3730×3292 / transform match; all 12,279,160 cells finite in `[0,1]`; zero on known-fault pixels |
| Leaderboard score estimate | **None.** HOLDOUT-DTI and SGMC are not leaderboard estimates |
| Registry completeness | **No.** Nine focus rasters plus one lattice are an explicit incomplete screen |
| Separate selector / lane clearance | **No / not supplied.** The referenced single-method paragraph was absent |
| Submission approval | **NO — `negative`** |

### Download status

There is **no approved submission download**. For audit only, the newly generated research bytes are available at:

[`docs/research/{FILENAME}`]({RASTER})

- Research-only name: `{CARD['submission_name']}`
- SHA-256: `{SHA}`
- Submission note ({CARD['submission_note_length']} characters): `{CARD['submission_note']}`
- Full machine-readable decision: [`run-card.json`](run-card.json)
- Three-pass review and negative controls: [`docs/verification.md`](docs/verification.md)
- No value here guarantees organizer acceptance; this candidate is explicitly not approved.

## Why GEMSDOE32 reportedly led

The reported **0.2778** is user-reported, not organizer-confirmed. Exact pixel algebra shows that GEMSDOE25 D2.8 (44,090 dots) was pruned to GEMSDOE31 by excluding catalogue distance `<=100 m` (40,199 dots), then to GEMSDOE32 by excluding `<=200 m` from D2.8 (37,654 dots). No dots were added. This can reduce low-credit false-positive mass under distance-weighted DTI and the official known-fault masking rule, but private-label causation cannot be observed.

GEMSDOE32 has HOLDOUT-DTI only **0.004515379**, while GEMSDOE25/30 have **0.096743304**. Across the nine selected rows, user-reported score versus holdout has descriptive Spearman ρ **−0.848739** (p=0.00381, n=9), not a leaderboard calibration. Whether 0.2778 can be beaten remains **unknown**; E1 does not establish it. See [`docs/champion.md`](docs/champion.md) and [`evidence/champion-lineage.json`](evidence/champion-lineage.json).

## Nine priority sites

All nine historical rasters match the single-band float32 grid and are finite in `[0,1]` inside the footprint. NaN outside is officially permitted; only GEMSDOE32 and GEMSDOE36 are finite zero-outside across the full grid. Every row is a historical near-duplicate under the 70% final-dot rule and is **not eligible as a new submission**.

{site_table_markdown()}

\* User-reported; no submission receipts. Every HOLDOUT-DTI uses `GEMSDOE32-HIDE-RECOVER-v3.0`, 22,232 withheld positives, 140 clusters and 1,000 bootstrap repetitions. Full CIs, SGMC diagnostics, hashes and directed overlap matrix: [`docs/data/focus9.json`](docs/data/focus9.json).

## Ranked geological hypotheses

| Rank | Hypothesis | Expected value / implementation cost | Named mimics |
|---|---|---|---|
'''+ '\n'.join('| '+' | '.join(row)+' |' for row in HYPOTHESES)+f'''

Each targets structures that can occur off catalogue rather than extending known traces. E1 is distinct from the recovered catalogue-tip relay and scarp-only density implementations, but no global novelty is asserted. Physical signatures, exact layers and differences are frozen in [`docs/hypotheses.md`](docs/hypotheses.md). Only E1 was run; alternatives were not tuned after seeing its result.

## Submission instructions

1. **Do not upload the current E1 or any historical focus TIFF.** The run card is `negative`; the duplicate stop is mandatory.
2. A future artifact may be considered only when its run card says `promote`, all format/holdout/uniqueness/provenance checks pass, a separate selector approves it, and the weekly-slot decision is explicitly made.
3. If those independent conditions are met, use the zero-outside float32 variant with its unique name and ≤140-character note; follow the [official DrivenData instructions and rules](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/). Preserve the local validator output and submit only through the official portal.
4. Do not translate HOLDOUT-DTI, SGMC, a score range or expected credit into an organizer score. Only an organizer receipt can confirm an upload result.

## Reproduce autonomously

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
scripts/download_competition_data.sh       # public hash-pinned mirrors; requires gh authentication
PYTHONPATH=src .venv/bin/python scripts/audit_lattice.py
PYTHONPATH=src .venv/bin/python scripts/audit_focus9.py
PYTHONPATH=src .venv/bin/python scripts/run_trc_experiment.py  # exit 2 is the expected negative verdict
PYTHONPATH=src .venv/bin/python scripts/build_report.py
PYTHONPATH=src .venv/bin/pytest -q
PYTHONPATH=src .venv/bin/python scripts/verify_delivery.py
```

The surface and placement are deterministic. Rerunning creates a new timestamped research filename, not a new experiment or submission approval. The input fetcher verifies all 17 hashes atomically and refuses to overwrite mismatched files. Data/cache TIFFs outside the small research deliverable are Git-ignored.

## Sources, limitations and irregularities

- Official competition, USGS GeoDAWN/3DEP and DOE INGENIOUS links and licenses: [`docs/sources.md`](docs/sources.md). Core and aligned rasters came from pinned third-party mirrors; SHA-256 matches do not authenticate them as organizer data.
- Upstream data terms are documented, but no separate derivative-mirror or vendored-code license grant was verified. This is part of the no-promotion decision.
- The current leaderboard and all nine historical scores lack receipts. Conflicting supplied overall leader values 0.4413 and 0.3195 remain unverified.
- The holdout is a static final-raster diagnostic, not nested model selection or a leaderboard estimate. Reusing it for future tuning can overfit. SGMC is a secondary proxy, not proof of fault existence.
- E1 cannot rule out lithologic/depositional contacts, soil/moisture gradients, terrace risers, channel banks or acquisition artifacts. No field verification was performed.
- The 19-band training stack and complete registry are unavailable. E1 does not require the former; the latter prevents any global uniqueness claim.
- The frozen note placed evaluation before writing; execution evaluated final saved bytes after the duplicate was detected, then stopped without another lane or submission. Details: [`docs/protocol.md`](docs/protocol.md).
- Standing brief for future sessions: [`docs/research-brief.md`](docs/research-brief.md).

## GitHub Pages

`docs/index.html` is the dependency-free report. Enable **Settings → Pages → Deploy from a branch → main /docs** after merge. No build service or browser-side localhost request is required.
'''
(ROOT/'README.md').write_text(readme)

result={'schema':'korea8.result-summary.v1','verdict':CARD['verdict'],
        'ok_to_download_and_submit':False,'research_raster':RASTER,'raster_sha256':SHA,
        'holdout_dti':H,'leaderboard_score_estimate':None,'organizer_confirmed_score':None,
        'final_lattice_overlap_3px':LATTICE['final_dot_overlap_within_3px'],
        'registry_complete':False,'format_pass':CARD['validator_output']['all_checks_passed'],
        'focus9':'data/focus9.json','run_card':'run-card.json','weekly_slot_used':False}
(ROOT/'docs/data/result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

verification=ROOT/'evidence/delivery-verification.json'
verification_text='Pending final verifier' if not verification.exists() else ('All independent delivery checks passed' if json.loads(verification.read_text())['all_passed'] else 'VERIFICATION FAILED — inspect evidence')
css=''' :root{--ink:#172033;--muted:#5b6474;--paper:#f6f8fb;--card:#fff;--line:#dfe5ee;--bad:#a52323;--badbg:#fff0ef;--good:#176a4a;--accent:#2455a4}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1220px;margin:auto;padding:32px 20px 64px}h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.1;margin:.2em 0}h2{margin-top:2.2em;border-bottom:1px solid var(--line);padding-bottom:.35em}h3{margin-bottom:.3em}.eyebrow{text-transform:uppercase;letter-spacing:.12em;color:var(--accent);font-weight:750;font-size:.8rem}.verdict{background:var(--badbg);border:2px solid var(--bad);border-radius:14px;padding:22px;margin:24px 0}.verdict strong{color:var(--bad)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}.metric{font-size:1.35rem;font-weight:750}.muted{color:var(--muted)}code{overflow-wrap:anywhere;background:#edf1f7;padding:.1em .3em;border-radius:4px}a{color:var(--accent)}a.button,button.button{display:inline-block;border-radius:8px;padding:11px 16px;text-decoration:none;font-weight:700;margin:6px 8px 6px 0;border:0}a.research{background:var(--ink);color:white}.disabled{background:#d5dae2;color:#646c78;cursor:not-allowed}.pill{padding:.15em .55em;border-radius:999px;font-size:.8rem;font-weight:750}.bad{background:var(--badbg);color:var(--bad)}.good{background:#e8f7f0;color:var(--good)}.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);white-space:nowrap}th{background:#edf2f8;position:sticky;top:0}tr:last-child td{border-bottom:0}.note{border-left:4px solid var(--accent);padding-left:16px}.footer{margin-top:48px;padding-top:20px;border-top:1px solid var(--line);font-size:.9rem;color:var(--muted)}@media(max-width:600px){main{padding:20px 12px}.card{padding:14px}th,td{padding:9px}}'''
(ROOT/'docs/css').mkdir(parents=True,exist_ok=True)
(ROOT/'docs/css/style.css').write_text(css+'\n')
(ROOT/'docs/.nojekyll').write_text('')
html_doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Auditable negative GEMS fault-discovery result; no approved submission."><title>Korea8 · GEMS fault research</title><link rel="stylesheet" href="css/style.css"></head><body><main>
<div class="eyebrow">Autonomous GEMS research · 2026-11-04</div><h1>Fault discovery,<br>without score theatre.</h1><p class="muted">Maximize P(Win). Own the Outcome. One pre-registered hypothesis, shared spatial holdout, explicit uniqueness gates.</p>
<section class="verdict" aria-label="Submission decision"><h2 style="margin-top:0">NEGATIVE — DO NOT SUBMIT</h2><p>The new E1 raster is format-valid but fails the mandatory 13GEMSDOE duplicate/lane-drift gate and the holdout baseline. <strong>No approved submission exists.</strong> No weekly slot was used.</p><a class="button disabled" aria-disabled="true">Submission download unavailable</a><a class="button research" href="research/{html.escape(FILENAME)}" download>Download research-only TIFF</a><p class="muted">Research download is for audit, not competition upload.</p></section>
<div class="grid"><div class="card"><div class="muted">HOLDOUT-DTI</div><div class="metric">{f(H['pooled_dti'])}</div><div>95% CI {ci(H['ci95'])}</div><small>{H['evaluator_version']} · {H['withheld_positives']:,} positives</small></div><div class="card"><div class="muted">Focus holdout baseline</div><div class="metric">{f(FOCUS['holdout_baseline_max'])}</div><div><span class="pill bad">Not beaten</span></div></div><div class="card"><div class="muted">Final lattice overlap</div><div class="metric">{100*LATTICE['final_dot_overlap_within_3px']:.4f}%</div><div><span class="pill bad">Duplicate stop &gt;70%</span></div></div><div class="card"><div class="muted">Saved-byte format</div><div class="metric"><span class="pill good">Pass</span></div><div>12,279,160 finite values in [0,1]</div></div></div>
<p class="note"><strong>No leaderboard estimate.</strong> Holdout and SGMC diagnostics are not organizer scores. The scoped registry is incomplete, no separate selector approved a lane, and the supplied method paragraph was absent.</p>
<h2 id="artifact">Artifact identity</h2><div class="card"><p><strong>Research file:</strong> <code>{html.escape(FILENAME)}</code></p><p><strong>SHA-256:</strong> <code>{SHA}</code></p><p><strong>Mechanism:</strong> {html.escape(CARD['mechanism'])}</p><p><a href="run-card.json">Full run card JSON</a> · <a href="data/result.json">Result summary JSON</a> · <a href="data/focus9.json">Nine-site evidence JSON</a> · <a href="data/verification.json">Delivery verification</a></p><p class="muted">{html.escape(verification_text)}</p></div>
<h2 id="sites">Nine priority sites</h2><p>Historical scores are user-reported, not receipts. All HOLDOUT-DTI rows use {H['evaluator_version']}, 22,232 withheld positives, 140 clusters and 1,000 bootstrap repetitions. Every historical row is a near-duplicate and ineligible as a new submission.</p><div class="tablewrap"><table><thead><tr><th>Site</th><th>User score*</th><th>HOLDOUT-DTI</th><th>95% CI</th><th>Dots</th><th>Worst other-focus overlap</th><th>Submit?</th></tr></thead><tbody>{site_table_html()}</tbody></table></div>
<h2 id="champion">Why did GEMSDOE32 reportedly lead?</h2><p>The reported 0.2778 has no inspected receipt. Exact set algebra shows 44,090 D2.8 dots pruned by a 100 m catalogue collar to 40,199, then by a 200 m collar to 37,654. No dots were added. Under distance-weighted DTI and official known-fault masking this can reduce low-credit false-positive mass, but private-label causation is unproven.</p><p>GEMSDOE32’s HOLDOUT-DTI is only 0.004515379, versus 0.096743304 for GEMSDOE25/30. Descriptive score–holdout Spearman ρ is −0.848739 (n=9), not a leaderboard calibration. Whether 0.2778 can be beaten remains unknown; E1 does not establish it.</p>
<h2 id="hypotheses">Ranked hypothesis slate</h2><div class="tablewrap"><table><thead><tr><th>Rank</th><th>Physical hypothesis</th><th>Expected value / cost</th><th>Named mimics</th></tr></thead><tbody>{hypotheses_html()}</tbody></table></div><p>Only E1 was run. Its maximum single-feature orientation-free AUC was 0.564168, below the 0.90 leakage alarm. Low AUC alarms do not establish geological validity.</p>
<h2 id="submit">Submission instructions</h2><ol><li><strong>Do not upload this E1 or any historical focus raster.</strong></li><li>A future candidate needs a <code>promote</code> run card, every format/holdout/uniqueness/provenance gate, separate selector approval and an explicit weekly-slot decision.</li><li>Only then use its zero-outside float32 variant, unique name and ≤140-character note through the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/">official portal instructions</a>. Preserve validator evidence.</li><li>Never present a holdout, SGMC value, expected credit or projection as an organizer-confirmed score.</li></ol>
<h2 id="limits">Sources and limitations</h2><ul><li><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/">Official format/metric</a>; <a href="https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516">official known-fault masking clarification</a>; <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/rules/">official rules gateway</a>.</li><li><a href="https://www.sciencebase.gov/catalog/item/657e1d85d34e23d3533209f7">USGS GeoDAWN (CC0/public domain)</a>; <a href="https://www.usgs.gov/3d-elevation-program">USGS 3DEP (free, without use restrictions)</a>; <a href="https://gdr.openei.org/submissions/1391">DOE INGENIOUS (CC BY 4.0)</a>.</li><li>Aligned rasters and tools are pinned third-party mirrors, not organizer-authenticated inputs. Separate derivative/code license grants were not verified.</li><li>No complete registry, 19-band training stack, current leaderboard receipt, private labels or field verification. The lattice’s 99.871327% footprint coverage makes representative uniqueness infeasible under the literal rule.</li><li>E1 cannot exclude lithologic/depositional contacts, soil/moisture gradients, terrace risers, channel banks or acquisition artifacts. Static holdout reuse can overfit future research.</li></ul>
<div class="footer">Korea8 · Generated from run-card.json and docs/data/focus9.json · <a href="https://github.com/karagemop466-tech/Korea8">Source repository</a><br>Current decision: <strong>negative</strong>. Format validity never overrides uniqueness, validation or provenance.</div>
</main></body></html>'''
(ROOT/'docs/index.html').write_text(html_doc)
print(f'Rendered README, docs/index.html and docs/data/result.json for {CARD["verdict"]} verdict')

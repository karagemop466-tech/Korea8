#!/usr/bin/env python3
"""Build a static GitHub Pages evidence site from evidence/*.json.

The download button is at the top of the home page. A red/green banner makes the
submit / do-not-submit verdict obvious. No human inspection is required.
"""
from __future__ import annotations

import html
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EVID = ROOT / "evidence"

SITES = [
    ("GEMSDOE24", "0.2477", "60,069", "nan-outside dot family"),
    ("GEMSDOE25", "0.2600", "44,090", "d28 dot family"),
    ("GEMSDOE27", "0.2449", "61,328", "nan-outside dot family"),
    ("GEMSDOE28", "0.2710", "37,660", "rung30 blind dot family"),
    ("GEMSDOE30", "0.2600", "44,090", "poisson300m off-cat d28"),
    ("GEMSDOE31", "0.2708", "40,199", "solo-d28"),
    ("GEMSDOE32", "0.2778", "37,654", "h33-h33-2-b2 zeros (subset of 25)"),
    ("GEMSDOE33", "0.2632", "41,865", "analog-tip-stepover-r30"),
    ("GEMSDOE36", "0.2750", "38,854", "anderson-geothermal-pinn"),
]


def load(name: str, default=None):
    p = EVID / name
    if not p.exists():
        return default
    return json.loads(p.read_text())


def esc(x) -> str:
    return html.escape(str(x))


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "downloads").mkdir(parents=True, exist_ok=True)
    (DOCS / "evidence").mkdir(parents=True, exist_ok=True)
    for p in EVID.glob("*.json"):
        (DOCS / "evidence" / p.name).write_text(p.read_text())
    card = load("run_card.json", {})
    hold = load("holdout.json", {})
    uniq = load("uniqueness_final.json", {})
    fmt = load("format_report.json", {})
    verdict = card.get("verdict", "pending")
    ok = verdict == "promote"
    banner_color = "#1a7f37" if ok else "#b42318"
    banner_text = ("OK TO SUBMIT — all gates passed" if ok else
                   "DO NOT SUBMIT — uniqueness/format/holdout gate failed (fail-closed)")
    raster = card.get("raster_path", "downloads/korea8_candidate.tif")
    raster_name = Path(raster).name
    sha = card.get("raster_sha256", "pending")
    dots = card.get("emitted_dots", "pending")
    dti = card.get("holdout", {}).get("pooled_dti")
    ci = card.get("holdout", {}).get("ci95", [None, None])
    dti_str = f"{dti:.4f}" if isinstance(dti, (int, float)) else "pending"
    ci_str = f"[{ci[0]:.4f}, {ci[1]:.4f}]" if ci[0] is not None else "pending"

    rows = []
    for site, score, ndots, note in SITES:
        rows.append(f"<tr><td>{esc(site)}</td><td>{esc(score)} <span class='tag'>USER-REPORTED</span></td>"
                    f"<td>{esc(ndots)}</td><td>{esc(note)}</td><td>near-duplicate dot family</td></tr>")
    rows.append(f"<tr class='candidate'><td>Korea8 candidate</td><td>{dti_str} <span class='tag'>HOLDOUT-DTI</span></td>"
                f"<td>{esc(dots)}</td><td>{esc(card.get('hypothesis','H1'))}</td>"
                f"<td>{'unique' if uniq.get('unique') else 'duplicate/drift vs registry'}</td></tr>")
    table = "\n".join(rows)

    index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Korea8 — DOE GEMS fault prediction</title>
<link rel="stylesheet" href="style.css"></head>
<body>
<header>
  <h1>Korea8 — DOE GEMS Prize Challenge</h1>
  <p class="sub">Auditable, fail-closed fault-prediction research. Generated {esc(time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()))}.</p>
</header>

<section class="download" id="download">
  <h2>Download candidate GeoTIFF</h2>
  <div class="banner" style="background:{banner_color}">{esc(banner_text)}</div>
  <p><a class="btn" href="downloads/{esc(raster_name)}" download>⬇ {esc(raster_name)}</a></p>
  <p class="mono">SHA-256: {esc(sha)}<br>Emitted dots: {esc(dots)} · HOLDOUT-DTI: {dti_str} (95% CI {ci_str})</p>
  <p><strong>Verdict:</strong> {esc(verdict)}. <a href="submit.html">Submission instructions &rarr;</a></p>
</section>

<section>
  <h2>Executive summary — requested sites</h2>
  <p>Scores below are <strong>USER-REPORTED</strong>, not organizer-confirmed receipts. The live leaderboard is client-rendered and was not independently scraped in this pass.</p>
  <table><thead><tr><th>Site</th><th>Score (evidence label)</th><th>Dots</th><th>Mechanism</th><th>Uniqueness</th></tr></thead>
  <tbody>{table}</tbody></table>
</section>

<section>
  <h2>Why GEMSDOE32 reported 0.2778</h2>
  <p>GEMSDOE32 is a strict subset of GEMSDOE25's 44,090 dots with 6,436 zero-credit dots (1–2 px from the catalogue) removed. For a binary map, DTI = TP / (0.2·D + 0.8·N); deleting zero-credit mass strictly raises the score. This is dot-pruning arithmetic, not hidden-fault detection skill.</p>
</section>

<section>
  <h2>Evidence</h2>
  <ul>
    <li><a href="evidence/run_card.json">run_card.json</a></li>
    <li><a href="evidence/holdout.json">holdout.json</a></li>
    <li><a href="evidence/uniqueness_final.json">uniqueness_final.json</a></li>
    <li><a href="evidence/format_report.json">format_report.json</a></li>
    <li><a href="evidence/canary.json">canary.json</a></li>
  </ul>
</section>

<footer><p>No contest submission was performed. Lane unspecified in brief; pre-registered H1. Data mirrors are hash-pinned but not organizer-authenticated.</p></footer>
</body></html>"""
    (DOCS / "index.html").write_text(index)

    submit = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Submission instructions — Korea8</title><link rel="stylesheet" href="style.css"></head>
<body><header><h1>Submission instructions</h1><p><a href="index.html">&larr; Home</a></p></header>
<section><div class="banner" style="background:{banner_color}">{esc(banner_text)}</div>
<h2>Before you upload</h2>
<ol>
  <li>Confirm the verdict above is <strong>promote</strong>. If it is <strong>negative</strong>, do not upload.</li>
  <li>Download <code>{esc(raster_name)}</code> and verify SHA-256 <code>{esc(sha)}</code>.</li>
  <li>The file is single-band float32, EPSG:32611, 3730×3292, 100 m. Outside-footprint cells are finite 0 with a GDAL internal mask band declaring them null. This avoids the portal error <em>"Predicted values must be in range [0, 1]"</em>.</li>
  <li>Use submission name <code>{esc(card.get('submission_name','korea8-accommodation-transfer-v1'))}</code>.</li>
  <li>Note (≤140 chars): <code>{esc(card.get('submission_note',''))}</code></li>
  <li>Weekly cap: 3 submissions/week (NLR rules); DrivenData page says 1 scored/UTC day. Do not exceed the stricter cap.</li>
  <li>Generative-AI disclosure is mandatory under the official rules.</li>
</ol>
<p>This site never performs an upload. A human selector must confirm the verdict and spend a slot.</p>
</section></body></html>"""
    (DOCS / "submit.html").write_text(submit)

    css = """body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:980px;margin:0 auto;padding:1.5rem;color:#1a1a1a;line-height:1.5}
header h1{margin-bottom:.2rem}.sub{color:#555}
.banner{color:#fff;padding:.8rem 1rem;border-radius:8px;font-weight:700;margin:.8rem 0}
.btn{display:inline-block;background:#0b5fff;color:#fff;padding:.7rem 1.2rem;border-radius:8px;text-decoration:none;font-weight:700}
table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{border:1px solid #ddd;padding:.5rem;text-align:left}
th{background:#f4f4f4}.candidate{background:#eef6ff}.tag{font-size:.7rem;background:#eee;border-radius:4px;padding:.1rem .3rem;color:#555}
.mono{font-family:ui-monospace,monospace;font-size:.85rem;word-break:break-all}
section{margin:2rem 0}footer{color:#666;font-size:.85rem;border-top:1px solid #eee;padding-top:1rem}
"""
    (DOCS / "style.css").write_text(css)
    (DOCS / ".nojekyll").write_text("")
    print("[site] built docs/index.html, submit.html, evidence/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

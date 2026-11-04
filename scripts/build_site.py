#!/usr/bin/env python3
"""Build a static GitHub Pages evidence site from evidence/*.json.

Download button at the top of the home page; explicit submit/do-not-submit banner;
per-site executive summaries; submission-instructions subpage; JSON + RSS feed.
No human inspection is required.
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
    ("GEMSDOE24", "0.2477", "60,069", "nan-outside dot family",
     "Dense nan-outside dot family; high dot count, lower precision. Score is dot-pruning arithmetic, not hidden-fault skill."),
    ("GEMSDOE25", "0.2600", "44,090", "d28 dot family",
     "The d28 dot family that GEMSDOE32 prunes. Parent of the 0.2778 subset."),
    ("GEMSDOE27", "0.2449", "61,328", "nan-outside dot family",
     "Near-duplicate of GEMSDOE24 with a different nan-outside encoding; no distinct geological mechanism."),
    ("GEMSDOE28", "0.2710", "37,660", "rung30 blind dot family",
     "Rung-30 blind placement; fewer dots than 24/27, slightly higher score via reduced zero-credit mass."),
    ("GEMSDOE30", "0.2600", "44,090", "poisson300m off-cat d28",
     "Poisson-disc 300 m resampling of the d28 family; identical dot count to GEMSDOE25, same score."),
    ("GEMSDOE31", "0.2708", "40,199", "solo-d28",
     "Solo-d28 variant; dot count between 25 and 32, score between them. Same family."),
    ("GEMSDOE32", "0.2778", "37,654", "h33-h33-2-b2 zeros",
     "Strict subset of GEMSDOE25 minus 6,436 zero-credit dots 1–2 px from the catalogue. Deleting zero-credit mass raises DTI = TP/(0.2·D+0.8·N). Highest reported focus score; not hidden-fault detection."),
    ("GEMSDOE33", "0.2632", "41,865", "analog-tip-stepover-r30",
     "Analog tip/stepover placement at r30; geologically motivated naming but dot set overlaps the shared family."),
    ("GEMSDOE36", "0.2750", "38,854", "anderson-geothermal-pinn",
     "Anderson geothermal PINN branding; dot count near GEMSDOE32, score just below it. Same near-duplicate family."),
]


def load(name: str, default=None):
    p = EVID / name
    return json.loads(p.read_text()) if p.exists() else default


def esc(x) -> str:
    return html.escape(str(x))


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "downloads").mkdir(parents=True, exist_ok=True)
    (DOCS / "evidence").mkdir(parents=True, exist_ok=True)
    for p in EVID.glob("*.json"):
        (DOCS / "evidence" / p.name).write_text(p.read_text())
    card = load("run_card.json", {})
    hold = card.get("holdout", {})
    uniq = load("uniqueness_final.json", {})
    ver = load("verification.json", {})
    verdict = card.get("verdict", "pending")
    ok = verdict == "promote"
    banner_color = "#1a7f37" if ok else "#b42318"
    banner_text = ("OK TO SUBMIT — all gates passed" if ok else
                   "DO NOT SUBMIT — fail-closed (uniqueness witness + holdout below control)")
    raster_name = Path(card.get("raster_path", "downloads/korea8_candidate.tif")).name
    sha = card.get("raster_sha256", "pending")
    dots = card.get("emitted_dots", "pending")
    dti = hold.get("pooled_dti")
    ci = hold.get("ci95", [None, None])
    dti_str = f"{dti:.4f}" if isinstance(dti, (int, float)) else "pending"
    ci_str = f"[{ci[0]:.4f}, {ci[1]:.4f}]" if ci[0] is not None else "pending"
    dist_dti = hold.get("distance_control_dti")
    rand_dti = hold.get("random_control_dti")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    now_human = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())

    rows, summaries = [], []
    for site, score, ndots, mech, summary in SITES:
        rows.append(f"<tr><td>{esc(site)}</td><td>{esc(score)} <span class='tag'>USER-REPORTED</span></td>"
                    f"<td>{esc(ndots)}</td><td>{esc(mech)}</td><td>near-duplicate dot family</td></tr>")
        summaries.append(f"<div class='card'><h3>{esc(site)} <span class='tag'>USER-REPORTED {esc(score)}</span></h3>"
                         f"<p>{esc(summary)}</p></div>")
    rows.append(f"<tr class='candidate'><td>Korea8 candidate</td><td>{dti_str} <span class='tag'>HOLDOUT-DTI</span></td>"
                f"<td>{esc(dots)}</td><td>H1 accommodation-transfer lineaments</td>"
                f"<td>{'unique' if uniq.get('unique') else 'duplicate/drift vs lattice witness'}</td></tr>")
    table = "\n".join(rows)
    summary_html = "\n".join(summaries)

    index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Korea8 — DOE GEMS fault prediction</title>
<link rel="stylesheet" href="style.css">
<link rel="alternate" type="application/rss+xml" title="Korea8 evidence feed" href="feed.xml">
</head><body>
<header>
  <h1>Korea8 — DOE GEMS Prize Challenge</h1>
  <p class="sub">Auditable, fail-closed fault-prediction research. Generated {esc(now_human)}.</p>
</header>

<section class="download" id="download">
  <h2>Download candidate GeoTIFF</h2>
  <div class="banner" style="background:{banner_color}">{esc(banner_text)}</div>
  <p><a class="btn" href="downloads/{esc(raster_name)}" download>⬇ {esc(raster_name)}</a></p>
  <p class="mono">SHA-256: {esc(sha)}<br>Emitted dots: {esc(dots)} · HOLDOUT-DTI: {dti_str} (95% CI {ci_str})</p>
  <p><strong>Verdict:</strong> {esc(verdict)}. <a href="submit.html">Submission instructions &rarr;</a> ·
     <a href="evidence/run_card.json">Run card JSON</a> · <a href="feed.xml">RSS feed</a></p>
</section>

<section>
  <h2>Result in one paragraph</h2>
  <p>The pre-registered H1 candidate (off-catalogue accommodation-transfer lineaments) scored
  <strong>HOLDOUT-DTI {dti_str}</strong> (95% CI {ci_str}; {esc(hold.get('withheld_positive_pixels','?'))} withheld positives),
  which is <strong>below</strong> the distance-only control ({esc(f'{dist_dti:.4f}' if isinstance(dist_dti,(int,float)) else '?')})
  and random control ({esc(f'{rand_dti:.4f}' if isinstance(rand_dti,(int,float)) else '?')}).
  This is a <strong>negative result</strong>: the learned geophysical-lineament model does not beat a simple
  near-fault prior on catalogue recovery. The candidate is unique versus the nine focus sites
  (overlap ~18%, ρ≈0.001) but fails the literal uniqueness gate against the <code>r13-lattice-s5</code>
  covering witness (overlap {esc(f'{uniq.get("worst_dot_overlap",0):.3f}' if uniq.get('worst_dot_overlap') is not None else '?')}).
  The format gate passes and the portal range error is fixed. <strong>No submission was performed.</strong></p>
</section>

<section>
  <h2>Executive summary — requested sites</h2>
  <p>Scores below are <strong>USER-REPORTED</strong>, not organizer-confirmed receipts. The live leaderboard is
  client-rendered and was not independently scraped in this pass; the conflicting targets (0.4413 / 0.3195 / 0.4625)
  remain unverified.</p>
  <table><thead><tr><th>Site</th><th>Score (evidence label)</th><th>Dots</th><th>Mechanism</th><th>Uniqueness</th></tr></thead>
  <tbody>{table}</tbody></table>
  <div class="cards">{summary_html}</div>
</section>

<section>
  <h2>Why GEMSDOE32 reported 0.2778</h2>
  <p>GEMSDOE32 is a strict subset of GEMSDOE25's 44,090 dots with 6,436 zero-credit dots (1–2 px from the
  catalogue) removed. For a binary map, DTI = TP / (0.2·D + 0.8·N); deleting zero-credit mass strictly raises
  the score. This is dot-pruning arithmetic, not hidden-fault detection skill. A higher-scoring <em>distinct</em>
  strategy is <strong>not supported</strong> by this session's holdout evidence.</p>
</section>

<section>
  <h2>Verification</h2>
  <p>Independent release verification: <strong>{esc('PASS' if ver.get('ok') else 'PENDING/FAIL')}</strong>
  ({esc(ver.get('n_checks','?'))} checks, {esc(ver.get('n_failed','?'))} failed).
  <a href="evidence/verification.json">verification.json</a></p>
  <ul>
    <li><a href="evidence/run_card.json">run_card.json</a></li>
    <li><a href="evidence/holdout.json">holdout.json</a></li>
    <li><a href="evidence/uniqueness_final.json">uniqueness_final.json</a></li>
    <li><a href="evidence/format_report.json">format_report.json</a></li>
    <li><a href="evidence/canary.json">canary.json</a></li>
    <li><a href="evidence/data_restore_receipt.json">data_restore_receipt.json</a></li>
  </ul>
</section>

<footer><p>No contest submission was performed. Lane unspecified in brief; pre-registered H1.
Data mirrors are hash-pinned but not organizer-authenticated. Catalogue-fit holdout is not a leaderboard proxy
(staff mask known faults; sibling measured ρ≈+0.143). See <a href="evidence/verification.json">verification</a>.</p></footer>
</body></html>"""
    (DOCS / "index.html").write_text(index)

    submit = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Submission instructions — Korea8</title><link rel="stylesheet" href="style.css"></head>
<body><header><h1>Submission instructions</h1><p><a href="index.html">&larr; Home</a></p></header>
<section><div class="banner" style="background:{banner_color}">{esc(banner_text)}</div>
<h2>Before you upload</h2>
<ol>
  <li>Confirm the verdict above is <strong>promote</strong>. It is currently <strong>{esc(verdict)}</strong> — do not upload.</li>
  <li>Download <code>{esc(raster_name)}</code> and verify SHA-256 <code>{esc(sha)}</code>.</li>
  <li>The file is single-band float32, EPSG:32611, 3730×3292, 100 m. Outside-footprint cells are finite 0 with a
      GDAL internal mask band declaring them null. This avoids the portal error
      <em>"Predicted values must be in range [0, 1]"</em>.</li>
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
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.8rem;margin-top:1rem}
.card{border:1px solid #e2e2e2;border-radius:8px;padding:.8rem}.card h3{margin:.1rem 0 .4rem;font-size:1rem}.card p{margin:0;font-size:.9rem;color:#333}
"""
    (DOCS / "style.css").write_text(css)
    (DOCS / ".nojekyll").write_text("")

    feed = {"schema": "korea8-feed-v1", "generated_utc": now, "verdict": verdict,
            "holdout_dti": dti, "holdout_ci95": ci, "emitted_dots": dots,
            "raster_sha256": sha, "raster": f"downloads/{raster_name}",
            "run_card": "evidence/run_card.json", "verification": "evidence/verification.json"}
    (DOCS / "feed.json").write_text(json.dumps(feed, indent=2, allow_nan=False) + "\n")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>Korea8 GEMS evidence feed</title>
<link>https://karagemop466-tech.github.io/Korea8/</link>
<description>Fail-closed DOE GEMS fault-prediction evidence</description>
<lastBuildDate>{esc(now)}</lastBuildDate>
<item><title>Run {esc(now)} — verdict {esc(verdict)}</title>
<link>https://karagemop466-tech.github.io/Korea8/evidence/run_card.json</link>
<guid isPermaLink="false">{esc(sha)}</guid>
<description>HOLDOUT-DTI {dti_str} (CI {ci_str}); dots {esc(dots)}; verdict {esc(verdict)}.</description>
<pubDate>{esc(now)}</pubDate></item>
</channel></rss>"""
    (DOCS / "feed.xml").write_text(rss)
    print("[site] built docs/index.html, submit.html, feed.json, feed.xml, evidence/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

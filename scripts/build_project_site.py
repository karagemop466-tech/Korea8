#!/usr/bin/env python3
"""Build the Bathtub Trip Lever project site (GitHub Pages, repo root).

Reads canonical data from project/*.json and generates static HTML at the repo
root (what GitHub Pages serves from `main`). Enforces the project's verification
rules:
  1. Every data row (estimates, benchmarks, providers, findings, sources, flags,
     key numbers where applicable) must carry >= 1 source link; build fails otherwise.
  2. Unverified values render as blank cells with a pointer to the
     Flagged-for-Review page - never inferred.
  3. All internal links are checked against the built file set; build fails on
     broken internal links.

Outputs: index.html, executive-summary.html, requirements.html, estimates.html,
providers.html, technical-approach.html, sources.html, flagged-for-review.html,
style.css, project/EXECUTIVE_SUMMARY.md, site-data/build-report.json
"""
import json
import os
import sys
from datetime import datetime, timezone
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "project")
OUT = ROOT

BUILD_STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def load(name):
    with open(os.path.join(PROJ, name), encoding="utf-8") as f:
        return json.load(f)


requirements = load("requirements.json")
estimates = load("estimates.json")
providers = load("providers.json")
sources = load("sources.json")
technical = load("technical.json")
flagged = load("flagged.json")
summary = load("summary.json")

errors = []

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("requirements.html", "Requirements"),
    ("estimates.html", "Estimates"),
    ("providers.html", "Providers"),
    ("technical-approach.html", "Technical Approach"),
    ("sources.html", "Sources"),
    ("flagged-for-review.html", "Flagged for Review"),
]


def links_html(links, flags=False):
    if not links:
        return '<span class="blank">—</span>'
    out = []
    for l in links:
        label = escape(l["label"])
        url = escape(l["url"], quote=True)
        cls = "srclink flagged-link" if flags else "srclink"
        out.append(f'<a class="{cls}" href="{url}" target="_blank" rel="noopener">{label}</a>')
    return " ".join(out)


def badge(ok, ok_text, bad_text):
    if ok:
        return f'<span class="badge badge-ok">{escape(ok_text)}</span>'
    return f'<span class="badge badge-warn">{escape(bad_text)}</span>'


def page(title, active, body, description=""):
    nav_items = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        nav_items.append(f'<a href="{href}"{cls}>{escape(label)}</a>')
    nav_html = "".join(nav_items)
    desc = f'<meta name="description" content="{escape(description)}">' if description else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} — Bathtub Overflow Trip Lever Project</title>
{desc}
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="index.html"><span class="brand-mark">◧</span> Trip Lever Project</a>
    <nav class="nav">{nav_html}</nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="wrap footer">
  <p>Bathtub wastewater overflow trip lever — requirements, estimates &amp; provider research ·
     Built {BUILD_STAMP} · Data: <a href="https://github.com/karagemop466-tech/Korea8/tree/main/project" target="_blank" rel="noopener">project/ (GitHub)</a> ·
     Board: <a href="https://github.com/karagemop466-tech/Korea8/blob/main/COORDINATION.md" target="_blank" rel="noopener">COORDINATION.md</a></p>
  <p class="muted">This dashboard is the canonical project site (resolved 2026-11-07 — see <a href="flagged-for-review.html#F-11">F-11</a>).
     Archived parallel-session briefs (superseded drafts, kept for traceability — each carries an archive banner):
     <a href="trip-lever/executive-summary.html">trip-lever/ dossier</a> ·
     <a href="bathroom-overflow/index.html">bathroom-overflow/ field brief</a> ·
     <a href="bathtub-overflow/index.html">bathtub-overflow/ data dossier</a> ·
     <a href="bathtub/index.html">bathtub/ independent verification dossier</a> ·
     <a href="docs/bathtub-summary.html">docs/ bathtub summary</a>.
     Legacy archive (unrelated prior project, preserved): <a href="docs/index.html">DOE GEMS evidence site</a>.
     Licenses re-verified {escape(providers["meta"]["verified_date"])} via official CSLB pages — statuses can change; re-check before contracting.</p>
</footer>
</body>
</html>"""


def table(headers, rows, cls="grid"):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def enforce(links, ctx, min_links=1):
    if len(links or []) < min_links:
        errors.append(f"{ctx}: expected >= {min_links} source link(s), found {len(links or [])}")


# ---------------- index.html ----------------
quoted = {e["provider_as_quoted"] for e in estimates["estimates"]}
multi_trade = [p for p in providers["providers"] if "B General Building" in p["classifications"] or "B-2 Residential Remodeling" in p["classifications"]]
documented = [p for p in providers["providers"] if "recent-jobs" in (p.get("source_links") or [{}])[0].get("url", "")]

idx_quotes = []
for e in estimates["estimates"]:
    enforce(e["source_links"], f"estimate {e['id']} (index mini-table)")
    idx_quotes.append([
        f'<a href="estimates.html#{e["id"]}">{e["id"]}</a>',
        escape(e["provider_as_quoted"]),
        escape(e["quoted_scope"]),
        f'<strong>${e["price_usd"]}</strong>',
        badge(False, "", "user-provided — unverified (F-02)"),
    ])

idx_providers = []
for p in multi_trade + documented:
    enforce(p["source_links"], f"provider {p['id']} (index mini-table)")
    if "B General Building" in p["classifications"]:
        tag = "multi-trade license (B, with C-36)" if "C-36 Plumbing" in p["classifications"] else "B general building (multi-trade prime)"
    elif "B-2 Residential Remodeling" in p["classifications"]:
        tag = "B-2 residential remodeling license"
    else:
        tag = "documented tub W&amp;O job in SF"
    idx_providers.append([
        f'<a href="providers.html#{p["id"]}">{escape(p["name"])}</a>',
        f'<a class="srclink" href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={p["license_number"]}" target="_blank" rel="noopener">#{p["license_number"]}</a>',
        escape(", ".join(p["classifications"])),
        f'<span class="pill">{tag}</span>',
    ])

idx_body = f"""
<section class="hero">
  <h1>Bathtub Wastewater Overflow <span class="accent">Trip Lever</span> — Repair Coordination</h1>
  <p class="lede">A stuck trip lever inside hidden plumbing behind the wall of a tenant-occupied
  San Francisco unit. 5+ licensed plumbers could not remove it from above. This dashboard collects the
  requirements, the three received estimates, and license-verified San Francisco providers — every row
  sourced, unverified values flagged, nothing inferred.</p>
  <div class="cta-row">
    <a class="btn" href="executive-summary.html">Read the executive summary</a>
    <a class="btn btn-ghost" href="providers.html">Browse verified providers</a>
    <a class="btn btn-ghost" href="flagged-for-review.html">Flagged for review ({len(flagged["flags"])})</a>
  </div>
</section>

<section class="cards">
  <div class="card"><div class="card-num">{len(estimates["estimates"])}</div><div class="card-label">estimates received<br>(2026-08-30, unverified)</div></div>
  <div class="card"><div class="card-num">{len(providers["providers"])}</div><div class="card-label">listed providers, all licenses<br>re-verified 2026-11-07 (CSLB)</div></div>
  <div class="card"><div class="card-num">{len(multi_trade)}</div><div class="card-label">can prime a multi-trade<br>(plumbing+drywall) contract</div></div>
  <div class="card"><div class="card-num">{len(documented)}</div><div class="card-label">documented tub W&amp;O<br>replacement job in SF</div></div>
  <div class="card card-warn"><div class="card-num">{len(flagged["flags"])}</div><div class="card-label">items flagged<br>for owner review</div></div>
</section>

<section>
  <div class="sec-head"><h2>Estimates at a glance</h2><a class="more" href="estimates.html">All details →</a></div>
  {table(["ID", "Provider (as quoted)", "Scope", "Price (USD)", "Verification"], idx_quotes)}
  <p class="note">Quotes are user-provided (2026-08-30) and were not re-verifiable against any official source — published as-is with <a href="flagged-for-review.html#F-02">flag F-02</a>. Third-party 2026 benchmarks for tub drain work: <strong>$200–$1,025</strong> (<a class="srclink" href="https://homeguide.com/costs/bathtub-repair-cost" target="_blank" rel="noopener">HomeGuide</a>, <a class="srclink" href="https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm" target="_blank" rel="noopener">Angi</a>); drywall patching adds <strong>$300–$930</strong> (<a class="srclink" href="https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm" target="_blank" rel="noopener">Angi</a>).</p>
</section>

<section>
  <div class="sec-head"><h2>Shortlist starters</h2><a class="more" href="providers.html">All {len(providers["providers"])} providers →</a></div>
  {table(["Company", "CSLB license (official)", "Classifications", "Why shortlisted"], idx_providers)}
</section>

<section>
  <div class="sec-head"><h2>The decision in one box</h2></div>
  <div class="callout">
    <p><strong>Preferred path — removal from above.</strong> Re-engage the three quoting companies and get a
    written yes/no on extracting the faceplate and fused internals from the tub side without opening the wall.</p>
    <p><strong>Fallback path — access from below (storage-unit ceiling).</strong> Requires one accountable contract
    covering plumbing <em>and</em> drywall. CSLB's official rule: multi-trade jobs belong with a B-licensed general
    contractor (<a class="srclink" href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx" target="_blank" rel="noopener">source</a>)
    — see <a href="technical-approach.html">Technical Approach</a>. Require a code-aligned 12-inch access panel instead of a solid patch
    (<a class="srclink" href="https://aa.iapmo.org/?code=UPC&amp;chapter=4" target="_blank" rel="noopener">CPC §402.10 via IAPMO</a>).</p>
  </div>
</section>
"""

# ---------------- executive-summary.html ----------------
situation_html = "".join(f"<li>{escape(s)}</li>" for s in summary["situation"])
rec_html = "".join(f"<li>{escape(r)}</li>" for r in summary["recommendations"])
open_html = "".join(f"<li>{escape(o)}</li>" for o in summary["open_items"])

kn_rows = []
for k in summary["key_numbers"]:
    flag = f'<a href="flagged-for-review.html#{k["flag"]}">{k["flag"]}</a>' if k.get("flag") else ""
    kn_rows.append([
        escape(k["metric"]),
        f"<strong>{escape(k['value'])}</strong>",
        escape(k["detail"]),
        badge(k["verified"], "verified (official source)", "unverified"),
        flag,
    ])

exec_body = f"""
<h1>Executive Summary</h1>
<p class="updated">Compiled {escape(summary["meta"]["compiled"])} · session {escape(summary["meta"]["prepared_by"])}</p>

<section>
  <h2>Situation</h2>
  <ul class="bullets">{situation_html}</ul>
</section>

<section>
  <h2>Key numbers</h2>
  {table(["Metric", "Value", "Detail", "Verification", "Flag"], kn_rows)}
</section>

<section>
  <h2>Recommendations</h2>
  <ol class="bullets">{rec_html}</ol>
</section>

<section>
  <h2>Open items</h2>
  <ul class="bullets">{open_html}</ul>
</section>

<section>
  <div class="callout">
    <h2 style="margin-top:0">Verification statement</h2>
    <p>{escape(summary["verification_statement"])}</p>
  </div>
</section>
"""

# ---------------- requirements.html ----------------
req_rows = []
for r in requirements["requirements"]:
    src = escape(r["source"])
    if r["source"].startswith("Project brief"):
        src = f'{escape(r["source"])} · <a class="srclink" href="https://github.com/karagemop466-tech/Korea8/blob/main/project/requirements.json" target="_blank" rel="noopener">data file</a>'
    req_rows.append([
        f'<code>{r["id"]}</code>',
        escape(r["category"]),
        escape(r["requirement"]),
        src,
        escape(r["status"]),
    ])

req_body = f"""
<h1>Requirements</h1>
<p class="updated">Compiled {escape(requirements["meta"]["compiled"])} — public-safe restatements of the project brief;
nothing inferred. {escape(requirements["meta"]["provenance_note"].split(".")[0])}.</p>
{table(["ID", "Category", "Requirement", "Source", "Status"], req_rows)}
"""

# ---------------- estimates.html ----------------
est_rows = []
for e in estimates["estimates"]:
    enforce(e["source_links"], f"estimate {e['id']}")
    est_rows.append([
        f'<span id="{e["id"]}"><code>{e["id"]}</code></span>',
        f'<strong>{escape(e["provider_as_quoted"])}</strong><br><span class="muted small">{escape(e["identified_entity"])}</span>',
        escape(e["date"]),
        escape(e["quoted_scope"]),
        f'<strong>${e["price_usd"]}</strong>',
        badge(False, "", "unverified — user-provided") + f' <span class="muted small">{escape(e["identification_status"])}</span>',
        links_html(e["source_links"]),
    ])

bench_rows = []
for b in estimates["benchmarks_third_party"]:
    bench_rows.append([
        f'<code>{b["id"]}</code>',
        escape(b["metric"]),
        f"<strong>{escape(b['value'])}</strong>",
        f'<span class="pill">third-party guide</span>',
        f'<a class="srclink" href="{escape(b["url"], quote=True)}" target="_blank" rel="noopener">{escape(b["source_label"])}</a>',
    ])

est_body = f"""
<h1>Estimates</h1>
<p class="updated">Quoted {escape(estimates["meta"]["quote_date"])} · recorded {escape(estimates["meta"]["recorded"])}</p>
<div class="callout callout-warn"><p><strong>Verification status:</strong> {escape(estimates["meta"]["verification_note"])}</p></div>
{table(["ID", "Provider (as quoted)", "Date", "Scope", "Price", "Verification", "Source links"], est_rows)}

<h2>Scope analysis</h2>
<p>{escape(estimates["analysis"])}</p>

<h2>Published cost benchmarks (third-party guides)</h2>
{table(["ID", "Metric", "Range", "Type", "Source"], bench_rows)}
"""

# ---------------- providers.html ----------------
def blank(text):
    return '<span class="blank">' + escape(text) + "</span>"


def reviews_cell(p):
    if not p.get("reviews"):
        return blank("— none captured (see F-09)")
    parts = []
    for rv in p["reviews"]:
        rating = ("<strong>" + escape(rv["rating"]) + "</strong>") if rv["rating"] else blank("rating —")
        count = ("<strong>" + escape(rv["count"]) + "</strong> reviews") if rv["count"] else blank("count —")
        parts.append(
            '<div class="rev"><a class="srclink" href="' + escape(rv["url"], quote=True)
            + '" target="_blank" rel="noopener">' + escape(rv["platform"]) + "</a>: "
            + rating + " " + count
            + '<br><span class="muted small">' + escape(rv["as_recorded"]) + "</span></div>"
        )
    return "".join(parts)


prov_rows = []
for p in providers["providers"]:
    # A provider row needs its official CSLB link plus the company site when one is on file.
    enforce(p["source_links"], f"provider {p['id']}", min_links=2 if p.get("website") else 1)
    reviews = reviews_cell(p)
    cslb_url = f'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={p["license_number"]}'
    prov_rows.append([
        f'<span id="{p["id"]}"><code>{p["id"]}</code></span>',
        f'<strong>{escape(p["name"])}</strong><br><span class="muted small">{escape(p["phone"])}</span>',
        f'<a class="srclink" href="{escape(cslb_url, quote=True)}" target="_blank" rel="noopener">#{p["license_number"]}</a>',
        f'{escape(p["license_status"])}<br><span class="muted small">{escape(p["entity_type"])} · exp. {escape(p["expire_date"])}</span>',
        escape(", ".join(p["classifications"])),
        escape(p["address_cslb"]),
        reviews,
        f'{escape(p["relevance"])}<br><span class="muted small">{escape(p["fit_notes"])}</span>',
        links_html(p["source_links"]),
    ])

prov_body = f"""
<h1>Providers — San Francisco</h1>
<p class="updated">License statuses verified {escape(providers["meta"]["verified_date"])} · {escape(providers["meta"]["verification_note"])}</p>
{table(["ID", "Company", "CSLB", "Status (official)", "Classifications", "Address of record", "Reviews (as displayed)", "Relevance & fit", "Source links"], prov_rows)}
"""

# ---------------- technical-approach.html ----------------
tech_rows = []
for t in technical["findings"]:
    tech_rows.append([
        f'<code>{t["id"]}</code>',
        f"<strong>{escape(t['topic'])}</strong>",
        escape(t["finding"]),
        f'<a class="srclink" href="{escape(t["url"], quote=True)}" target="_blank" rel="noopener">{escape(t["source_label"])}</a>',
    ])

tech_body = f"""
<h1>Technical Approach</h1>
<p class="updated">Compiled {escape(technical["meta"]["compiled"])} — {escape(technical["meta"]["note"])}</p>
{table(["ID", "Topic", "Finding (verified)", "Source"], tech_rows)}
"""

# ---------------- sources.html ----------------
type_order = [
    "Official government", "Code publisher", "Code publication (state scan)",
    "Code reprint (complete, unofficial)", "Manufacturer", "Manufacturer index",
    "Provider official site", "Third-party (reputable trade media)",
    "Third-party cost guide", "Third-party (independent ratings org)",
    "Third-party (review platform, bot-blocked)", "Third-party directory",
    "Third-party (community anecdote)",
]
by_type = {}
for s in sources["sources"]:
    by_type.setdefault(s["type"], []).append(s)

src_sections = []
for t in type_order:
    items = by_type.get(t)
    if not items:
        continue
    rows = []
    for s in items:
        rows.append([
            f'<code>{s["id"]}</code>',
            f'<a class="srclink" href="{escape(s["url"], quote=True)}" target="_blank" rel="noopener">{escape(s["title"])}</a>',
            escape(s["used_for"]),
            escape(s["fetched"]),
        ])
    src_sections.append(f"<h2>{escape(t)}</h2>" + table(["ID", "Source (link)", "Used for", "Fetched"], rows))

src_body = f"""
<h1>Sources</h1>
<p class="updated">{escape(sources["meta"]["note"])}</p>
{"".join(src_sections)}
"""

# ---------------- flagged-for-review.html ----------------
sev_class = {"unverified-data": "pill-warn", "discrepancy": "pill-warn",
             "scope-ambiguity": "pill-warn", "gap": "pill-warn",
             "verification-limit": "pill-info", "citation-note": "pill-info",
             "informational": "pill-info"}

flag_blocks = []
for f in flagged["flags"]:
    enforce(f["source_links"], f"flag {f['id']}")
    pill = sev_class.get(f["severity"], "pill-info")
    flag_blocks.append(f"""
<article class="flagcard" id="{f["id"]}">
  <div class="flag-head">
    <code>{f["id"]}</code>
    <span class="pill {pill}">{escape(f["severity"])}</span>
    <h3>{escape(f["title"])}</h3>
  </div>
  <p>{escape(f["detail"])}</p>
  <p class="srclinks">{links_html(f["source_links"], flags=True)}</p>
</article>""")

flag_body = f"""
<h1>Flagged for Review</h1>
<p class="updated">{escape(flagged["meta"]["note"])}</p>
{"".join(flag_blocks)}
"""

# ---------------- style.css ----------------
STYLE = """:root{--bg:#f6f7f9;--panel:#ffffff;--ink:#16212e;--muted:#5b6b7c;--line:#e3e8ee;--brand:#0b5cad;--brand-ink:#0a4a8c;--ok:#0c7a43;--ok-bg:#e7f5ed;--warn:#9a6700;--warn-bg:#fff3d6;--pill:#eef2f6}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.topbar{position:sticky;top:0;background:#ffffffee;backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:10}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 20px;flex-wrap:wrap}
.brand{font-weight:700;color:var(--ink);text-decoration:none;font-size:17px}
.brand-mark{color:var(--brand)}
.nav{display:flex;gap:4px;flex-wrap:wrap}
.nav a{padding:7px 11px;border-radius:8px;color:var(--muted);text-decoration:none;font-size:14px;font-weight:500}
.nav a:hover{background:var(--pill);color:var(--ink)}
.nav a.active{background:var(--brand);color:#fff}
main.wrap{padding:28px 20px 10px}
h1{font-size:30px;margin:8px 0 6px;letter-spacing:-.02em}
h2{font-size:20px;margin:34px 0 12px;letter-spacing:-.01em}
h3{margin:0 0 6px;font-size:16.5px}
.updated{color:var(--muted);font-size:14px;margin:0 0 8px}
.hero{padding:26px 0 8px}
.hero h1{font-size:36px;max-width:900px}
.accent{color:var(--brand)}
.lede{font-size:17.5px;color:var(--muted);max-width:880px}
.cta-row{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 6px}
.btn{display:inline-block;background:var(--brand);color:#fff;padding:10px 16px;border-radius:9px;text-decoration:none;font-weight:600;font-size:15px}
.btn:hover{background:var(--brand-ink)}
.btn-ghost{background:#fff;color:var(--brand);border:1px solid var(--line)}
.btn-ghost:hover{background:var(--pill);color:var(--brand-ink)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:26px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}
.card-num{font-size:34px;font-weight:750;letter-spacing:-.02em}
.card-label{color:var(--muted);font-size:13.5px;margin-top:4px}
.card-warn{background:var(--warn-bg);border-color:#ecd9a0}
.card-warn .card-num{color:var(--warn)}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.sec-head h2{margin-bottom:6px}
.more{font-size:14px;text-decoration:none;color:var(--brand);font-weight:600}
.tablewrap{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th{position:sticky;top:0;background:#fbfcfe;text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fafbfd}
code{background:var(--pill);padding:1px 6px;border-radius:6px;font-size:13px}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12.5px;font-weight:600;white-space:nowrap}
.badge-ok{background:var(--ok-bg);color:var(--ok)}
.badge-warn{background:var(--warn-bg);color:var(--warn)}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;background:var(--pill);font-size:12.5px;font-weight:600;color:#3c4b5c}
.pill-warn{background:var(--warn-bg);color:var(--warn)}
.pill-info{background:#e3edfb;color:var(--brand-ink)}
.srclink{color:var(--brand);text-decoration:none;border-bottom:1px solid #c4d7ef;font-size:14px}
.srclink:hover{border-bottom-color:var(--brand)}
.srclinks .srclink{display:inline-block;margin:2px 10px 2px 0}
.muted{color:var(--muted)}
.small{font-size:13px}
.blank{color:#a5b1bd;font-style:italic}
.note{font-size:14px;color:var(--muted)}
.bullets li{margin:7px 0}
.callout{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--brand);border-radius:12px;padding:16px 20px;margin:14px 0}
.callout-warn{border-left-color:var(--warn);background:#fffdf5}
.rev{margin:2px 0 8px}
.flagcard{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:14px 0}
.flag-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.flag-head h3{margin:0}
.footer{border-top:1px solid var(--line);margin-top:40px;padding:18px 20px 30px;color:var(--muted);font-size:13.5px}
.footer a{color:var(--brand);text-decoration:none}
@media(max-width:640px){.hero h1{font-size:28px}h1{font-size:25px}}
"""

# ---------------- write outputs ----------------
outputs = {
    "index.html": page("Dashboard", "index.html", idx_body,
                       "Bathtub wastewater overflow trip lever repair — requirements, estimates and license-verified San Francisco providers."),
    "executive-summary.html": page("Executive Summary", "executive-summary.html", exec_body,
                                   "Executive summary: situation, key numbers, recommendations, open items, verification statement."),
    "requirements.html": page("Requirements", "requirements.html", req_body,
                              "Full compiled requirements list for the bathtub trip lever repair project."),
    "estimates.html": page("Estimates", "estimates.html", est_body,
                           "The three received estimates with verification status and third-party cost benchmarks."),
    "providers.html": page("Providers", "providers.html", prov_body,
                           f"{len(providers['providers'])} San Francisco-area providers with CSLB-verified license statuses (re-verified {providers['meta']['verified_date']}), classifications, reviews and source links."),
    "technical-approach.html": page("Technical Approach", "technical-approach.html", tech_body,
                                    "Trip lever mechanics, access paths, plumbing code access requirements and licensing structure."),
    "sources.html": page("Sources", "sources.html", src_body,
                         "Master source register: official government, code publisher, manufacturer and third-party sources."),
    "flagged-for-review.html": page("Flagged for Review", "flagged-for-review.html", flag_body,
                                    "Non-blocking flagged items published for owner review, with source links."),
}

# enforcement pass over remaining row types
for s in sources["sources"]:
    if not s.get("url"):
        errors.append(f"source {s['id']}: missing url")
for t in technical["findings"]:
    if not t.get("url"):
        errors.append(f"technical {t['id']}: missing source url")
for b in estimates["benchmarks_third_party"]:
    if not b.get("url"):
        errors.append(f"benchmark {b['id']}: missing source url")

if errors:
    for e in errors:
        print("ENFORCEMENT FAILURE:", e)
    sys.exit(1)

built = []
for fname, content in outputs.items():
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    built.append(fname)
with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as fh:
    fh.write(STYLE)
built.append("style.css")

# internal link check (relative targets must exist as built files or pre-existing repo files)
preexisting = set()
for dirpath, dirnames, filenames in os.walk(OUT):
    dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
    for fn in filenames:
        preexisting.add(os.path.relpath(os.path.join(dirpath, fn), OUT))
import re
broken = []
for fname, content in outputs.items():
    for m in re.finditer(r'(?:href|src)="([^"]+)"', content):
        url = m.group(1)
        if url.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = url.split("#")[0]
        if target and target not in preexisting:
            broken.append(f"{fname} -> {url}")
if broken:
    for b in broken:
        print("BROKEN INTERNAL LINK:", b)
    sys.exit(1)

# executive summary markdown mirror
md = f"""# Executive Summary — Bathtub Wastewater Overflow Trip Lever
_Compiled {summary['meta']['compiled']} · {summary['meta']['prepared_by']} · live page: `executive-summary.html`_

## Situation
""" + "\n".join(f"- {s}" for s in summary["situation"]) + """

## Key numbers

| Metric | Value | Detail | Verification | Flag |
|---|---|---|---|---|
""" + "\n".join(
    f"| {k['metric']} | {k['value']} | {k['detail']} | {'verified (official source)' if k['verified'] else 'unverified'} | {k.get('flag') or ''} |"
    for k in summary["key_numbers"]) + """

## Recommendations
""" + "\n".join(f"{i}. {r}" for i, r in enumerate(summary["recommendations"], 1)) + """

## Open items
""" + "\n".join(f"- {o}" for o in summary["open_items"]) + f"""

## Verification statement
{summary['verification_statement']}
"""
with open(os.path.join(PROJ, "EXECUTIVE_SUMMARY.md"), "w", encoding="utf-8") as fh:
    fh.write(md)
built.append("project/EXECUTIVE_SUMMARY.md")

os.makedirs(os.path.join(OUT, "site-data"), exist_ok=True)
report = {
    "built_at": BUILD_STAMP,
    "outputs": built,
    "enforcement": {
        "rows_with_source_links_checked": len(estimates["estimates"]) + len(estimates["benchmarks_third_party"]) + len(providers["providers"]) + len(technical["findings"]) + len(sources["sources"]) + len(flagged["flags"]),
        "failures": [],
        "broken_internal_links": [],
    },
    "counts": {
        "requirements": len(requirements["requirements"]),
        "estimates": len(estimates["estimates"]),
        "benchmarks": len(estimates["benchmarks_third_party"]),
        "providers": len(providers["providers"]),
        "technical_findings": len(technical["findings"]),
        "sources": len(sources["sources"]),
        "flags": len(flagged["flags"]),
    },
}
with open(os.path.join(OUT, "site-data", "build-report.json"), "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2)
built.append("site-data/build-report.json")

print(f"OK — built {len(built)} outputs; enforcement passed "
      f"({report['enforcement']['rows_with_source_links_checked']} rows link-checked, 0 broken internal links)")

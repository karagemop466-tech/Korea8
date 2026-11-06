#!/usr/bin/env python3
"""Build the trip-lever dashboard site at the repository root.

Inputs : data/tub/*.json
Outputs: index.html, style.css and seven subpages, plus a small JSON feed.

Design rules enforced here:
  * every table row carries a source cell (S-IDs or an explicit UNVERIFIED label);
  * no value is invented -- a missing value renders as a blank cell plus a flag;
  * the site never states or plans around the owner's private constraint.

Run:  python3 scripts/build_tub_site.py
Then: python3 scripts/verify_tub_site.py
"""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tub"

PAGES = {
    "index.html": ("Overview", "Executive summary and the decision in one screen."),
    "providers.html": ("Providers", "Every firm checked, with its CSLB record."),
    "quotes.html": ("Quotes", "The three estimates, normalised by scope."),
    "requirements.html": ("Requirements", "The full requirement list, verified against sources."),
    "rules.html": ("Permits & rules", "Official permit, licensing, tenancy and safety rules."),
    "access.html": ("Scope & access", "From above vs. from below, and what to ask before cutting."),
    "sources.html": ("Sources", "Every source, its publisher, and what it was used for."),
    "flagged.html": ("Flagged for review", "Unverified values, irregularities, and open questions."),
}

CSS = """
:root{--ink:#111827;--muted:#5b6472;--line:#e5e7eb;--bg:#f8fafc;--card:#fff;
--accent:#0f4c81;--ok:#0f7b47;--warn:#a15c00;--bad:#a4161a;--chip:#eef2f7}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header.top{background:var(--accent);color:#fff}
header.top .wrap{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:center;padding-top:14px;padding-bottom:14px}
header.top .brand{font-weight:700;font-size:1.05rem;letter-spacing:.2px}
header.top .brand span{font-weight:400;opacity:.85}
nav.main{display:flex;flex-wrap:wrap;gap:4px;margin-left:auto}
nav.main a{color:#dbe7f3;text-decoration:none;padding:6px 11px;border-radius:6px;font-size:.9rem}
nav.main a:hover{background:rgba(255,255,255,.13);color:#fff}
nav.main a.on{background:#fff;color:var(--accent);font-weight:600}
main{padding:26px 0 60px}
h1{font-size:1.7rem;margin:.2rem 0 .4rem;letter-spacing:-.01em}
h2{font-size:1.18rem;margin:2rem 0 .6rem}
h3{font-size:1rem;margin:1.3rem 0 .4rem}
p.lede{color:var(--muted);margin:.1rem 0 1.2rem;max-width:76ch}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin:1rem 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.kpi .v{font-size:1.65rem;font-weight:700;line-height:1.1}
.kpi .l{font-size:.84rem;color:var(--muted);margin-top:3px}
.kpi .b{font-size:.76rem;color:var(--muted);margin-top:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:1rem 0}
.card h3{margin-top:0}
table{border-collapse:collapse;width:100%;background:var(--card);font-size:.88rem;
border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:.7rem 0 1.6rem}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eef2f7;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:#374151}
tbody tr:hover{background:#fafcff}
td.blank{background:#fff7ed;color:var(--warn);font-style:italic}
caption{caption-side:top;text-align:left;font-weight:600;padding:0 0 .5rem;font-size:.95rem}
.chip{display:inline-block;font-size:.7rem;padding:1px 7px;border-radius:99px;background:var(--chip);
color:#374151;border:1px solid var(--line);white-space:nowrap}
.chip.ok{background:#e7f6ed;border-color:#bfe3cd;color:var(--ok)}
.chip.warn{background:#fdf3e3;border-color:#f0d9ad;color:var(--warn)}
.chip.bad{background:#fdeaea;border-color:#f3c3c3;color:var(--bad)}
.chip.src{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.68rem}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem}
.muted{color:var(--muted)}
.gov{font-size:.72rem;color:var(--ok);font-weight:600}
.note{border-left:3px solid var(--accent);background:#f4f8fc;padding:10px 14px;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.92rem}
.warnbox{border-left:3px solid var(--warn);background:#fffaf0;padding:10px 14px;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.92rem}
.okbox{border-left:3px solid var(--ok);background:#f2fbf5;padding:10px 14px;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.92rem}
ol,ul{padding-left:1.25rem}
li{margin:.3rem 0}
footer{border-top:1px solid var(--line);padding:18px 0 40px;color:var(--muted);font-size:.82rem}
.small{font-size:.82rem}
@media(max-width:640px){table{font-size:.8rem}th,td{padding:6px 7px}h1{font-size:1.4rem}}
"""


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def load(name: str):
    return json.loads((DATA / f"{name}.json").read_text())


SRC: dict[str, dict] = {}
for s in load("sources")["sources"]:
    SRC[s["id"]] = s


def ids_of(obj) -> list:
    """Accept either key name so the renderer never guesses."""
    return obj.get("source_ids") or obj.get("sources") or []


def src_cell(ids) -> str:
    """Render a mandatory source cell. Empty -> explicit unverified marker."""
    if not ids:
        return '<td class="blank">UNVERIFIED — no official source</td>'
    bits = []
    for sid in ids:
        s = SRC.get(sid)
        if not s:
            bits.append(f'<span class="chip src">{esc(sid)}?</span>')
            continue
        bits.append(
            f'<span class="chip src"><a href="{esc(s["url"])}" title="{esc(s["title"])}">{esc(sid)}</a></span>'
        )
    return "<td>" + " ".join(bits) + "</td>"


def src_list(ids) -> str:
    if not ids:
        return '<span class="muted">no source</span>'
    out = []
    for sid in ids:
        s = SRC.get(sid)
        if s:
            out.append(f'<a href="{esc(s["url"])}">{esc(sid)}</a>')
        else:
            out.append(f'<span class="chip src">{esc(sid)}?</span>')
    return " ".join(out)


def blank(v, alt="Not stated") -> str:
    if v is None or v == "" or (isinstance(v, (list, dict)) and not v):
        return f'<td class="blank">{esc(alt)}</td>'
    return f"<td>{esc(v)}</td>"


def chip(text, kind="") -> str:
    return f'<span class="chip {kind}">{esc(text)}</span>'


def status_chip(status: str) -> str:
    s = status.lower()
    if "cancel" in s:
        return chip(status, "bad")
    if "advisory" in s:
        return chip(status, "warn")
    if "active" in s:
        return chip(status, "ok")
    return chip(status, "warn")


def page(title: str, sub: str, body: str, here: str, generated: str) -> str:
    nav = []
    for fn, (label, _desc) in PAGES.items():
        cls = ' class="on"' if fn == here else ""
        nav.append(f'<a href="{fn}"{cls}>{esc(label)}</a>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — Bathtub overflow trip lever, San Francisco</title>
<link rel="stylesheet" href="style.css">
</head><body>
<header class="top"><div class="wrap">
  <div class="brand">Overflow trip lever <span>· San Francisco</span></div>
  <nav class="main">{''.join(nav)}</nav>
</div></header>
<main><div class="wrap">
<h1>{esc(title)}</h1>
<p class="lede">{sub}</p>
{body}
</div></main>
<footer><div class="wrap">
<p>Internal working document. Built {esc(generated)} from <span class="mono">data/tub/*.json</span>.
Every table row cites a source; blanks mean <em>unverified</em>, not zero.
Contractor licence data was read from the California Contractors State License Board on 2026-11-06 and is
point-in-time — re-check before hiring. <a href="flagged.html">Unverified items and irregularities</a> ·
<a href="sources.html">All sources</a> · <a href="gems_site/index.html">GEMS archive</a></p>
</div></footer>
</body></html>
"""


# ---------------------------------------------------------------- pages
def build_index(generated: str) -> str:
    ex = load("executive")
    v = load("vendors")
    est = load("estimates")
    req = load("requirements")
    rules = load("rules")
    fl = load("flagged")

    kpis = "".join(
        f'<div class="kpi"><div class="v">{esc(k["value"])}</div>'
        f'<div class="l">{esc(k["label"])}</div>'
        f'<div class="b">{esc(k["basis"])}</div></div>'
        for k in ex["key_numbers"]
    )

    bottom = "".join(f"<li>{esc(b)}</li>" for b in ex["bottom_line"])

    rec = ex["recommendation"]
    today = "".join(
        f'<tr><td>{esc(k["label"])}</td><td><strong>{esc(k["value"])}</strong></td>'
        f'<td class="muted small">{esc(k["basis"])}</td>{src_cell(k["source_ids"])}</tr>'
        for k in ex["key_numbers"]
    )

    top3 = sorted([x for x in v["vendors"] if x["rank"] > 0], key=lambda x: x["rank"])[:3]
    rows = ""
    for x in top3:
        rows += (
            "<tr>"
            f'<td><strong>{esc(x["name"])}</strong><br><span class="mono">#{esc(x["licence"])}</span></td>'
            f"<td>{status_chip(x['status'])}</td>"
            f'<td class="small">{esc(", ".join(c.split(" - ")[0] for c in x["classifications"]))}</td>'
            f'<td class="small">{esc(x["phone"])}</td>'
            f'<td class="small">{esc(x["why"])}</td>'
            f"{src_cell(x['source_ids'])}</tr>"
        )

    est_rows = ""
    for e in est["estimates"]:
        est_rows += (
            '<tr data-kind="estimate">'
            f'<td><strong>{esc(e["amount_as_written"])}</strong> {chip(e["evidence_label"], "warn")}</td>'
            f'<td>{esc(e["vendor_as_written"])}</td>'
            f'<td class="small">{esc(e["stated_scope_as_written"])}</td>'
            f"{blank(e['open_wall_work_included'])}"
            f"{blank(e['drywall_repair_included'])}"
            f'<td class="small">{esc(e["licence_verified"])}</td>'
            f"{src_cell(e['source_ids'])}</tr>"
        )

    body = f"""
<div class="note"><strong>Bottom line.</strong> {esc(ex["one_liner"])}</div>

<div class="grid">{kpis}</div>

<h2>What to do, in order</h2>
<ol>{bottom}</ol>

<div class="okbox"><strong>Recommended primary provider:</strong> {esc(rec["primary"])}<br>
<strong>Why:</strong> {esc(rec["why"])}<br>
<strong>Condition:</strong> {esc(rec["condition"])}<br>
<strong>Runner-up:</strong> {esc(rec["runner_up"])}<br>
<strong>Cheapest first move:</strong> {esc(rec["cheapest_first_move"])}</div>

<h2>Top three providers, by fit</h2>
<table><caption>Ranked on verified licence scope, not on reviews. Reviews could not be verified — see the Flagged page.</caption>
<thead><tr><th>Firm / CSLB #</th><th>Licence status</th><th>Classifications</th><th>Phone</th><th>Why it ranks here</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>
<p class="small"><a href="providers.html">All 13 records checked →</a></p>

<h2>The three quotes, by scope</h2>
<table><caption>All three amounts are USER-REPORTED from the brief, dated only "8/30/26". Blank cells mean the brief did not say.</caption>
<thead><tr><th>Amount</th><th>As written</th><th>Stated scope</th><th>Opens wall?</th><th>Drywall?</th><th>Licence</th><th>Source</th></tr></thead>
<tbody>{est_rows}</tbody></table>
<p class="small"><a href="quotes.html">Full quote analysis →</a> · Official reference: a DBI Category 1P single-fixture plumbing permit is
<strong>${esc(est["official_cost_reference"]["amount_usd"])}</strong> ({src_list(est["official_cost_reference"]["source_ids"])}).</p>

<h2>The decision that actually matters</h2>
<div class="card"><h3>From above, or from below?</h3>
<p>There are two access routes and they are not equally reversible. Through the overflow opening costs almost
nothing to try and opens no wall. Through the storage-unit ceiling below reaches the trap tee that
overflow-side work cannot reach, but SF.gov states a permit is needed <em>before cutting into or replacing
pipes, particularly pipes that will be covered by a wall</em>
({src_list(["S20"])}), and it needs a drywall trade on top of the plumber.</p>
<p><a href="access.html"><strong>Compare the three access options, with the evidence for each →</strong></a></p></div>

<h2>Scope of this analysis</h2>
<table><caption>What was checked, how, and what it rests on.</caption>
<thead><tr><th>Item</th><th>Value</th><th>Basis</th><th>Source</th></tr></thead>
<tbody>{today}</tbody></table>

<h2>How to read this site</h2>
<div class="card"><ul class="small">
<li><strong>Every row has a source.</strong> The right-hand column of every table links to the official page
the value came from. A row with no official source shows <span class="chip warn">UNVERIFIED</span> and is listed on the
<a href="flagged.html">Flagged for review</a> page.</li>
<li><strong>Blanks are deliberate.</strong> Where the brief or an official source did not state a value, the cell is
left blank rather than estimated. Nothing was inferred to fill a gap.</li>
<li><strong>Labels.</strong> {chip("OFFICIAL", "ok")} = government, statute or regulator.
{chip("USER-REPORTED", "warn")} = supplied by the owner, no document.
{chip("INFERENCE", "warn")} = reasoning, clearly marked as such.</li>
<li><strong>Sources: {esc(ex["source_count"])}</strong> — see <a href="sources.html">Sources</a>.
Requirements: {len(req["requirements"])}. Rules: {len(rules["rules"])}.
Unverified items: {len(fl["unverified_items"])}. Irregularities: {len(fl["irregularities"])}.</li>
</ul></div>

<div class="warnbox"><strong>Read this before acting.</strong> Contractor licence status is point-in-time. Every
licence on this site was read from cslb.ca.gov on 2026-11-06, where the CSLB page stated "Data current as of
11/6/2026". Re-check any licence on the day you sign. No review score is reported because none could be
verified.</div>
"""
    return page("Bathtub overflow trip lever", esc(load("executive")["one_liner"]), body, "index.html", generated)


def build_providers(generated: str) -> str:
    v = load("vendors")
    rows = ""
    for x in sorted(v["vendors"], key=lambda a: (-a["rank"], a["name"])):
        gates = "".join(
            chip(g, "ok") if g in x["gates_met"] else chip(g, "bad") for g in
            ["G1", "G2", "G3", "G4", "G5", "G6"]
        )
        rows += (
            f'<tr data-kind="vendor"><td>{esc(x["rank"]) if x["rank"] else "—"}</td>'
            f'<td><strong>{esc(x["name"])}</strong><br><span class="mono">#{esc(x["licence"])}</span></td>'
            f"<td>{status_chip(x['status'])}</td>"
            f'<td class="small">{esc(", ".join(x["classifications"]))}</td>'
            f'<td class="small">{esc(x["address"])}<br>{esc(x["phone"])}</td>'
            f"<td>{blank(x['issue_date'])}</td>".replace("<td>", "<td class='small'>", 1)
            + f"<td class='small'>{esc(x['expire_date'])}</td>"
            f'<td class="small">{esc(x["workers_comp"])}</td>'
            f"<td>{gates}</td>"
            f'<td class="small">{esc(x["why"])}</td>'
            f"{src_cell(x['source_ids'])}</tr>"
        )

    detail = ""
    for x in sorted(v["vendors"], key=lambda a: (-a["rank"], a["name"])):
        extra = ""
        if x.get("open_question"):
            extra += f'<p class="small"><strong>Open question:</strong> {esc(x["open_question"])}</p>'
        if x.get("note"):
            extra += f'<p class="small"><strong>Note:</strong> {esc(x["note"])}</p>'
        if x.get("liability_insurance"):
            extra += f'<p class="small"><strong>Liability insurance on record:</strong> {esc(x["liability_insurance"])}</p>'
        detail += f"""<div class="card">
<h3>#{esc(x["licence"])} — {esc(x["name"])} {status_chip(x["status"])}</h3>
<p class="small">{esc(x["why"])}</p>
<p class="small muted">Bond: {esc(x["bond"])}</p>
{extra}
<p class="small">Sources: {src_list(x["source_ids"])}</p>
</div>"""

    rubric = "".join(f"<li class='small'>{esc(g)}</li>" for g in v["fit_rubric"])

    body = f"""
<div class="note">{esc(v["verification_method"])}</div>
<div class="warnbox">{esc(v["rating_columns_note"])}</div>

<h2>Fit rubric</h2>
<ul>{rubric}</ul>

<h2>All records</h2>
<table><caption>Rank 0 = excluded, with the reason shown. Gates: {chip("G1","ok")} C-36 plumbing holder,
{chip("G2","ok")} can cover drywall too, {chip("G3","ok")} San Francisco address,
{chip("G4","ok")} workers' comp on file, {chip("G5","ok")} published bath-waste work,
{chip("G6","ok")} no CSLB advisory.</caption>
<thead><tr><th>Rank</th><th>Firm / CSLB #</th><th>Status</th><th>Classifications</th><th>Address / phone</th>
<th>Issued</th><th>Expires</th><th>Workers' comp</th><th>Gates</th><th>Assessment</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>Record detail</h2>
{detail}
"""
    return page("Providers", "Thirteen CSLB records read directly on 2026-11-06. Licences, classifications and dates are copied from the state record, not from marketing.", body, "providers.html", generated)


def build_quotes(generated: str) -> str:
    est = load("estimates")
    rows = ""
    for e in est["estimates"]:
        rows += (
            '<tr data-kind="estimate">'
            f'<td><strong>{esc(e["amount_as_written"])}</strong></td>'
            f'<td>{esc(e["vendor_as_written"])}</td>'
            f'<td class="small">{esc(e["stated_scope_as_written"])}</td>'
            f"{blank(e['includes_labour_and_materials'])}"
            f"{blank(e['open_wall_work_included'])}"
            f"{blank(e['drywall_repair_included'])}"
            f"{blank(e['permit_included'])}"
            f'<td class="small">{esc(e["licence_verified"])}</td>'
            f'<td>{chip(e["evidence_label"], "warn")}</td>'
            f"{src_cell(e['source_ids'])}</tr>"
        )
    cards = ""
    for e in est["estimates"]:
        cards += f"""<div class="card"><h3>{esc(e["amount_as_written"])} — {esc(e["vendor_as_written"])}</h3>
<p class="small"><strong>Scope as written:</strong> {esc(e["stated_scope_as_written"])}</p>
<p class="small">{esc(e["analysis"])}</p>
<p class="small">Sources: {src_list(e["source_ids"])}</p></div>"""

    off = est["official_cost_reference"]
    sp = est["spread"]
    body = f"""
<div class="warnbox">{esc(est["provenance"])}</div>

<h2>Side by side</h2>
<table><caption>Blank = the brief did not state it. It was not guessed.</caption>
<thead><tr><th>Amount</th><th>Vendor as written</th><th>Scope as written</th><th>Labour + materials?</th>
<th>Opens wall?</th><th>Drywall?</th><th>Permit?</th><th>Licence verified</th><th>Label</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>What each quote actually buys</h2>
{cards}

<h2>Spread</h2>
<div class="card"><h3>{esc(sp["ratio_max_over_min"])}x between the highest and lowest</h3>
<p class="small">${esc(sp["min_usd"])} to ${esc(sp["max_usd"])}, a difference of ${esc(sp["difference_usd"])}.
{esc(sp["note"])}</p></div>

<h2>Official reference point</h2>
<table><caption>{esc(off["label"])}</caption>
<thead><tr><th>Amount</th><th>Effective</th><th>Label</th><th>Source</th></tr></thead>
<tbody><tr><td><strong>${esc(off["amount_usd"])}</strong></td><td class="small">{esc(off["effective"])}</td>
<td>{chip(off["evidence_label"], "ok")}</td>{src_cell(off["source_ids"])}</tr></tbody></table>
<p class="small">{esc(off["analysis"])}</p>

<div class="note"><strong>Decision note.</strong> {esc(est["decision_note"])}
<a href="flagged.html">The ten questions to ask every bidder →</a></div>
"""
    return page("Quotes", "Three amounts, three different scopes. Normalised so they can actually be compared — and labelled, because none of them is documented.", body, "quotes.html", generated)


def build_requirements(generated: str) -> str:
    req = load("requirements")
    groups: dict[str, list] = {}
    for r in req["requirements"]:
        groups.setdefault(r["category"], []).append(r)

    body = f'<div class="note">{esc(req["requirement_note"])}</div>'
    for cat, items in groups.items():
        rows = ""
        for r in items:
            state = r["verification_state"]
            kind = {"verified": "ok", "unverified": "warn", "partial": "warn",
                    "purposely_omitted": ""}.get(state, "warn")
            rows += (
                f'<tr data-kind="req"><td class="mono">{esc(r["id"])}</td>'
                f'<td>{esc(r["requirement"])}</td>'
                f'<td class="small">{esc(r["why"])}</td>'
                f'<td class="small">{esc(r["how_addressed"])}</td>'
                f'<td>{chip(state.replace("_", " "), kind)}</td>'
                f'<td class="small">{esc(r["note"])}</td>'
                f"{src_cell(r['source_ids'])}</tr>"
            )
        body += f"""<h2>{esc(cat)}</h2>
<table><caption>{len(items)} requirement(s) in this category.</caption>
<thead><tr><th>ID</th><th>Requirement</th><th>Why</th><th>How it is addressed</th><th>Verification</th><th>Note</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>"""
    return page("Requirements", "Every requirement as stated, how it is met, and whether an official source backs the answer.", body, "requirements.html", generated)


def build_rules(generated: str) -> str:
    rules = load("rules")
    rows = ""
    for r in rules["rules"]:
        rows += (
            f'<tr data-kind="rule"><td class="mono">{esc(r["id"])}</td>'
            f'<td>{esc(r["topic"])}</td>'
            f'<td class="small">{esc(r["statement"])}</td>'
            f"{blank(r.get('exact_limit') or r.get('effective'))}"
            f'<td class="small">{esc(r.get("effect_on_this_job") or r.get("effect") or "")}</td>'
            f'<td>{chip(r["evidence_label"], "ok")}</td>'
            f"{src_cell(r['source_ids'])}</tr>"
        )
    body = f"""
<div class="note">{esc(rules["note"])}</div>
<table><caption>Every rule below quotes or closely paraphrases the linked official text.</caption>
<thead><tr><th>ID</th><th>Topic</th><th>Rule</th><th>Limit / effective</th><th>Effect on this job</th><th>Label</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>Two rules that decide the job</h2>
<div class="card"><h3>1. A permit is triggered by cutting into concealed pipe</h3>
<p class="small">SF.gov: <em>"You need a permit before cutting into or replacing pipes, particularly pipes that
will be covered by a wall or buried in the ground."</em> {src_list(["S20"])}</p>
<h3>2. The exempt-work list does not cover replacing a concealed waste-and-overflow</h3>
<p class="small">SF Plumbing Code 104.2 exempts leak repair and unstopping <em>not requiring cutting into or
removing piping</em>, faucet/angle-stop/hose-bibb maintenance, toilet replacement, and a short list of similar
items. None of them covers removing or replacing a tub waste-and-overflow assembly.
{src_list(["S21", "S22"])}</p></div>

<div class="warnbox"><strong>If a permit is taken out:</strong> the DBI fee for a single residential unit with a
single plumbing fixture is <strong>${esc(load("estimates")["official_cost_reference"]["amount_usd"])}</strong>
({src_list(["S32"])}), and the work must be inspected before pipes are covered
({src_list(["S45"])}).</div>
"""
    return page("Permits & rules", "Thirteen rules, each quoted from the official text: licensing, permits, contract form, tenant notice, construction hours and lead safety.", body, "rules.html", generated)


def build_access(generated: str) -> str:
    sc = load("scope")
    cards = ""
    for o in sc["options"]:
        pre = "".join(f"<li class='small'>{esc(p)}</li>" for p in o["prerequisites_unverified"])
        cards += f"""<div class="card"><h3>Option {esc(o["id"])} — {esc(o["name"])}</h3>
<p class="small"><strong>What happens:</strong> {esc(o["what_happens"])}</p>
<p class="small"><strong>Evidence for:</strong> {esc(o["evidence_for"])}</p>
<p class="small"><strong>Evidence against:</strong> {esc(o["evidence_against"])}</p>
<p class="small"><strong>Opens drywall:</strong> {"Yes" if o["opens_drywall"] else "No"} ·
<strong>Tenant impact:</strong> {esc(o["tenant_impact"])}</p>
<p class="small"><strong>If it fails:</strong> {esc(o["what_if_it_fails"])}</p>
<p class="small"><strong>Unverified prerequisites:</strong></p><ul>{pre}</ul>
<p class="small">Label: {chip(o["evidence_label"], "warn")} · Sources: {src_list(o["source_ids"])}</p></div>"""

    opt_rows = ""
    for o in sc["options"]:
        opt_rows += (
            f'<tr><td><strong>{esc(o["id"])}</strong></td>'
            f'<td>{esc(o["name"])}</td>'
            f'<td>{"Yes" if o["opens_drywall"] else "No"}</td>'
            f'<td class="small">{esc(o["tenant_impact"])}</td>'
            f'<td class="small">{esc(o["estimated_time_on_site"])}</td>'
            f'<td>{chip(o["evidence_label"], "warn")}</td>'
            f"{src_cell(o['source_ids'])}</tr>"
        )

    steps = ""
    for s in sc["recommended_sequence"]:
        steps += (f'<tr><td class="mono">{esc(s["step"])}</td><td class="small">{esc(s["action"])}</td>'
                  f"{src_cell(ids_of(s))}</tr>")

    hy = sc["why_plumbers_may_have_declined"]
    hy_items = "".join(f"<li class='small'>{esc(c)}</li>" for c in hy["candidates"])

    body = f"""
<div class="warnbox">{esc(sc["disclaimer"])}</div>

<h2>Compare the options</h2>
<table><caption>Times are inference and are labelled as such; nothing on this row was measured.</caption>
<thead><tr><th>Option</th><th>What it is</th><th>Opens drywall</th><th>Tenant impact</th><th>On-site time</th><th>Label</th><th>Source</th></tr></thead>
<tbody>{opt_rows}</tbody></table>
{cards}

<h2>Recommended sequence</h2>
<table><caption>Each step names the rule or document it rests on.</caption>
<thead><tr><th>#</th><th>Action</th><th>Source</th></tr></thead><tbody>{steps}</tbody></table>

<h2>Why plumbers may have declined</h2>
<div class="warnbox">{chip(hy["label"], "warn")} {esc(hy["status"])}</div>
<ul>{hy_items}</ul>

<h2>Photo and information checklist</h2>
<table><caption>No photographs were supplied, so nothing here was assessed from an image. This is what to send bidders.</caption>
<thead><tr><th>Item</th><th>Why</th><th>Source</th></tr></thead><tbody>
<tr><td>Overflow plate, straight on, with a coin for scale</td><td>Shows the plate type, screw condition and finish</td>{src_cell([])}</tr>
<tr><td>Overflow plate off, looking into the tube</td><td>Shows whether the linkage is attached or sheared</td><td>{src_list(["S42"])}</td></tr>
<tr><td>Under-tub drain from the storage unit, if visible</td><td>Shows fitting type: slip joint vs. glued/soldered</td><td>{src_list(["S33"])}</td></tr>
<tr><td>Storage-unit ceiling directly below the tub</td><td>Shows clearance, obstructions and finish texture</td>{src_cell([])}</tr>
<tr><td>Year built (Assessor/Planning record)</td><td>Decides whether lead-safe work practices apply</td><td>{src_list(["S34"])}</td></tr>
</tbody></table>
"""
    return page("Scope & access", "From above or from below: what each route requires, what it costs in disruption, and what must be decided before anyone cuts.", body, "access.html", generated)


def build_sources(generated: str) -> str:
    srcs = load("sources")["sources"]
    rows = ""
    for s in srcs:
        if s.get("official"):
            kind = chip("OFFICIAL", "ok")
        elif s.get("self_published"):
            kind = chip("SELF-PUBLISHED", "warn")
        else:
            kind = chip("THIRD PARTY", "warn")
        rows += (
            f'<tr data-kind="source"><td class="mono"><a href="{esc(s["url"])}">{esc(s["id"])}</a></td><td>{kind}</td>'
            f'<td class="small">{esc(s["publisher"])}</td>'
            f'<td class="small"><a href="{esc(s["url"])}">{esc(s["title"])}</a></td>'
            f'<td class="small">{esc(s["used_for"])}</td>'
            f'<td class="small mono">{esc(s["url"])}</td></tr>'
        )
    n_off = sum(1 for s in srcs if s.get("official"))
    body = f"""
<div class="note">{esc(load("sources")["note"])}</div>
<div class="grid">
  <div class="kpi"><div class="v">{len(srcs)}</div><div class="l">sources cited</div></div>
  <div class="kpi"><div class="v">{n_off}</div><div class="l">official (government / statute / regulator)</div></div>
  <div class="kpi"><div class="v">{len(srcs) - n_off}</div><div class="l">self-published or third-party (never used as verification)</div></div>
</div>
<table><caption>Every source is listed with the exact URL used, so each claim can be re-checked by hand.</caption>
<thead><tr><th>ID</th><th>Class</th><th>Publisher</th><th>Document</th><th>Used for</th><th>URL</th></tr></thead>
<tbody>{rows}</tbody></table>
"""
    return page("Sources", "Every source, who published it, and exactly what it was used to verify.", body, "sources.html", generated)


def build_flagged(generated: str) -> str:
    fl = load("flagged")
    u_rows = ""
    for u in fl["unverified_items"]:
        u_rows += (f'<tr><td class="mono">{esc(u["id"])}</td><td class="small">{esc(u["item"])}</td>'
                   f'<td class="small">{esc(u["what_is_missing"])}</td>'
                   f'<td class="small">{esc(u["effect"])}</td>'
                   f'<td class="small">{esc(u["how_to_close_it"])}</td>'
                   f"{src_cell(u['source_ids'])}</tr>")
    i_rows = ""
    for i in fl["irregularities"]:
        sev = {"high": "bad", "medium": "warn", "low": "", "info": ""}.get(i["severity"], "warn")
        i_rows += (f'<tr><td class="mono">{esc(i["id"])}</td><td>{chip(i["severity"].upper(), sev)}</td>'
                   f'<td class="small"><strong>{esc(i["finding"])}</strong><br>{esc(i["detail"])}</td>'
                   f'<td class="small">{esc(i["action_taken"])}</td>'
                   f'<td class="small">{esc(i["review_question"])}</td>'
                   f"{src_cell(i['source_ids'])}</tr>")
    q_rows = ""
    for q in fl["questions_to_ask"]:
        q_rows += (f'<tr><td class="mono">{esc(q["n"])}</td><td>{esc(q["question"])}</td>'
                   f'<td class="small">{esc(q["why"])}</td>{src_cell(q["sources"])}</tr>')
    p_rows = ""
    for p in fl["private_exclusions"]:
        p_rows += (f'<tr><td class="mono">{esc(p["id"])}</td><td class="small">{esc(p["decision"])}</td>'
                   f'<td class="small">{esc(p["reason"])}</td><td class="small">{esc(p["how_to_handle"])}</td>'
                   f'<td class="blank">N/A — no source by design: this row records an omission, '
                   f'not a value</td></tr>')

    body = f"""
<div class="warnbox">{esc(fl["note"])}</div>

<h2>Unverified items — {len(fl["unverified_items"])}</h2>
<table><caption>Nothing here blocks the shortlist. Each row says how to close the gap.</caption>
<thead><tr><th>ID</th><th>Item</th><th>What is missing</th><th>Effect</th><th>How to close it</th><th>Source</th></tr></thead>
<tbody>{u_rows}</tbody></table>

<h2>Irregularities — {len(fl["irregularities"])}</h2>
<table><caption>Things that looked wrong while verifying, with what was done about each.</caption>
<thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Action taken</th><th>What to review</th><th>Source</th></tr></thead>
<tbody>{i_rows}</tbody></table>
<p class="small">Repository-level findings (the repo's contents not matching this project, a build script that
overwrote the site root, duplicate raster trees) are documented in
<a href="https://github.com/karagemop466-tech/Korea8/blob/main/REPO_REVIEW.md"><span class="mono">REPO_REVIEW.md</span></a>.</p>

<h2>Ten questions to ask every bidder</h2>
<table><caption>Ask all ten of all three firms and compare the answers, not the totals.</caption>
<thead><tr><th>#</th><th>Question</th><th>Why it matters</th><th>Source</th></tr></thead>
<tbody>{q_rows}</tbody></table>

<h2>Deliberate exclusions</h2>
<table><caption>Recorded so the omission is auditable rather than accidental.</caption>
<thead><tr><th>ID</th><th>Decision</th><th>Reason</th><th>How it is handled</th><th>Source</th></tr></thead>
<tbody>{p_rows}</tbody></table>
"""
    return page("Flagged for review", "Everything this project could not verify, and everything that looked wrong while checking. Nothing here blocked publication — review it and ask for changes.", body, "flagged.html", generated)


def main() -> int:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    builders = {
        "index.html": build_index,
        "providers.html": build_providers,
        "quotes.html": build_quotes,
        "requirements.html": build_requirements,
        "rules.html": build_rules,
        "access.html": build_access,
        "sources.html": build_sources,
        "flagged.html": build_flagged,
    }
    for fn, fn_build in builders.items():
        (ROOT / fn).write_text(fn_build(generated), encoding="utf-8")
        print(f"[tub-site] wrote {fn}")
    (ROOT / "style.css").write_text(CSS, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    feed = {
        "schema": "tub-feed-v1",
        "generated_utc": generated,
        "pages": [{"path": p, "title": t, "description": d} for p, (t, d) in PAGES.items()],
        "sources": len(SRC),
        "unverified_items": len(load("flagged")["unverified_items"]),
        "irregularities": len(load("flagged")["irregularities"]),
    }
    (ROOT / "feed.json").write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
    print(f"[tub-site] wrote style.css, .nojekyll, feed.json ({len(PAGES)} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

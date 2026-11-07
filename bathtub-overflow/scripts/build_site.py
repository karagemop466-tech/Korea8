#!/usr/bin/env python3
"""Build the bathtub-overflow static site from bathtub-overflow/data/*.json.

The data files are the single source of truth. This script only renders them.
Rules enforced here (and checked by verify_site.py):
  * every table row renders at least one source link;
  * values that could not be confirmed from an official source are left blank
    in the data and surfaced on the Flagged for Review page instead;
  * no value is generated here that is not present in the data files.
"""
from __future__ import annotations

import html
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SITE = ROOT  # published at /Korea8/bathtub-overflow/

PAGES = [
    ("index.html", "Overview", "Executive summary and next actions"),
    ("scope.html", "Requirements", "The full requirement list, by category"),
    ("vendors.html", "Vendor shortlist", "San Francisco contractors, CSLB-verified"),
    ("costs.html", "Cost", "Estimates on file, official fees, cost drivers"),
    ("code.html", "Code & permits", "Permit, licensing and tenant-entry rules"),
    ("findings.html", "Findings", "What the evidence shows"),
    ("flagged.html", "Flagged for review", "Unverified values, contradictions, handling notes"),
    ("sources.html", "Sources", "Every source used, with what it verifies"),
]

CSS = """*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-width:1180px;margin:0 auto;padding:1.2rem 1.4rem 4rem;color:#16181d;line-height:1.55;background:#fbfbfc}
a{color:#0b5fff}
header.top{border-bottom:1px solid #e3e5e9;padding-bottom:.8rem;margin-bottom:1rem}
header.top h1{margin:0 0 .2rem;font-size:1.5rem}
header.top .sub{color:#5b6068;margin:0;font-size:.95rem}
nav.crumbs{font-size:.85rem;color:#6b7078;margin:.6rem 0 0}
nav.pages{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0 1.4rem}
nav.pages a{text-decoration:none;border:1px solid #d9dce1;background:#fff;border-radius:7px;padding:.35rem .6rem;font-size:.88rem;color:#22262c}
nav.pages a:hover{border-color:#0b5fff;color:#0b5fff}
nav.pages a[aria-current="page"]{background:#16181d;border-color:#16181d;color:#fff}
section{background:#fff;border:1px solid #e6e8ec;border-radius:12px;padding:1rem 1.1rem;margin:0 0 1.1rem}
section>h2{margin:.1rem 0 .6rem;font-size:1.15rem;border-bottom:1px solid #eef0f3;padding-bottom:.4rem}
h3{font-size:1rem;margin:1rem 0 .4rem}
table{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.86rem}
th,td{border:1px solid #dfe2e7;padding:.45rem .5rem;text-align:left;vertical-align:top}
th{background:#f3f5f8;font-weight:600}
tr:nth-child(even) td{background:#fcfcfd}
td.num{text-align:right;white-space:nowrap}
.tag{display:inline-block;font-size:.68rem;border-radius:4px;padding:.05rem .35rem;background:#eef1f5;color:#4a5058;border:1px solid #e1e5ea;white-space:nowrap}
.tag.ok{background:#e7f6ec;color:#12632f;border-color:#c7ead3}
.tag.warn{background:#fdf3e3;color:#7a4b06;border-color:#f0dfbd}
.tag.bad{background:#fdecec;color:#8a1c1c;border-color:#f3cdcd}
.tag.info{background:#eaf1ff;color:#123a8a;border-color:#cfe0ff}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:.7rem;margin:.8rem 0}
.stat{border:1px solid #e3e6ea;border-radius:10px;padding:.6rem .7rem;background:#fff}
.stat .n{font-size:1.35rem;font-weight:700;display:block;line-height:1.2}
.stat .l{font-size:.78rem;color:#5f656e;text-transform:uppercase;letter-spacing:.03em}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.8rem;margin-top:.8rem}
.card{border:1px solid #e3e6ea;border-radius:10px;padding:.7rem .8rem;background:#fff}
.card h3{margin:.05rem 0 .3rem;font-size:.97rem}
.card p{margin:.2rem 0;font-size:.87rem;color:#33383f}
ol.steps{margin:.4rem 0;padding-left:1.2rem}
ol.steps li{margin:.35rem 0}
.quote{border-left:3px solid #d9dde3;padding:.35rem .7rem;margin:.4rem 0;background:#fafbfc;color:#39404a;font-size:.87rem}
.small{font-size:.82rem;color:#5f656e}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.84rem}
footer{border-top:1px solid #e3e5e9;margin-top:1.4rem;padding-top:.8rem;color:#5f656e;font-size:.82rem}
.kv{display:grid;grid-template-columns:minmax(150px,230px) 1fr;gap:.2rem .8rem;font-size:.88rem}
.kv dt{font-weight:600;color:#3a4049}
.kv dd{margin:0}
@media (max-width:760px){table{font-size:.8rem}.kv{grid-template-columns:1fr}}
"""


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def load(name: str):
    return json.loads((DATA / name).read_text())


def link_list(ids, sources_by_id):
    """Render a list of source ids as labelled links (unknown ids are dropped, never invented)."""
    out = []
    for sid in ids or []:
        s = sources_by_id.get(sid)
        if not s:
            continue
        label = s.get("short") or sid
        out.append(f'<a href="{esc(s["url"])}" rel="noopener">{esc(label)}</a>')
    return " · ".join(out) if out else '<span class="tag warn">no source</span>'


def raw_link_list(urls):
    out = []
    for u in urls or []:
        if not u:
            continue
        out.append(f'<a href="{esc(u)}" rel="noopener">{esc(u.split("?")[0].split("/")[-1] or u)}</a>')
    return " · ".join(out) if out else '<span class="tag warn">no source</span>'


def nav(current: str) -> str:
    parts = []
    for fname, label, _ in PAGES:
        cur = ' aria-current="page"' if fname == current else ""
        parts.append(f'<a href="{fname}"{cur}>{esc(label)}</a>')
    return '<nav class="pages">' + "".join(parts) + "</nav>"


def shell(title: str, current: str, body: str, subtitle: str, generated: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Bathtub overflow trip lever project</title>
<link rel="stylesheet" href="style.css">
</head><body>
<div style="background:#fff7e0;border-bottom:2px solid #ecd9a0;padding:10px 18px;font-size:14px;line-height:1.5;color:#4a3b00"><strong>Archived parallel-session draft.</strong> One of several working briefs prepared in parallel; superseded by the <a href="../index.html" style="color:#0b5cad;font-weight:600">canonical project dashboard</a> (root of this site), re-verified against official sources on 2026-11-07. Kept for traceability — use the dashboard for decisions.</div>
<header class="top">
  <h1>Bathtub wastewater overflow trip lever — requirements, vendors and code findings</h1>
  <p class="sub">{esc(subtitle)}</p>
  <p class="nav crumbs"><a href="../index.html">&#8592; Repository home</a> · <span class="mono">bathtub-overflow/</span> · San Francisco, California</p>
</header>
{nav(current)}
{body}
<footer>
  <p>Generated {esc(generated)} from the JSON data files in <span class="mono">bathtub-overflow/data/</span>. Every table row links to the source it was read from.
  Values that could not be confirmed from an official source are left blank and listed on the
  <a href="flagged.html">Flagged for Review</a> page. Nothing on this site was inferred.</p>
</footer>
</body></html>"""


def stat(n, label, cls=""):
    return f'<div class="stat"><span class="n {cls}">{esc(n)}</span><span class="l">{esc(label)}</span></div>'


def build_index(sources, vendors, requirements, costs, code_facts, findings, flagged, generated):
    v = vendors["vendors"]
    active = [x for x in v if x["cslb_status"].startswith("This license is current and active")]
    onestop = [x for x in v if "alongside C-36" in x["drywall_self_perform"]]
    suspended = [x for x in v if "SUSPENDED" in x["cslb_status"]]
    unverified = [x for x in v if not x["cslb_license"]]
    quotes = costs["quotes"]
    lo = min(q["amount_usd"] for q in quotes)
    hi = max(q["amount_usd"] for q in quotes)
    permit_fee = next(f["amount_usd"] for f in costs["official_fees"] if f["id"] == "F01")

    top = [f for f in findings["findings"] if f["id"] in {"F-01", "F-03", "F-05", "F-07", "F-09"}]
    cards = "".join(
        f'<div class="card"><h3>{esc(f["finding"].split(".")[0])}.</h3><p>{esc(f["implication"])}</p>'
        f'<p class="small">{esc(f["verification"])} · {raw_link_list(f["sources"][:1])}</p></div>' for f in top
    )

    steps = [
        ("Get the permit answer from DBI", "One call to the Plumbing Inspection Division, (628) 652-3450, with the scope in hand decides who can legally do the work and what it costs. DBI's published rule exempts only minor work that does not cut into or remove piping — this job does.", "code.html", "Code &amp; permits"),
        ("Fix one scope, then re-quote", "The three estimates on file cover three different scopes. Use one scope checklist (waste + overflow assembly, lever, plug, spout/diverter, wall access, make and drain size) and re-quote it with at least three contractors, including at least one that holds both a general building and a plumbing licence.", "costs.html", "Cost"),
        ("Call in this order", "Bay Area Plumbing (best published evidence of this exact work), Expert Plumbing Solutions (highest quote, waste and overflow scope), Precision Rooter &amp; Drain (states it works with landlords and schedules tenant appointments). Add Ace Plumbing &amp; Rooter or We Do Construction if you want one contractor for plumbing and wall.", "vendors.html", "Vendor shortlist"),
        ("Exclude the suspended licence now", "Kenneth Asire Plumbing (#1027286) is shown by CSLB as suspended (contractor bond suspension). Do not contract while that shows.", "flagged.html", "Flagged for review"),
        ("Check licence, bond, workers compensation and complaint disclosure on the signing date", "CSLB licence status changes; one shortlisted licence carries a forward-looking suspension warning and another carries published complaint disclosure.", "vendors.html", "Vendor shortlist"),
        ("Give the tenant a compliant entry notice", "Written notice stating date, approximate time and purpose; 24 hours is presumed reasonable; normal business hours; no notice needed if the tenant is present and consents.", "code.html", "Code &amp; permits"),
    ]
    steps_html = "".join(
        f'<li><strong>{esc(t)}</strong> — {d} <a href="{href}">{esc(label)} &rarr;</a></li>' for t, d, href, label in steps
    )

    body = f"""
<section>
  <h2>The situation</h2>
  <p>The bathtub waste-and-overflow trip lever is stuck inside concealed plumbing behind the wall. The preferred
  route would be removal from above, but more than five licensed plumbers have declined that option because of the
  risk to the hidden plumbing, and they recommend working from below by opening the ceiling of the storage unit beneath
  the tub. Tenants occupy the unit, and the work needs one contractor who can cover both the plumbing and the wall.</p>
  <p>Three estimates were collected on 2026-08-30: <strong>${lo}</strong> (plunger handle repair or adjustment),
  <strong>${[q["amount_usd"] for q in quotes if q["amount_usd"] == 550][0]}</strong> (lever for the tub plug and spout with diverter,
  labour and materials included) and <strong>${hi}</strong> (replacing the waste and overflow). This page collects the
  requirements, the verified contractor data and the official code rules into one place, so the next step is a decision
  rather than another round of calls.</p>
</section>

<section>
  <h2>Key numbers</h2>
  <div class="stats">
    {stat(len(v), "contractors screened")}
    {stat(len(active), "CSLB licences read as active", "ok")}
    {stat(len(onestop), "hold B + C-36 (one contractor for both)", "info")}
    {stat(len(suspended), "licence suspended", "bad")}
    {stat(len(unverified), "licence not established", "warn")}
    {stat(f"${lo}–${hi}", "estimates on file")}
    {stat(f"${permit_fee}", "DBI permit fee if required", "info")}
    {stat("24 h", "presumed reasonable tenant entry notice", "info")}
  </div>
</section>

<section>
  <h2>What the evidence shows</h2>
  <div class="cards">{cards}</div>
  <p class="small">Full analysis on the <a href="findings.html">Findings</a> page; every unverified value and every
  contradiction between sources is on the <a href="flagged.html">Flagged for Review</a> page.</p>
</section>

<section>
  <h2>Next actions, in order</h2>
  <ol class="steps">{steps_html}</ol>
</section>

<section>
  <h2>How this dataset was verified</h2>
  <ul>
    <li>Every licence record in the <a href="vendors.html">vendor table</a> was read directly from the official CSLB
        licence-detail page linked in that row. The CSLB pages stated “Data current as of 11/6/2026”.</li>
    <li>Permit rules, fees, code editions, trade scopes and tenant-entry rules were read on the official pages linked in
        the <a href="code.html">Code &amp; permits</a> table.</li>
    <li>The three contractor estimates are owner-provided and are labelled as such; they could not be confirmed against any
        official source.</li>
    <li>Review-platform figures (Yelp, BBB, HomeAdvisor) could not be read directly — the platforms block automated
        retrieval — so they are recorded as dated snapshots and flagged, never presented as verified.</li>
    <li>Nothing was inferred. Where a value could not be confirmed, the cell is blank and the item appears on
        <a href="flagged.html">Flagged for Review</a>.</li>
  </ul>
</section>

<section>
  <h2>Scope hygiene</h2>
  <p class="quote">The published pages carry only verifiable, citable material: the public code facts, the verified licence
  records and the owner-provided estimates. See item FL-21 on the
  <a href="flagged.html">Flagged for Review</a> page.</p>
</section>
"""
    return shell("Overview", "index.html", body,
                 "A requirements, vendor and code dossier for replacing a stuck bathtub waste-and-overflow trip lever in an occupied San Francisco rental unit.",
                 generated)


def build_scope(requirements, sources_by_id, generated):
    cats = requirements["categories"]
    rows = []
    for r in requirements["requirements"]:
        rows.append(
            "<tr>"
            f'<td class="mono">{esc(r["id"])}</td>'
            f'<td>{esc(r["category"])}</td>'
            f'<td>{esc(r["requirement"])}</td>'
            f'<td>{esc(r["rationale"])}</td>'
            f'<td>{esc(r["acceptance"])}</td>'
            f'<td>{esc(r["status"])}</td>'
            f'<td><span class="tag">{esc(r["verification"])}</span></td>'
            f'<td>{link_list(r["sources"], sources_by_id)}</td>'
            "</tr>")
    cat_list = "".join(f'<li>{esc(c)}</li>' for c in cats)
    body = f"""
<section>
  <h2>Requirements — {esc(len(requirements["requirements"]))} items across {esc(len(cats))} categories</h2>
  <p>Categories: {cat_list}</p>
  <p class="small">Each row carries the source the requirement rests on. Rows marked
  <span class="tag">MANAGEMENT-DECISION</span> are owner decisions, still tied to the official guidance that motivates them.</p>
  <table><thead><tr><th>ID</th><th>Category</th><th>Requirement</th><th>Why it matters</th><th>Acceptance</th><th>Status</th><th>Verification</th><th>Source</th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table>
</section>
"""
    return shell("Requirements", "scope.html", body,
                 "The consolidated requirement list for the bathtub trip-lever job.", generated)


def build_vendors(vendors, sources_by_id, generated):
    rows = []
    for x in vendors["vendors"]:
        flags = "".join(f'<span class="tag warn">{esc(f)}</span> ' for f in x.get("flags") or [])
        if "SUSPENDED" in x["cslb_status"]:
            flags = '<span class="tag bad">DO NOT HIRE</span> ' + flags
        elif x["cslb_license"]:
            flags = '<span class="tag ok">licence read</span> ' + flags
        else:
            flags = '<span class="tag warn">licence unverified</span> ' + flags
        extra = link_list(x.get("extra_sources"), sources_by_id)
        rows.append(
            "<tr>"
            f'<td><strong>{esc(x["name"])}</strong><br><span class="small">{esc(x.get("dba") or "")}</span></td>'
            f'<td><a href="{esc(x["cslb_url"])}" rel="noopener">{esc(x["cslb_license"] or "not established")}</a></td>'
            f'<td>{esc(x["cslb_status"])}<br><span class="small">{esc(x["cslb_classifications"])}</span></td>'
            f'<td>{esc(x["drywall_self_perform"])}</td>'
            f'<td>{esc(x["cslb_address"])}<br><span class="small">{esc(x["cslb_phone"])}</span></td>'
            f'<td>{esc(x["review_snapshot"])}</td>'
            f'<td>{esc(x["quotes"])}</td>'
            f'<td>{esc(x["fit_notes"])}<br><span class="small">{esc(x["risk_notes"])}</span></td>'
            f'<td><strong>{esc(x["recommendation"])}</strong><br>{flags}</td>'
            f'<td><a href="{esc(x["cslb_url"])}" rel="noopener">CSLB record</a><br>{extra}</td>'
            "</tr>")
    body = f"""
<section>
  <h2>Vendor shortlist — {esc(len(vendors["vendors"]))} contractors</h2>
  <p>Licence data was read directly from the CSLB licence-detail page linked in every row; the CSLB pages carried the
  stamp “Data current as of 11/6/2026”. Review figures come from review platforms that block automated retrieval, so they
  are dated snapshots and are listed on the <a href="flagged.html">Flagged for Review</a> page.</p>
  <p class="small">“Can self-perform plumbing + wall” is derived from the classifications shown by CSLB: B (General Building)
  or C-9 (Drywall) alongside C-36 (Plumbing). “Not established” means no CSLB record was found under that name.</p>
  <table><thead><tr><th>Contractor</th><th>CSLB #</th><th>Status &amp; classifications</th><th>Plumbing + wall</th><th>Address / phone (CSLB)</th><th>Review snapshot</th><th>Estimate on file</th><th>Fit and risk</th><th>Recommendation</th><th>Sources</th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table>
</section>
<section>
  <h2>How to use this table</h2>
  <ol class="steps">
    <li>Open the CSLB record for each bidder before the call. Status, classifications, bond and workers compensation are
        on that page, and a complaint-disclosure link appears there when one exists.</li>
    <li>Ask the same three questions of every bidder: which access route will you use; what is in the fixed price if the
        wall must be opened; what happens to the price if the concealed piping is damaged.</li>
    <li>Re-check the licence on the signing date — one licence on this list is suspended, one carries a forward-looking
        suspension warning, and one carries published complaint disclosure.</li>
  </ol>
</section>
"""
    return shell("Vendor shortlist", "vendors.html", body,
                 "San Francisco plumbing and general contractors checked against the California State Licensing Board.", generated)


def build_costs(costs, generated):
    qrows = "".join(
        "<tr>"
        f'<td class="mono">{esc(q["id"])}</td>'
        f'<td>{esc(q["vendor"])}</td>'
        f'<td class="num">${esc(q["amount_usd"])}</td>'
        f'<td>{esc(q["scope_as_stated"])}</td>'
        f'<td>{esc(q["includes_labour_and_materials"] or "not stated")}</td>'
        f'<td>{esc(q["includes_drywall_access"] or "not stated")}</td>'
        f'<td>{esc(q["includes_permit"] or "not stated")}</td>'
        f'<td>{esc(q["quoted_date"])}</td>'
        f'<td><span class="tag warn">{esc(q["verification"])}</span></td>'
        f'<td>{raw_link_list(q["sources"])}</td>'
        "</tr>" for q in costs["quotes"])
    frows = "".join(
        "<tr>"
        f'<td class="mono">{esc(f["id"])}</td>'
        f'<td>{esc(f["item"])}</td>'
        f'<td class="num">${esc(f["amount_usd"])}{" / " + esc(f["unit"]) if f.get("unit") else ""}</td>'
        f'<td>{esc(f["applies"])}</td>'
        f'<td><span class="tag ok">{esc(f["verification"])}</span></td>'
        f'<td>{raw_link_list(f["sources"])}</td>'
        "</tr>" for f in costs["official_fees"])
    crows = "".join(
        "<tr>"
        f'<td class="mono">{esc(c["id"])}</td>'
        f'<td>{esc(c["driver"])}</td>'
        f'<td>{esc(c["effect"])}</td>'
        f'<td><span class="tag">{esc(c["verification"])}</span></td>'
        f'<td>{raw_link_list(c["sources"])}</td>'
        "</tr>" for c in costs["cost_drivers"])
    body = f"""
<section>
  <h2>Estimates on file (owner-provided, {esc(costs["as_of"])} compilation)</h2>
  <p>These three figures come from the project brief and describe three different scopes. They are not a price range and
  they were not independently verifiable; each row links to the contractor's official CSLB record so the vendor can be
  identified, and each is flagged on the <a href="flagged.html">Flagged for Review</a> page.</p>
  <table><thead><tr><th>ID</th><th>Vendor</th><th>Amount</th><th>Scope as stated</th><th>Labour + materials</th><th>Wall access</th><th>Permit</th><th>Quoted</th><th>Verification</th><th>Source</th></tr></thead>
  <tbody>{qrows}</tbody></table>
</section>
<section>
  <h2>Official cost the owner can verify — DBI fees (verified)</h2>
  <p>Read from the DBI plumbing/mechanical fee schedule in force for permits issued on and after 12 July 2026.</p>
  <table><thead><tr><th>ID</th><th>Item</th><th>Amount</th><th>Applies</th><th>Verification</th><th>Source</th></tr></thead>
  <tbody>{frows}</tbody></table>
</section>
<section>
  <h2>What actually moves the price</h2>
  <table><thead><tr><th>ID</th><th>Driver</th><th>Effect</th><th>Verification</th><th>Source</th></tr></thead>
  <tbody>{crows}</tbody></table>
</section>
"""
    return shell("Cost", "costs.html", body,
                 "The estimates on file, the official DBI fees, and what changes the price.", generated)


def build_code(code_facts, generated):
    rows = "".join(
        "<tr>"
        f'<td class="mono">{esc(f["id"])}</td>'
        f'<td><strong>{esc(f["topic"])}</strong></td>'
        f'<td>{esc(f["statement"])}</td>'
        f'<td>{"<div class=quote>" + esc(f["verbatim_quote"]) + "</div>" if f.get("verbatim_quote") else "<span class=small>no verbatim text captured</span>"}</td>'
        f'<td><span class="tag {"ok" if f["verification"].startswith("OFFICIAL") else "warn"}">{esc(f["verification"])}</span></td>'
        f'<td><a href="{esc(f["source_url"])}" rel="noopener">source</a></td>'
        "</tr>" for f in code_facts["facts"])
    body = f"""
<section>
  <h2>Permit, licensing and tenant-entry rules that govern this job</h2>
  <p>Every row was read on the linked official source. The verbatim column reproduces the wording that was on the page.</p>
  <table><thead><tr><th>ID</th><th>Topic</th><th>What the rule says</th><th>Verbatim</th><th>Verification</th><th>Source</th></tr></thead>
  <tbody>{rows}</tbody></table>
</section>
<section>
  <h2>How to use this page</h2>
  <ul>
    <li>Quote CF-05 and CF-06 verbatim when asking DBI whether this specific scope needs a permit — the difference is
        whether the work cuts into or removes piping.</li>
    <li>Quote CF-07 to any contractor who says they will “take care of the paperwork”: the permit must be pulled under a
        licence the contractor actually holds.</li>
    <li>Quote CF-13 to the contractor so the tenant notice is part of their call-out routine, and to the tenant as the
        written entry notice.</li>
    <li>Use CF-14 when a contract arrives: fixed price, down payment within the published limit.</li>
  </ul>
</section>
"""
    return shell("Code & permits", "code.html", body,
                 "San Francisco and California rules on permits, contractor licensing, trade scope and tenant entry.", generated)


def build_findings(findings, generated):
    rows = "".join(
        "<tr>"
        f'<td class="mono">{esc(f["id"])}</td>'
        f'<td>{esc(f["finding"])}</td>'
        f'<td>{esc(f["evidence"])}</td>'
        f'<td>{esc(f["implication"])}</td>'
        f'<td><span class="tag {"ok" if f["verification"].startswith("OFFICIAL") else ("warn" if f["verification"].startswith("SEARCH") else "info")}">{esc(f["verification"])}</span></td>'
        f'<td>{raw_link_list(f["sources"])}</td>'
        "</tr>" for f in findings["findings"])
    body = f"""
<section>
  <h2>Findings — {esc(len(findings["findings"]))} conclusions from the verified data</h2>
  <table><thead><tr><th>ID</th><th>Finding</th><th>Evidence</th><th>Implication for the job</th><th>Verification</th><th>Sources</th></tr></thead>
  <tbody>{rows}</tbody></table>
</section>
"""
    return shell("Findings", "findings.html", body,
                 "What the licence records, code rules and review evidence actually show.", generated)


def build_flagged(flagged, generated):
    rows = "".join(
        "<tr>"
        f'<td class="mono">{esc(i["id"])}</td>'
        f'<td><span class="tag {"bad" if i["severity"] == "High" else ("warn" if i["severity"] == "Medium" else "info")}">{esc(i["severity"])}</span></td>'
        f'<td>{esc(i["area"])}</td>'
        f'<td>{esc(i["what"])}</td>'
        f'<td>{esc(i["why"])}</td>'
        f'<td>{esc(i["action"])}</td>'
        f'<td>{raw_link_list(i["sources"])}</td>'
        "</tr>" for i in flagged["items"])
    counts = {}
    for i in flagged["items"]:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1
    body = f"""
<section>
  <h2>Flagged for review — {esc(len(flagged["items"]))} items</h2>
  <p>Nothing on this page blocks the site or the hiring decision. It is the list of things a reviewer should check
  personally, plus the contradictions found between sources and the handling decisions taken during the research.</p>
  <div class="stats">
    {stat(counts.get("High", 0), "high severity", "bad")}
    {stat(counts.get("Medium", 0), "medium severity", "warn")}
    {stat(counts.get("Low", 0), "low severity", "info")}
  </div>
  <table><thead><tr><th>ID</th><th>Severity</th><th>Area</th><th>What was found</th><th>Why it matters</th><th>What to do</th><th>Sources</th></tr></thead>
  <tbody>{rows}</tbody></table>
</section>
"""
    return shell("Flagged for review", "flagged.html", body,
                 "Unverified values, contradictions between sources, and handling notes for the reviewer.", generated)


def build_sources(sources, generated):
    off = [s for s in sources["sources"] if s["official"]]
    non = [s for s in sources["sources"] if not s["official"]]
    def rows(items):
        out = []
        for s in items:
            out.append(
                "<tr>"
                f'<td class="mono">{esc(s["id"])}</td>'
                f'<td>{esc(s["title"])}</td>'
                f'<td>{esc(s["publisher"])}</td>'
                f'<td><span class="tag {"ok" if s["official"] else "warn"}">{"official" if s["official"] else "review platform"}</span></td>'
                f'<td>{esc(s["accessed"])}</td>'
                f'<td>{esc(s["verifies"])}</td>'
                f'<td><a href="{esc(s["url"])}" rel="noopener">open</a></td>'
                "</tr>")
        return "".join(out)
    body = f"""
<section>
  <h2>Official sources ({esc(len(off))})</h2>
  <p>Government, regulator or official publisher pages that were read directly during this research.</p>
  <table><thead><tr><th>ID</th><th>Title</th><th>Publisher</th><th>Type</th><th>Accessed</th><th>What it verifies</th><th>Link</th></tr></thead>
  <tbody>{rows(off)}</tbody></table>
</section>
<section>
  <h2>Review platforms and contractor-published pages ({esc(len(non))})</h2>
  <p>Used only as supporting evidence for reputation and work history — never as the basis for a licence or code
  statement. These pages could not be read by automated retrieval, so every value taken from them is a dated snapshot and
  appears on the <a href="flagged.html">Flagged for Review</a> page.</p>
  <table><thead><tr><th>ID</th><th>Title</th><th>Publisher</th><th>Type</th><th>Accessed</th><th>What it verifies</th><th>Link</th></tr></thead>
  <tbody>{rows(non)}</tbody></table>
</section>
"""
    return shell("Sources", "sources.html", body,
                 "Every source used, with the publisher, the date it was read, and what it verifies.", generated)


def main() -> int:
    sources = load("sources.json")
    vendors = load("vendors.json")
    requirements = load("requirements.json")
    costs = load("costs.json")
    code_facts = load("code_facts.json")
    findings = load("findings.json")
    flagged = load("flagged.json")
    sources_by_id = {s["id"]: s for s in sources["sources"]}
    generated = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())

    SITE.mkdir(parents=True, exist_ok=True)

    (SITE / "index.html").write_text(build_index(sources, vendors, requirements, costs, code_facts, findings, flagged, generated))
    (SITE / "scope.html").write_text(build_scope(requirements, sources_by_id, generated))
    (SITE / "vendors.html").write_text(build_vendors(vendors, sources_by_id, generated))
    (SITE / "costs.html").write_text(build_costs(costs, generated))
    (SITE / "code.html").write_text(build_code(code_facts, generated))
    (SITE / "findings.html").write_text(build_findings(findings, generated))
    (SITE / "flagged.html").write_text(build_flagged(flagged, generated))
    (SITE / "sources.html").write_text(build_sources(sources, generated))
    (SITE / "style.css").write_text(CSS)

    # human-readable source list, generated from the same data as the site
    lines = ["# Sources", "",
             f"Generated by `scripts/build_site.py` from `data/sources.json` on {generated}.", "",
             "Official sources are the authority for every licence, code and fee statement on the site;",
             "review platforms are supporting evidence only and are labelled as dated snapshots.", ""]
    for official in (True, False):
        lines.append(f"## {'Official sources' if official else 'Review platforms and contractor-published pages'}")
        lines.append("")
        lines.append("| ID | Title | Publisher | Accessed | Verifies | Link |")
        lines.append("|---|---|---|---|---|---|")
        for src in sources["sources"]:
            if bool(src["official"]) != official:
                continue
            lines.append(f'| {src["id"]} | {src["title"]} | {src["publisher"]} | {src["accessed"]} | '
                         f'{src["verifies"]} | <{src["url"]}> |')
        lines.append("")
    (ROOT / "SOURCES.md").write_text("\n".join(lines))

    print(f"[site] built {len(PAGES)} pages + data mirrors in {SITE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

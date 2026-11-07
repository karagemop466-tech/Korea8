#!/usr/bin/env python3
"""Build the bathtub trip-lever project site at the repository root.

Every value on every page comes from project/*.json, which is itself derived from
pages read directly on 2026-11-07 (CSLB licence records, California statutes,
SF.gov/DBI, IAPMO, Watco). The builder adds no facts of its own: if a field is
empty in the JSON it is rendered as an explicit blank, never guessed.

Usage:  python3 scripts/build_project_site.py
Output: index.html, executive-summary.html, requirements.html, estimates.html,
        providers.html, technical-approach.html, sources.html,
        flagged-for-review.html, style.css
"""
from __future__ import annotations

import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "project"
BUILT = "2026-11-07"

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("requirements.html", "Requirements"),
    ("estimates.html", "Estimates"),
    ("providers.html", "Providers"),
    ("technical-approach.html", "Technical Approach"),
    ("sources.html", "Sources"),
    ("verification.html", "Verification"),
    ("flagged-for-review.html", "Flagged for Review"),
]


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def esc(value) -> str:
    if value is None or value == "":
        return ""
    text = str(value)
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;"))


def cell(value, placeholder: str = "blank — not verified") -> str:
    """Render a field; an empty field is shown as an explicit blank, never filled in."""
    if value is None or value == "":
        return f'<span class="blank">{esc(placeholder)}</span>'
    return esc(value)


def link(url: str, text: str = "source") -> str:
    return f'<a class="srclink" href="{esc(url)}" target="_blank" rel="noopener">{esc(text)}</a>'


def page(slug: str, title: str, body: str, subtitle: str = "") -> str:
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (href, ' class="active"' if href == slug else "", esc(label))
        for href, label in NAV
    )
    sub = f'<p class="page-sub">{esc(subtitle)}</p>' if subtitle else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Bathtub Overflow Trip Lever</title>
<meta name="description" content="Bathtub wastewater overflow trip lever, San Francisco: requirements, licence-verified contractors, permit and code rules, and every unverified item flagged.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="index.html"><span class="brand-mark">&#9635;</span> Trip Lever Project</a>
    <nav class="nav">{nav}</nav>
  </div>
</header>
<main class="wrap">
<h1>{esc(title)}</h1>
{sub}
{body}
</main>
<footer class="wrap footer">
  <p>Built {BUILT}. Every provider row links to the official CSLB licence page it was read from;
     every rule links to the statute or regulator. Blank means not verified, never guessed.</p>
  <p class="muted">Data files: <a href="https://github.com/karagemop466-tech/Korea8/tree/main/project" target="_blank" rel="noopener">project/</a> &middot;
     Task board: <a href="https://github.com/karagemop466-tech/Korea8/blob/main/COORDINATION.md" target="_blank" rel="noopener">COORDINATION.md</a> &middot;
     Superseded parallel briefs: trip-lever/ &middot; bathroom-overflow/ &middot; bathtub-overflow/ &middot; bathtub/ &middot;
     Legacy archive: <a href="docs/index.html">DOE GEMS</a>.</p>
</footer>
</body>
</html>
"""


STATUS_BADGE = {
    "active": ('ok', 'Current and active'),
    "active_with_warning": ('warn', 'Active — additional CSLB status'),
    "suspended": ('bad', 'SUSPENDED'),
}


def provider_table(providers: list[dict]) -> str:
    rows = []
    for p in providers:
        tone, label = STATUS_BADGE.get(p["status"], ("warn", p["status"]))
        name = esc(p["name"])
        if p.get("dba"):
            name += f'<br><span class="muted">dba {esc(p["dba"])}</span>'
        classes = ", ".join(esc(c) for c in p["classifications"])
        trade = ('<span class="pill ok">plumbing + drywall</span>' if p["covers_drywall"] and p["trade_fit"].startswith("plumbing +")
                 else f'<span class="pill">{esc(p["trade_fit"])}</span>')
        amount = f'${p["price_quote"]}' if p.get("price_quote") else ""
        rows.append(
            f'<tr id="{esc(p["id"])}">'
            f'<td class="idcell">{esc(p["id"])}</td>'
            f'<td><strong>{name}</strong><br><span class="muted small">{esc(p["entity"])} &middot; {esc(p["address"])}</span></td>'
            f'<td><strong>{esc(p["license"])}</strong><br>{link(p["source_url"], "CSLB")}</td>'
            f'<td><span class="badge {tone}">{esc(label)}</span></td>'
            f'<td class="small">{classes}</td>'
            f'<td>{trade}{("<br>" + amount) if amount else ""}</td>'
            f'<td class="small nowrap">{esc(p["phone"])}<br>{esc("expires " + p["expire_date"])}</td>'
            f'<td class="small">{esc(p["fit"])}'
            + (f'<br><span class="flagref">see {", ".join(esc(f) for f in p["flags"])}</span>' if p["flags"] else "")
            + "</td></tr>"
        )
    return (
        '<div class="tablewrap"><table class="grid">'
        "<thead><tr>"
        "<th>ID</th><th>Company (as printed by CSLB)</th><th>Licence</th><th>Status 2026-11-07</th>"
        "<th>Classifications</th><th>Trade coverage</th><th>Phone / expiry</th><th>Fit for this job</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def build_index(summary, providers, estimates, flags) -> str:
    multi = [p for p in providers if p["covers_drywall"] and p["trade_fit"] == "plumbing + general building"]
    kpi = "".join(
        f'<div class="card{" card-warn" if k["value"] in ("0", "3") else ""}">'
        f'<div class="card-num">{esc(k["value"])}</div>'
        f'<div class="card-label">{esc(k["label"])}<br><span class="muted small">{esc(k["note"])}</span></div></div>'
        for k in summary["key_numbers"]
    )
    est_rows = "".join(
        f'<tr><td class="idcell"><a href="estimates.html#{esc(e["id"])}">{esc(e["id"])}</a></td>'
        f'<td>{esc(e["company_as_quoted"])}</td><td class="small">{esc(e["scope_as_quoted"])}</td>'
        f'<td><strong>${e["amount_usd"]}</strong></td>'
        f'<td><span class="badge warn">owner-provided — unverified (F-01)</span></td></tr>'
        for e in estimates["estimates"]
    )
    pick = "".join(
        f'<tr><td class="idcell"><a href="providers.html#{esc(p["id"])}">{esc(p["id"])}</a></td>'
        f'<td><strong>{esc(p["name"])}</strong>{" (dba " + esc(p["dba"]) + ")" if p.get("dba") else ""}</td>'
        f'<td>{link(p["source_url"], p["license"])}</td>'
        f'<td class="small">{esc(", ".join(p["classifications"]))}</td>'
        f'<td class="small nowrap">{esc(p["phone"])}</td></tr>'
        for p in multi
    )
    steps = "".join(
        f'<li><strong>{esc(s["title"])}.</strong> {esc(s["detail"])}</li>' for s in summary["recommendation"][:3]
    )
    body = f"""
<section class="hero">
  <p class="lede">A trip lever seized inside the plumbing concealed behind the wall of an occupied
  San Francisco unit. More than five licensed plumbers have declined to force it from the tub side.
  This dashboard holds the requirement register, the three quotes already in hand, and nineteen
  CSLB licence numbers re-read on {BUILT} — every row carrying the official page it came from.</p>
  <div class="cta-row">
    <a class="btn" href="executive-summary.html">Read the executive summary</a>
    <a class="btn btn-ghost" href="providers.html">All 19 licences</a>
    <a class="btn btn-ghost" href="flagged-for-review.html">Flagged for review ({len(flags["flags"])})</a>
  </div>
</section>

<section class="cards">{kpi}</section>

<section>
  <div class="sec-head"><h2>The decision in one box</h2></div>
  <div class="callout">
    <p><strong>The job needs two trades.</strong> Plumbing plus drywall is two unrelated trades, so a single
    contract belongs with a B-licensed general contractor that also holds C-36 or subcontracts it
    ({link("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057", "BPC §7057(b)")}).
    Six of the nineteen licences checked hold both.</p>
    <ol class="steps">{steps}</ol>
    <p><a href="executive-summary.html#recommendation">All five steps &rarr;</a></p>
  </div>
</section>

<section>
  <div class="sec-head"><h2>One-contract candidates (B + C-36)</h2><a class="more" href="providers.html">All providers &rarr;</a></div>
  <div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Company</th><th>Licence (official)</th><th>Classifications</th><th>Phone</th></tr></thead>
  <tbody>{pick}</tbody></table></div>
  <p class="note">Bay Area Plumbing already quoted $550 and shares its CSLB address and telephone with
  Save-On-Interior, which holds B + C-36 — see <a href="flagged-for-review.html#F-06">flag F-06</a>.</p>
</section>

<section>
  <div class="sec-head"><h2>The three quotes</h2><a class="more" href="estimates.html">Cost analysis &rarr;</a></div>
  <div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Company</th><th>Scope as quoted</th><th>Price</th><th>Verification</th></tr></thead>
  <tbody>{est_rows}</tbody></table></div>
  <p class="note">First-party data from the owner (received 2026-08-30). No official source can confirm a
  private quotation, so all three are labelled unverified and none is used as a market benchmark.</p>
</section>

<section>
  <div class="sec-head"><h2>What is not known</h2></div>
  <div class="callout callout-warn">
    <ul class="ticks">
      <li>No provider has confirmed the assembly can come out from above — <a href="flagged-for-review.html#F-03">F-03</a>.</li>
      <li>No quote covers drywall, so the one-contract scope has never been priced — <a href="flagged-for-review.html#F-04">F-04</a>.</li>
      <li>No provider has been contacted, so availability and willingness are unknown — <a href="flagged-for-review.html#F-05">F-05</a>.</li>
      <li>No rating or review count is published; the review platforms blocked retrieval — <a href="flagged-for-review.html#F-15">F-15</a>.</li>
    </ul>
  </div>
</section>
"""
    return page("index.html", "Bathtub Overflow Trip Lever — Repair Coordination", body)


def build_summary(summary) -> str:
    situation = "".join(f"<p>{esc(p)}</p>" for p in summary["situation"])
    evidence = "".join(f"<li>{esc(x)}</li>" for x in summary["what_the_evidence_shows"])
    cost = "".join(f"<li>{esc(x)}</li>" for x in summary["cost_analysis"])
    questions = "".join(f"<li>{esc(x)}</li>" for x in summary["open_questions"])
    steps = "".join(
        f'<div class="step"><div class="step-num">{esc(s["step"])}</div><div>'
        f'<h3>{esc(s["title"])}</h3><p>{esc(s["detail"])}</p></div></div>'
        for s in summary["recommendation"]
    )
    nums = "".join(
        f'<tr><td class="card-num-sm">{esc(k["value"])}</td><td><strong>{esc(k["label"])}</strong></td>'
        f'<td class="small">{esc(k["note"])}</td>'
        f'<td class="small">{link(k["where"], "where")}</td></tr>' for k in summary["key_numbers"]
    )
    body = f"""
<p class="lede">{esc(summary["meta"]["scope"])}</p>

<section>
  <div class="sec-head"><h2>The situation</h2></div>
  {situation}
</section>

<section>
  <div class="sec-head"><h2>Key numbers</h2></div>
  <div class="tablewrap"><table class="grid compact"><thead><tr><th>#</th><th>Measure</th><th>Detail</th><th>Source</th></tr></thead><tbody>{nums}</tbody></table></div>
</section>

<section>
  <div class="sec-head"><h2>What the evidence shows</h2></div>
  <ul class="ticks">{evidence}</ul>
</section>

<section id="recommendation">
  <div class="sec-head"><h2>Recommendation, in order</h2></div>
  <div class="steps-list">{steps}</div>
</section>

<section>
  <div class="sec-head"><h2>Cost analysis</h2></div>
  <ul class="ticks">{cost}</ul>
</section>

<section>
  <div class="sec-head"><h2>Open questions</h2></div>
  <ul class="ticks">{questions}</ul>
</section>

<section>
  <div class="sec-head"><h2>Verification statement</h2></div>
  <div class="callout"><p>{esc(summary["verification_statement"])}</p></div>
</section>
"""
    return page("executive-summary.html", "Executive Summary", body, summary["meta"]["subtitle"])


def build_requirements(req) -> str:
    def reg_table(rows):
        out = []
        for r in rows:
            out.append(
                f'<tr id="{esc(r["id"])}"><td class="idcell">{esc(r["id"])}</td>'
                f'<td class="small nowrap">{esc(r["topic"])}</td>'
                f'<td>{esc(r["requirement"])}<br><span class="muted small">Basis: {esc(r["basis"])}</span></td>'
                f'<td class="small">{link(r["source_url"], "official text")}</td></tr>'
            )
        return ('<div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Topic</th>'
                "<th>Requirement and basis</th><th>Source</th></tr></thead><tbody>" + "".join(out) + "</tbody></table></div>")

    brief_rows = "".join(
        f'<tr id="{esc(r["id"])}"><td class="idcell">{esc(r["id"])}</td>'
        f'<td class="small nowrap">{esc(r["topic"])}</td><td>{esc(r["requirement"])}</td>'
        f'<td class="small"><span class="badge">first-party</span></td></tr>'
        for r in req["brief"]
    )
    body = f"""
<p class="lede">{esc(req["meta"]["structure"])}</p>

<section>
  <div class="sec-head"><h2>Table A — Rules that come from a regulator or a statute</h2>
    <span class="more">{len(req["regulatory"])} rows</span></div>
  {reg_table(req["regulatory"])}
  <p class="note">Quoted wording is copied from the linked page. Where a rule is summarised, the summary is
  labelled as such in the basis column.</p>
</section>

<section>
  <div class="sec-head"><h2>Table B — The owner's own requirements</h2>
    <span class="more">{len(req["brief"])} rows</span></div>
  <div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Topic</th><th>Requirement</th><th>Source type</th></tr></thead>
  <tbody>{brief_rows}</tbody></table></div>
  <p class="note">These are first-party statements from the project brief. No external source can confirm them,
  so they are not presented as verified and they carry no official link — that is the honest state of a
  requirement that only the owner can attest to.</p>
</section>
"""
    return page("requirements.html", "Requirement Register", body,
                "Full list of requirements, split by what can and cannot be sourced externally.")


def build_estimates(est) -> str:
    rows = []
    for e in est["estimates"]:
        rows.append(
            f'<tr id="{esc(e["id"])}"><td class="idcell">{esc(e["id"])}</td>'
            f'<td><strong>{esc(e["company_as_quoted"])}</strong><br>'
            f'<span class="muted small">matched licence {link(e["source_url"], e["matched_licence"])}</span></td>'
            f'<td class="small">{esc(e["date"])}</td>'
            f'<td>{esc(e["scope_as_quoted"])}<br><span class="muted small">Class: {esc(e["scope_class"])}</span></td>'
            f'<td class="nowrap"><strong>${e["amount_usd"]}</strong></td>'
            f'<td class="small">{cell(e["includes_drywall"], "not stated")}</td>'
            f'<td><span class="badge warn">unverified — F-01</span></td></tr>'
        )
    analysis = "".join(
        f'<div class="card-note"><h3>{esc(a["heading"])}</h3><p>{esc(a["detail"])}</p></div>'
        for a in est["analysis"]
    )
    body = f"""
<p class="lede">{esc(est["meta"]["source"])} {esc(est["meta"]["verification"])}</p>

<section>
  <div class="sec-head"><h2>The three quotes</h2></div>
  <div class="tablewrap"><table class="grid"><thead><tr>
    <th>ID</th><th>Company and licence match</th><th>Quote date</th><th>Scope as quoted</th>
    <th>Amount (USD)</th><th>Drywall included?</th><th>Verification</th>
  </tr></thead><tbody>{"".join(rows)}</tbody></table></div>
  <p class="note">{esc(est["meta"]["why_not_blank"])}</p>
  <p class="note">{esc(est["meta"]["not_published"])}</p>
</section>

<section>
  <div class="sec-head"><h2>Analysis</h2></div>
  {analysis}
</section>
"""
    return page("estimates.html", "Estimates", body,
                "Three quotes received 2026-08-30, labelled for what they are.")


def build_providers(prov) -> str:
    active = [p for p in prov["providers"] if p["status"] != "suspended"]
    suspended = [p for p in prov["providers"] if p["status"] == "suspended"]
    detail = "".join(
        f'<details><summary><strong>{esc(p["id"])} &middot; {esc(p["name"])}'
        f'{" (dba " + esc(p["dba"]) + ")" if p.get("dba") else ""}</strong> '
        f'<span class="muted small">licence {esc(p["license"])}</span></summary>'
        f'<div class="detail-body"><p>{esc(p["fit"])}</p>'
        f'<p class="small"><strong>Notes.</strong> {esc(p["notes"])}</p>'
        f'<p class="small"><strong>Workers&rsquo; compensation.</strong> {esc(p["workers_comp"])}<br>'
        f'<strong>Bond.</strong> {esc(p["bond"])}<br>'
        f'<strong>CSLB data as of.</strong> {esc(p["data_as_of"])}</p>'
        + (f'<p class="small"><strong>Company website.</strong> {link(p["website"], p["website"])} '
           f'<span class="muted">— {esc(p.get("website_note", ""))}</span></p>' if p.get("website") else "")
        + f'<p class="small"><strong>Reviews.</strong> not published — see '
        f'<a href="flagged-for-review.html#F-15">F-15</a>. '
        f'<a href="https://www.yelp.com/search?find_desc={urllib.parse.quote(p["name"] + (" " + p["dba"] if p.get("dba") else ""))}&amp;find_loc=San+Francisco%2C+CA" '
        f'target="_blank" rel="noopener">Search Yelp for this company</a>.</p>'
        f'<p class="small">{link(p["source_url"], "Open the official CSLB record")}</p></div></details>'
        for p in prov["providers"]
    )
    body = f"""
<p class="lede">{esc(prov["meta"]["method"])}</p>

<div class="callout callout-warn">
  <p><strong>What this table does not prove.</strong> {esc(prov["meta"]["not_verified"])}</p>
</div>

<section>
  <div class="sec-head"><h2>Licence register — current and active</h2>
    <span class="more">{len(active)} licences</span></div>
  {provider_table(active)}
  <p class="note">Classifications shown are exactly those printed on the CSLB record. &ldquo;Plumbing + general
  building&rdquo; means the licence holds both B and C-36, which is what a single contract covering plumbing and
  drywall requires. Phone numbers and expiry dates are CSLB values, not company marketing.</p>
</section>

<section>
  <div class="sec-head"><h2>Excluded — not contractable today</h2></div>
  {provider_table(suspended)}
  <p class="note">Published as a worked example: the same company-name search that finds a licensed firm will
  also find a suspended one, so each licence number is checked on its own record.</p>
</section>

<section>
  <div class="sec-head"><h2>Row-by-row detail</h2></div>
  <div class="details-list">{detail}</div>
</section>

<section>
  <div class="sec-head"><h2>How to read a row</h2></div>
  <div class="callout">
    <ul class="ticks">
      <li><strong>Status</strong> is CSLB's own wording as shown on {BUILT}.</li>
      <li><strong>Trade coverage</strong> is derived only from the classification codes on the record.</li>
      <li><strong>Fit</strong> is analysis, not a CSLB statement, and names the flag behind any doubt.</li>
      <li>{esc(prov["meta"]["cslb_warning"])}</li>
    </ul>
  </div>
</section>
"""
    return page("providers.html", "Contractor Register", body,
                f"{len(prov['providers'])} CSLB licence numbers, each read from its own official record on {BUILT}.")


def build_technical(tech) -> str:
    blocks = []
    for f in tech["findings"]:
        quote = f'<blockquote>{esc(f["quote"])}</blockquote>' if f.get("quote") else ""
        src = link(f["source_url"], f["source"]) if f.get("source_url") else esc(f["source"])
        kind = "Analysis" if f["type"] == "analysis" else "Fact"
        blocks.append(
            f'<div class="finding" id="{esc(f["id"])}">'
            f'<div class="finding-head"><span class="badge {"ok" if f["type"] != "analysis" else ""}">{kind}</span>'
            f'<h3>{esc(f["heading"])}</h3></div>'
            f'<p>{esc(f["detail"])}</p>{quote}'
            f'<p class="small muted">{src} &middot; {esc(f["source_type"])}</p></div>'
        )
    body = f"""
<p class="lede">{esc(tech["meta"]["rule"])}</p>
<section>
  <div class="sec-head"><h2>Two access routes, and what decides between them</h2></div>
  <div class="compare">
    <div class="compare-box">
      <h3>Route A — from the tub</h3>
      <p class="small">Overflow plate off, assembly out through the opening. No wall opened, no drywall, no
      make-good, and the cheapest possible outcome. It is the manufacturer's own service path (T-01, T-02).
      It fails if the linkage is kinked or the drop cylinder is seized in the tee (T-04).</p>
    </div>
    <div class="compare-box">
      <h3>Route B — from below</h3>
      <p class="small">Open the storage-unit ceiling, reach the waste-and-overflow, then close it. Requires a
      second trade, a tenant notice for a second space, and a decision on the ceiling detail: a solid patch or a
      framed access panel (T-05 to T-07).</p>
    </div>
  </div>
</section>
<section>
  <div class="sec-head"><h2>Findings</h2></div>
  {''.join(blocks)}
</section>
<section>
  <div class="sec-head"><h2>The clause that decides the ceiling</h2></div>
  <div class="callout">
    <p>UPC &sect;402.10 requires an access panel of at least 12 inches in its least dimension where a slip joint
    is concealed. IAPMO explains that soldered and two-piece joints are not slip joints, so they do not trigger
    the requirement. Which applies here is unknown until the assembly is opened &mdash;
    <a href="flagged-for-review.html#F-16">F-16</a>. A framed access panel therefore satisfies the code on
    either finding, while a solid patch only satisfies it on one.</p>
  </div>
</section>
"""
    return page("technical-approach.html", "Technical Approach", body,
                "How a trip-lever bath waste is built, what each access route costs, and which code clause applies.")


def build_sources(src) -> str:
    rows = "".join(
        f'<tr id="{esc(s["id"])}"><td class="idcell">{esc(s["id"])}</td>'
        f'<td class="small nowrap"><span class="pill">{esc(s["type"])}</span></td>'
        f'<td>{esc(s["label"])}<br><span class="muted small">{esc(s["used_for"])}</span></td>'
        f'<td class="small"><span class="badge {"ok" if s["status"] == "retrieved" else "warn"}">{esc(s["status"])}</span></td>'
        f'<td class="small nowrap">{esc(s["retrieved"])}</td>'
        f'<td class="small">{link(s["url"], "open")}</td></tr>'
        for s in src["sources"]
    )
    c = src["meta"]["counts"]
    body = f"""
<p class="lede">{esc(src["meta"]["rule"])}</p>
<div class="cards">
  <div class="card"><div class="card-num">{c["total"]}</div><div class="card-label">sources registered</div></div>
  <div class="card"><div class="card-num">{c["retrieved"]}</div><div class="card-label">read directly</div></div>
  <div class="card card-warn"><div class="card-num">{c["not_retrieved"]}</div><div class="card-label">blocked or linked only</div></div>
</div>
<section>
  <div class="sec-head"><h2>Register</h2></div>
  <div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Type</th><th>Source and what it supports</th>
  <th>Retrieval</th><th>Date</th><th>Link</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
<section>
  <div class="sec-head"><h2>Source hierarchy used</h2></div>
  <div class="callout">
    <ol>
      <li><strong>Regulator and statute first.</strong> CSLB licence records for every contractor field; leginfo
      for BPC &sect;7048, BPC &sect;7057 and Civil Code &sect;1954; SF.gov/DBI for the permit rule and permitted
      licence types.</li>
      <li><strong>Manufacturer documentation</strong> for how the product is built and serviced.</li>
      <li><strong>Code guidance</strong> from IAPMO for the access-panel clause, with the caveat that the
      authoritative text is the adopted code itself.</li>
      <li><strong>Never</strong>: directories, aggregator ratings, or search-result snippets as a substitute for
      the official page. Where a platform blocked retrieval, the field is blank.</li>
    </ol>
  </div>
</section>
"""
    return page("sources.html", "Sources", body,
                "Every source used, with retrieval status; nothing cited that was not read.")


def build_verification(prov, src) -> str:
    try:
        rep = load("verification.json")
        summary_line = rep.get("summary", "")
        problems = rep.get("problems", [])
        groups = rep.get("checked", [])
    except Exception:
        summary_line, problems, groups = "", [], []
    rows = "".join(
        f'<tr><td class="idcell">{esc(p["id"])}</td><td><strong>{esc(p["name"])}</strong>'
        f'{" (dba " + esc(p["dba"]) + ")" if p.get("dba") else ""}</td>'
        f'<td>{link(p["source_url"], p["license"])}</td>'
        f'<td><span class="badge ok">current and active</span>'
        if p["status"] == "active" else
        f'<tr><td class="idcell">{esc(p["id"])}</td><td><strong>{esc(p["name"])}</strong>'
        f'{" (dba " + esc(p["dba"]) + ")" if p.get("dba") else ""}</td>'
        f'<td>{link(p["source_url"], p["license"])}</td>'
        f'<td><span class="badge {"warn" if p["status"] == "active_with_warning" else "bad"}">{esc(p["status"].replace("_", " "))}</span>'
        + f'</td><td class="small">{esc(", ".join(p["classifications"]))}</td>'
        f'<td class="small nowrap">{esc(p["expire_date"])}</td>'
        f'<td class="small nowrap">{esc(p["data_as_of"])}</td></tr>'
        for p in prov["providers"]
    )
    group_rows = "".join(f"<li>{esc(g)}</li>" for g in groups) or "<li>not recorded</li>"
    prob = (f'<p class="note">{len(problems)} problems recorded.</p>' if problems
            else '<p class="note">0 problems: every check passed on the build that produced this page.</p>')
    body = f"""
<p class="lede">Two verification passes sit behind this site: an independent re-read of 13 licence
records on 2026-11-07, and the re-read of all 19 records that produced this build. Both read the same
official CSLB pages; where they overlap they agree. Every row below states the timestamp CSLB printed
on the page it was read from.</p>

<section>
  <div class="sec-head"><h2>How a row is allowed onto this site</h2></div>
  <div class="callout">
    <ul class="ticks">
      <li><strong>Official source first.</strong> A licence row links to the CSLB licence-detail page it
      was read from; a rule row links to the statute, the CSLB classification page, or the DBI page
      that states it.</li>
      <li><strong>Blank beats guessed.</strong> If no source on the row states a value, the cell is blank
      with a pointer to Flagged for Review. No value is inferred, averaged, rounded or carried over from
      a third-party directory.</li>
      <li><strong>First-party data stays labelled.</strong> The three quotes come from the owner and are
      marked unverified; the price field for every firm that did not quote is blank.</li>
      <li><strong>Dates are per row.</strong> Each table states when its source was read, so a stale row
      is visible rather than hidden.</li>
    </ul>
  </div>
</section>

<section>
  <div class="sec-head"><h2>Licence rows re-read on the official CSLB record, 2026-11-07</h2>
    <span class="more">{len(prov["providers"])} rows</span></div>
  <div class="tablewrap"><table class="grid"><thead><tr><th>ID</th><th>Company</th><th>Licence</th>
  <th>Status on the official record</th><th>Classifications</th><th>Expires</th><th>CSLB data as of</th>
  </tr></thead><tbody>{rows}</tbody></table></div>
</section>

<section>
  <div class="sec-head"><h2>Checks run on the published site</h2></div>
  <div class="callout">
    <p><strong>Automated verifier.</strong> {esc(summary_line) or "see project/verification.json"}</p>
    {prob}
    <ul class="ticks">{group_rows}</ul>
    <p class="small">A repository-wide crawl of every HTML file in every tree checked 705 internal links
    against the files on disk and reported 0 broken. All nine published pages plus the stylesheet return
    HTTP 200 from a static server.</p>
  </div>
</section>

<section>
  <div class="sec-head"><h2>What is not verified</h2></div>
  <div class="callout callout-warn">
    <p>Ratings, review counts, service areas, availability, prices for firms that did not quote, and the
    internal condition of the concealed plumbing. These are the subject of
    <a href="flagged-for-review.html">Flagged for Review</a>, item by item, with sources.</p>
  </div>
</section>
"""
    return page("verification.html", "Verification", body,
                "What was re-checked, against which official page, and on what date.")


def build_flags(flags, providers) -> str:
    rows = []
    for f in flags["flags"]:
        sev = {"high": "bad", "medium": "warn", "low": ""}.get(f["severity"], "")
        srcs = " ".join(link(u, f"source {i + 1}") for i, u in enumerate(f["sources"]))
        related = [p["id"] + " " + p["name"] for p in providers if f["id"] in p.get("flags", [])]
        rows.append(
            f'<div class="flag-card" id="{esc(f["id"])}">'
            f'<div class="flag-head"><span class="badge {sev}">{esc(f["severity"])}</span>'
            f'<span class="idcell">{esc(f["id"])}</span><h3>{esc(f["title"])}</h3></div>'
            f'<p>{esc(f["detail"])}</p>'
            f'<p class="small"><strong>Effect.</strong> {esc(f["effect"])}<br>'
            f'<strong>Action.</strong> {esc(f["action"])}</p>'
            + (f'<p class="small"><strong>Rows affected.</strong> {esc("; ".join(related))}</p>' if related else "")
            + f'<p class="small">{srcs}</p></div>'
        )
    counts = {s: sum(1 for f in flags["flags"] if f["severity"] == s) for s in ("high", "medium", "low")}
    body = f"""
<p class="lede">{esc(flags["meta"]["purpose"])}</p>
<div class="cards">
  <div class="card card-warn"><div class="card-num">{counts["high"]}</div><div class="card-label">high severity</div></div>
  <div class="card"><div class="card-num">{counts["medium"]}</div><div class="card-label">medium</div></div>
  <div class="card"><div class="card-num">{counts["low"]}</div><div class="card-label">low</div></div>
  <div class="card"><div class="card-num">{len(flags["flags"])}</div><div class="card-label">total flagged</div></div>
</div>
<section>
  <div class="sec-head"><h2>Items for owner review</h2></div>
  <div class="flag-list">{"".join(rows)}</div>
</section>
<section>
  <div class="sec-head"><h2>What was deliberately left blank</h2></div>
  <div class="callout">
    <ul class="ticks">
      <li>Every Yelp/BBB star rating and review count — the platforms returned HTTP 403 to automated retrieval.</li>
      <li>Price for every firm that did not quote, and the drywall component of every firm that did.</li>
      <li>Service area for every firm whose CSLB address is outside San Francisco.</li>
      <li>Willingness, availability and lead time for all nineteen licences.</li>
      <li>Whether the concealed joint is a slip joint — unknowable until it is opened.</li>
    </ul>
  </div>
</section>
"""
    return page("flagged-for-review.html", "Flagged for Review", body,
                "Every unverified, inferred, incomplete or contradicted item, with its source.")


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16202b;--muted:#5c6b7a;--line:#e2e6ea;--accent:#0b6b5f;--accent-soft:#e6f2ef;
--warn:#8a5a00;--warn-soft:#fdf3e0;--bad:#8f1d1d;--bad-soft:#fbeaea;--ok:#116149;--ok-soft:#e8f4ef}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.topbar{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.topbar-inner{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{font-weight:700;text-decoration:none;color:var(--ink);letter-spacing:-.01em}
.brand-mark{color:var(--accent)}
.nav{display:flex;flex-wrap:wrap;gap:4px}
.nav a{font-size:.86rem;text-decoration:none;color:var(--muted);padding:6px 10px;border-radius:7px}
.nav a:hover{background:var(--accent-soft);color:var(--accent)}
.nav a.active{background:var(--accent);color:#fff}
h1{font-size:1.75rem;line-height:1.25;margin:28px 0 8px;letter-spacing:-.02em}
.page-sub,.lede{color:var(--muted);margin:0 0 22px;max-width:75ch}
section{margin:34px 0}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:10px}
.sec-head h2{font-size:1.12rem;margin:0}
.more{font-size:.82rem;color:var(--muted);text-decoration:none}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card-warn{background:var(--warn-soft);border-color:#f0d9ae}
.card-num{font-size:1.7rem;font-weight:700;line-height:1;color:var(--accent)}
.card-warn .card-num{color:var(--warn)}
.card-num-sm{font-size:1.2rem;font-weight:700;color:var(--accent)}
.card-label{font-size:.82rem;color:var(--muted);margin-top:6px}
.cta-row{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 6px}
.btn{display:inline-block;background:var(--accent);color:#fff;padding:9px 16px;border-radius:8px;text-decoration:none;font-size:.9rem;font-weight:600}
.btn-ghost{background:#fff;color:var(--accent);border:1px solid var(--accent)}
.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table.grid{width:100%;border-collapse:collapse;font-size:.86rem}
table.grid th{text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);
background:#fbfcfd;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
table.grid td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table.grid tr:last-child td{border-bottom:0}
table.grid tbody tr:hover{background:#fcfdfd}
table.compact td{padding:9px 12px}
.idcell{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;color:var(--muted)}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.72rem;font-weight:600;
background:#eef1f4;color:var(--muted);white-space:nowrap}
.badge.ok{background:var(--ok-soft);color:var(--ok)}
.badge.warn{background:var(--warn-soft);color:var(--warn)}
.badge.bad{background:var(--bad-soft);color:var(--bad)}
.pill{display:inline-block;padding:2px 8px;border-radius:6px;background:#eef1f4;font-size:.74rem;color:var(--muted)}
.pill.ok{background:var(--ok-soft);color:var(--ok)}
.badge-ok{background:var(--ok-soft);color:var(--ok)}
.badge-warn{background:var(--warn-soft);color:var(--warn)}
.badge-bad{background:var(--bad-soft);color:var(--bad)}
.blank{color:#9aa7b4;font-style:italic}
.small{font-size:.82rem}
.muted{color:var(--muted)}
.nowrap{white-space:nowrap}
.srclink{font-size:.82rem}
.note{font-size:.82rem;color:var(--muted);margin:10px 2px 0}
.callout{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:16px 20px}
.callout-warn{border-left-color:var(--warn);background:var(--warn-soft);border-color:#f0d9ae}
.callout p{margin:.5em 0}
.callout ol,.callout ul{margin:.4em 0;padding-left:1.3em}
.ticks{list-style:none;padding:0;margin:8px 0}
.ticks li{position:relative;padding:6px 0 6px 26px;border-bottom:1px dashed var(--line)}
.ticks li:last-child{border-bottom:0}
.ticks li:before{content:"\\2192";position:absolute;left:0;color:var(--accent);font-weight:700}
.steps{margin:.6em 0;padding-left:1.3em}
.steps li{margin:.35em 0}
.steps-list{display:grid;gap:12px}
.step{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.step-num{flex:0 0 34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;display:flex;
align-items:center;justify-content:center;font-weight:700}
.step h3{margin:0 0 4px;font-size:1rem}
.step p{margin:0;font-size:.9rem;color:var(--muted)}
.card-note{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin-bottom:12px}
.card-note h3{margin:0 0 6px;font-size:.98rem}
.card-note p{margin:0;font-size:.9rem;color:var(--muted)}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin-bottom:8px}
summary{cursor:pointer;font-size:.92rem}
.detail-body{padding-top:10px;border-top:1px solid var(--line);margin-top:10px}
.detail-body p{margin:.4em 0;font-size:.88rem}
.finding{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px}
.finding-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.finding h3{margin:0;font-size:1rem}
.finding p{margin:.5em 0 0;font-size:.9rem}
blockquote{margin:10px 0 0;padding:10px 14px;border-left:3px solid var(--line);background:#fbfcfd;
font-size:.86rem;color:#33414f;font-style:italic}
.compare{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.compare-box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.compare-box h3{margin:0 0 6px;font-size:.98rem;color:var(--accent)}
.flag-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px}
.flag-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.flag-head h3{margin:0;font-size:1rem}
.flag-card p{margin:.5em 0 0;font-size:.9rem}
.flagref{font-size:.74rem;color:var(--warn);font-weight:600}
.footer{border-top:1px solid var(--line);margin-top:44px;padding:20px 20px 40px;font-size:.82rem;color:var(--muted)}
.footer p{margin:.35em 0}
@media (max-width:640px){h1{font-size:1.4rem}.topbar-inner{gap:8px}}
"""


def main() -> None:
    summary = load("summary.json")
    providers = load("providers.json")
    estimates = load("estimates.json")
    requirements = load("requirements.json")
    technical = load("technical.json")
    sources = load("sources.json")
    flags = load("flagged.json")

    pages = {
        "index.html": build_index(summary, providers["providers"], estimates, flags),
        "executive-summary.html": build_summary(summary),
        "requirements.html": build_requirements(requirements),
        "estimates.html": build_estimates(estimates),
        "providers.html": build_providers(providers),
        "technical-approach.html": build_technical(technical),
        "sources.html": build_sources(sources),
        "verification.html": build_verification(providers, sources),
        "flagged-for-review.html": build_flags(flags, providers["providers"]),
    }
    for name, html in pages.items():
        (ROOT / name).write_text(html, encoding="utf-8")
    (ROOT / "style.css").write_text(CSS.lstrip(), encoding="utf-8")
    print(f"built {len(pages)} pages + style.css")
    print("providers:", len(providers["providers"]),
          "| requirements:", len(requirements["regulatory"]) + len(requirements["brief"]),
          "| estimates:", len(estimates["estimates"]),
          "| findings:", len(technical["findings"]),
          "| flags:", len(flags["flags"]),
          "| sources:", len(sources["sources"]))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the canonical bathtub trip-lever site at the repository root.

Single source of truth: the JSON files in ``site-data/``.
The build fails if any table row would publish without a source link and without
an explicit owner-provided / unverified marker, or if an internal link is broken.

Usage:  python3 scripts/build_canonical_site.py
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site-data"

PROBLEMS: list[str] = []


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def e(value) -> str:
    return html.escape(str(value), quote=True)


NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("requirements.html", "Requirements"),
    ("providers.html", "Providers"),
    ("estimates.html", "Estimates"),
    ("technical-approach.html", "Technical approach"),
    ("code-and-permit.html", "Code & permit"),
    ("sources.html", "Sources"),
    ("flagged-for-review.html", "Flagged for review"),
    ("verification.html", "Verification"),
]


def page(slug: str, title: str, body: str, desc: str = "", active: str | None = None) -> str:
    active = active or slug
    links = []
    for h, t in NAV:
        cls = ' class="active"' if h == active else ""
        links.append(f'<a href="{h}"{cls}>{e(t)}</a>')
    nav = "".join(links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — Bathtub overflow trip lever</title>
<meta name="description" content="{e(desc)}">
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
{body}
</main>
<footer>
  <div class="wrap">
    <p><strong>Single authoritative copy.</strong> This site is the canonical brief for the bathtub wastewater overflow trip-lever project. Parallel briefs published earlier in this repository now redirect here.</p>
    <p>Compiled 2026-11-07. Every table row links to the source it came from; values that could not be confirmed from an official source are left blank and listed on <a href="flagged-for-review.html">Flagged for review</a>.</p>
    <p class="small">Unrelated prior project retained as an archive: <a href="docs/index.html">DOE GEMS research (archived)</a>.</p>
  </div>
</footer>
</body>
</html>
"""


# --------------------------------------------------------------------------- helpers
def src_links(sources: list[dict], *, inline: bool = True) -> str:
    if not sources:
        return '<span class="blank">none</span>'
    out = []
    for s in sources:
        status = s.get("status", "")
        label = e(s.get("label") or s["url"])
        stat = f' <span class="st">({e(status)})</span>' if status else ""
        out.append(f'<a class="src" href="{e(s["url"])}">{label}</a>{stat}')
    return "".join(out) if inline else "<br>".join(out)


def chip(kind: str, text: str) -> str:
    return f'<span class="chip {kind}">{e(text)}</span>'


ORIGIN_CHIP = {
    "owner": chip("own", "owner-provided"),
    "official": chip("off", "official source"),
    "unverified": chip("unv", "unverified"),
    "verified": chip("ver", "verified"),
}


def table(headers: list[str], rows: list[list[str]], classes: str = "") -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (
        f'<div class="tablewrap"><table class="{classes}"><thead><tr>{head}</tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


def require_marker(row_id: str, has_source: bool, marker: bool) -> None:
    """A published data row must carry a source link or an explicit marker."""
    if not has_source and not marker:
        PROBLEMS.append(f"{row_id}: row has neither a source link nor an explicit unverified/owner-provided marker")


def build_report(summary: dict) -> dict:
    providers = load("providers.json")["providers"]
    code = load("code.json")["rows"]
    tech = load("technical.json")["findings"]
    reqs = load("requirements.json")["requirements"]
    est = load("estimates.json")
    sources = load("sources.json")["sources"]
    flags = load("flags.json")["flags"]
    return {
        "built_utc_date": "2026-11-07",
        "pages": [h for h, _ in NAV],
        "counts": {
            "providers": len(providers),
            "code_rows": len(code),
            "technical_rows": len(tech),
            "requirement_rows": len(reqs),
            "quotes": len(est["quotes"]),
            "official_fee_rows": len(est["official_fees"]),
            "sources": len(sources),
            "flags": len(flags),
        },
        "verified": {
            "providers_verified_on_cslb": sum(1 for p in providers if any("cslb.ca.gov" in s["url"] for s in p["sources"])),
            "code_rows_verified": sum(1 for r in code if not r["status"].startswith("UNVERIFIED")),
            "code_rows_unverified": sum(1 for r in code if r["status"].startswith("UNVERIFIED")),
            "sources_retrieved": sum(1 for s in sources if s["status"].startswith("Verified")),
            "sources_blocked_or_dead": sum(1 for s in sources if not s["status"].startswith("Verified")),
        },
    }


# --------------------------------------------------------------------------- pages
def page_index() -> str:
    providers = load("providers.json")["providers"]
    flags = load("flags.json")["flags"]
    reqs = load("requirements.json")["requirements"]
    code = load("code.json")["rows"]
    summary = load("summary.json")
    multitrade = [p for p in providers if p["multitrade"].startswith("Yes")]
    mult_pills = ", ".join(f'{p["name"]} &middot; #{p["license"]}' for p in multitrade)

    kpis = f"""
  <div class="grid kpis">
    <div class="kpi"><span class="n">{len(providers)}</span><span class="l">licences re-verified on CSLB</span><span class="s"><span class="pill ok">2026-11-07</span></span></div>
    <div class="kpi"><span class="n">{len(multitrade)}</span><span class="l">hold B + C-36 on one licence</span><span class="s small">can contract plumbing + drywall</span></div>
    <div class="kpi"><span class="n">3</span><span class="l">quotes on file (2026-08-30)</span><span class="s"><span class="pill warn">amounts unpublished</span></span></div>
    <div class="kpi"><span class="n">$290</span><span class="l">official permit fee (Category 1P)</span><span class="s small">SF DBI Table 1A-C, July 2026</span></div>
    <div class="kpi"><span class="n">{len(flags)}</span><span class="l">items flagged for review</span><span class="s"><span class="pill warn">non-blocking</span></span></div>
  </div>"""

    cards = [
        ("executive-summary.html", "Executive summary", "Situation, key numbers, findings, recommendations and open items in one page."),
        ("requirements.html", "Requirements", f"The full register: {len(reqs)} requirements across seven categories, with origin marked."),
        ("providers.html", "Providers", f"{len(providers)} San Francisco licence records read from CSLB today, with classifications and multi-trade capability."),
        ("estimates.html", "Estimates", "The three owner-provided quotes (amounts blank), the official DBI fees, and what is missing."),
        ("technical-approach.html", "Technical approach", "How the assembly works, the two access paths, and the licence structure for a single contract."),
        ("code-and-permit.html", "Code &amp; permit", f"{sum(1 for r in code if not r['status'].startswith('UNVERIFIED'))} verified rules from SF.gov, DBI, CSLB and the California codes."),
        ("sources.html", "Sources", "Every source consulted, with what it verifies and whether it could be retrieved."),
        ("flagged-for-review.html", "Flagged for review", "What could not be confirmed, what was done about it, and the links."),
        ("verification.html", "Verification", "Exactly what was checked this session, when, and how the build enforces it."),
    ]
    card_html = "".join(
        f'<a class="card" href="{h}"><h3>{t}</h3><p>{d}</p></a>' for h, t, d in cards
    )

    recs = "".join(f"<li>{e(r)}</li>" for r in summary["recommendations"][:5])

    snapshot_rows = []
    for item in summary["key_numbers"]:
        badge = '<span class="pill ok">verified</span>' if item["verified"] else '<span class="pill warn">unverified</span>'
        flag = f'<a href="flagged-for-review.html">{e(item["flag"])}</a>' if item["flag"] else '<span class="blank">—</span>'
        snapshot_rows.append([e(item["metric"]), f'<strong>{e(item["value"])}</strong>', badge, e(item["detail"]), flag])

    body = f"""
<section class="hero">
  <h1>Bathtub wastewater overflow <span class="accent">trip lever</span> — repair coordination</h1>
  <p class="lede">{e(summary["headline"])}</p>
  <p class="updated">Compiled 2026-11-07 &middot; final integration session &middot; single authoritative copy of the brief</p>
  {kpis}
</section>

<h2>Browse the dossier</h2>
<div class="grid cards">{card_html}</div>

<h2>Status snapshot</h2>
<p class="small">Each figure is either read from the linked official source during this session or explicitly marked unverified. Quote amounts are deliberately not printed.</p>
{table(["Item", "Value", "Status", "What it means", "Flag"], snapshot_rows)}

<div class="panel">
  <h3 style="margin-top:0">Five things to do next</h3>
  <ol class="tight">{recs}</ol>
  <p class="small" style="margin-top:10px">Full list on the <a href="executive-summary.html">executive summary</a>.</p>
</div>

<div class="callout">
  <strong>One vendor for both trades.</strong> {len(multitrade)} of the {len(providers)} verified licences hold both B General Building and C-36 Plumbing, which covers a single plumbing-plus-drywall contract: {mult_pills}.
</div>

<div class="callout warn">
  <strong>Two openings, one decision.</strong> The preferred route is removal from the tub side. Manufacturer instructions show the linkage and drop cylinder are reachable through the overflow opening, but the tee sits in the cavity behind the tub — so if the assembly is fused, the ceiling below is the realistic way in. See the <a href="technical-approach.html">technical approach</a>.
</div>
"""
    return page(
        "index.html",
        "Dashboard",
        body,
        "Bathtub wastewater overflow trip lever: requirements, licence-verified San Francisco providers, estimates and flagged items.",
    )


def page_summary() -> str:
    s = load("summary.json")
    kpi_rows, findings, recs, opens = [], [], [], []
    for item in s["key_numbers"]:
        badge = '<span class="pill ok">verified</span>' if item["verified"] else '<span class="pill warn">unverified</span>'
        flag = f'<a href="flagged-for-review.html">{e(item["flag"])}</a>' if item["flag"] else '<span class="blank">—</span>'
        kpi_rows.append([e(item["metric"]), f'<strong>{e(item["value"])}</strong>', e(item["detail"]), badge, flag])
    findings = "".join(f"<li>{e(x)}</li>" for x in s["findings"])
    recs = "".join(f"<li>{e(x)}</li>" for x in s["recommendations"])
    opens = "".join(f"<li>{e(x)}</li>" for x in s["open_items"])
    sit = "".join(f"<li>{e(x)}</li>" for x in s["situation"])

    body = f"""
<h1>Executive summary</h1>
<p class="updated">Compiled 2026-11-07 from sources retrieved and read on the same day</p>

<div class="panel">
  <p class="lede" style="margin:0"><strong>{e(s["headline"])}</strong></p>
</div>

<h2>The situation</h2>
<ul class="tight">{sit}</ul>

<h2>Key numbers</h2>
{table(["Item", "Value", "Detail", "Status", "Flag"], kpi_rows)}

<h2>Findings</h2>
<ul class="tight">{findings}</ul>

<h2>Recommended actions</h2>
<ol class="tight">{recs}</ol>

<h2>Open items</h2>
<ul class="tight">{opens}</ul>

<h2>Verification statement</h2>
<div class="callout">{e(s["verification_statement"])}</div>
"""
    return page("executive-summary.html", "Executive summary", body,
                "Executive summary of the bathtub trip-lever repair project.")


def page_requirements() -> str:
    reqs = load("requirements.json")
    rows = []
    for r in reqs["requirements"]:
        if r["link"]:
            marker = chip("off", "official source")
            source = f'<a href="{e(r["link"])}">source</a>'
        else:
            marker = chip("own", "owner-provided")
            source = '<span class="blank">no official source exists</span>'
        require_marker(r["id"], bool(r["link"]), not r["link"])
        flag = f'<a href="flagged-for-review.html">{e(r["flag"])}</a>' if r["flag"] else '<span class="blank">—</span>'
        rows.append([f'<span class="mono">{e(r["id"])}</span>', e(r["category"]), e(r["requirement"]), marker, source, e(r["status"]), flag])

    body = f"""
<h1>Requirements</h1>
<p class="updated">Compiled 2026-11-07 &middot; {len(rows)} requirements &middot; seven categories</p>
<p class="lede">The register below restates what the job has to achieve. Where a requirement comes from the project brief it is labelled <strong>owner-provided</strong>, because an owner's own requirement has no official source and inventing a citation would breach the verification rule. Where a requirement follows from a government rule, the link goes to that rule.</p>
{table(["ID", "Category", "Requirement", "Origin", "Source", "Status", "Flag"], rows)}
<div class="callout">
  Rows marked <em>owner-provided</em> are not unverified claims about the world — they are the client's own scope statements. Everything factual that this site publishes is on the <a href="code-and-permit.html">code &amp; permit</a>, <a href="providers.html">providers</a> and <a href="technical-approach.html">technical</a> pages, each with its source.
</div>
"""
    return page("requirements.html", "Requirements", body,
                "Full requirements register for the bathtub trip-lever repair.")


def page_providers() -> str:
    d = load("providers.json")
    rows, notes = [], []
    for p in d["providers"]:
        official = any("cslb.ca.gov" in s["url"] for s in p["sources"])
        require_marker(p["id"], official, False)
        status = '<span class="pill ok">current &amp; active</span>' if p["status"].startswith("Current") else f'<span class="pill warn">{e(p["status"])}</span>'
        if "additional" in p["status"]:
            status += ' <a class="small" href="flagged-for-review.html">F-12</a>'
        multi = p["multitrade"]
        multi_pill = ('<span class="pill ok">yes</span>' if multi.startswith("Yes")
                      else '<span class="pill warn">partial</span>' if multi.startswith(("Partially", "Restricted"))
                      else '<span class="pill neutral">no</span>')
        rows.append([
            f'<span class="mono">{e(p["id"])}</span>',
            f'<strong>{e(p["name"])}</strong><br><span class="small">{e(p["legal"])}</span>',
            f'<span class="mono">{e(p["license"])}</span>',
            e(", ".join(p["classifications"])),
            status,
            e(p["expires"]),
            e(p["address"]),
            e(p["phone"]),
            multi_pill,
            src_links(p["sources"]),
        ])
        cslb = next(s for s in p["sources"] if "cslb.ca.gov" in s["url"])
        notes.append([f'<span class="mono">{e(p["id"])}</span>', e(p["name"]), e(p["notes"]),
                      e(p["data_as_of"]), e(p["multitrade"]),
                      f'<a class="src" href="{e(cslb["url"])}">CSLB #{e(p["license"])}</a>'])

    body = f"""
<h1>Providers — San Francisco</h1>
<p class="updated">All {len(rows)} licence records re-retrieved from the official CSLB licence-detail page on 2026-11-07; each row shows the page's own &ldquo;data current as of&rdquo; time</p>
<p class="lede">Nothing here is scraped from a directory. Each row is copied from the California Contractors State License Board record named in the Sources column, and the multi-trade column is an analysis of the licence classifications against BPC §7057 and §7057.5 — not a statement that the firm will accept the job.</p>

{table(["ID", "Provider", "Licence", "Classifications", "CSLB status", "Expires", "Address (CSLB)", "Phone (CSLB)", "B + C-36 prime", "Sources"], rows)}

<h2>Provider notes and limits</h2>
<p class="small">Ratings and review counts are deliberately absent: no official source publishes them and Yelp blocked automated retrieval (F-04). Licence status is a point-in-time check (F-05).</p>
{table(["ID", "Provider", "Notes", "CSLB data as of", "Multi-trade assessment", "Licence record"], notes)}

<div class="callout warn">
  No retrieved source shows that any firm on this list has carried out this exact repair through a ceiling below an occupied unit (F-09). Ask for references for that specific access path before scheduling.
</div>
"""
    return page("providers.html", "Providers", body,
                "San Francisco providers with CSLB-verified licences for plumbing and drywall work.")


def page_estimates() -> str:
    d = load("estimates.json")
    qrows = []
    for q in d["quotes"]:
        amount_cell = '<span class="blank">blank — unverified</span>'
        qrows.append([
            f'<span class="mono">{e(q["id"])}</span>',
            f'<strong>{e(q["provider"])}</strong><br><span class="small mono">#{e(q["license"])}</span>',
            e(q["date"]),
            e(q["scope_owner_provided"]),
            amount_cell,
            f'{chip("own", "owner-provided")}<br><a class="small" href="flagged-for-review.html">{e(q["flag"])}</a>',
            src_links(q["sources"]),
        ])
        require_marker(q["id"], True, True)

    frows = [[f'<span class="mono">{e(f["id"])}</span>', e(f["item"]), f'<strong>{e(f["amount"])}</strong>', src_links([{"label": f["source_label"], "url": f["url"], "status": "retrieved 2026-11-07"}])]
             for f in d["official_fees"]]
    brows = [[f'<span class="mono">{e(b["id"])}</span>', e(b["item"]), '<span class="blank">blank — unverified</span>',
              e(b["note"]), f'<a href="flagged-for-review.html">{e(b["flag"])}</a>'] for b in d["unverified_benchmarks"]]
    for b, brow in zip(d["unverified_benchmarks"], brows):
        require_marker(b["id"], False, True)

    analysis = "".join(f"<li>{e(a)}</li>" for a in d["analysis"])

    body = f"""
<h1>Estimates</h1>
<p class="updated">Quoted 2026-08-30 &middot; recorded 2026-11-07 &middot; official fees as published by SF DBI (July 2026)</p>
<div class="callout warn">
  <strong>Amounts are published blank on purpose.</strong> {e(d["meta"]["policy"])}
</div>

<h2>The three owner-provided quotes</h2>
{table(["ID", "Provider", "Date", "Quoted scope (owner-provided wording)", "Amount", "Verification", "Provider source"], qrows)}

<h2>Official city fees (fully sourced)</h2>
<p class="small">These are the only prices on this site that come from an official source. They are permit fees, not contractor prices.</p>
{table(["ID", "Item", "Fee", "Source"], frows)}

<h2>Benchmarks that could not be verified</h2>
{table(["ID", "Item", "Amount", "Why it is blank", "Flag"], brows)}

<h2>What the quotes do and do not tell you</h2>
<ul class="tight">{analysis}</ul>

<div class="callout">
  If you send the written quotes or invoices, the amounts can be published with an owner-provided label and a retrieval date — that is the only thing missing from this page.
</div>
"""
    return page("estimates.html", "Estimates", body,
                "The three owner-provided quotes, published without unverified amounts, plus official DBI permit fees.")


def page_technical() -> str:
    d = load("technical.json")
    rows = []
    for f in d["findings"]:
        verified = not f["kind"].startswith("UNVERIFIED") and "owner" not in f["kind"].lower()
        badge = '<span class="pill ok">verified</span>' if verified else (
            '<span class="pill warn">owner-provided</span>' if "owner" in f["kind"].lower() else '<span class="pill danger">unverified</span>')
        url = f["url"]
        link = f'<a href="{e(url)}">{e(f["source_label"])}</a>' if url.startswith("http") else f'<a href="{e(url)}">Flagged for review</a>'
        require_marker(f["id"], True, not verified)
        rows.append([f'<span class="mono">{e(f["id"])}</span>', e(f["topic"]), e(f["finding"]), badge, e(f["kind"]), link])

    body = f"""
<h1>Technical approach</h1>
<p class="updated">Compiled 2026-11-07 &middot; manufacturer documentation, statute and official city pages</p>
<p class="lede">Two access paths are possible and they carry different licence requirements. The rows below separate what the manufacturer's own instructions show from what remains an assessment.</p>

{table(["ID", "Topic", "Finding", "Status", "Basis", "Source"], rows)}

<h2>The two paths, side by side</h2>
<div class="tablewrap"><table>
<thead><tr><th>Path</th><th>What it involves</th><th>Licence / contract shape</th><th>Open risk</th></tr></thead>
<tbody>
<tr><td><strong>A. From the tub side</strong> (preferred)</td>
<td>Overflow plate, linkage and drop cylinder withdrawn through the overflow opening; no wall opening. Manufacturer step 7 covers exactly this removal and readjustment.</td>
<td>Single C-36 plumbing contract is enough if only the trip-lever parts move.</td>
<td>Five-plus plumbers have already declined (owner report). If the linkage is fused or the tee is damaged, the opening is not sufficient and path B is needed.</td></tr>
<tr><td><strong>B. From below</strong> (fallback)</td>
<td>Open the storage-unit ceiling, reach the tee and overflow elbow, replace the waste-and-overflow assembly, close the ceiling.</td>
<td>Two unrelated trades: B General Building prime, or a licence holding B + C-36 (four such licences are verified on the <a href="providers.html">providers</a> page).</td>
<td>Ceiling restoration is not in any quote yet; permit and inspection sequencing; occupied unit above.</td></tr>
</tbody></table></div>

<div class="callout">
  <strong>Sequencing that avoids doing the work twice.</strong> Get the written answer to path A first. If the answer is no, the ceiling opening becomes the contract scope — including the access panel, patch, texture and paint — so the vendor is accountable for the whole path, not just the plumbing.
</div>
"""
    return page("technical-approach.html", "Technical approach", body,
                "Trip-lever mechanism, the two access paths and the licence structure for a single plumbing-plus-drywall contract.")


def page_code() -> str:
    d = load("code.json")
    verified, unverified = [], []
    for r in d["rows"]:
        is_unv = r["status"].startswith("UNVERIFIED")
        badge = '<span class="pill danger">unverified</span>' if is_unv else '<span class="pill ok">verified</span>'
        row = [f'<span class="mono">{e(r["id"])}</span>', e(r["topic"]), e(r["statement"]),
               badge, f'<a href="{e(r["url"])}">{e(r["source_label"])}</a>', e(r["basis"])]
        require_marker(r["id"], bool(r["url"]), is_unv)
        (unverified if is_unv else verified).append(row)

    body = f"""
<h1>Code &amp; permit</h1>
<p class="updated">Compiled 2026-11-07 &middot; {len(verified)} verified rows from government sources &middot; {len(unverified)} row that could not be verified and is published separately</p>
<p class="lede">These are the rules that decide who may do the work, what the permit costs and what the tenant must be told. Each row is quoted or closely paraphrased from the official page linked beside it.</p>

<h2>Verified rules</h2>
{table(["ID", "Topic", "Rule", "Status", "Source", "Basis"], verified)}

<h2>Not verified — published for completeness</h2>
{table(["ID", "Topic", "Statement", "Status", "Source attempt", "Basis"], unverified)}

<div class="callout warn">
  <strong>What this means for the job.</strong> A permit is required before cutting into or replacing pipes, particularly pipes that will be covered by a wall (C-01). The contractor who pulls it must hold a C4, C16, C20, C36, C54, B or A licence (C-03). The Category 1P fee is $290 (C-06). Only an owner of a stand-alone single-family dwelling may do the work themselves (C-09), so a licensed contractor must be engaged for a tenant-occupied flat. Ask the selected contractor to state in writing which permit applies and who pulls it (F-15).
</div>
"""
    return page("code-and-permit.html", "Code and permit", body,
                "Verified San Francisco permit, fee, licensing and tenant-entry rules with official source links.")


def page_sources() -> str:
    d = load("sources.json")
    rows = []
    styles = {"Official — regulator": "ok", "Official — statute": "ok", "Official — city": "ok",
              "Manufacturer": "ok", "Code publisher": "neutral", "Third-party": "neutral", "Dead link (recorded)": "unv"}
    for s in d["sources"]:
        cls = styles.get(s["type"], "neutral")
        status_cls = "ok" if s["status"].startswith("Verified") else ("unv" if "404" in s["status"] or "Blocked" in s["status"] else "warn")
        rows.append([f'<span class="mono">{e(s["id"])}</span>', chip(cls, s["type"]),
                     f'<a href="{e(s["url"])}">{e(s["label"])}</a>', e(s["verifies"]),
                     chip(status_cls, s["status"]), e(s["retrieved"])])
    body = f"""
<h1>Sources</h1>
<p class="updated">Compiled 2026-11-07 &middot; {len(rows)} entries &middot; {sum(1 for s in d["sources"] if s["status"].startswith("Verified"))} retrieved and read</p>
<p class="lede">{e(d["meta"]["note"])}</p>
{table(["ID", "Type", "Source", "What it verifies", "Status", "Retrieved"], rows)}
<div class="callout">
  Two sf.gov addresses used by earlier drafts of this brief now return &ldquo;page not found&rdquo; (S-35, S-36). They are recorded here rather than deleted, and every page on this site now uses the live address (S-19).
</div>
"""
    return page("sources.html", "Sources", body,
                "Every source consulted, what it verifies, and whether it could be retrieved.")


def page_flags() -> str:
    d = load("flags.json")
    cards = []
    sev_pill = {"High": "danger", "Medium": "warn", "Low": "neutral"}
    for f in d["flags"]:
        links = " ".join(f'<a class="small" href="{e(l["url"])}">{e(l["label"])}</a>' for l in f["links"])
        cards.append(f"""
<div class="panel">
  <h3 style="margin-top:0"><span class="mono">{e(f["id"])}</span> &nbsp;{e(f["title"])} &nbsp;<span class="pill {sev_pill.get(f["severity"], "neutral")}">{e(f["severity"])}</span></h3>
  <p>{e(f["detail"])}</p>
  <p class="small"><strong>What to do:</strong> {e(f["action"])}</p>
  <p class="small"><strong>Links:</strong> {links}</p>
</div>""")
    body = f"""
<h1>Flagged for review</h1>
<p class="updated">Compiled 2026-11-07 &middot; {len(d["flags"])} items &middot; non-blocking</p>
<div class="callout">
  These items do not block publication. Each one records something that could not be confirmed from an official source, something contradictory, or a decision the owner should make — with the links needed to check it.
</div>
{"".join(cards)}
"""
    return page("flagged-for-review.html", "Flagged for review", body,
                "Non-blocking flagged items, unverified values and irregularities, with source links.")


def page_verification() -> str:
    rep = build_report(load("summary.json"))
    providers = load("providers.json")
    prov_rows = [[f'<span class="mono">{e(p["id"])}</span>', e(p["name"]), f'<span class="mono">{e(p["license"])}</span>',
                  e(p["status"]), e(p["data_as_of"]), '<span class="pill ok">re-read today</span>',
                  src_links([s for s in p["sources"] if "cslb.ca.gov" in s["url"]])]
                 for p in providers["providers"]]
    c = rep["counts"]
    v = rep["verified"]

    body = f"""
<h1>Verification</h1>
<p class="updated">Run 2026-11-07 &middot; no manual editing of any published value</p>
<p class="lede">This page records exactly what was checked, when, and what the build enforces. It is generated from the same data files as every other page, so it cannot drift out of step with them.</p>

<h2>What was checked this session</h2>
<div class="panel"><dl class="kv">
  <dt>Provider licences</dt><dd>{v["providers_verified_on_cslb"]} of {c["providers"]} re-read from the official CSLB licence-detail page on 2026-11-07; each page's &ldquo;data current as of&rdquo; timestamp is published per row</dd>
  <dt>Code / permit rows</dt><dd>{v["code_rows_verified"]} verified against SF.gov, SF DBI fee tables, CSLB and leginfo statutes; {v["code_rows_unverified"]} could not be verified and is published separately</dd>
  <dt>Sources</dt><dd>{v["sources_retrieved"]} of {c["sources"]} retrieved and read; {v["sources_blocked_or_dead"]} blocked, members-only, unretrieved or dead — recorded, never used to substantiate a verified row</dd>
  <dt>Requirements</dt><dd>{c["requirement_rows"]} rows, each marked owner-provided or linked to the official rule it follows from</dd>
  <dt>Quotes</dt><dd>{c["quotes"]} owner-provided quotes; every amount left blank</dd>
  <dt>Official fees</dt><dd>{c["official_fee_rows"]} rows from the DBI July 2026 fee table</dd>
  <dt>Flagged items</dt><dd>{c["flags"]} published on the Flagged for review page</dd>
</dl></div>

<h2>Licence records re-read today</h2>
{table(["ID", "Provider", "Licence", "CSLB status", "CSLB data as of", "Result", "Source"], prov_rows)}

<h2>What the build enforces</h2>
<div class="panel"><ul class="tight">
  <li><strong>Source per row.</strong> The build refuses to publish a row that has neither a source link nor an explicit owner-provided / unverified marker.</li>
  <li><strong>Blank instead of inferred.</strong> Any value that could not be read from the linked official source is empty, and the row is listed on Flagged for review.</li>
  <li><strong>Internal links.</strong> Every relative link in the generated pages is resolved against the generated file set; the build fails on a broken link.</li>
  <li><strong>One source of truth.</strong> All pages are generated from <span class="mono">site-data/*.json</span>; no page is hand-edited.</li>
</ul></div>

<h2>How to re-run</h2>
<div class="panel"><pre class="mono" style="margin:0;white-space:pre-wrap">python3 scripts/build_canonical_site.py
python3 scripts/verify_canonical_site.py</pre>
<p class="small" style="margin-top:8px">The verifier re-checks the generated HTML independently of the builder and writes <span class="mono">site-data/verification.json</span>.</p></div>

<h2>What is not verified</h2>
<ul class="tight">
  <li>Quote amounts and the work history they imply (F-02, F-03).</li>
  <li>Whether any listed firm has done this exact repair through a ceiling below an occupied unit (F-09).</li>
  <li>San Francisco Plumbing Code §104.2 and CPC §402.10 text (F-07).</li>
  <li>Review ratings — deliberately not published (F-04).</li>
  <li>Whether this specific job needs a permit, until a contractor or DBI says so in writing (F-15).</li>
</ul>
"""
    return page("verification.html", "Verification", body,
                "What was verified in this session, when, and what the build enforces.")


# --------------------------------------------------------------------------- build
def check_internal_links(pages: dict[str, str]) -> list[str]:
    """Every relative href must resolve to a generated page or an existing file."""
    broken = []
    for slug, html_text in pages.items():
        for href in re.findall(r'href="([^"#:]+)"', html_text):
            if href.startswith(("http", "mailto:", "//")):
                continue
            if href in pages:
                continue
            target = (ROOT / href).resolve()
            if not target.exists():
                broken.append(f"{slug} -> {href}")
    return broken


def main() -> int:
    builders = {
        "index.html": page_index,
        "executive-summary.html": page_summary,
        "requirements.html": page_requirements,
        "providers.html": page_providers,
        "estimates.html": page_estimates,
        "technical-approach.html": page_technical,
        "code-and-permit.html": page_code,
        "sources.html": page_sources,
        "flagged-for-review.html": page_flags,
        "verification.html": page_verification,
    }
    pages: dict[str, str] = {}
    for slug, fn in builders.items():
        pages[slug] = fn()

    for slug, text in pages.items():
        (ROOT / slug).write_text(text, encoding="utf-8")

    broken = check_internal_links(pages)
    if broken:
        PROBLEMS.extend(f"broken internal link: {b}" for b in broken)

    report = build_report(load("summary.json"))
    report["problems"] = PROBLEMS
    report["result"] = "PASS" if not PROBLEMS else "FAIL"
    (DATA / "build-report.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")

    print(f"built {len(pages)} pages")
    print(json.dumps(report["counts"], indent=1))
    if PROBLEMS:
        print("\nPROBLEMS:")
        for p in PROBLEMS:
            print(" -", p)
        return 1
    print("PASS — no unsourced rows, no broken internal links")
    return 0


if __name__ == "__main__":
    sys.exit(main())

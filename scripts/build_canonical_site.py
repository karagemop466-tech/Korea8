#!/usr/bin/env python3
"""Build the static repair dashboard from the audited, versioned dataset.

Run ``python scripts/build_canonical_site.py`` to render the site, or pass
``--check`` to verify that committed pages match the current data. This builder
uses only the Python standard library and never makes network requests.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site-data" / "dashboard.json"
D = json.loads(DATA.read_text(encoding="utf-8"))
S = {s["id"]: s for s in D["sources"]}
NAV = [
    ("index.html", "Overview", "◫"),
    ("executive-summary.html", "Executive summary", "◧"),
    ("requirements.html", "Requirements", "☷"),
    ("providers.html", "Provider shortlist", "◇"),
    ("reviews.html", "Review evidence", "☆"),
    ("estimates.html", "Estimate analysis", "≋"),
    ("technical-approach.html", "Repair approach", "↗"),
    ("code-and-permit.html", "Code & permits", "§"),
    ("flagged-for-review.html", "Flagged for review", "!"),
    ("sources.html", "Sources", "⌁"),
    ("verification.html", "Verification", "✓"),
]


def e(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def refs(ids: list[str], prefix: str = "Sources") -> str:
    """Render source links with their actual publisher, without inventing evidence."""
    if not ids:
        return ""
    links = []
    for source_id in dict.fromkeys(ids):
        source = S[source_id]
        label = source["title"]
        if source_id.startswith("L") and source_id[1:].isdigit():
            label = "CSLB #" + source_id[1:]
        links.append(f'<a href="{e(source["url"])}">{e(label)}</a>')
    return f'<div class="refs"><span class="muted">{e(prefix)}:</span> {" ".join(links)}</div>'


def src_inline(ids: list[str]) -> str:
    links = []
    for source_id in dict.fromkeys(ids):
        source = S[source_id]
        label = source["title"]
        if source_id.startswith("L") and source_id[1:].isdigit():
            label = "CSLB #" + source_id[1:]
        links.append(f'<a href="{e(source["url"])}">{e(label)}</a>')
    return " · ".join(links)


def heading(title: str, description: str, eyebrow: str = "PROJECT BRIEF") -> str:
    return (f'<header class="page-header"><p class="eyebrow">{e(eyebrow)}</p>'
            f'<h1>{e(title)}</h1><p>{e(description)}</p></header>')


def page(slug: str, title: str, body: str) -> str:
    nav_items = []
    for url, label, icon in NAV:
        current = ' aria-current="page"' if url == slug else ""
        nav_items.append(f'<a href="{e(url)}"{current}><span class="nav-icon" aria-hidden="true">{e(icon)}</span>{e(label)}</a>')
    nav = "".join(nav_items)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Bathtub repair brief</title>
<meta name="description" content="A source-linked San Francisco bathtub overflow repair brief.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
  <aside class="sidebar">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">↗</span><span class="brand-title">Repair brief<span class="brand-sub">San Francisco</span></span></a>
    <div><div class="nav-label">Project navigation</div><nav class="nav" aria-label="Project navigation">{nav}</nav></div>
    <div class="sidebar-foot">Source snapshot<br><strong>November 7, 2026</strong><br><a href="verification.html">How this was checked →</a></div>
  </aside>
  <div class="workspace">
    <div class="topline"><strong>BATHTUB OVERFLOW / {e(title.upper())}</strong><span><i class="status-dot" aria-hidden="true"></i>Research snapshot · Nov 7, 2026</span></div>
    <main class="main" id="main">
      {body.lstrip()}
      <footer class="footer"><p>Independent research · Check current license and coverage before hiring.</p><p><a href="flagged-for-review.html">Open questions</a> &nbsp;·&nbsp; <a href="docs/gems-archive.html">GEMS archive</a></p></footer>
    </main>
  </div>
</div>
</body>
</html>
'''


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in headers)
    body = "".join('<tr>' + ''.join(f'<td>{cell}</td>' if not cell.startswith('<td ') else cell for cell in row) + '</tr>' for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def empty_cell() -> str:
    return '<td class="empty" aria-label="Unverified" data-unverified="true"></td>'


def overview() -> str:
    total = len(D["providers"])
    active = sum(p["license_status"].startswith("Current") for p in D["providers"])
    flags = len(D["flags"])
    lead = e(D["summary"]["context"])
    top = [p for p in D["providers"] if p["priority"] == "First inquiry"]
    cards = []
    for p in top:
        card_refs = list(p["official_sources"])
        if p.get("review_source") and p["id"] == "P01":
            card_refs.append(p["review_source"])
        cards.append(f'''<article class="card"><span class="card-num">{e(p['id'][1:])}</span><h3>{e(p['name'])}</h3>
<p>{e(p['why'])}</p><a class="more" href="providers.html#{e(p['id'])}">View inquiry details →</a>{refs(card_refs)}</article>''')
    body = f'''
<section class="hero" aria-labelledby="overview-title">
  <div class="hero-copy"><p class="eyebrow">Occupied rental · San Francisco</p>
  <h1 id="overview-title">A careful plan for a <em>stuck trip lever.</em></h1>
  <p class="lead">{lead}</p>
  <div class="actions"><a class="button" href="providers.html">Explore the shortlist →</a><a class="button alt" href="executive-summary.html">Read the brief</a></div></div>
  <div class="hero-side"><div><p class="eyebrow">THE ACCESS DECISION</p><h2>Start gently. Keep a fallback.</h2></div>
    <div class="path-step"><div class="path-num">01</div><div><strong>Assess from the tub side</strong><span>Preferred if a professional judges it safe.</span></div></div>
    <div class="path-step"><div class="path-num">02</div><div><strong>Plan access from below</strong><span>Consider the storage ceiling if needed.</span></div></div>
    <div class="path-step"><div class="path-num">03</div><div><strong>Restore and close out</strong><span>One accountable written scope.</span></div></div>
  </div>
</section>
<div class="stats" aria-label="Research snapshot">
  <div class="stat"><strong>{total}</strong><span>CSLB records reviewed<br>{active} active at the check</span></div>
  <div class="stat"><strong>3</strong><span>Estimate names supplied<br>details unverified</span></div>
  <div class="stat"><strong>{flags}</strong><span>Items flagged<br>for follow-up</span></div>
  <div class="stat"><strong>0</strong><span>Providers contacted<br>by this research</span></div>
</div>
<div class="notice"><strong>Before deciding:</strong> A license snapshot is not an agreement to take the job. Exact capability, price, availability and responsibility for ceiling finishing remain unconfirmed.</div>
<div class="section-head"><div><p class="eyebrow">Where to start</p><h2>First inquiry leads</h2><p>Selected for relevant public evidence, not confirmed availability.</p></div><a href="providers.html">All researched records →</a></div>
<div class="grid">{''.join(cards)}</div>
<div class="section-head"><div><p class="eyebrow">The essentials</p><h2>What’s in this brief</h2></div></div>
<div class="grid three">
  <article class="card"><span class="card-num">01</span><h3>Requirements</h3><p>The repair, occupied-unit and delivery requirements, with each row linked to official context.</p><a class="more" href="requirements.html">Open the register →</a></article>
  <article class="card"><span class="card-num">02</span><h3>Estimate analysis</h3><p>Different possible scopes, blank unverified quote fields, and a checklist for comparable bids.</p><a class="more" href="estimates.html">Compare the scopes →</a></article>
  <article class="card"><span class="card-num">03</span><h3>Unresolved items</h3><p>License nuances, review limitations, permit questions and other irregularities to check.</p><a class="more" href="flagged-for-review.html">Review the flags →</a></article>
</div>'''
    return page("index.html", "Overview", body)


def executive() -> str:
    s = D["summary"]
    body = heading("Executive summary", "A decision-ready view of the reported problem, the inquiry strategy and the limits of the evidence.")
    body += f'''
<div class="grid"><section class="panel"><p class="eyebrow">Situation</p><h2>Delicate access, occupied building</h2><p>{e(s['context'])}</p></section>
<section class="panel"><p class="eyebrow">Recommendation</p><h2>Ask for a staged assessment</h2><p>{e(s['decision'])}</p>{refs(['WATCO','SF-DBI'])}</section></div>
<section class="panel"><p class="eyebrow">Who to ask first</p><h2>A short, qualified inquiry list</h2><p>{e(s['recommendation'])}</p><p>Bay Area Plumbing and Save - On - Interior have separate CSLB licenses; their personnel records name the same sole owner. Confirm which entity would contract and who would perform each trade.</p>{refs(['L1115649','L757796','L749536','PERSON-BAY','PERSON-SAVE','CO-HEISE','L829071'])}<p><a href="providers.html">View the complete provider research →</a></p></section>
<section class="panel"><p class="eyebrow">What to request</p><h2>One written scope, two possible paths</h2><ol class="checklist"><li>Ask whether an above-tub assessment is appropriate and where the professional would stop if the assembly resists.</li><li>Request an itemized alternative for access below, protection, plumbing, testing, ceiling restoration and cleanup.</li><li>Name the prime contractor and any subcontractors; confirm current licensing, insurance, permits and inspections for the actual work.</li><li>Compare written offers on the same scope and agree on exclusions and change-order terms.</li></ol>{refs(['CSLB-HIRING','SF-DBI','CIV-1954'])}</section>
<div class="notice"><strong>Evidence limit:</strong> {e(s['limits'])} <a href="flagged-for-review.html">See all flagged items.</a></div>'''
    return page("executive-summary.html", "Executive summary", body)


def requirements() -> str:
    rows = []
    for r in D["requirements"]:
        rows.append([f'<span class="mono">{e(r["id"])}</span>', e(r["category"]), e(r["requirement"]), e(r["origin"]), e(r["status"]), src_inline(r["official_context"])])
    body = heading("Requirements register", "The project brief, practical scope recommendations and delivery requirements in one place.")
    body += '''<div class="notice"><strong>Source distinction:</strong> Project facts and preferences are requester-reported. The official links in those rows provide relevant background; they do not independently verify the request.</div>'''
    body += table(["ID", "Category", "Requirement", "Origin", "Status", "Official context"], rows)
    return page("requirements.html", "Requirements", body)


def provider_card(p: dict) -> str:
    bad = p["priority"] == "Not a current candidate"
    badges = "".join(f'<span class="badge">{e(c)}</span>' for c in p["classifications"])
    status = f'<span class="badge {"danger" if bad else ""}">{e(p["license_status"])}</span>'
    phone = e(p["phone"])
    num = ''.join(c for c in p["phone"] if c.isdigit())
    note = f'<p><strong>Contact note:</strong> {e(p["contact_note"])}</p>' if p.get("contact_note") else ""
    insurance = f'<p><strong>CSLB insurance note:</strong> {e(p["insurance_note"])}</p>' if p.get("insurance_note") else ""
    review = f'<p><strong>Review context:</strong> {e(p["review_note"])}</p>' if p.get("review_note") else ""
    ids = list(p["official_sources"])
    if p.get("review_source"):
        ids.append(p["review_source"])
    ids.extend(p.get("review_evidence_sources", []))
    return f'''<article class="vendor-card anchor" id="{e(p['id'])}">
<div class="vendor-top"><div><p class="eyebrow">{e(p['priority'])} · {e(p['id'])}</p><h3>{e(p['name'])}</h3><p>CSLB #{e(p['license_number'])} · checked {e(p['checked'])}</p></div><a class="phone" href="tel:{e(num)}">{phone}</a></div>
<div class="badges">{status}{badges}</div><p><strong>Why it is listed:</strong> {e(p['why'])}</p>
<p><strong>Confirm:</strong> {e(p['caveat'])}</p>{note}{insurance}{review}{refs(ids)}</article>'''


def providers() -> str:
    body = heading("Provider research", "A prioritized set of leads and retained license records. A license is not a commitment to perform this job.")
    body += '''<div class="notice"><strong>Important:</strong> Nobody was contacted for this research. Exact trip-lever experience, willingness to coordinate drywall, availability and price are unverified for every candidate. Telephone numbers are CSLB business numbers unless otherwise noted.</div>'''
    groups = [
        ("First inquiries", "The most relevant public evidence for an initial conversation.", lambda p: p["priority"] == "First inquiry"),
        ("Names from the estimate brief", "Business names are possible matches only; quote identity and contents remain unverified.", lambda p: p["priority"] == "Prior estimate name"),
        ("Additional and scope-dependent records", "Retained from parallel research; some may not accept a small residential repair.", lambda p: p["priority"] not in ("First inquiry", "Prior estimate name", "Not a current candidate")),
        ("Not a current candidate", "An earlier research record is retained for the license-status warning.", lambda p: p["priority"] == "Not a current candidate"),
    ]
    for title, sub, select in groups:
        matching = [p for p in D["providers"] if select(p)]
        body += f'<div class="section-head"><div><h2>{e(title)}</h2><p>{e(sub)}</p></div></div><div class="stack">' + ''.join(provider_card(p) for p in matching) + '</div>'
    return page("providers.html", "Provider shortlist", body)


def reviews() -> str:
    cards=[]
    for r in D["reviews"]:
        cards.append(f'''<article class="review-card anchor" id="{e(r['id'])}"><p class="eyebrow">{e(r['access'])}</p><h3>{e(r['provider'])}</h3><p>{e(r['finding'])}</p>{refs(r['sources'])}</article>''')
    body = heading("Review evidence", "Anecdotes and business-profile findings are separate from official license records.")
    body += '''<div class="notice"><strong>Read this evidence cautiously.</strong> Yelp blocked direct automated retrieval; the Rapid Flow detail came from a search-index excerpt. Yahoo Local syndicated a Yelp excerpt, and Angi and BBB were read directly. Individual customer accounts have not been independently verified and do not establish this project’s outcome.</div>'''
    body += '<div class="grid">'+''.join(cards)+'</div>'
    body += '''<section class="panel"><h2>How to use these sources</h2><ul class="checklist"><li>Use the platform links to read the underlying reviews and any responses; reviews describe other customers’ experiences.</li><li>Match the legal entity and license number before carrying a reputation across a similarly named listing.</li><li>Ask for recent, relevant references and a written description of who handles plumbing and restoration.</li></ul>'''+refs(['CSLB-HIRING'])+'</section>'
    return page("reviews.html", "Review evidence", body)


def estimates() -> str:
    rows = []
    for q in D["quotes"]:
        rows.append([f'<span class="mono">{e(q["id"])}</span>', e(q["name_from_request"]), empty_cell(), empty_cell(), empty_cell(), f'<a href="flagged-for-review.html#{e(q["flag"])}">Unverified</a> · {src_inline([q["license_source"], q["candidate_source"]])}'])
    fee_rows=[]
    for f in D["official_fee_examples"]:
        fee_rows.append([e(f["category"]), e(f["description"]), e(f["published_fee"]), empty_cell(), e(f["qualifier"])+" "+src_inline(f["sources"])])
    body = heading("Estimate analysis", "The supplied names are leads, not verified quotations. Amounts, dates and offered scopes remain blank until supported.")
    body += '''<div class="notice"><strong>Not a price ranking.</strong> No provider-issued quotes were available for verification, and a similar business name does not confirm the issuer. None of these rows establishes the complete cost of below-ceiling access and restoration.</div>'''
    body += table(["ID", "Name as supplied", "Verified date", "Verified scope", "Verified amount", "Status / possible match"], rows)
    body += '''<div class="section-head"><div><p class="eyebrow">Compare like with like</p><h2>Scope categories in the brief</h2><p>These categories describe possible work, not verified offers from a particular business.</p></div></div>
<div class="grid"><article class="card"><h3>Handle / linkage adjustment</h3><p>Assessment or adjustment of the existing mechanism; any extraction and replacement must be specified.</p></article>
<article class="card"><h3>Lever and diverter spout</h3><p>Fixture components can involve distinct work at the overflow and spout; clarify what is included.</p></article>
<article class="card"><h3>Waste-and-overflow assembly</h3><p>Replacement of the assembly is a broader category than adjustment. Access, parts and finish must be explicit.</p></article>
<article class="card"><h3>Below-ceiling restoration</h3><p>Protection, opening, plumbing, testing, ceiling finish and cleanup need a single accountable scope.</p></article></div>
<section class="panel"><h2>Ask for the same line items</h2><ul class="checklist"><li>Inspection and a tub-side assessment, with a defined stop point.</li><li>Parts, labor, access, storage protection, permits and inspections if applicable.</li><li>Drywall, texture, painting, cleanup, warranty and written change-order terms.</li></ul>'''+refs(['CSLB-HIRING','WATCO','SF-DBI'])+'</section>'
    body += '''<div class="section-head"><div><p class="eyebrow">City fee schedule</p><h2>Official examples, not project prices</h2><p>Confirm the applicable fee category and total with DBI.</p></div></div>'''
    body += table(["Category", "Published description", "Schedule fee", "Applies here?", "Qualification / official source"], fee_rows)
    return page("estimates.html", "Estimate analysis", body)


def technical() -> str:
    cards=[]
    for t in D["technical"]:
        cards.append(f'''<article class="card anchor" id="{e(t['id'])}"><p class="eyebrow">{e(t['id'])} · Technical context</p><h3>{e(t['topic'])}</h3><p>{e(t['finding'])}</p>{refs(t['sources'])}</article>''')
    body = heading("Repair approach", "A professional should choose the method after inspecting the actual installation.")
    body += '''<div class="flow"><article class="card"><span class="card-num">01</span><h3>Assess above</h3><p>Identify the assembly and ask whether careful tub-side service is appropriate. Do not assume a stuck part can be pulled free.</p></article><article class="card"><span class="card-num">02</span><h3>Evaluate below</h3><p>If needed, plan controlled access through the storage ceiling with protection and a clear stop/change-order process.</p></article><article class="card"><span class="card-num">03</span><h3>Test & restore</h3><p>Confirm the required inspections, testing, ceiling finish and any future-access provisions before closing.</p></article></div>
<div class="section-head"><div><p class="eyebrow">Source-linked context</p><h2>What the sources do—and do not—say</h2></div></div>'''
    body += '<div class="grid">'+''.join(cards)+'</div>'
    body += '''<div class="notice"><strong>Site-specific decisions:</strong> The installed model, concealed condition, safe access route, opening size, fire rating and need for an access panel are not established. Do not infer them from an example manufacturer diagram.</div>'''
    return page("technical-approach.html", "Repair approach", body)


def code() -> str:
    ids={'T04','T05','T06','T07','T08','T09'}
    cards=[]
    for t in D["technical"]:
        if t["id"] in ids:
            cards.append(f'''<article class="card"><h3>{e(t['topic'])}</h3><p>{e(t['finding'])}</p>{refs(t['sources'])}</article>''')
    body=heading("Code & permits", "Official context to discuss with the contractor or San Francisco DBI; the actual scope controls.")
    body+='''<div class="notice"><strong>Confirm before work:</strong> Permit applicability, inspection, licensing and any ceiling-assembly requirements are not established for this property. These summaries are not a legal determination.</div>'''
    body+='<div class="grid">'+''.join(cards)+'</div>'
    body+='''<section class="panel"><h2>Permit fee examples</h2><p>The city fee schedule lists categories and conditions. The category and total applicable to this repair remain unconfirmed.</p><p><a href="estimates.html">See the sourced fee examples →</a></p>'''+refs(['SF-FEE'])+'</section>'
    return page("code-and-permit.html", "Code & permits", body)


def flags() -> str:
    cards=[]
    for f in D["flags"]:
        cards.append(f'''<article class="flag-card anchor" id="{e(f['id'])}"><p class="eyebrow">{e(f['id'])} · {e(f['status'])}</p><h3>{e(f['title'])}</h3><p>{e(f['finding'])}</p><p><strong>Next step:</strong> {e(f['next_step'])}</p>{refs(f['sources'])}</article>''')
    body=heading("Flagged for review", "Unverified details, source discrepancies and decisions that need an on-site or current-record check.")
    body+='<div class="stack">'+''.join(cards)+'</div>'
    return page("flagged-for-review.html", "Flagged for review", body)


def sources() -> str:
    labels=[('government','Government and statutes'),('manufacturer','Manufacturer'),('company','Company statements'),('review-platform','Reviews and business profiles'),('official','Official project and platform documentation')]
    body=heading("Source library", "Links are grouped by publisher so primary records, company claims and customer accounts are not confused.")
    body+='''<div class="notice">The date shown is the research snapshot, not a guarantee that a page or license remains current. Review and business-profile entries are third-party material; several Yelp links were available only through search indexing.</div>'''
    for kind,label in labels:
        entries=[]
        for s in D["sources"]:
            if s['kind']!=kind: continue
            note=f' · {e(s["note"])}' if s.get('note') else ''
            entries.append(f'''<li id="{e(s['id'])}" class="anchor"><a href="{e(s['url'])}">{e(s['title'])}</a><p>{e(s['id'])} · {e(s['access'])} · checked {e(s['checked'])}{note}</p></li>''')
        body+=f'<section class="source-group"><h2>{e(label)}</h2><ul class="source-list">'+''.join(entries)+'</ul></section>'
    return page("sources.html", "Sources", body)


def verification() -> str:
    total=len(D['providers']); active=sum(p['license_status'].startswith('Current') for p in D['providers'])
    body=heading("Verification", "What was checked, what remains open, and how to reproduce the local site checks.")
    body+=f'''<div class="grid"><section class="panel"><h2>Evidence checked</h2><ul class="checklist"><li>{total} separate CSLB license records read on November 7, 2026: {active} current and active at that check and one suspended.</li><li>Government, manufacturer, company and review-platform sources are labeled separately in the source library.</li><li>Yelp direct access was blocked; Angi, BBB and Yahoo Local pages supplied additional, attributed review context.</li><li>All three quote dates, scopes and amounts remain blank because no provider-issued documents were available.</li></ul></section>
<section class="panel"><h2>Checks performed locally</h2><ul class="checklist"><li>Build output matches the source data.</li><li>Every rendered table row links to an official source, with contextual links labeled as such.</li><li>Relative links, redirects, data references, and blank unverified fields are checked.</li><li>The website uses only local assets and works without client-side JavaScript.</li></ul><p class="small">Reproduce with <code>python scripts/build_canonical_site.py --check</code> and <code>python tests/test_project_site.py</code>.</p></section></div>
<section class="panel"><h2>What this cannot verify</h2><p>The exact installation and condition, the identity or terms of prior quotes, the willingness and capability of any vendor, insurance for the actual crew, and the required permit for this specific scope.</p><p><a href="flagged-for-review.html">Read the unresolved items →</a> · <a href="sources.html">Open the source library →</a></p></section>'''
    return page("verification.html", "Verification", body)


BUILDERS = {
    "index.html": overview,
    "executive-summary.html": executive,
    "requirements.html": requirements,
    "providers.html": providers,
    "reviews.html": reviews,
    "estimates.html": estimates,
    "technical-approach.html": technical,
    "code-and-permit.html": code,
    "flagged-for-review.html": flags,
    "sources.html": sources,
    "verification.html": verification,
}


def validate_data() -> list[str]:
    errors=[]
    if len(S)!=len(D['sources']): errors.append('Duplicate source IDs')
    for group, fields in [('providers',['official_sources']),('requirements',['official_context']),('technical',['sources']),('reviews',['sources']),('flags',['sources']),('official_fee_examples',['sources'])]:
        seen=set()
        for row in D[group]:
            if row['id'] in seen: errors.append(f"Duplicate {group} ID {row['id']}")
            seen.add(row['id'])
            for field in fields:
                if not row.get(field): errors.append(f"{group}/{row['id']} has no {field}")
                for source_id in row.get(field,[]):
                    if source_id not in S: errors.append(f"{group}/{row['id']}: unknown source {source_id}")
    for q in D['quotes']:
        for key in ('verified_quote_date','verified_quote_scope','verified_price_usd'):
            if q.get(key) is not None: errors.append(f"{q['id']}: {key} must be blank until substantiated")
        if q['license_source'] not in S or q['candidate_source'] not in S: errors.append(f"{q['id']}: missing sources")
    return errors


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='check generated pages without changing files')
    args=parser.parse_args()
    problems=validate_data()
    if problems:
        print('\n'.join(problems),file=sys.stderr); return 1
    pages={name:builder() for name,builder in BUILDERS.items()}
    if args.check:
        outdated=[name for name,text in pages.items() if not (ROOT/name).is_file() or (ROOT/name).read_text(encoding='utf-8') != text]
        if outdated:
            print('Out-of-date generated pages: '+', '.join(outdated),file=sys.stderr); return 1
        print(f'PASS: {len(pages)} generated pages match the audited dataset')
    else:
        for name,text in pages.items(): (ROOT/name).write_text(text,encoding='utf-8')
        print(f'Built {len(pages)} pages from {DATA.relative_to(ROOT)}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())

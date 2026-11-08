#!/usr/bin/env python3
"""Build the canonical bathtub overflow dashboard from reviewed scoped data.

Standard library only. Writes root HTML/CSS, executive-summary markdown and a
build report. Does not touch redirect stubs, archives or unrelated GEMS files.
"""
from __future__ import annotations
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'overflow-integration' / 'data'


def load(name: str):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


S = {s['id']: s for s in load('sources.json')['rows']}
P = load('providers.json')['rows']
R = load('requirements.json')['rows']
E = load('estimates.json')
T = load('technical.json')['rows']
C = load('compliance.json')['rows']
V = load('reviews.json')['rows']
F = load('flags.json')['rows']
AS_OF = load('providers.json')['as_of']

NAV = [
    ('index.html', 'Dashboard'),
    ('executive-summary.html', 'Executive summary'),
    ('requirements.html', 'Requirements'),
    ('providers.html', 'Providers'),
    ('estimates.html', 'Estimates'),
    ('technical-approach.html', 'Technical approach'),
    ('code-and-permit.html', 'Code & permit'),
    ('sources.html', 'Sources'),
    ('flagged-for-review.html', 'Flagged for review'),
    ('verification.html', 'Verification'),
]


def e(x) -> str:
    return html.escape(str(x if x is not None else ''), quote=True)


def blank() -> str:
    return '<span class="blank" aria-label="blank"></span> <span class="pill unv">unverified</span>'


def val(x) -> str:
    return e(x) if x not in (None, '', []) else blank()


def link(url: str, label: str | None = None) -> str:
    if not url:
        return blank()
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label or url)}</a>'


def src_links(ids, official_url: str | None = None) -> str:
    out = []
    seen = set()
    for i in ids or []:
        s = S.get(i)
        if not s:
            continue
        u = s['url']
        if u in seen:
            continue
        seen.add(u)
        label = s['title']
        if len(label) > 72:
            label = label[:69] + '…'
        out.append(link(u, label))
    if official_url and official_url not in seen:
        out.append(link(official_url, 'Official source'))
    return '<div class="sources">' + ' · '.join(out) + '</div>' if out else blank()


def pill(text: str, kind: str = 'neutral') -> str:
    return f'<span class="pill {kind}">{e(text)}</span>'


def table(caption: str, headers: list[str], rows: list[list[str]], id: str | None = None, row_tags: list[str] | None = None) -> str:
    h = ''.join(f'<th scope="col">{e(x)}</th>' for x in headers)
    trs = []
    for idx, row in enumerate(rows):
        cells = list(row)
        if row_tags and idx < len(row_tags) and row_tags[idx] and cells:
            cells[0] = f'<span data-tags="{e(row_tags[idx])}" hidden></span>' + cells[0]
        trs.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    body = ''.join(trs)
    tid = f' id="{e(id)}"' if id else ''
    return f'<div class="tablewrap"><table{tid}><caption>{e(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'


def filter_ui(table_id: str, chips: list[tuple[str, str]], placeholder: str) -> str:
    btns = ''.join(
        f'<button type="button" class="chip{" active" if idx == 0 else ""}" data-filter="{e(val_key)}">{e(label)}</button>'
        for idx, (val_key, label) in enumerate(chips)
    )
    return (
        f'<div class="filterbar" data-for="{e(table_id)}">'
        f'<input type="search" class="filter-search" placeholder="{e(placeholder)}" aria-label="{e(placeholder)}">'
        f'<div class="chips" role="group" aria-label="Filters">{btns}</div>'
        f'<span class="filter-count small" aria-live="polite"></span>'
        f'</div>'
    )


FILTER_SCRIPT = '''<script>
(function(){
  document.querySelectorAll('.filterbar').forEach(function(bar){
    var tbl=document.getElementById(bar.getAttribute('data-for'));
    if(!tbl||!tbl.tBodies.length)return;
    var rows=Array.prototype.slice.call(tbl.tBodies[0].rows);
    var search=bar.querySelector('.filter-search');
    var chips=bar.querySelectorAll('.chip');
    var count=bar.querySelector('.filter-count');
    var activeFilter='all';
    function apply(){
      var q=(search&&search.value?search.value:'').toLowerCase().trim();
      var shown=0;
      rows.forEach(function(r){
        var el=r.querySelector('[data-tags]');
        var tags=(el?el.getAttribute('data-tags'):'').split(',').filter(Boolean);
        var txt=r.textContent.toLowerCase();
        var matchChip=(activeFilter==='all')||tags.indexOf(activeFilter)!==-1;
        var matchSearch=!q||txt.indexOf(q)!==-1;
        var vis=matchChip&&matchSearch;
        r.style.display=vis?'':'none';
        if(vis)shown++;
      });
      if(count)count.textContent='Showing '+shown+' of '+rows.length+' rows';
    }
    chips.forEach(function(c){
      c.addEventListener('click',function(){
        chips.forEach(function(b){b.classList.remove('active');});
        c.classList.add('active');
        activeFilter=c.getAttribute('data-filter')||'all';
        apply();
      });
    });
    if(search)search.addEventListener('input',apply);
    apply();
  });
})();
</script>'''


def page(slug: str, title: str, subtitle: str, body: str, has_filters: bool = False) -> str:
    nav = ''.join(f'<a href="{e(u)}"{" class=active" if u == slug else ""}>{e(t)}</a>' for u, t in NAV)
    script = FILTER_SCRIPT if has_filters else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — Bathtub overflow trip lever</title><meta name="description" content="{e(subtitle)}">
<link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="wrap topbar-inner"><a class="brand" href="index.html">Trip Lever Project</a><nav class="nav" aria-label="Primary">{nav}</nav></div></header>
<main id="main" class="wrap"><section class="hero"><p class="eyebrow">San Francisco · tenant-occupied unit · reviewed {e(AS_OF)}</p><h1>{e(title)}</h1><p class="lede">{e(subtitle)}</p></section>
{body}
<footer class="footer"><p>Canonical repair dashboard. Parallel drafts are preserved as redirect stubs/archives; unrelated DOE GEMS research archive remains at <a href="docs/executive-summary.html">docs/executive-summary.html</a>. Source links open in a new tab. Unconfirmed values are blank and flagged.</p><p><a href="https://github.com/karagemop466-tech/Korea8/blob/main/COORDINATION.md">Coordination log</a> · <a href="https://github.com/karagemop466-tech/Korea8">Repository</a></p></footer></main>{script}</body></html>'''


def money(x) -> str:
    return f'${x:,.0f}' if isinstance(x, (int, float)) else blank()


def badge_list(p: dict) -> str:
    bits = []
    if p.get('rank'):
        bits.append(pill(f"Rank #{p['rank']}", 'info'))
    wc = p.get('workers_comp', '')
    if 'Policy recorded' in wc:
        bits.append(pill('WC insured', 'ok'))
    elif 'Exempt' in wc:
        bits.append(pill('WC exempt', 'warn'))
    bbb = p.get('bbb_status', '')
    if 'BBB A+' in bbb:
        bits.append(pill('BBB A+', 'ok'))
    elif 'BBB A ' in bbb or bbb.startswith('BBB A'):
        bits.append(pill('BBB A', 'ok'))
    elif 'BBB B-' in bbb:
        bits.append(pill('BBB B-', 'bad'))
    if p.get('diamond_certified'):
        bits.append(pill('Diamond Certified', 'ok'))
    return ''.join(bits)


active = [p for p in P if p['status'] == 'Current and active']
susp = [p for p in P if p['status'] == 'Suspended']
unresolved = [p for p in P if not p['license']]
cslb_checked = [p for p in P if p['license']]
bc = [p for p in active if 'B' in p['classifications'] and 'C-36' in p['classifications']]
c9 = [p for p in active if 'C-9' in p['classifications']]

group_order = {
    'Combined-scope lead': 0,
    'Priority specialty lead': 1,
    'Conditional combined-scope lead': 2,
    'Restoration partner': 3,
    'Existing estimate': 4,
    'Technical case-study lead': 5,
    'Additional registry candidate': 6,
    'Conditional registry candidate': 7,
    'High-risk caution — active citation': 8,
    'Not eligible — suspended': 9,
    'Identity unresolved': 10,
}
Ps = sorted(
    P,
    key=lambda p: (
        0 if p.get('rank') is not None else 1,
        p.get('rank') if p.get('rank') is not None else 999,
        group_order.get(p['group'], 99),
        p['name'],
    ),
)
ranked_short = sorted([p for p in P if p.get('rank') is not None], key=lambda p: p['rank'])


def shortlist_rows() -> list[list[str]]:
    rows = []
    for p in ranked_short:
        cls = ', '.join(p['classifications']) if p['classifications'] else ''
        contact = f"<span class='mono'>{e(p['phone'])}</span><br><span class='small'>{e(p['registered_city'])} · CSLB #{e(p['license'])} ({e(cls)})</span>"
        trust = badge_list(p) + (f"<br><span class='small'>{e(p['bbb_status'])}</span>" if p.get('bbb_status') else '') + (f"<br><span class='small'>{e(p['diamond_certified'])}</span>" if p.get('diamond_certified') else '')
        links_cell = src_links(p['source_ids'], p['official_url'])
        if p.get('website'):
            links_cell += link(p['website'], 'Official website') + ' · '
        if p.get('review_url'):
            links_cell += link(p['review_url'], 'Review page')
        rows.append([
            f"<strong>#{e(p['rank'])} {e(p['name'])}</strong><br><span class='small'>{e(p['rank_tier'])}</span>",
            contact,
            trust,
            e(p['ranking_reason']),
            e(p['cost_driver']),
            links_cell,
        ])
    return rows


# 1. Dashboard (index.html)
kpis = [
    (str(len(cslb_checked)), 'CSLB license records rechecked', f'{len(active)} active · {len(susp)} suspended · {len(unresolved)} identities unresolved ({AS_OF})'),
    (str(len(bc)), 'Active B + C-36 candidates', 'Combined classification only; restoration party must be named in writing'),
    (str(len(c9)), 'Active C-9 restoration partner', 'Bernal Hill Drywall (#995163); pairs with C-36 specialists when ceiling opens'),
    (str(len(R)), 'Requirements captured', f'{len(S)} verified source records · {len(F)} flagged items published'),
]
kpi_html = '<div class="grid kpis">' + ''.join(f'<div class="kpi"><span class="n">{e(n)}</span><span class="l">{e(l)}</span><span class="s">{e(s)}</span></div>' for n, l, s in kpis) + '</div>'

cards = [
    ('executive-summary.html', 'Executive summary', 'Decision path, ranked shortlist reasoning, pricing analysis and pre-contract controls.'),
    ('providers.html', 'Providers & Ranking', f'{len(P)} identities: ranked #1–#11 shortlist, phone numbers, BBB/WC checks, cautions & filtering.'),
    ('estimates.html', 'Estimates & Cost Drivers', 'Owner-reported $614/$550/$135 quotes, 6 cost drivers and SF DBI Table 1A-C fees.'),
    ('requirements.html', 'Requirements', f'{len(R)} source-linked requirements with acceptance checks, origin labels and search filters.'),
    ('technical-approach.html', 'Technical approach', 'Tub-side service path first, below-ceiling storage fallback and Watco testing.'),
    ('code-and-permit.html', 'Code & permit', 'PermitSF portal (Sept 2026), 2025 SF Codes, §104.2 exemptions and Civil Code §1954.'),
    ('sources.html', 'Sources', f'{len(S)} source records directly rechecked {AS_OF} with retrieval status and limitations.'),
    ('flagged-for-review.html', 'Flagged for review', f'{len(F)} irregularities, citations (BPC §7114.A), BBB B- alerts and open items.'),
    ('verification.html', 'Verification', 'Automated checks, independent audit parity and publication record.'),
]
card_html = '<div class="grid cards">' + ''.join(f'<a class="card" href="{e(u)}"><h3>{e(t)}</h3><p>{e(d)}</p></a>' for u, t, d in cards) + '</div>'

snapshot = [
    ['CSLB & credential sweep', f'{len(cslb_checked)} licenses checked ({AS_OF})', f'{len(active)} active; #1027286 Kenneth Asire still bond-suspended; #297604 D G holds BPC §7114.A citation; Portola & LFM unresolved.', src_links(['CSLB-1027286', 'DG-CITATION', 'CSLB-SEARCH'])],
    ['Top ranked combined leads', '#1 Ace · #2 Rapid Flow', 'Ace (#829071) leads on B+C-36 + WC + 22-yr BBB A+ + Diamond Certified + HOA/PM fit; Rapid Flow (#1115649) is #2 B+C-36 with recent SF permit (check GL/WC).', src_links(['CSLB-829071', 'BBB-ACE', 'DC-ACE', 'CSLB-1115649', 'BZ-RAPIDFLOW'])],
    ['Top C-36 + C-9 pair', '#3 Atlas + #6 Bernal Hill', 'Atlas (#868994, BBB A+ & Diamond Certified, bathtub drain-lever evidence) + Bernal Hill (#995163, B+C-9 pipe tear-out patching) cover two-trade fallback.', src_links(['CSLB-868994', 'BBB-ATLAS', 'DC-ATLAS', 'CSLB-995163', 'BERNAL'])],
    ['Heise’s status update', 'Demoted to #10 backup', 'Direct BBB profile shows B- rating (1 unanswered complaint in 12 mos) & expired #787733; no B/C-9; Ingleside case URL still embeds 404 block.', src_links(['BBB-HEISE', 'CSLB-787733', 'CSLB-1089561', 'HEISE-INGLESIDE'])],
    ['Owner estimates & spread', '$614 / $550 / $135 owner-reported (2026-08-30)', 'Owner-reported only (verified blank). Scopes differ ($135 owner-reported handle adjustment vs $614 owner-reported assembly); none explicitly prices ceiling drywall restoration.', src_links(['OWNER', 'CSLB-977638', 'CSLB-757796', 'CSLB-1024971'])],
    ['Permit & code regime', '2025 SF Codes · PermitSF', 'SF Plumbing Code §104.2 exemptions do not cover cutting/removing piping; OTC permits moved to PermitSF Sept 2026; Category 1P is $290 if required.', src_links(['SF-PERMIT', 'SF-CODE-104', 'SF-CODES-2025', 'SF-FEES'])],
]

top5_rows = shortlist_rows()[:6]
body = (
    kpi_html
    + '<div class="panel"><h3>Recommended action sequence</h3><ol class="tight">'
    + '<li><strong>Call #1 Ace Plumbing &amp; Rooter ((415) 824-6444)</strong> and <strong>#2 Rapid Flow ((415) 866-8401)</strong> first for unified <code>B + C-36</code> bids (confirming named drywall finish scope, GL/WC coverage, and tub-side attempt before ceiling opening).</li>'
    + '<li><strong>Call #3 Atlas Plumbing &amp; Rooter ((415) 849-2346)</strong> for specialist C-36 tub-lever extraction — and if below-ceiling access is needed, pair with <strong>#6 Bernal Hill Drywall ((415) 533-8274)</strong> for <code>C-9 + B</code> ceiling/access-panel restoration.</li>'
    + '<li><strong>Re-scope existing quotes (#7 Expert, #8 Fast Response, #9 Bay Area/Save-On)</strong> on one identical checklist rather than comparing owner-reported $135 vs $550 vs $614 across mismatched scopes.</li>'
    + '<li><strong>Exclude or hold</strong> #1027286 Kenneth Asire (suspended), #297604 D G Construction (BPC §7114.A citation), #1009195 Advanced (tax/liability suspension warning), and unresolved names (Portola, LFM).</li>'
    + '</ol></div>'
    + '<h2>Decision-making shortlist (Top 6 of 11 ranked leads)</h2>'
    + table('Ranked by license scope, active insurance, BBB/Diamond Certified standing, SF permit/repair evidence, and occupied-unit readiness (full 28-identity matrix on Providers).', ['Rank & Provider', 'Phone / City / License', 'Verified Credentials', 'Ranking Reasoning', 'Pricing & Cost Drivers', 'Verified Links'], top5_rows)
    + '<p><a href="providers.html">View all 11 ranked leads and full 28-provider register →</a> · <a href="estimates.html">See full pricing analysis &amp; 6 cost drivers →</a></p>'
    + '<h2>Browse the dossier</h2>'
    + card_html
    + '<h2>Verification status snapshot (' + e(AS_OF) + ')</h2>'
    + table('Each row links the source it rests on; unconfirmed values remain blank.', ['Item', 'Value', 'What it means', 'Sources'], snapshot)
)
(ROOT / 'index.html').write_text(page('index.html', 'Bathtub wastewater overflow trip lever', 'A source-checked repair decision dashboard: ranked contractor shortlist, pricing & cost-driver analysis, verified licenses/BBB/reviews, and strict separation of unconfirmed facts.', body), encoding='utf-8')

# 2. Executive summary (Markdown + HTML)
ranked_md_lines = []
for p in ranked_short:
    cls = ', '.join(p['classifications'])
    cred = '; '.join([x for x in [p.get('workers_comp', ''), p.get('bbb_status', ''), p.get('diamond_certified', '')] if x])
    ranked_md_lines.append(
        f"- **#{p['rank']} {p['name']} (`#{p['license']}`, {cls}) — Phone: `{p['phone']}`**\n"
        f"  - *Credentials:* {cred}\n"
        f"  - *Why ranked #{p['rank']}:* {p['ranking_reason']}\n"
        f"  - *Cost drivers:* {p['cost_driver']}"
    )

cost_driver_md = '\n'.join(f"- **{cd['driver']} ({cd['impact']}):** {cd['detail']}" for cd in E['cost_drivers'])

summary_md = f'''# Executive summary — bathtub wastewater overflow trip lever

Reviewed {AS_OF}. San Francisco tenant-occupied unit. This summary is based on directly retrieved
CSLB, SF DBI, California legislative, manufacturer, BBB and company records plus a neutral owner
record; it is not a contractor booking or legal advice.

## Decision
Use a two-path scope:
1. First, ask a licensed `C-36` plumber to identify the waste-and-overflow brand/model and attempt the
   least-destructive tub-side adjustment or extraction through the overflow faceplate.
2. Only if the tub-side route fails or risks hidden piping, execute a below-ceiling fallback through
   the storage unit under a written contract that explicitly names both the licensed plumbing (`C-36`)
   and drywall/restoration (`B` or `C-9`) parties, storage-unit access consent, and DBI permit steps.

Do not assume a permit exemption: SF.gov requires a permit before cutting into or replacing piping,
SF Plumbing Code §104.2 exemptions are conditional, OTC permits moved to PermitSF in Sept 2026, and
2025 California/SF codes apply with no grace period.

## Ranked contractor shortlist & reasoning (inquiry order, not confirmed bookings)
{chr(10).join(ranked_md_lines)}

### Exclusions & high-risk cautions (do not prioritize)
- **Kenneth Asire Plumbing (`#1027286`) — EXCLUDE (Suspended):** CSLB Contractors Bond Suspension confirmed still active on {AS_OF}.
- **D G Construction Co (`#297604`, `(415) 308-0803`) — HIGH-RISK CAUTION:** Active `B + C-36`, but WC-exempt and CSLB Citation Violation Disclosure shows **Citation `#2 2022 2099` (`03/23/2023`) for `BPC §7114.A` ("Aided and abetted non-licensee")**.
- **Advanced Plumbing & Drain (`#1009195`) — HOLD:** Active `C-36`, WC-exempt, carries unresolved FTB/DIR/EDD/CSLB final-liability future-suspension warning.
- **Portola Plumbing Services & LFM Construction and Plumbing (`(650) 501-8609` Yelp lead) — UNVERIFIED:** No CSLB license verified (`#1029661` ruled out as unrelated Truckee M Renovations LLC); do not solicit until CSLB license is verified.

## Pricing analysis & cost drivers
Owner-supplied amounts dated 2026-08-30: **Expert $614** (replace waste and overflow), **Bay Area $550**
(lever/plug/spout with diverter, labor/materials), **Fast Response $135** (repair/adjust plunger handle).
These are owner reports, not independently verified prices; verified amounts remain blank. The scopes
differ fundamentally—$135 reflects a surface plunger-handle adjustment rather than concealed pipe replacement
or ceiling restoration—so the $479 arithmetic spread is not a like-for-like market range.

Key cost drivers that determine total project outlay:
{cost_driver_md}

## Required pre-signing controls
- Verify exact legal entity, CSLB license status/classifications, bond and WC/GL certificates on signing day.
- Put drywall/texture/paint or framed access-panel scope in writing (`B + C-36` is not automatic proof of in-house drywall finishing).
- Get DBI's written permit determination and schedule inspection before covering concealed pipes (`Category 1P` $290 / `11P/M` $320 if applicable).
- Deliver written Civil Code §1954 tenant notice (24h presumed reasonable), confirm storage-unit entry authority, and agree water shut-off/dust protection.
- Screen conditionally for pre-1978 paint (EPA RRP) and suspect asbestos before cutting finishes.
- Execute a written itemized contract (>$500 statutory rule), lawful down payment (lesser of 10% or $1,000), written change orders, fill/leak test and photo log.
'''
(ROOT / 'overflow-integration' / 'EXECUTIVE_SUMMARY.md').write_text(summary_md, encoding='utf-8')
(ROOT / 'OVERFLOW_EXECUTIVE_SUMMARY.md').write_text(summary_md, encoding='utf-8')

exec_rows = [
    ['Decision', 'Two-path scope: tub-side overflow service first; below-ceiling storage fallback only with named plumbing + C-9/B restoration trades and written permit answer.', src_links(['OWNER', 'WATCO', 'SF-PERMIT', 'CSLB-C9'])],
    ['Top Combined Leads', '#1 Ace (#829071, (415) 824-6444: B+C-36, WC, BBB A+, Diamond Certified, HOA/PM fit) and #2 Rapid Flow (#1115649, (415) 866-8401: B+C-36, 2026 SF permit, check GL/drywall).', src_links(['CSLB-829071', 'BBB-ACE', 'DC-ACE', 'CSLB-1115649', 'BZ-RAPIDFLOW'])],
    ['Top Two-Trade Pair', '#3 Atlas (#868994, (415) 849-2346: BBB A+, Diamond Certified, WC, bathtub drain-lever review) + #6 Bernal Hill Drywall (#995163, (415) 533-8274: B+C-9 leaky-pipe ceiling patching).', src_links(['CSLB-868994', 'BBB-ATLAS', 'DC-ATLAS', 'YELP-ATLAS', 'CSLB-995163', 'BERNAL'])],
    ['Demoted & Excluded', '#10 Heise’s demoted on direct BBB B- (1 unanswered complaint) & expired #787733; #1027286 Asire excluded (Suspended); #297604 D G flagged (BPC §7114.A citation); Portola & LFM unresolved.', src_links(['BBB-HEISE', 'CSLB-1027286', 'DG-CITATION', 'CSLB-SEARCH'])],
    ['Estimates & Drivers', 'Owner-reported $614 / $550 / $135 (verified blank); unlike scopes ($135 owner-reported adjustment vs $614 owner-reported replacement); DBI 1P $290 + drywall/access/travel drivers govern actual total.', src_links(['OWNER', 'SF-FEES', 'CSLB-977638', 'CSLB-757796', 'CSLB-1024971'])],
    ['Permit & Tenant Controls', 'PermitSF OTC portal (Sept 2026), 2025 SF Codes, §104.2 limits, Civil Code §1954 24h notice, EPA RRP/asbestos screening and >$500 contract rules.', src_links(['SF-DBI', 'SF-CODES-2025', 'SF-CODE-104', 'CIV-1954', 'EPA-RRP', 'CSLB-CONTRACT'])],
]
body = (
    '<div class="panel"><h3>Bottom line (' + e(AS_OF) + ' verification)</h3>'
    + '<p><strong>Best combined-license call first:</strong> <strong>#1 Ace Plumbing &amp; Rooter</strong> (<code>#829071</code>, <code>(415) 824-6444</code>) holds B + C-36, active WC, 22-year BBB A+, Diamond Certified since 2007, and HOA/property-manager alignment. Follow with <strong>#2 Rapid Flow</strong> (<code>#1115649</code>, <code>(415) 866-8401</code>). '
    + '<strong>Best C-36 specialist + restoration pair:</strong> <strong>#3 Atlas Plumbing &amp; Rooter</strong> (<code>#868994</code>, <code>(415) 849-2346</code>; BBB A+ &amp; Diamond Certified) paired with <strong>#6 Bernal Hill Drywall</strong> (<code>#995163</code>, <code>(415) 533-8274</code>). '
    + '<strong>Key risk changes:</strong> Heise’s (<code>#1089561</code>) drops to #10 after a direct BBB <strong>B-</strong> rating check; D G Construction (<code>#297604</code>) carries an active <strong>BPC §7114.A</strong> aiding-an-unlicensed-person citation.</p></div>'
    + table('Executive findings', ['Topic', 'Finding', 'Sources'], exec_rows)
    + '<h2>Ranked shortlist &amp; reasoning</h2>'
    + table('Ordered inquiry plan based on 2026-11-08 re-verified CSLB, BBB, Diamond Certified, BuildZoom, and official website records.', ['Rank & Provider', 'Phone / City / License', 'Verified Credentials', 'Ranking Reasoning', 'Pricing & Cost Drivers', 'Verified Links'], shortlist_rows())
    + '<h2>Owner-supplied estimates vs cost drivers</h2>'
    + table('Owner-reported amounts are not verified prices.', ['Provider', 'Supplied scope', 'Supplied amount', 'Verified amount', 'Sources'], [[e(x['provider']), e(x['scope_owner']), money(x['amount_owner']), blank(), src_links(x['source_ids'])] for x in E['rows']])
    + table('Six factors driving actual total project cost', ['Cost driver', 'Budget impact', 'How it applies here', 'Sources'], [[e(cd['driver']), e(cd['impact']), e(cd['detail']), src_links(cd['source_ids'], cd['official_url'])] for cd in E['cost_drivers']])
    + '<h2>Next steps</h2><ol class="tight">'
    + '<li>Send one identical neutral scope to #1 Ace, #2 Rapid Flow, #3 Atlas (+ #6 Bernal Hill if below-ceiling), and requote #7 Expert on the exact same checklist.</li>'
    + '<li>Confirm storage-unit ownership/entry authority and serve written Civil Code §1954 tenant notice before scheduling.</li>'
    + '<li>Collect photos/brand/drain dimensions, screen pre-1978 paint/asbestos, and get DBI’s written permit answer before cutting finishes.</li>'
    + '<li>Sign an itemized contract (&gt;$500 rule) capping down payment at 10% or $1,000, requiring fill/leak testing and rough inspection before ceiling closure.</li>'
    + '</ol><p><a href="OVERFLOW_EXECUTIVE_SUMMARY.md">Markdown executive summary</a></p>'
)
(ROOT / 'executive-summary.html').write_text(page('executive-summary.html', 'Executive summary', 'Decision path, ranked shortlist reasoning, estimate comparison, cost drivers and pre-contract controls.', body), encoding='utf-8')

# 3. Requirements
r_rows = []
r_attrs = []
cat_map = {
    'Problem & outcome': 'problem',
    'Access': 'access',
    'Scope & restoration': 'scope',
    'Provider & licensing': 'provider',
    'Permit & code': 'permit',
    'Tenant & occupancy': 'tenant',
    'Commercial & evidence': 'commercial',
    'Publication & audit': 'commercial',
}
for r in R:
    tags = [cat_map.get(r['category'], 'other')]
    if r['origin'] == 'Official rule':
        tags.append('official')
    else:
        tags.append('open')
    r_attrs.append(','.join(tags))
    r_rows.append([
        e(r['id']),
        e(r['category']),
        e(r['requirement']),
        f"<strong>Basis:</strong> {e(r['basis'])}<br><strong>Acceptance:</strong> {e(r['acceptance_check'])}<br><span class='small'>Legacy mapping: {e(r['legacy_ids'])}</span>",
        pill(r['origin'], 'ok' if r['origin'] == 'Official rule' else 'warn') + f"<br><span class='small'>{e(r['status'])}</span>",
        src_links(r['source_ids'], r['official_url']),
    ])
r_filter = filter_ui(
    'requirements-table',
    [('all', 'All (42)'), ('official', 'Official rules'), ('provider', 'Licensing & Providers'), ('permit', 'Permit & Code'), ('access', 'Access'), ('scope', 'Scope & Restoration'), ('tenant', 'Tenant & Safety'), ('commercial', 'Commercial & Bids')],
    'Filter requirements by keyword, code section, or ID…',
)
body = f'<p>{len(R)} requirements deduplicated from the parallel registers and updated {e(AS_OF)}. Owner requirements and proposed controls are not presented as official rules; official context links are provided for review.</p>' + r_filter + table('Full requirement register', ['ID', 'Category', 'Requirement', 'Basis / acceptance check', 'Origin / status', 'Sources'], r_rows, 'requirements-table', r_attrs)
(ROOT / 'requirements.html').write_text(page('requirements.html', 'Requirements', 'Full source-linked register with acceptance checks, origin labels, legacy mappings and interactive category filters.', body, has_filters=True), encoding='utf-8')

# 4. Providers (Ranked Shortlist Table #1 + Full 28-Provider Filterable Register Table #2 + Reviews Table #3)
prows = []
pattrs = []
for p in Ps:
    lic = f"<span class='mono'>{e(p['license'])}</span>" if p['license'] else blank()
    status = pill(p['status'], 'ok' if p['status'] == 'Current and active' else 'bad' if p['status'] == 'Suspended' else 'unv')
    cls_str = ', '.join(p['classifications']) if p['classifications'] else blank()
    extra = f"<br><span class='pill warn'>CSLB note</span> <span class='small'>{e(p['additional_status'])}</span>" if p.get('additional_status') and p['additional_status'] != 'None on CSLB LicenseDetail' else ''
    cred_bits = badge_list(p)
    bbb_line = f"<br><span class='small'><strong>BBB:</strong> {e(p['bbb_status'])}</span>" if p.get('bbb_status') else ''
    dc_line = f"<br><span class='small'><strong>Certification:</strong> {e(p['diamond_certified'])}</span>" if p.get('diamond_certified') else ''
    fit_cell = (
        f"<strong>{e(p.get('rank_tier') or p['group'])}.</strong> {e(p['ranking_reason'])}"
        + f"<br><span class='small'><strong>Cost drivers:</strong> {e(p['cost_driver'])}</span>"
        + extra
        + bbb_line
        + dc_line
    )
    if p['service_claim']:
        fit_cell += f"<br><span class='small'>Service profile: {e(p['service_claim'])}</span>"
    contact = (e(p['registered_city']) + '<br><span class="mono">' + e(p['phone']) + '</span>') if p['registered_city'] else blank()
    wc_cell = (e(p['workers_comp']) if p['workers_comp'] else blank()) + ('<br>' + cred_bits if cred_bits else '')
    links_cell = src_links(p['source_ids'], p['official_url'])
    extra_links = []
    if p.get('website'):
        extra_links.append(link(p['website'], 'Company site'))
    if p.get('review_url'):
        extra_links.append(link(p['review_url'], 'Review page'))
    if extra_links:
        links_cell += '<div class="small">' + ' · '.join(extra_links) + '</div>'

    ptags = []
    if p.get('rank') is not None:
        ptags.append('ranked')
    if 'B' in p['classifications'] and 'C-36' in p['classifications'] and p['status'] == 'Current and active':
        ptags.append('bc36')
    if 'C-36' in p['classifications'] and p['status'] == 'Current and active':
        ptags.append('c36')
    if 'C-9' in p['classifications'] and p['status'] == 'Current and active':
        ptags.append('c9')
    if 'Policy recorded' in p.get('workers_comp', ''):
        ptags.append('wc')
    if 'BBB A' in p.get('bbb_status', '') or p.get('diamond_certified'):
        ptags.append('trusted')
    if p['status'] == 'Suspended' or not p['license'] or 'citation' in p['group'].lower() or 'warning' in (p.get('additional_status') or '').lower() or 'BBB B-' in p.get('bbb_status', '') or 'Exempt' in p.get('workers_comp', '') or p['classifications'] in (['B'], ['B-2']):
        ptags.append('caution')
    pattrs.append(','.join(ptags))

    prows.append([
        f"<strong>{e(p['name'])}</strong><br><span class='small'>{e(p['legal_name'])}</span>",
        lic + '<br>' + status + (f"<br><span class='small'>expires {e(p['expiry'])}</span>" if p['expiry'] else ''),
        e(cls_str) if p['classifications'] else cls_str,
        contact,
        wc_cell,
        fit_cell,
        links_cell,
    ])

vrows = [
    [
        e(v['provider']),
        e(v['platform']),
        e(v['observation']),
        blank(),
        blank(),
        pill('BBB direct / Yelp unverified' if 'direct' in v['platform'] else 'Unverified numeric lead', 'warn'),
        e(v['limit']),
        src_links(v['source_ids'], v['official_url']) + '<br>' + link(v['review_url'], 'Review lead'),
    ]
    for v in V
]

p_filter = filter_ui(
    'providers-table',
    [
        ('all', f'All ({len(P)})'),
        ('ranked', f'Ranked Shortlist ({len(ranked_short)})'),
        ('bc36', f'Active B + C-36 ({len(bc)})'),
        ('c36', 'Active C-36'),
        ('c9', 'C-9 Restoration'),
        ('wc', 'Active Workers’ Comp'),
        ('trusted', 'BBB A/A+ or Diamond'),
        ('caution', 'Cautions / Excluded / Pending'),
    ],
    'Search contractor name, CSLB #, phone, city, BBB, or keyword…',
)

body = (
    '<h2>Ranked contractor decision shortlist (#1–#11)</h2>'
    + '<p>Ordered by license completeness, active workers’ compensation, direct BBB and Diamond Certified standing, SF permit/bathtub repair evidence, and occupied-unit coordination. Excluded: Kenneth Asire (#1027286, bond suspended), D G Construction (#297604, active BPC §7114.A citation), Advanced (#1009195, tax/liability suspension warning), and unresolved identities.</p>'
    + table('Decision-making inquiry order with reasoning, phone numbers, verified links and pricing drivers (not a booking or performance guarantee).', ['Rank & Provider', 'Phone / City / License', 'Verified Credentials', 'Ranking Reasoning', 'Pricing & Cost Drivers', 'Verified Links'], shortlist_rows())
    + f'<h2>Full provider register ({len(P)} identities)</h2>'
    + '<p>Every CSLB field was directly rechecked on <code>2026-11-08</code>. Exact-job acceptance, ceiling restoration price and schedule remain unconfirmed until written quotes are returned.</p>'
    + p_filter
    + table(f'{len(P)} identities: {len(cslb_checked)} CSLB records rechecked 2026-11-08 and {len(unresolved)} unresolved names.', ['Provider / legal name', 'License / status', 'Classifications', 'City / phone', 'Workers-comp & badges', 'Ranking reasoning, cost drivers & fit', 'Sources & links'], prows, 'providers-table', pattrs)
    + '<h2>Review &amp; credential observations</h2>'
    + '<p>BBB accreditation/ratings for Ace (A+), Atlas (A+), We Do (A+), Bernal Hill (0 complaints) and Heise’s (B-) were directly fetched on <code>2026-11-08</code>. Numeric Yelp star ratings and review counts remain blank because Yelp business pages return HTTP 403 to automated retrieval.</p>'
    + table('Credential checks and unverified Yelp search-index leads', ['Provider', 'Platform', 'Observation', 'Rating', 'Count', 'Status', 'Limits', 'Sources'], vrows)
)
(ROOT / 'providers.html').write_text(page('providers.html', 'Providers & contractor ranking', 'Ranked shortlist with reasoning, phone numbers, verified CSLB/BBB/review links, cost drivers and interactive filtering.', body, has_filters=True), encoding='utf-8')

# 5. Estimates
erows = [
    [
        e(x['provider']) + f"<br><span class='mono small'>CSLB #{e(x['license'])}</span>",
        e(x['scope_owner']),
        e(x['date']),
        money(x['amount_owner']),
        blank(),
        e(x['analysis']),
        pill(x['status'], 'warn'),
        src_links(x['source_ids'], x['official_url']),
    ]
    for x in E['rows']
]
cdrows = [
    [
        e(cd['driver']),
        e(cd['impact']),
        e(cd['detail']),
        src_links(cd['source_ids'], cd['official_url']),
    ]
    for cd in E['cost_drivers']
]
frows = [
    [e(f['item']), money(f['amount']), e(f['unit']), e(f['note']), src_links(f['source_ids'], f['official_url'])]
    for f in E['official_fees']
]
body = (
    '<div class="panel"><h3>How to read the supplied numbers</h3><p>The three owner-reported amounts ($614, $550, $135, dated 2026-08-30) are unverified owner statements, not independently verified quotes. Verified amounts remain blank. Crucially, the three scopes differ ($135 owner-reported handle adjustment vs $614 owner-reported full waste-and-overflow assembly), and none explicitly includes storage-ceiling drywall restoration or DBI permit fees.</p></div>'
    + table('Owner-supplied estimates dated 2026-08-30', ['Provider', 'Supplied scope', 'Supplied date', 'Supplied amount', 'Verified amount', 'Scope-gap analysis', 'Status', 'Sources'], erows, 'estimates-table')
    + '<h2>Pricing analysis &amp; six cost drivers</h2>'
    + table('What drives final total project cost for an SF occupied-unit waste-and-overflow repair', ['Cost driver', 'Budget impact', 'Mechanism & what to verify in bids', 'Sources'], cdrows)
    + '<h2>Official SF DBI fees (not contractor quotes)</h2>'
    + table('July 2026 Table 1A-C (effective 2026-07-12); category applicability unconfirmed.', ['Item', 'Amount', 'Unit', 'Note', 'Source'], frows)
    + '<h2>Key commercial takeaways</h2><ul class="tight">' + ''.join(f'<li>{e(a)}</li>' for a in E['analysis']) + '</ul>'
)
(ROOT / 'estimates.html').write_text(page('estimates.html', 'Estimates & cost drivers', 'Owner-reported amounts, blank verified amounts, six project cost drivers and official SF DBI permit/inspection fees.', body), encoding='utf-8')

# 6. Technical
trows = [[e(t['id']), e(t['topic']), e(t['statement']), pill(t['status'], 'warn'), e(t['limit']), src_links(t['source_ids'], t['official_url'])] for t in T]
body = '<div class="panel"><h3>Access decision</h3><ol class="tight"><li>Identify the assembly brand/model and attempt the least-destructive tub-side path through the overflow faceplate if safe.</li><li>If it cannot be freed without risking concealed piping, use below-ceiling access through the storage unit only with a written opening/restoration plan and named licensed trades.</li><li>Fill/leak-test and complete DBI inspection before closing the cavity; evaluate a serviceable access panel without asserting unverified code dimensions.</li></ol></div>' + table('Technical findings and limits', ['ID', 'Topic', 'Finding', 'Status', 'Limit', 'Sources'], trows)
(ROOT / 'technical-approach.html').write_text(page('technical-approach.html', 'Technical approach', 'Manufacturer-based service path, adjacent ceiling-access case evidence and restoration limits.', body), encoding='utf-8')

# 7. Compliance
crows = [[e(c['id']), e(c['topic']), e(c['rule']), e(c['application']), src_links(c['source_ids'], c['official_url'])] for c in C]
body = '<p>Official rules were directly re-reviewed ' + e(AS_OF) + ' against primary SF.gov, American Legal Publishing, California Legislative Information, CSLB and EPA pages; job-specific applicability still requires contractor/DBI confirmation.</p>' + table('Code, permit, licensing, tenant and contract rules', ['ID', 'Topic', 'Official rule / guidance', 'Application to this job', 'Sources'], crows)
(ROOT / 'code-and-permit.html').write_text(page('code-and-permit.html', 'Code & permit', 'PermitSF workflow, 2025 SF Codes, conditional §104.2 exemptions, B/B-2/C-9/C-36 licensing, tenant entry and contract rules.', body), encoding='utf-8')

# 8. Sources (all 100 sources + filter bar + official cross-ref)
cross = {
    'OWNER': 'CSLB-CONTRACT', 'REPO': 'GH-ACTIONS', 'REPO-OLD-INDEX': 'REPO', 'REPO-OLD-EXEC': 'REPO',
    'REPO-PR33': 'REPO', 'REPO-BOARD': 'REPO', 'PAGES-API': 'GH-ACTIONS',
    'YELP-RF': 'CSLB-1115649', 'YELP-RF2': 'CSLB-1115649', 'YELP-ACE': 'CSLB-829071',
    'YELP-WEDO': 'CSLB-1096552', 'YELP-HEISE': 'CSLB-1089561', 'YELP-PORTOLA': 'CSLB-SEARCH',
    'YELP-ATLAS': 'CSLB-868994', 'YELP-BERNAL': 'CSLB-995163', 'YELP-EXPERT': 'CSLB-977638',
    'YELP-BAYAREA': 'CSLB-757796', 'YELP-FASTRESP': 'CSLB-1024971', 'YELP-PLUMBING1': 'CSLB-1034873',
    'YELP-DISCOVER': 'CSLB-1041846', 'YELP-LFM': 'CSLB-SEARCH',
    'BBB-ACE': 'CSLB-829071', 'BBB-ATLAS': 'CSLB-868994', 'BBB-WEDO': 'CSLB-1096552',
    'BBB-HEISE': 'CSLB-1089561', 'BBB-BERNAL': 'CSLB-995163', 'BBB-DISCOVER': 'CSLB-1041846',
    'BBB-PLUMBING1': 'CSLB-1034873', 'DC-ACE': 'CSLB-829071', 'DC-ATLAS': 'CSLB-868994',
    'DC-DISCOVER': 'CSLB-1041846', 'BZ-RAPIDFLOW': 'CSLB-1115649',
    'IAPMO': 'SF-CODE-104', 'WATCO': 'SF-CODE-104',
    'RF': 'CSLB-1115649', 'ACE': 'CSLB-829071', 'HEISE': 'CSLB-1089561',
    'HEISE-INGLESIDE': 'CSLB-1089561', 'HEISE-MISSION': 'CSLB-1089561',
    'HEISE-MARINA': 'CSLB-1089561', 'HEISE-MAINT': 'CSLB-1089561',
    'EXPERT': 'CSLB-977638', 'BAY': 'CSLB-757796', 'FAST': 'CSLB-1024971',
    'WEDO': 'CSLB-1096552', 'AYOOB': 'CSLB-392967', 'BERNAL': 'CSLB-995163',
    'SFBG': 'CSLB-1106131', 'ATLAS': 'CSLB-868994', 'PLUMBING1': 'CSLB-1034873',
}
srows = []
sattrs = []
src_list = load('sources.json')['rows']
for s in src_list:
    ids = [s['id']] + ([cross[s['id']]] if s['id'] in cross else [])
    stags = []
    if s['kind'] == 'official-government':
        stags.append('gov')
    elif s['kind'] == 'company-official':
        stags.append('company')
    elif 'credential' in s['kind'] or 'review' in s['kind'] or 'permit-aggregator' in s['kind']:
        stags.append('review')
    if s['retrieval'] == 'direct':
        stags.append('direct')
    else:
        stags.append('excerpt')
    sattrs.append(','.join(stags))
    srows.append([
        e(s['id']),
        link(s['url'], s['title']),
        e(s['publisher']) + '<br>' + pill(s['kind'], 'ok' if s['kind'] == 'official-government' else 'neutral') + f"<br><span class='small'>checked {e(s['checked'])}</span>",
        pill(s['retrieval'], 'ok' if s['retrieval'] == 'direct' else 'warn'),
        e(s['supports']),
        e(s['limitations']),
        src_links(ids),
    ])
s_filter = filter_ui(
    'sources-table',
    [('all', f'All ({len(src_list)})'), ('gov', 'Official Gov / Code'), ('direct', 'Directly Retrieved'), ('company', 'Company Sites'), ('review', 'BBB / Diamond / Yelp'), ('excerpt', 'Search Excerpts / Blocked')],
    'Filter sources by publisher, CSLB #, URL, or keyword…',
)
body = f'<p>{len(src_list)} source records updated {e(AS_OF)}. “Direct” means the exact URL/PDF was retrieved directly in this session; search excerpts, HTTP-403 Yelp pages and repository records are explicitly labeled, with official cross-references on every non-government row.</p>' + s_filter + table('Source register', ['ID', 'Source', 'Publisher / type', 'Retrieval', 'Supports', 'Limitations', 'Links'], srows, 'sources-table', sattrs)
(ROOT / 'sources.html').write_text(page('sources.html', 'Sources', 'Every consulted official, company, BBB, Diamond Certified and review source with retrieval status and limitations.', body, has_filters=True), encoding='utf-8')

# 9. Flags (41 flags + filter bar)
frows = []
fattrs = []
for f in F:
    ftags = [f['severity'].lower()]
    if f['status'].startswith('Resolved'):
        ftags.append('resolved')
    else:
        ftags.append('open')
    fattrs.append(','.join(ftags))
    frows.append([
        e(f['id']),
        pill(f['severity'], 'bad' if f['severity'] == 'High' else 'warn' if f['severity'] == 'Medium' else 'neutral'),
        e(f['category']),
        f"<strong>{e(f['title'])}</strong><br>{e(f['detail'])}",
        e(f['action']),
        pill(f['status'], 'ok' if f['status'].startswith('Resolved') else 'warn'),
        src_links(f['source_ids'], f['official_url']),
    ])
f_filter = filter_ui(
    'flags-table',
    [('all', f'All ({len(F)})'), ('open', 'Open items'), ('high', 'High severity'), ('medium', 'Medium severity'), ('resolved', 'Resolved')],
    'Filter flags by ID, contractor, citation, or keyword…',
)
body = f'<p>{len(F)} flagged items (updated {e(AS_OF)}). Open/unverified items do not block publication; they are surfaced transparently alongside high-risk CSLB citations, BBB B- complaints and resolved audit corrections.</p>' + f_filter + table('Flagged for review', ['ID', 'Severity', 'Category', 'Finding', 'Action', 'Status', 'Sources'], frows, 'flags-table', fattrs)
(ROOT / 'flagged-for-review.html').write_text(page('flagged-for-review.html', 'Flagged for review', 'Irregularities, statutory citations, BBB alerts, unconfirmed values and resolved corrections.', body, has_filters=True), encoding='utf-8')

# 10. Verification
deploy_path = DATA / 'deployment.json'
deploy = json.loads(deploy_path.read_text()) if deploy_path.exists() else {'status': 'Pending final merge and live check', 'pr': '', 'merge_commit': '', 'pages_url': 'https://karagemop466-tech.github.io/Korea8/', 'checked': ''}
vrows = [
    ['Canonical pages', f'{len(NAV)} root pages generated from overflow-integration/data (as of {AS_OF})', src_links(['REPO'])],
    ['Provider records', f'{len(cslb_checked)} CSLB records directly rechecked {AS_OF} ({len(active)} active, {len(susp)} suspended); {len(unresolved)} unresolved identities left blank', src_links(['CSLB-SEARCH', 'CSLB-1027286', 'DG-CITATION'])],
    ['Requirements', f'{len(R)} rows with official context links and legacy mappings', src_links(['REPO', 'OWNER'])],
    ['Sources', f'{len(S)} records with retrieval status, date and official cross-references', src_links(['REPO'])],
    ['Flags', f'{len(F)} published irregularities/citations/open items', src_links(['REPO', 'DG-CITATION', 'BBB-HEISE'])],
    ['Deployment', e(deploy['status']) + (f"<br>PR: {link(deploy['pr'])}" if deploy.get('pr') else '') + (f"<br>Merge commit: <span class='mono'>{e(deploy['merge_commit'])}</span>" if deploy.get('merge_commit') else '') + (f"<br>Checked: {e(deploy['checked'])}" if deploy.get('checked') else ''), src_links(['PAGES-API', 'REPO-BOARD'])],
]
body = '<p>The verifier checks local links/anchors, row-source coverage, CSLB license-link parity, blank unverified fields, HTML balance, ranked shortlist integrity and neutral public wording. Build/test reports are written to <code>overflow-integration/</code> and <code>site-data/</code>.</p>' + table('Verification summary', ['Check area', 'Result', 'Sources'], vrows) + '<p><a href="overflow-integration/REPO_AUDIT.md">Repository audit</a> · <a href="overflow-integration/build-report.json">Build report</a> · <a href="overflow-integration/verification-report.json">Verification report</a></p>'
(ROOT / 'verification.html').write_text(page('verification.html', 'Verification', 'Audit, build and publication checks for the canonical dashboard.', body), encoding='utf-8')

# CSS
css = '''
:root{--bg:#f5f7fb;--card:#fff;--ink:#14213d;--muted:#52627a;--line:#dbe3ef;--accent:#0e6b78;--accent2:#123c69;--warn:#8a5600;--bad:#a12626;--ok:#176b3a;--info:#154c8a}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink);font-variant-numeric:tabular-nums}
a{color:var(--accent2)}a:hover{color:var(--accent)}a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-9999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:20}
.topbar{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10;box-shadow:0 1px 4px #123c690a}
.topbar-inner{display:flex;gap:16px;align-items:center;justify-content:space-between;padding-top:11px;padding-bottom:11px;flex-wrap:wrap}
.brand{font-weight:800;text-decoration:none;color:var(--accent2);white-space:nowrap;font-size:1.05rem}
.nav{display:flex;gap:5px;flex-wrap:wrap}
.nav a{padding:6px 10px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:.88rem;font-weight:500}
.nav a.active,.nav a:hover{background:#e7f3f5;color:var(--accent);font-weight:600}
.hero{padding:32px 0 18px}
.eyebrow{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:.77rem;margin:0 0 8px}
h1{font-size:clamp(1.7rem,3vw,2.45rem);line-height:1.15;margin:0 0 12px}
h2{margin:30px 0 12px;font-size:1.35rem;color:var(--accent2)}
h3{margin:0 0 8px;font-size:1.08rem}
.lede{font-size:1.06rem;color:var(--muted);max-width:880px;margin:0}
.grid{display:grid;gap:14px}
.kpis{grid-template-columns:repeat(auto-fit,minmax(215px,1fr));margin:18px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:0 1px 3px #123c6908}
.kpi .n{display:block;font-size:2rem;font-weight:800;color:var(--accent2);line-height:1.1}
.kpi .l{display:block;font-weight:700;margin-top:4px}
.kpi .s{display:block;color:var(--muted);font-size:.84rem;margin-top:6px}
.cards{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;text-decoration:none;color:inherit;transition:border-color .15s,box-shadow .15s}
.card:hover{border-color:var(--accent);box-shadow:0 4px 14px #123c6914}
.card p{margin:0;color:var(--muted);font-size:.91rem}
.panel{background:#eef6f7;border:1px solid #c7dfe3;border-radius:14px;padding:18px;margin:18px 0}
.filterbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:12px 0}
.filter-search{flex:1 1 240px;padding:8px 12px;border:1px solid var(--line);border-radius:8px;font:inherit;font-size:.92rem;color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--line);background:#f7f9fc;color:var(--muted);padding:5px 11px;border-radius:999px;font:inherit;font-size:.82rem;font-weight:600;cursor:pointer}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip.active{background:var(--accent2);border-color:var(--accent2);color:#fff}
.filter-count{margin-left:auto;white-space:nowrap}
.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px;margin:12px 0;box-shadow:0 1px 3px #123c6908}
table{border-collapse:collapse;width:100%;min-width:780px;font-size:.91rem}
caption{text-align:left;font-weight:700;padding:12px 14px;color:var(--accent2);border-bottom:1px solid var(--line);background:#fafcff}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{background:#f0f4fa;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
tbody tr:hover{background:#fafcff}
tr:last-child td{border-bottom:0}
.sources{font-size:.81rem;overflow-wrap:anywhere}
.small{font-size:.82rem;color:var(--muted)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.pill{display:inline-block;border-radius:999px;padding:2px 8px;font-size:.74rem;font-weight:700;background:#eef1f6;color:var(--muted);margin:2px 3px 2px 0;white-space:nowrap}
.pill.ok{background:#e5f4ea;color:var(--ok)}
.pill.warn{background:#fff3d9;color:var(--warn)}
.pill.bad{background:#fde7e7;color:var(--bad)}
.pill.unv{background:#f0ecfa;color:#5b3fa2}
.pill.info{background:#e4eefb;color:var(--info)}
.blank{display:inline-block;min-width:1.2em;border-bottom:1px dotted var(--muted)}
.tight{margin:8px 0;padding-left:22px}.tight li{margin:6px 0}
.footer{margin:36px 0 24px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}
@media(max-width:720px){.topbar-inner{align-items:flex-start}.nav a{font-size:.81rem;padding:5px 7px}table{min-width:660px}.filter-count{margin-left:0}}
@media print{.topbar,.filterbar{display:none}.tablewrap{overflow:visible;box-shadow:none}body{background:#fff}}
'''
(ROOT / 'style.css').write_text(css.strip() + '\n', encoding='utf-8')

report = {
    'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'generator': 'scripts/build_overflow_site.py',
    'data': 'overflow-integration/data',
    'as_of': AS_OF,
    'pages': [u for u, _ in NAV],
    'counts': {
        'providers': len(P),
        'cslb_records': len(cslb_checked),
        'active': len(active),
        'suspended': len(susp),
        'unresolved': len(unresolved),
        'b_c36': len(bc),
        'c9': len(c9),
        'ranked_shortlist': len(ranked_short),
        'requirements': len(R),
        'estimates': len(E['rows']),
        'cost_drivers': len(E['cost_drivers']),
        'technical': len(T),
        'compliance': len(C),
        'reviews': len(V),
        'sources': len(S),
        'flags': len(F),
    },
    'preserved': ['redirect stubs', 'archive/', 'docs/ GEMS', 'src/', 'vendor/', 'registry/', 'evidence/', 'downloads/', 'submissions/'],
    'owner_amounts_published_as_unverified': True,
}
(ROOT / 'overflow-integration' / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
(ROOT / 'site-data' / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report['counts'], indent=2))

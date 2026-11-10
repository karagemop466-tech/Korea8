#!/usr/bin/env python3
"""Build the canonical bathtub overflow dashboard from reviewed scoped data.

Standard library only. Writes root HTML/CSS, executive-summary markdown and a
build report. Does not touch redirect stubs, archives or unrelated GEMS files.
"""
from __future__ import annotations
import html, json, pathlib, datetime
ROOT=pathlib.Path(__file__).resolve().parent.parent
DATA=ROOT/'overflow-integration'/'data'
def load(n): return json.loads((DATA/n).read_text(encoding='utf-8'))
S={s['id']:s for s in load('sources.json')['rows']}
P=load('providers.json')['rows']; R=load('requirements.json')['rows']; E=load('estimates.json')
T=load('technical.json')['rows']; C=load('compliance.json')['rows']; V=load('reviews.json')['rows']; F=load('flags.json')['rows']
RK=load('ranking.json'); W={w['id']:w for w in RK['weights']}
AS_OF=load('providers.json')['as_of']
NAV=[('index.html','Dashboard'),('executive-summary.html','Executive summary'),('decision-analysis.html','Ranking'),('requirements.html','Requirements'),('providers.html','Providers'),('estimates.html','Estimates'),('technical-approach.html','Technical approach'),('code-and-permit.html','Code & permit'),('sources.html','Sources'),('flagged-for-review.html','Flagged for review'),('verification.html','Verification')]
def e(x): return html.escape(str(x if x is not None else ''),quote=True)
def blank(): return '<span class="blank" aria-label="blank"></span> <span class="pill unv">unverified</span>'
def val(x): return e(x) if x not in (None,'',[]) else blank()
def link(url,label=None):
 if not url: return blank()
 return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label or url)}</a>'
def src_links(ids, official_url=None):
 out=[]; seen=set()
 for i in ids or []:
  s=S.get(i)
  if not s: continue
  u=s['url']
  if u in seen: continue
  seen.add(u); label=s['title']
  if len(label)>72: label=label[:69]+'…'
  out.append(link(u,label))
 if official_url and official_url not in seen: out.append(link(official_url,'Official source'))
 return '<div class="sources">'+' · '.join(out)+'</div>' if out else blank()
def pill(text,kind='neutral'): return f'<span class="pill {kind}">{e(text)}</span>'
def table(caption,headers,rows,id=None):
 h=''.join(f'<th scope="col">{e(x)}</th>' for x in headers)
 body=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)
 tid=f' id="{e(id)}"' if id else ''
 return f'<div class="tablewrap"><table{tid}><caption>{e(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'
def page(slug,title,subtitle,body):
 nav=''.join(f'<a href="{e(u)}"{" class=active" if u==slug else ""}>{e(t)}</a>' for u,t in NAV)
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — Bathtub overflow trip lever</title><meta name="description" content="{e(subtitle)}">
<link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="wrap topbar-inner"><a class="brand" href="index.html">Trip Lever Project</a><nav class="nav" aria-label="Primary">{nav}</nav></div></header>
<main id="main" class="wrap"><section class="hero"><p class="eyebrow">San Francisco · tenant-occupied unit · reviewed {e(AS_OF)}</p><h1>{e(title)}</h1><p class="lede">{e(subtitle)}</p></section>
{body}
<footer class="footer"><p>Canonical repair dashboard. Parallel drafts are preserved as redirect stubs/archives; unrelated DOE GEMS research remains at <a href="docs/index.html">docs/index.html</a>. Source links open in a new tab. Unconfirmed values are blank and flagged.</p><p><a href="https://github.com/karagemop466-tech/Korea8/blob/main/COORDINATION.md">Coordination log</a> · <a href="https://github.com/karagemop466-tech/Korea8">Repository</a></p></footer></main></body></html>'''
def money(x): return f'${x:,.0f}' if isinstance(x,(int,float)) else blank()
active=[p for p in P if p['status']=='Current and active']; susp=[p for p in P if p['status']=='Suspended']; unresolved=[p for p in P if not p['license']]
bc=[p for p in P if 'B' in p['classifications'] and 'C-36' in p['classifications']]
c9=[p for p in P if 'C-9' in p['classifications']]
order={'Combined-scope lead':0,'Technical case-study lead':1,'Existing estimate':2,'Restoration partner':3,'Conditional combined-scope lead':4,'Conditional review lead':5,'Additional registry candidate':6,'Conditional registry candidate':7,'Not eligible — suspended':8,'Identity unresolved':9}
Ps=sorted(P,key=lambda p:(order.get(p['group'],9),p['name']))
short=[p for p in Ps if p['group'] in {'Combined-scope lead','Technical case-study lead','Restoration partner','Existing estimate'}]
def rscore(r): return sum(r['score_components'][k]*w['weight'] for k,w in W.items())
RKs=sorted(RK['ranked'],key=lambda r:(-rscore(r),-r['score_components']['C2'],r['name']))
PARTNER=RK['partner']
# Dashboard
counts={'providers':len(P),'cslb_records':len([p for p in P if p['license']]),'active':len(active),'suspended':len(susp),'unresolved':len(unresolved),'b_c36':len(bc),'c9':len(c9),'requirements':len(R),'flags':len(F),'sources':len(S),'ranking':len(RK['ranked']),'ranking_held':len(RK['not_recommended'])}
kpis=[(str(counts['cslb_records']),'CSLB records rechecked',f"{counts['active']} active · {counts['suspended']} suspended · {counts['unresolved']} identity unresolved"),(str(counts['b_c36']),'B + C-36 inquiry leads','Classification combination only; restoration party must be named'),(str(counts['c9']),'C-9 restoration partner','Bernal Hill Drywall; no C-36 on that license'),(str(len(R)),'requirements captured','Deduplicated from parallel registers with provenance')]
kpi_html='<div class="grid kpis">'+''.join(f'<div class="kpi"><span class="n">{e(n)}</span><span class="l">{e(l)}</span><span class="s">{e(s)}</span></div>' for n,l,s in kpis)+'</div>'
cards=[('executive-summary.html','Executive summary','Decision, shortlist, estimate comparison and next steps.'),('decision-analysis.html','Ranked decision analysis','Best-to-hire order with reasoning, cost basis, phones and official links.'),('requirements.html','Requirements',f'{len(R)} source-linked requirements and acceptance checks.'),('providers.html','Providers',f"{len(P)} identities: {counts['cslb_records']} CSLB records plus one unresolved name; review limits separated."),('estimates.html','Estimates','Owner-reported amounts, blank verified amounts and official DBI fees.'),('technical-approach.html','Technical approach','Tub-side service path, ceiling fallback and model-specific limits.'),('code-and-permit.html','Code & permit','Permit trigger, conditional exemptions, licensing, tenant entry and fees.'),('sources.html','Sources',f'{len(S)} source records with retrieval status and limitations.'),('flagged-for-review.html','Flagged for review',f'{len(F)} irregularities/open items; non-blocking but published.'),('verification.html','Verification','Audit checks, build report and publication record.')]
card_html='<div class="grid cards">'+''.join(f'<a class="card" href="{e(u)}"><h3>{e(t)}</h3><p>{e(d)}</p></a>' for u,t,d in cards)+'</div>'
snapshot=[
 ['License records rechecked',str(counts['cslb_records']),f"{counts['active']} current and active; Kenneth Asire #1027286 suspended; Portola identity unresolved",src_links(['CSLB-1027286','CSLB-SEARCH'])],
 ['Combined-classification leads',f"{counts['b_c36']} B + C-36",'Rapid Flow, Ace, We Do, Save-On-Interior, Ayoob & Peery, D G. Ask who performs restoration.',src_links(['CSLB-1115649','CSLB-829071','CSLB-1096552','CSLB-749536','CSLB-392967','CSLB-297604','CSLB-C9'])],
 ['Strongest adjacent technical case','Heise’s Ingleside','Company-published ceiling-access tub waste/overflow replacement and advertised drywall/ceiling patching; this job’s restoration unconfirmed.',src_links(['HEISE-INGLESIDE','HEISE-PATCH','CSLB-1089561'])],
 ['Owner estimates','3 supplied','Amounts are owner-reported; verified amounts blank; scopes differ.',src_links(['OWNER','CSLB-977638','CSLB-757796','CSLB-1024971'])],
 ['Ranked hiring order','<a href="decision-analysis.html">Ace, Heise’s, Rapid Flow</a>','Editorial weighted ranking; first three leads, with reasoning and cost basis on the ranking page.',src_links(['CSLB-829071','CSLB-1089561','CSLB-1115649'],'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx')],
 ['Permit determination','Open','SF.gov permit trigger and §104.2 conditional exemptions reviewed; exact job answer not supplied.',src_links(['SF-PERMIT','SF-CODE-104'])],
 ['Exact all-in-one acceptance','Unconfirmed','No provider contacted/booked; no combined ceiling-restoration quote on file.',src_links(['OWNER','REPO-BOARD','CSLB-CONTRACT','GH-PR'])]]
top5=''.join(f'<li><strong>{e(r["name"])}</strong> — {e(r["phone"])}: {e(r["short_why"])}.</li>' for r in RKs[:5])
body=kpi_html+'<h2>Browse the dossier</h2>'+card_html+'<h2>Status snapshot</h2>'+table('Each row links the source it rests on; unconfirmed values remain blank.',['Item','Value','What it means','Sources'],snapshot)+'<div class="panel"><h3>Who to call first</h3><p>Weighted hire order from the ranking page. It is editorial decision support, not a verified performance rating: no provider has been contacted.</p><ol class="tight">'+top5+'</ol><p>Pair any plumbing lead with <a href="decision-analysis.html">Bernal Hill Drywall</a> for the ceiling, and ask every lead for one written combined scope, the named restoration party, an occupied-unit schedule and the permit position. <a href="decision-analysis.html">Full ranking and reasoning &rarr;</a></p></div>'
(ROOT/'index.html').write_text(page('index.html','Bathtub wastewater overflow trip lever','A source-checked repair dashboard: find a lawful combined plumbing-and-restoration path, compare unlike estimates carefully, and keep every unconfirmed value blank.',body),encoding='utf-8')
# Executive summary
summary_md=f'''# Executive summary — bathtub wastewater overflow trip lever

Reviewed {AS_OF}. San Francisco tenant-occupied unit. This summary is based on the linked
official/company sources and a neutral owner record; it is not a contractor booking or legal advice.

## Decision
Use a two-path scope: first ask a licensed plumber to identify the assembly and attempt the least
destructive tub-side adjustment/removal; if that fails, use below-ceiling access through the storage
unit only under a written combined contract that names the plumbing and drywall/restoration parties.
Do not assume a permit exemption: SF.gov requires a permit before cutting/replacing pipes, and
SF Plumbing Code §104.2 exemptions are conditional.

## Ranked hiring order (decision support, not a verified performance rating)
Weighted on licence capability, scope evidence, licence standing, occupied-unit experience and price
evidence; full reasoning, scores and cost basis are on the Ranked decision analysis page.

1. Ace Plumbing & Rooter #829071, (415) 824-6444 — B + C-36 + A/C-4/C-16/C-10, active since 2003, current workers comp, advertised HOA/property-manager work. No quote on file.
2. Heise’s Plumbing #1089561, (415) 333-0704 — C-36/C-10/A/C-20; published San Francisco ceiling-access tub waste-and-overflow case and advertised plumbing-access and ceiling patching; no B or C-9, so the restoration party and contract structure must be confirmed. No quote on file.
3. Rapid Flow Plumbing & Rooter #1115649, (415) 866-8401 — B + C-36, published simple-repair-to-renovation offer; 2024 licence, workers-comp exempt. No quote on file.
4. Ayoob & Peery #392967, (415) 550-0975 — B + C-36, active since 1980, current workers comp; no scope evidence.
5. We Do Construction #1096552, (415) 416-5494 — B + C-36; larger-scope positioning, small-repair acceptance unconfirmed.
6. Expert Plumbing Solutions #977638, (415) 531-5340 — C-36 only; owner-reported $614 for "replace waste and overflow".
7. Save-On-Interior #749536, (415) 668-8000 — B + C-36 at Bay Area Plumbing's address/phone; ownership unproven, 2015–2016 CSLB cash-deposit letters.
8. Bay Area Plumbing #757796, (415) 668-8000 — C-36 only; owner-reported $550 but the wording may describe a spout/diverter, not the overflow body.
9. Discount Plumbing Rooter Services #1140843, (650) 991-2100 — C-36 + A, $2M liability and LLC bond on file; Burlingame, no building classification.
10. Fast Response Plumbing & Rooter #1024971, (415) 596-6115 — C-36 only; owner-reported $135 is adjustment-only; workers comp expires 2026-12-18.

Restoration partner: Bernal Hill Drywall #995163, (415) 533-8274 — C-9 + B; not a plumbing candidate.
Atlas Plumbing & Rooter #868994 is a conditional review lead held outside the hiring order pending a direct trip-lever reference, restoration party and current dispatch number.
Held back: D G Construction (CSLB citation disclosed), Advanced Plumbing (future-suspension warning),
24/7 SF Handyman (B-2), SF Building Group (B only), Precision (drain cleaning), Clever (licensed 2026-09-04),
Cahill (no C-36), Kenneth Asire (suspended), Portola (identity unresolved), Atlas (conditional review lead).

## Estimates
Owner-supplied amounts dated 2026-08-30: Expert $614 (replace waste and overflow), Bay Area $550
(lever/plug/spout with diverter, labor/materials), Fast Response $135 (repair/adjust plunger handle).
These are owner reports, not independently verified prices; verified amounts remain blank. The scopes
differ and none explicitly names ceiling opening/restoration. The $479 spread is arithmetic, not a
like-for-like market range. Official DBI Category 1P is $290, but the job category and quote inclusions
are unconfirmed.

## Key controls
- Verify the legal contracting entity, license status/classifications, bond and insurance on signing day.
- Name who performs drywall/texture/paint; B + C-36 is not proof of drywall self-performance.
- Get the DBI permit determination and inspection-before-covering path in writing.
- Give affected tenants Civil Code §1954 notice; coordinate storage-unit authority, water shut-off and contents protection.
- Screen conditionally for lead/asbestos before disturbing finishes; building age/materials are unknown.
- Use a written itemized contract, lawful down payment, written change orders, leak/function test and photo record.

## Open items
No provider has confirmed this exact stuck-lever job, ceiling restoration, availability or price.
Portola’s identity is unresolved. Yelp ratings/counts are blank because business pages were blocked.
Access-panel dimensions remain unverified. See the Flagged for Review page for all {len(F)} items.
'''
(ROOT/'overflow-integration'/'EXECUTIVE_SUMMARY.md').write_text(summary_md,encoding='utf-8')
(ROOT/'OVERFLOW_EXECUTIVE_SUMMARY.md').write_text(summary_md,encoding='utf-8')
exec_rows=[['Decision','Two-path scope: tub-side first; below-ceiling fallback only with named trades and written permit answer.',src_links(['OWNER','WATCO','SF-PERMIT','CSLB-C9'])],['Ranked order','Ace first, Heise’s second, Rapid Flow third, then Ayoob & Peery; Bernal Hill is the ceiling-restoration partner. Reasoning, weighted scores and cost basis are on the ranking page.',src_links(['CSLB-829071','CSLB-1089561','CSLB-1115649','CSLB-392967','CSLB-995163'],'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx')],['Estimates','Owner-reported $614/$550/$135; verified amounts blank; scopes differ.',src_links(['OWNER','CSLB-977638','CSLB-757796','CSLB-1024971'])],['Permit','DBI determination open; cutting/replacing pipes triggers permit guidance; exemptions conditional.',src_links(['SF-PERMIT','SF-CODE-104'])],['Tenant/site','Notice, storage authority, water shut-off, contents protection and conditional lead/asbestos screening.',src_links(['CIV-1954','EPA-RRP','EPA-ASBESTOS'])],['Evidence gap','No exact-job acceptance, booking, photos, model or combined restoration quote.',src_links(['OWNER','REPO-BOARD','CSLB-CONTRACT','GH-PR'])]]
body='<div class="panel"><h3>Bottom line</h3><p>Call Ace Plumbing &amp; Rooter first: it is the only lead that combines a B + C-36 licence, current workers compensation, a 2003 licence date and published HOA/property-manager work. Heise’s ranks second with a company-published San Francisco ceiling-access tub waste-and-overflow case and advertised drywall and ceiling patching. Its licence has no B or C-9; confirm the restoration party and contract structure. Rapid Flow ranks third on single-contract capability. None of them has confirmed this exact stuck-lever job, an occupied-unit schedule or a combined price.</p><p><a href="decision-analysis.html">Ranked decision analysis: reasoning, cost basis, phone numbers and official links &rarr;</a></p></div>'+table('Executive findings',['Topic','Finding','Sources'],exec_rows)+'<h2>Estimate comparison</h2>'+table('Owner-reported amounts are not verified prices.',['Provider','Supplied scope','Supplied amount','Verified amount','Sources'],[[e(x['provider']),e(x['scope_owner']),money(x['amount_owner']),blank(),src_links(x['source_ids'])] for x in E['rows']])+'<h2>Next steps</h2><ol class="tight"><li>Send one identical neutral scope to the shortlist; ask for the named restoration party, occupied-unit plan, permit path and current written price.</li><li>Confirm storage-unit authority and tenant notice before scheduling.</li><li>Collect photos/model/size and screen finishes before demolition.</li><li>Use a written contract with lawful payment terms, change orders, testing and cleanup.</li></ol><p><a href="OVERFLOW_EXECUTIVE_SUMMARY.md">Markdown executive summary</a></p>'
(ROOT/'executive-summary.html').write_text(page('executive-summary.html','Executive summary','Decision, shortlist, estimate comparison and the controls that must be settled before work.',body),encoding='utf-8')

# Ranked decision analysis
def rank_cell(r):
    comps=' · '.join(f"{k} {r['score_components'][k]}" for k in sorted(r['score_components']))
    return f"<strong>{rscore(r):.2f}</strong><br><span class='small mono'>{e(comps)}</span>"
def provider_cell(r):
    lic=f"<span class='mono'>{e(r['license'])}</span>" if r['license'] else blank()
    stat=pill(r['status'],'ok' if r['status']=='Current and active' else 'bad' if r['status']=='Suspended' else 'unv')
    cls=', '.join(r['classifications']) if r['classifications'] else blank()
    phone=e(r['phone']) if r['phone'] else blank()
    web=('<br>'+link(r['website'],'Company site')) if r['website'] else ''
    return f"<strong>{e(r['name'])}</strong><br><span class='small'>{e(r['legal_name'])}</span><br>{phone}<br>{lic} {stat}<br><span class='small'>{e(cls)} · {e(r['city'])}</span>"+web
rrows=[]
for i,r in enumerate(RKs,1):
    cost=(money(r['cost_amount_owner'])+' '+pill('owner-reported','warn')) if r['cost_amount_owner'] else blank()
    rrows.append([f'<strong>{i}</strong>',provider_cell(r),rank_cell(r),e(r['why']),cost+f"<br><span class='small'>{e(r['cost_note'])}</span>",e(r['ask']),src_links(r['source_ids'],r['official_url'])])
wrows=[[e(w['id']),e(w['criterion']),f"{w['weight']:.2f}",e(w['basis']),src_links(w['source_ids'])] for w in RK['weights']]
prow=[['Partner',provider_cell(PARTNER),rank_cell(PARTNER),e(PARTNER['why']),blank()+f"<br><span class='small'>{e(PARTNER['cost_note'])}</span>",e(PARTNER['ask']),src_links(PARTNER['source_ids'],PARTNER['official_url'])]]
nrows=[[e(r['name'])+(f"<br><span class='mono'>{e(r['license'])}</span> <span class='small'>{e(r['status'])}</span>" if r['license'] else '')+(f"<br>{e(r['phone'])}" if r['phone'] else ''),e(r['reason']),src_links(r['source_ids'],r['official_url'])] for r in RK['not_recommended']]
ranking_note=e(RK.get('final_verification_note',''))
body=(f'<div class="panel"><h3>How to read this ranking</h3><p>This is editorial decision support, not a verified performance or quality rating. Each candidate is scored only on the official CSLB record, company-published service statements and the owner-supplied quote wording, all re-read on 2026-11-08. No provider was contacted, no reference was taken, and no availability, schedule or combined price has been confirmed by anyone. The weights and the evidence behind every score are listed below, so you can disagree with the weights and re-order the list yourself.</p><p class="small">{ranking_note}</p></div>'
 +'<h2>Ranked hiring order</h2><p class="small">C1–C5 are the scoring criteria defined in the next table. Costs are owner-reported only, and a blank means no quote exists — not a zero or an estimate.</p>'+table('Weighted order, highest first. Cost column: owner-reported amount where one exists, otherwise blank with no quote on file.',['#','Provider / contact','Score','Why this rank','Cost basis','What to ask','Sources'],rrows,'ranking-table')
 +'<h2>Scoring criteria</h2>'+table('Weights sum to 1.00; scores are 1–5 per criterion.',['ID','Criterion','Weight','Basis for the rating','Sources'],wrows)
 +'<h2>Restoration partner</h2><p>The ceiling repair is the second half of the all-in-one requirement. Pair one of the plumbing leads above with the only drywall specialist on the register rather than assuming a B + C-36 holder performs the patch itself.</p>'+table('Restoration partner, scored on the same criteria but not a plumbing candidate',['#','Provider / contact','Score','Why this rank','Cost basis','What to ask','Sources'],prow)
 +'<h2>Assessed and not recommended for this job</h2><p>These identities were checked on the official CSLB record and are listed so that nothing is silently dropped. Each carries the reason it sits outside the hiring order.</p>'+table('Held back or excluded, with the reason and the official record',['Provider / licence','Reason','Sources'],nrows)
 +'<h2>Cost picture</h2><ul class="tight"><li>Owner-reported amounts dated 2026-08-30: $614 for "replace waste and overflow", $550 for "lever, plug and spout with diverter", $135 for "repair or adjust plunger handle". All three are owner reports, not verified prices; verified amounts are blank everywhere on this site.</li><li>None of the three supplied scopes prices the ceiling opening, the drywall patch, texture or paint. A combined price therefore has to be requested; it cannot be calculated from these figures.</li><li>Official DBI fees are separate from any contractor price: Category 1P is $290 per permit and Category 11P/M is $320, and category applicability for this job is unconfirmed.</li><li>Review evidence is missing by force, not by choice: Yelp returned HTTP 403 again on 2026-11-08, so no rating, review count or review text is published.</li></ul>')
(ROOT/'decision-analysis.html').write_text(page('decision-analysis.html','Ranked decision analysis','Best-to-hire order with the reasoning, the cost basis, phone numbers and official licence links behind it.',body),encoding='utf-8')
# Requirements
rows=[]
for r in R:
 rows.append([e(r['id']),e(r['category']),e(r['requirement']),f"<strong>Basis:</strong> {e(r['basis'])}<br><strong>Acceptance:</strong> {e(r['acceptance_check'])}<br><span class='small'>Legacy mapping: {e(r['legacy_ids'])}</span>",pill(r['origin'],'ok' if r['origin']=='Official rule' else 'warn')+f"<br><span class='small'>{e(r['status'])}</span>",src_links(r['source_ids'],r['official_url'])])
body=f'<p>{len(R)} requirements deduplicated from the parallel registers. Owner requirements and proposed controls are not presented as official facts; official context links are provided for review.</p>'+table('Full requirement register',['ID','Category','Requirement','Basis / acceptance check','Origin / status','Sources'],rows,'requirements-table')
(ROOT/'requirements.html').write_text(page('requirements.html','Requirements','Full source-linked register with acceptance checks, origin labels and legacy mappings.',body),encoding='utf-8')
# Providers
prows=[]
for p in Ps:
 lic=f"<span class='mono'>{e(p['license'])}</span>" if p['license'] else blank()
 status=pill(p['status'],'ok' if p['status']=='Current and active' else 'bad' if p['status']=='Suspended' else 'unv')
 cls=', '.join(p['classifications']) if p['classifications'] else blank()
 extra=f"<br><span class='pill warn'>CSLB note</span> <span class='small'>{e(p['additional_status'])}</span>" if p['additional_status'] else ''
 fit=f"<strong>{e(p['group'])}.</strong> {e(p['fit'])}{extra}"
 if p['service_claim']: fit+=f"<br><span class='small'>Company self-description: {e(p['service_claim'])}</span>"
 contact=(e(p['registered_city'])+'<br>'+e(p['phone'])) if p['registered_city'] else blank()
 prows.append([f"<strong>{e(p['name'])}</strong><br><span class='small'>{e(p['legal_name'])}</span>",lic+'<br>'+status+ (f"<br><span class='small'>expires {e(p['expiry'])}</span>" if p['expiry'] else ''),e(cls),contact,e(p['workers_comp']) if p['workers_comp'] else blank(),fit,src_links(p['source_ids'],p['official_url'])+(('<br>'+link(p['website'],'Company site')) if p['website'] else '')])
srows=[]
for i,r in enumerate(RKs,1):
 srows.append([f'<strong>{i}</strong>',e(r['name'])+f"<br><span class='small'>{e(r['phone'])}</span>",e(r['why']),src_links(r['source_ids'],r['official_url'])])
vrows=[[e(v['provider']),e(v['platform']),e(v['observation']),blank(),blank(),pill('Unverified','unv'),e(v['limit']),src_links(v['source_ids'],v['official_url'])+'<br>'+link(v['review_url'],'Review lead')] for v in V]
body='<h2>Ranked hiring shortlist</h2><p>Full method, weighted scores, cost basis and the excluded candidates are on the <a href="decision-analysis.html">ranked decision analysis</a> page. The order is editorial decision support, not a verified performance rating.</p>'+table('Top ten in ranked order; no provider has been contacted.',['#','Provider / phone','Why this rank','Sources'],srows)+'<h2>Full provider register</h2><p>CSLB fields are point-in-time official records. Company service claims are self-descriptions. Exact-job acceptance, ceiling restoration and availability are unconfirmed for every provider.</p>'+table(f"{len(P)} identities: {counts['cslb_records']} checked CSLB records and one unresolved name.",['Provider / legal name','License / status','Classifications','Registered city / phone','Workers-comp record','Fit and limits','Sources'],prows,'providers-table')+'<h2>Review-platform observations</h2><p>Numeric ratings and review counts are blank because they were not verified. Search-index excerpts are leads, not directly retrieved reviews.</p>'+table('Unverified review leads',['Provider','Platform','Observation','Rating','Count','Status','Limits','Sources'],vrows)
(ROOT/'providers.html').write_text(page('providers.html','Providers','License-checked inquiry leads, restoration partners, estimate providers and unresolved identities.',body),encoding='utf-8')
# Estimates
erows=[[e(x['provider'])+f"<br><span class='mono small'>{e(x['license'])}</span>",e(x['scope_owner']),e(x['date']),money(x['amount_owner']),blank(),e(x['analysis']),pill(x['status'],'warn'),src_links(x['source_ids'],x['official_url'])] for x in E['rows']]
frows=[[e(f['item']),money(f['amount']),e(f['unit']),e(f['note']),src_links(f['source_ids'],f['official_url'])] for f in E['official_fees']]
body='<div class="panel"><h3>How to read the amounts</h3><p>Supplied amounts are owner-reported primary statements, not independently verified contractor prices. Verified amounts remain blank. The scopes differ, so the arithmetic spread is not a market range.</p><p>Which provider is called first, and why, is set out in the <a href="decision-analysis.html">ranked decision analysis</a>.</p></div>'+table('Owner-supplied estimates dated 2026-08-30',['Provider','Supplied scope','Supplied date','Supplied amount','Verified amount','Analysis','Status','Sources'],erows,'estimates-table')+'<h2>Official DBI fees (not project quotes)</h2>'+table('July 2026 Table 1A-C; category applicability unconfirmed.',['Item','Amount','Unit','Note','Source'],frows)+'<h2>Analysis</h2><ul class="tight">'+''.join(f'<li>{e(a)}</li>' for a in E['analysis'])+'</ul>'
(ROOT/'estimates.html').write_text(page('estimates.html','Estimates','Owner-reported amounts, blank verified amounts, scope gaps and official permit/inspection fees.',body),encoding='utf-8')
# Technical
trows=[[e(t['id']),e(t['topic']),e(t['statement']),pill(t['status'],'warn'),e(t['limit']),src_links(t['source_ids'],t['official_url'])] for t in T]
body='<div class="panel"><h3>Access decision</h3><ol class="tight"><li>Identify the assembly and attempt the least-destructive tub-side path if safe.</li><li>If it cannot be freed, use below-ceiling access only with a written opening/restoration plan and named licensed trades.</li><li>Test and inspect before closing; agree future service access without asserting unverified dimensions.</li></ol></div>'+table('Technical findings and limits',['ID','Topic','Finding','Status','Limit','Sources'],trows)
(ROOT/'technical-approach.html').write_text(page('technical-approach.html','Technical approach','Manufacturer-based service path, adjacent ceiling-access case evidence and restoration limits.',body),encoding='utf-8')
# Compliance
crows=[[e(c['id']),e(c['topic']),e(c['rule']),e(c['application']),src_links(c['source_ids'],c['official_url'])] for c in C]
body='<p>Official rules are reviewed at source; job-specific applicability still needs contractor/DBI confirmation. This page uses neutral repair-scope language.</p>'+table('Code, permit, licensing, tenant and contract rules',['ID','Topic','Official rule / guidance','Application to this job','Sources'],crows)
(ROOT/'code-and-permit.html').write_text(page('code-and-permit.html','Code & permit','Permit trigger, conditional exemptions, licensing structure, tenant entry, contract and fee rules.',body),encoding='utf-8')
# Sources
cross={'OWNER':['CSLB-CONTRACT'],'REPO':['GH-PAGES','GH-PR'],'REPO-OLD-INDEX':['REPO','GH-PAGES'],'REPO-OLD-EXEC':['REPO','GH-PAGES'],'REPO-PR33':['REPO','GH-PR'],'REPO-BOARD':['REPO','GH-PR'],'PAGES-API':['GH-PAGES'],'GH-ACTIONS':['GH-PAGES'],'GH-PR':['GH-PAGES'],'YELP-ATLAS':['CSLB-868994'],'BBB-ATLAS':['CSLB-868994'],'ANGI-SF':['CSLB-SEARCH'],'YELP-ACE-Q':['CSLB-829071'],'YELP-EXPERT':['CSLB-977638'],'YELP-BAY':['CSLB-757796'],'YELP-FAST':['CSLB-1024971'],'YELP-RF':['CSLB-1115649'],'YELP-RF2':['CSLB-1115649'],'YELP-ACE':['CSLB-829071'],'YELP-WEDO':['CSLB-1096552'],'YELP-HEISE':['CSLB-1089561'],'YELP-PORTOLA':['CSLB-SEARCH'],'IAPMO':['SF-CODE-104']}
srows=[]
for s in load('sources.json')['rows']:
 ids=[s['id']]+cross.get(s['id'],[])
 srows.append([e(s['id']),link(s['url'],s['title']),e(s['publisher'])+'<br>'+pill(s['kind'],'ok' if s.get('official',True) else 'neutral'),pill(s['retrieval'],'ok' if s['retrieval']=='direct' else 'warn'),e(s['supports']),e(s['limitations']),src_links(ids)])
body=f'<p>{len(S)} source records. “Direct” means the page/PDF was retrieved on its listed check date; search excerpts, blocked pages and repository records are labeled. Non-official rows include an official cross-reference where available.</p>'+table('Source register',['ID','Source','Publisher / type','Retrieval','Supports','Limitations','Links'],srows,'sources-table')
(ROOT/'sources.html').write_text(page('sources.html','Sources','Every consulted source with retrieval status, support and limitations.',body),encoding='utf-8')
# Flags
frows=[[e(f['id']),pill(f['severity'],'bad' if f['severity']=='High' else 'warn' if f['severity']=='Medium' else 'neutral'),e(f['category']),f"<strong>{e(f['title'])}</strong><br>{e(f['detail'])}",e(f['action']),pill(f['status'],'ok' if f['status'].startswith('Resolved') else 'warn'),src_links(f['source_ids'],f['official_url'])] for f in F]
body=f'<p>{len(F)} flagged items. Open/unverified items do not block publication; they are published with source links and required follow-up. Resolved items record corrections made in this canonical rebuild.</p>'+table('Flagged for review',['ID','Severity','Category','Finding','Action','Status','Sources'],frows,'flags-table')
body += '<div class="panel"><h2>10 November publication review</h2><p>Fresh external-source verification could not be performed in this session. Existing research dates are retained. <a href="audit/2026-11-10-660ab2dd.md">Read the publication audit and source-access limitation</a>. No current availability, exact-job acceptance or combined quote is established.</p></div>'
(ROOT/'flagged-for-review.html').write_text(page('flagged-for-review.html','Flagged for review','Irregularities, unconfirmed values and corrections, published with source links.',body),encoding='utf-8')
# Verification placeholder (updated by verifier/deploy record)
deploy_path=DATA/'deployment.json'
deploy=json.loads(deploy_path.read_text()) if deploy_path.exists() else {'status':'Pending final merge and live check','pr':'','merge_commit':'','pages_url':'https://karagemop466-tech.github.io/Korea8/','checked':''}
vrows=[[f'Canonical pages',f'{len(NAV)} root pages generated from overflow-integration/data',src_links(['REPO','GH-PAGES'])],['Provider records',f"{counts['cslb_records']} CSLB records directly rechecked; {counts['unresolved']} unresolved identity left blank",src_links(['CSLB-SEARCH','CSLB-1027286'])],[f'Ranking',f"{len(RK['ranked'])} ranked candidates, 1 restoration partner and {len(RK['not_recommended'])} held-back identities, each with an official CSLB link",src_links(['CSLB-SEARCH'])],['Requirements',f'{len(R)} rows with official context links and legacy mappings',src_links(['REPO','OWNER','GH-PAGES','CSLB-CONTRACT'])],[f'Sources',f'{len(S)} records with retrieval status and limitations',src_links(['REPO','GH-PAGES'])],[f'Flags',f'{len(F)} published irregularities/open items',src_links(['REPO','GH-PAGES'])],['Deployment',e(deploy['status'])+(f"<br>PR: {link(deploy['pr'])}" if deploy.get('pr') else '')+(f"<br>Merge commit: <span class='mono'>{e(deploy['merge_commit'])}</span>" if deploy.get('merge_commit') else '')+(f"<br>Checked: {e(deploy['checked'])}" if deploy.get('checked') else ''),src_links(['PAGES-API','REPO-BOARD','GH-PAGES','GH-PR'])]]
body='<p>The verifier checks local links/anchors, row-source coverage, CSLB license-link parity, blank unverified fields, HTML balance and neutral public wording. These structural checks do not establish that every source supports every claim or that external links are currently reachable. Source dates and the targeted audit show what was actually rechecked. Build/test reports are written to <code>overflow-integration/</code>.</p>'+table('Verification summary',['Check area','Result','Sources'],vrows)+'<p><strong>10 November publication audit:</strong> <a href="audit/2026-11-10-660ab2dd.md">Publication boundary, reproducibility checks and source-access limitation</a>. That audit did not recheck provider sources.</p><p><a href="overflow-integration/REPO_AUDIT.md">Repository audit</a> · <a href="overflow-integration/build-report.json">Build report</a> · <a href="overflow-integration/verification-report.json">Verification report</a> · <a href="audit/2026-11-10-47d993da/REPORT.md">2026-11-10 targeted independent review</a> · <a href="audit/2026-11-08-215f5c79/REPORT.md">2026-11-08 independent freshness audit</a> · <a href="audit/verification_3946905e/REPORT_2026-11-08_3946905e.md">Final source-verification audit</a></p>'
(ROOT/'verification.html').write_text(page('verification.html','Verification','Audit, build and publication checks for the canonical dashboard.',body),encoding='utf-8')
# CSS
css='''
:root{--bg:#f6f8fb;--card:#fff;--ink:#17233b;--muted:#5b6b84;--line:#dfe6f0;--accent:#0f6b78;--accent2:#123c69;--warn:#8a5a00;--bad:#a12626;--ok:#176b3a}*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}a{color:var(--accent2)}a:hover{color:var(--accent)}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}.skip{position:absolute;left:-9999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:10}.topbar{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}.topbar-inner{display:flex;gap:18px;align-items:center;justify-content:space-between;padding-top:12px;padding-bottom:12px;flex-wrap:wrap}.brand{font-weight:800;text-decoration:none;color:var(--accent2);white-space:nowrap}.nav{display:flex;gap:6px;flex-wrap:wrap}.nav a{padding:6px 9px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:.9rem}.nav a.active,.nav a:hover{background:#e8f2f4;color:var(--accent)}.hero{padding:34px 0 18px}.eyebrow{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:.78rem;margin:0 0 8px}h1{font-size:clamp(1.7rem,3vw,2.5rem);line-height:1.15;margin:0 0 12px}h2{margin:30px 0 12px;font-size:1.35rem}h3{margin:0 0 8px}.lede{font-size:1.08rem;color:var(--muted);max-width:850px;margin:0}.grid{display:grid;gap:14px}.kpis{grid-template-columns:repeat(auto-fit,minmax(210px,1fr));margin:18px 0}.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}.kpi .n{display:block;font-size:2rem;font-weight:800;color:var(--accent2)}.kpi .l{display:block;font-weight:700}.kpi .s{display:block;color:var(--muted);font-size:.85rem;margin-top:6px}.cards{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;text-decoration:none;color:inherit}.card:hover{border-color:var(--accent);box-shadow:0 4px 14px #123c6912}.card p{margin:0;color:var(--muted);font-size:.92rem}.panel{background:#eef6f7;border:1px solid #cfe3e6;border-radius:14px;padding:16px;margin:18px 0}.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px;margin:12px 0}table{border-collapse:collapse;width:100%;min-width:760px;font-size:.92rem}caption{text-align:left;font-weight:700;padding:12px 14px;color:var(--accent2);border-bottom:1px solid var(--line)}th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}th{background:#f0f4f9;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}tr:last-child td{border-bottom:0}.sources{font-size:.82rem;overflow-wrap:anywhere}.small{font-size:.82rem;color:var(--muted)}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.pill{display:inline-block;border-radius:999px;padding:2px 8px;font-size:.75rem;font-weight:700;background:#eef1f6;color:var(--muted);margin:2px 2px 2px 0}.pill.ok{background:#e5f4ea;color:var(--ok)}.pill.warn{background:#fff3d9;color:var(--warn)}.pill.bad{background:#fde7e7;color:var(--bad)}.pill.unv{background:#f0ecfa;color:#5b3fa2}.blank{display:inline-block;min-width:1.2em;border-bottom:1px dotted var(--muted)}.tight{margin:8px 0;padding-left:22px}.tight li{margin:6px 0}.footer{margin:36px 0 24px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}@media(max-width:700px){.topbar-inner{align-items:flex-start}.nav a{font-size:.82rem;padding:5px 7px}table{min-width:640px}}
'''
(ROOT/'style.css').write_text(css.strip()+'\n',encoding='utf-8')
report={'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'scripts/build_overflow_site.py','data':'overflow-integration/data','pages':[u for u,_ in NAV],'counts':{'providers':len(P),'cslb_records':len([p for p in P if p['license']]),'active':len(active),'suspended':len(susp),'unresolved':len(unresolved),'b_c36':len(bc),'c9':len(c9),'requirements':len(R),'estimates':len(E['rows']),'technical':len(T),'compliance':len(C),'reviews':len(V),'sources':len(S),'flags':len(F),'ranking':len(RK['ranked']),'ranking_held':len(RK['not_recommended'])},'preserved':['redirect stubs','archive/','docs/ GEMS','src/','vendor/','registry/','evidence/','downloads/','submissions/'],'owner_amounts_published_as_unverified':True}
(ROOT/'overflow-integration'/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(ROOT/'site-data'/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['counts'],indent=2))

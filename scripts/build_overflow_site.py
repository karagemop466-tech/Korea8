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
T=load('technical.json')['rows']; C=load('compliance.json')['rows']; V=load('reviews.json')['rows']; F=load('flags.json')['rows']; D=load('decision.json')
AS_OF=load('providers.json')['as_of']
NAV=[('index.html','Dashboard'),('executive-summary.html','Executive summary'),('requirements.html','Requirements'),('providers.html','Providers'),('decision-analysis.html','Decision analysis'),('estimates.html','Estimates'),('technical-approach.html','Technical approach'),('code-and-permit.html','Code & permit'),('sources.html','Sources'),('flagged-for-review.html','Flagged for review'),('verification.html','Verification')]
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
# Dashboard
counts={'providers':len(P),'cslb_records':len([p for p in P if p['license']]),'active':len(active),'suspended':len(susp),'unresolved':len(unresolved),'b_c36':len(bc),'c9':len(c9),'requirements':len(R),'estimates':len(E['rows']),'technical':len(T),'compliance':len(C),'reviews':len(V),'sources':len(S),'flags':len(F),'decision_rows':len(D['rows'])}
kpis=[(str(counts['cslb_records']),'CSLB records rechecked',f"{counts['active']} active · {counts['suspended']} suspended · {counts['unresolved']} identity unresolved"),(str(counts['b_c36']),'B + C-36 inquiry leads','Classification combination only; restoration party must be named'),(str(len(R)),'requirements captured','Owner requirements, official rules and proposed controls separated'),(str(len(F)),'flagged items','Open evidence gaps and irregularities; non-blocking review page')]
kpi_html='<div class="grid kpis">'+''.join(f'<div class="kpi"><span class="n">{e(n)}</span><span class="l">{e(l)}</span><span class="s">{e(s)}</span></div>' for n,l,s in kpis)+'</div>'
cards=[('executive-summary.html','Executive summary','Decision, shortlist, estimate comparison and next steps.'),('decision-analysis.html','Decision analysis','Transparent inquiry ranking, evidence gates and cost limits.'),('requirements.html','Requirements',f'{len(R)} source-linked requirements and acceptance checks.'),('providers.html','Providers',f"{len(P)} identities: {counts['cslb_records']} CSLB records plus one unresolved name; review limits separated."),('estimates.html','Estimates','Owner-reported amounts, blank verified amounts and official DBI fees.'),('technical-approach.html','Technical approach','Tub-side service path, ceiling fallback and model-specific limits.'),('code-and-permit.html','Code & permit','Permit trigger, conditional exemptions, licensing, tenant entry and fees.'),('sources.html','Sources',f'{len(S)} source records with retrieval status and limitations.'),('flagged-for-review.html','Flagged for review',f'{len(F)} irregularities/open items; non-blocking but published.'),('verification.html','Verification','Audit checks, build report and publication record.')]
card_html='<div class="grid cards">'+''.join(f'<a class="card" href="{e(u)}"><h3>{e(t)}</h3><p>{e(d)}</p></a>' for u,t,d in cards)+'</div>'
snapshot=[
 ['License records rechecked',str(counts['cslb_records']),f"{counts['active']} current and active; Kenneth Asire #1027286 suspended; Portola identity unresolved",src_links(['CSLB-1027286','CSLB-SEARCH'])],
 ['Combined-classification leads',f"{counts['b_c36']} B + C-36",'Rapid Flow, Ace, We Do, Save-On-Interior, Ayoob & Peery, D G. Ask who performs restoration.',src_links(['CSLB-1115649','CSLB-829071','CSLB-1096552','CSLB-749536','CSLB-392967','CSLB-297604','CSLB-C9'])],
 ['Strongest adjacent technical case','Heise’s Ingleside','Company-published exterior-ceiling tub waste/overflow replacement; not confirmed as this storage-unit ceiling; restoration unverified.',src_links(['HEISE-INGLESIDE','CSLB-1089561'])],
 ['Owner estimates','3 supplied','Amounts are owner-reported; verified amounts blank; scopes differ.',src_links(['OWNER','CSLB-977638','CSLB-757796','CSLB-1024971'])],
 ['Permit determination','Open','SF.gov permit trigger and §104.2 conditional exemptions reviewed; exact job answer not supplied.',src_links(['SF-PERMIT','SF-CODE-104'])],
 ['Exact all-in-one acceptance','Unconfirmed','No provider contacted/booked; no combined ceiling-restoration quote on file.',src_links(['OWNER','REPO-BOARD','CSLB-CONTRACT','GH-PR'])]]
body=kpi_html+'<h2>Browse the dossier</h2>'+card_html+'<h2>Status snapshot</h2>'+table('Each row links the source it rests on; unconfirmed values remain blank.',['Item','Value','What it means','Sources'],snapshot)+'<div class="panel"><h3>Recommended inquiry order</h3><p>Start with Rapid Flow and Ace for combined-scope quotes; ask Heise’s for the adjacent ceiling-access reference and a named restoration party. Bernal Hill is a restoration partner, not a plumber. Requote the three existing estimates on one identical scope. <a href="decision-analysis.html">See the full ranking and cost limits.</a></p></div>'
(ROOT/'index.html').write_text(page('index.html','Bathtub wastewater overflow trip lever','A source-checked repair dashboard: compare combined plumbing-and-restoration leads, keep unlike estimates separate, and leave every unconfirmed value blank.',body),encoding='utf-8')
# Executive summary
summary_md=f"""# Executive summary — bathtub wastewater overflow trip lever

Reviewed {AS_OF}. San Francisco tenant-occupied unit. Based on linked official/company sources
and a neutral owner record; not a contractor booking or legal advice.

## Decision
Use a two-path scope: first ask a licensed plumber to identify the assembly and attempt the least
destructive tub-side adjustment/removal; if that fails, use below-ceiling access through the storage
unit only under a written combined contract naming the plumbing and drywall/restoration parties.
Do not assume a permit exemption: SF.gov requires a permit before cutting/replacing pipes, and
SF Plumbing Code §104.2 exemptions are conditional.

## Ranked inquiry shortlist (not confirmed hires)
1. Rapid Flow Plumbing & Rooter #1115649 — B + C-36; published simple-repair-to-renovation scope.
2. Ace Plumbing & Rooter #829071 — B + C-36; published HOA/property-manager coordination.
3. Heise’s Plumbing #1089561 — C-36; adjacent self-published exterior-ceiling case; no B/C-9 or restoration proof.
4. Bernal Hill Drywall #995163 — B + C-9 restoration partner; no C-36.
5. Expert #977638, Fast Response #1024971, Bay Area #757796 — requote existing estimates on one scope.
Atlas #868994 is a conditional review lead; We Do #1096552 and SF Building Group #1106131 are
larger-project fallbacks. No provider confirms this exact job, ceiling restoration, availability or price.

## Estimates
Owner-supplied amounts dated 2026-08-30: Expert $614 (replace waste and overflow), Bay Area $550
(lever/plug/spout with diverter, labor/materials), Fast Response $135 (repair/adjust plunger handle).
These are owner reports, not independently verified prices; verified amounts remain blank. Scopes
differ and none explicitly names ceiling opening/restoration. The $479 spread is arithmetic, not a
like-for-like market range. Official DBI Category 1P is $290, but category and quote inclusions are unconfirmed.

## Key controls
- Recheck legal entity, license, bond, insurance and complaint disclosures on signing day.
- Name who performs drywall/texture/paint; B + C-36 is not proof of drywall self-performance.
- Get the DBI permit determination and inspection-before-covering path in writing.
- Give affected tenants Civil Code §1954 notice; coordinate storage authority, shut-off and contents protection.
- Screen conditionally for lead/asbestos before disturbing finishes; building age/materials are unknown.
- Use a written itemized contract, lawful down payment, written change orders, leak/function test and photo record.

## Open items
Portola identity is unresolved. Yelp business pages remain blocked; ratings/counts are blank.
Heise’s case pages still embed a 404 block; “exterior ceiling” is not confirmed as the storage-unit ceiling.
Access-panel dimensions remain unverified. See Flagged for Review for all {len(F)} items.
"""
(ROOT/'overflow-integration'/'EXECUTIVE_SUMMARY.md').write_text(summary_md,encoding='utf-8')
(ROOT/'OVERFLOW_EXECUTIVE_SUMMARY.md').write_text(summary_md,encoding='utf-8')
exec_rows=[['Decision','Two-path scope: tub-side first; below-ceiling fallback only with named trades and written permit answer.',src_links(['OWNER','WATCO','SF-PERMIT','CSLB-C9'])],['Ranked inquiry shortlist','Rapid Flow → Ace → Heise’s; Bernal Hill restoration partner; requote existing estimates. No confirmed hire.',src_links(['CSLB-1115649','CSLB-829071','HEISE-INGLESIDE','CSLB-995163'])],['Estimates','Owner-reported $614/$550/$135; verified amounts blank; scopes differ.',src_links(['OWNER','CSLB-977638','CSLB-757796','CSLB-1024971'])],['Permit','DBI determination open; cutting/replacing pipes triggers permit guidance; exemptions conditional.',src_links(['SF-PERMIT','SF-CODE-104'])],['Tenant/site','Notice, storage authority, water shut-off, contents protection and conditional lead/asbestos screening.',src_links(['CIV-1954','EPA-RRP','EPA-ASBESTOS'])],['Evidence gap','No exact-job acceptance, booking, photos, model or combined restoration quote.',src_links(['OWNER','REPO-BOARD','CSLB-CONTRACT','GH-PR'])]]
body='<div class="panel"><h3>Bottom line</h3><p>Rapid Flow and Ace are the first combined-classification inquiries. Heise’s has the strongest adjacent self-published exterior-ceiling case but no B/C-9 or restoration proof; Bernal Hill is a restoration partner. No provider is confirmed for the exact all-in-one job.</p></div>'+table('Executive findings',['Topic','Finding','Sources'],exec_rows)+'<h2>Estimate comparison</h2>'+table('Owner-reported amounts are not verified prices.',['Provider','Supplied scope','Supplied amount','Verified amount','Sources'],[[e(x['provider']),e(x['scope_owner']),money(x['amount_owner']),blank(),src_links(x['source_ids'])] for x in E['rows']])+'<h2>Next steps</h2><ol class="tight"><li>Send one identical neutral scope to the shortlist; ask for the named restoration party, occupied-unit plan, permit path and current written price.</li><li>Confirm storage-unit authority and tenant notice before scheduling.</li><li>Collect photos/model/size and screen finishes before demolition.</li><li>Use a written contract with lawful payment terms, change orders, testing and cleanup.</li></ol><p><a href="OVERFLOW_EXECUTIVE_SUMMARY.md">Markdown executive summary</a></p>'
(ROOT/'executive-summary.html').write_text(page('executive-summary.html','Executive summary','Decision, shortlist, estimate comparison and the controls that must be settled before work.',body),encoding='utf-8')
# Requirements
rows=[]
for r in R:
 rows.append([e(r['id']),e(r['category']),e(r['requirement']),f"<strong>Basis:</strong> {e(r['basis'])}<br><strong>Acceptance:</strong> {e(r['acceptance_check'])}<br><span class='small'>Legacy mapping: {e(r['legacy_ids'])}</span>",pill(r['origin'],'ok' if r['origin']=='Official rule' else 'warn')+f"<br><span class='small'>{e(r['status'])}</span>",src_links(r['source_ids'],r['official_url'])])
body=f'<p>{len(R)} requirements deduplicated from the parallel registers. Owner requirements and proposed controls are not presented as official facts; official context links are provided for review.</p>'+table('Full requirement register',['ID','Category','Requirement','Basis / acceptance check','Origin / status','Sources'],rows,'requirements-table')
(ROOT/'requirements.html').write_text(page('requirements.html','Requirements','Full source-linked register with acceptance checks, origin labels and legacy mappings.',body),encoding='utf-8')
# Decision analysis
Pby={p['id']:p for p in P}
drows=[]
for d in D['rows']:
 p=Pby[d['provider_id']]
 drows.append([str(d['rank']),f"<strong>{e(p['name'])}</strong><br><span class='small'>CSLB {e(p['license'])} · {e(', '.join(p['classifications']))}</span>",e(d['decision']),e(d['reason']),e(d['cost']),e(d['gates']),src_links(d['source_ids'],p['official_url'])+('<br>'+link(p['website'],'Company site') if p['website'] else '')])
body='<div class="panel"><h3>How this ranking works</h3><p>'+e(D['method'])+'</p><p>No numeric performance score is invented. Verified prices are blank unless a source confirms them; owner-reported amounts are labeled. A higher rank means a better-supported inquiry path, not a guarantee of competence, availability or award.</p></div>'+table('Ranked inquiry order — evidence gates and costs',['Rank','Provider / license','Role','Reasoning','Cost evidence','Before award','Sources'],drows,'decision-table')+'<h2>Decision rules</h2><ul class="tight"><li>Exclude suspended or unresolved identities from the active inquiry order.</li><li>Do not treat B + C-36 as proof of drywall self-performance; name the restoration party.</li><li>Do not convert unlike owner estimates into a market range or price score.</li><li>Require one written scope with tub-side attempt, ceiling fallback, restoration, permit path, occupied-unit protections, testing and cleanup.</li><li>Recheck license/insurance and obtain DBI determination before signing or covering work.</li></ul>'
(ROOT/'decision-analysis.html').write_text(page('decision-analysis.html','Decision analysis','Transparent best-to-inquire ordering with source-checked reasoning, explicit cost limits and pre-award gates.',body),encoding='utf-8')
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
for p in short:
 srows.append([e(p['name']),e(p['group']),e(p['fit']),src_links(p['source_ids'],p['official_url'])])
vrows=[[e(v['provider']),e(v['platform']),e(v['observation']),blank(),blank(),pill('Unverified','unv'),e(v['limit']),src_links(v['source_ids'],v['official_url'])+'<br>'+link(v['review_url'],'Review lead')] for v in V]
body='<h2>Priority inquiry leads</h2>'+table('Editorial inquiry order, not a verified performance ranking. See Decision analysis for the full ranked method.',['Provider','Lead type','Why ask / what remains unconfirmed','Sources'],srows)+'<h2>Full provider register</h2><p>CSLB fields are point-in-time official records. Company service claims are self-descriptions. Exact-job acceptance, ceiling restoration and availability are unconfirmed for every provider.</p>'+table(f"{len(P)} identities: {counts['cslb_records']} checked CSLB records and one unresolved name.",['Provider / legal name','License / status','Classifications','Registered city / phone','Workers-comp record','Fit and limits','Sources'],prows,'providers-table')+'<h2>Review-platform observations</h2><p>Numeric ratings and review counts are blank because they were not verified. Search-index excerpts are leads, not directly retrieved reviews.</p>'+table('Unverified review leads',['Provider','Platform','Observation','Rating','Count','Status','Limits','Sources'],vrows)
(ROOT/'providers.html').write_text(page('providers.html','Providers','License-checked inquiry leads, restoration partners, estimate providers and unresolved identities.',body),encoding='utf-8')
# Estimates
erows=[[e(x['provider'])+f"<br><span class='mono small'>{e(x['license'])}</span>",e(x['scope_owner']),e(x['date']),money(x['amount_owner']),blank(),e(x['analysis']),pill(x['status'],'warn'),src_links(x['source_ids'],x['official_url'])] for x in E['rows']]
frows=[[e(f['item']),money(f['amount']),e(f['unit']),e(f['note']),src_links(f['source_ids'],f['official_url'])] for f in E['official_fees']]
body='<div class="panel"><h3>How to read the amounts</h3><p>Supplied amounts are owner-reported primary statements, not independently verified contractor prices. Verified amounts remain blank. The scopes differ, so the arithmetic spread is not a market range.</p></div>'+table('Owner-supplied estimates dated 2026-08-30',['Provider','Supplied scope','Supplied date','Supplied amount','Verified amount','Analysis','Status','Sources'],erows,'estimates-table')+'<h2>Official DBI fees (not project quotes)</h2>'+table('July 2026 Table 1A-C; category applicability unconfirmed.',['Item','Amount','Unit','Note','Source'],frows)+'<h2>Analysis</h2><ul class="tight">'+''.join(f'<li>{e(a)}</li>' for a in E['analysis'])+'</ul>'
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
body=f'<p>{len(S)} source records. “Direct” means the page/PDF was retrieved in this session; search excerpts, blocked pages and repository records are labeled. Non-official rows include an official cross-reference where available.</p>'+table('Source register',['ID','Source','Publisher / type','Retrieval','Supports','Limitations','Links'],srows,'sources-table')
(ROOT/'sources.html').write_text(page('sources.html','Sources','Every consulted source with retrieval status, support and limitations.',body),encoding='utf-8')
# Flags
frows=[[e(f['id']),pill(f['severity'],'bad' if f['severity']=='High' else 'warn' if f['severity']=='Medium' else 'neutral'),e(f['category']),f"<strong>{e(f['title'])}</strong><br>{e(f['detail'])}",e(f['action']),pill(f['status'],'ok' if f['status'].startswith('Resolved') else 'warn'),src_links(f['source_ids'],f['official_url'])] for f in F]
body=f'<p>{len(F)} flagged items. Open/unverified items do not block publication; they are published with source links and required follow-up. Resolved items record corrections made in this canonical rebuild.</p>'+table('Flagged for review',['ID','Severity','Category','Finding','Action','Status','Sources'],frows,'flags-table')
(ROOT/'flagged-for-review.html').write_text(page('flagged-for-review.html','Flagged for review','Irregularities, unconfirmed values and corrections, published with source links.',body),encoding='utf-8')
# Verification placeholder (updated by verifier/deploy record)
deploy_path=DATA/'deployment.json'
deploy=json.loads(deploy_path.read_text()) if deploy_path.exists() else {'status':'Pending final merge and live check','pr':'','merge_commit':'','pages_url':'https://karagemop466-tech.github.io/Korea8/','checked':''}
vrows=[['Canonical pages',f'{len(NAV)} root pages generated from overflow-integration/data',src_links(['REPO','GH-PAGES'])],['Provider records',f"{counts['cslb_records']} CSLB records directly rechecked; {counts['unresolved']} unresolved identity left blank",src_links(['CSLB-SEARCH','CSLB-1027286'])],['Requirements',f'{len(R)} rows with official context links and legacy mappings',src_links(['REPO','OWNER','GH-PAGES','CSLB-CONTRACT'])],['Sources',f'{len(S)} records with retrieval status and limitations',src_links(['REPO','GH-PAGES'])],['Flags',f'{len(F)} published irregularities/open items',src_links(['REPO','GH-PAGES'])],['Deployment',e(deploy['status'])+(f"<br>PR: {link(deploy['pr'])}" if deploy.get('pr') else '')+(f"<br>Merge commit: <span class='mono'>{e(deploy['merge_commit'])}</span>" if deploy.get('merge_commit') else '')+(f"<br>Checked: {e(deploy['checked'])}" if deploy.get('checked') else ''),src_links(['PAGES-API','REPO-BOARD','GH-PAGES','GH-PR'])]]
body='<p>The verifier checks local links/anchors, row-source coverage, CSLB license-link parity, blank unverified fields, HTML balance and neutral public wording. Build/test reports are written to <code>overflow-integration/</code>.</p>'+table('Verification summary',['Check area','Result','Sources'],vrows)+'<p><a href="overflow-integration/REPO_AUDIT.md">Repository audit</a> · <a href="overflow-integration/build-report.json">Build report</a> · <a href="overflow-integration/verification-report.json">Verification report</a></p>'
(ROOT/'verification.html').write_text(page('verification.html','Verification','Audit, build and publication checks for the canonical dashboard.',body),encoding='utf-8')
# CSS
css='''
:root{--bg:#f6f8fb;--card:#fff;--ink:#17233b;--muted:#5b6b84;--line:#dfe6f0;--accent:#0f6b78;--accent2:#123c69;--warn:#8a5a00;--bad:#a12626;--ok:#176b3a}*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}a{color:var(--accent2)}a:hover{color:var(--accent)}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}.skip{position:absolute;left:-9999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:10}.topbar{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}.topbar-inner{display:flex;gap:18px;align-items:center;justify-content:space-between;padding-top:12px;padding-bottom:12px;flex-wrap:wrap}.brand{font-weight:800;text-decoration:none;color:var(--accent2);white-space:nowrap}.nav{display:flex;gap:6px;flex-wrap:wrap}.nav a{padding:6px 9px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:.9rem}.nav a.active,.nav a:hover{background:#e8f2f4;color:var(--accent)}.hero{padding:34px 0 18px}.eyebrow{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:.78rem;margin:0 0 8px}h1{font-size:clamp(1.7rem,3vw,2.5rem);line-height:1.15;margin:0 0 12px}h2{margin:30px 0 12px;font-size:1.35rem}h3{margin:0 0 8px}.lede{font-size:1.08rem;color:var(--muted);max-width:850px;margin:0}.grid{display:grid;gap:14px}.kpis{grid-template-columns:repeat(auto-fit,minmax(210px,1fr));margin:18px 0}.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}.kpi .n{display:block;font-size:2rem;font-weight:800;color:var(--accent2)}.kpi .l{display:block;font-weight:700}.kpi .s{display:block;color:var(--muted);font-size:.85rem;margin-top:6px}.cards{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;text-decoration:none;color:inherit}.card:hover{border-color:var(--accent);box-shadow:0 4px 14px #123c6912}.card p{margin:0;color:var(--muted);font-size:.92rem}.panel{background:#eef6f7;border:1px solid #cfe3e6;border-radius:14px;padding:16px;margin:18px 0}.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px;margin:12px 0}table{border-collapse:collapse;width:100%;min-width:760px;font-size:.92rem}caption{text-align:left;font-weight:700;padding:12px 14px;color:var(--accent2);border-bottom:1px solid var(--line)}th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}th{background:#f0f4f9;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}tr:last-child td{border-bottom:0}.sources{font-size:.82rem;overflow-wrap:anywhere}.small{font-size:.82rem;color:var(--muted)}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.pill{display:inline-block;border-radius:999px;padding:2px 8px;font-size:.75rem;font-weight:700;background:#eef1f6;color:var(--muted);margin:2px 2px 2px 0}.pill.ok{background:#e5f4ea;color:var(--ok)}.pill.warn{background:#fff3d9;color:var(--warn)}.pill.bad{background:#fde7e7;color:var(--bad)}.pill.unv{background:#f0ecfa;color:#5b3fa2}.blank{display:inline-block;min-width:1.2em;border-bottom:1px dotted var(--muted)}.tight{margin:8px 0;padding-left:22px}.tight li{margin:6px 0}.footer{margin:36px 0 24px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}@media(max-width:700px){.topbar-inner{align-items:flex-start}.nav a{font-size:.82rem;padding:5px 7px}table{min-width:640px}}
'''
(ROOT/'style.css').write_text(css.strip()+'\n',encoding='utf-8')
report={'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'scripts/build_overflow_site.py','data':'overflow-integration/data','pages':[u for u,_ in NAV],'counts':{'providers':len(P),'cslb_records':len([p for p in P if p['license']]),'active':len(active),'suspended':len(susp),'unresolved':len(unresolved),'b_c36':len(bc),'c9':len(c9),'requirements':len(R),'estimates':len(E['rows']),'technical':len(T),'compliance':len(C),'reviews':len(V),'sources':len(S),'flags':len(F),'decision_rows':len(D['rows'])},'preserved':['redirect stubs','archive/','docs/ GEMS','src/','vendor/','registry/','evidence/','downloads/','submissions/'],'owner_amounts_published_as_unverified':True}
(ROOT/'overflow-integration'/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(ROOT/'site-data'/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['counts'],indent=2))

#!/usr/bin/env python3
"""Build a self-contained, source-linked static dashboard from reviewed JSON."""
from pathlib import Path
import json, html, shutil, csv, io
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/'data'
OUT=HERE/'site'
D={p.stem:json.loads(p.read_text()) for p in DATA.glob('*.json')}
S={r['id']:r for r in D['sources']['rows']}
E=html.escape
NAV=[('index.html','Overview'),('executive-summary.html','Executive summary'),('requirements.html','Requirements'),('estimates.html','Estimates'),('providers.html','Providers'),('technical.html','Technical approach'),('analysis.html','Analysis'),('sources.html','Sources'),('flagged-for-review.html','Flagged for review'),('repository.html','Repository audit'),('verification.html','Verification')]
def a(url,label,cls='source'):
 return f'<a class="{cls}" href="{E(url,quote=True)}" target="_blank" rel="noopener">{E(label)}<span aria-hidden="true"> ↗</span></a>'
def sources(ids):
 return '<div class="sources">'+''.join(a(S[i]['url'],i) for i in ids)+'</div>'
def flags(ids):
 return ' '.join(f'<a class="flag" href="flagged-for-review.html#flags-table-{E(i)}">{E(i)}</a>' for i in ids)
def blank(): return '<span class="blank" aria-label="Unverified value left blank"></span>'
def cell(v): return E(str(v)) if v not in ['',None] else blank()
def table(headers,rows,id='',cls=''):
 head=''.join(f'<th scope="col">{E(h)}</th>' for h in headers)
 body=''.join('<tr' +(f' id="{E((id+"-" if id else "")+r[0])}"' if r and isinstance(r[0],str) and r[0].startswith(('P-','R-','E-','T-','A-','F-','S-','B-','CSLB-','WEB-','RV-','CA-','WATCO-','IAPMO-','SF-','GH-')) else '')+'>'+''.join(f'<td>{c}</td>' for c in r[1:])+'</tr>' for r in rows)
 return f'<div class="table-wrap"><table id="{E(id)}" class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
def page(name,title,lead,body):
 links=''.join(f'<a href="{h}"'+(' aria-current="page"' if h==name else '')+f'>{E(l)}</a>' for h,l in NAV)
 doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(lead)}"><title>{E(title)} · Overflow Trip Lever</title><link rel="stylesheet" href="assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><div class="shell"><aside class="sidebar"><a class="brand" href="index.html"><span class="brand-icon">⌁</span><span>Overflow<span class="brand-sub">Repair research desk</span></span></a><div class="nav-label">PROJECT</div><nav aria-label="Main navigation">{links}</nav><div class="sidebar-foot"><span class="dot"></span> Source-linked research<br><small>Checked 7 Nov 2026</small></div></aside><div class="content"><header class="topbar"><span>San Francisco · Bathtub waste & overflow</span><span class="status">Research · not a booking</span></header><main id="main"><div class="page-head"><div class="eyebrow">REPAIR COORDINATION</div><h1>{E(title)}</h1><p class="lead">{E(lead)}</p></div>{body}</main><footer>Every data row includes a source link. Blank cells are intentionally unverified.<br><a href="sources.html">Source register</a> · <a href="flagged-for-review.html">Review flags</a> · <a href="verification.html">Build evidence</a></footer></div></div><script src="assets/app.js"></script></body></html>'''
 (OUT/name).write_text(doc)
def card(num,label,note=''):return f'<div class="metric"><strong>{E(str(num))}</strong><span>{E(label)}</span><small>{E(note)}</small></div>'
def note(text,kind=''):return f'<div class="notice {kind}">{text}</div>'
def sec(title,body,extra=''):return f'<section class="section"><div class="section-head"><h2>{E(title)}</h2>{extra}</div>{body}</section>'
OUT.mkdir(exist_ok=True); (OUT/'assets').mkdir(exist_ok=True); (OUT/'data').mkdir(exist_ok=True)
for p in DATA.glob('*.json'):shutil.copyfile(p,OUT/'data'/p.name)
prov=D['providers']['rows']; active=[p for p in prov if p['status']=='This license is current and active.']
bc=[p for p in active if any(x.startswith('B - ') for x in p['classifications']) and any(x.startswith('C36') for x in p['classifications'])]
counts={'provider_rows':len(prov),'numeric_licenses':sum(bool(p['license']) for p in prov),'active':len(active),'suspended':sum('suspension' in p['status'].lower() for p in prov),'b_c36':len(bc),'requirements':len(D['requirements']['rows']),'estimates':len(D['estimates']['rows']),'technical':len(D['technical']['rows']),'findings':len(D['findings']['rows']),'flags':len(D['flags']['rows']),'sources':len(S)}
(OUT/'data'/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
# Overview
body='<div class="metrics">'+card(counts['requirements'],'requirements captured','Scope, access, licensing and delivery')+card(counts['numeric_licenses'],'license records checked','Official CSLB detail pages')+card(counts['b_c36'],'active B + C-36 records','Combined-scope screening group')+card(counts['estimates'],'quote scopes received','Amounts blank pending confirmation')+card(counts['flags'],'items flagged','Visible limitations, not hidden caveats')+'</div>'
body+=note('<strong>Recommended next step:</strong> screen Heise’s Plumbing for the documented ceiling-access plumbing work, and Rapid Flow / Ace for a single plumbing-plus-restoration contract. Bernal Hill Drywall is a verified C-9 + B build-back specialist, not a plumber. No provider has accepted this exact job.')
rows=[]
for lic,why in [('1089561','Published Ingleside tub W&O job used exterior-ceiling access'),('1115649','B + C-36; advertises one-call plumbing and general contracting'),('829071','B + C-36; advertises HOA/property-manager coordination'),('995163','C-9 + B; small drywall repairs and texture matching')]:
 p=next(x for x in prov if x['license']==lic); rows.append([p['id'],f'<strong>{E(p["display_name"])}</strong><br><small>{E(p["role"])}</small>',cell(lic),E(why),sources(['CSLB-'+lic, 'WEB-Heise-Ingleside'] if lic=='1089561' else p['source_ids'][:2])+flags(p['flags'])])
body+=sec('Priority screening candidates',table(['ID','Provider','CSLB #','Evidence-based reason','Sources / flags'],rows,'overview-providers'))
body+=sec('Decision path','<div class="steps"><article><span>01</span><h3>Identify before forcing</h3><p>Confirm the overflow plate, linkage family and symptoms. Ask for a model-specific tub-side assessment first.</p></article><article><span>02</span><h3>Plan the fallback</h3><p>If ceiling access is needed, agree the opening, storage protection, plumbing repair and finish restoration in one written scope.</p></article><article><span>03</span><h3>Compare like for like</h3><p>Use identical specifications for every bid. Confirm the actual licensed performers, insurance, exclusions and acceptance tests.</p></article></div>')
body+=sec('Read the full brief','<div class="link-grid">'+''.join(f'<a href="{h}"><strong>{E(l)}</strong><span>Open category →</span></a>' for h,l in NAV[1:])+'</div>')
page('index.html','Bathtub overflow trip lever','A source-checked repair brief for a concealed, stuck trip-lever mechanism in a tenant-occupied San Francisco home.',body)
# Executive summary
body=note('<strong>Bottom line:</strong> the safest procurement path is a written, model-specific diagnosis followed by a single accountable scope for any required ceiling access and restoration. The research identifies candidates; it does not guarantee extraction, price or availability.')
rows=[['A','Problem','Owner reports a stuck trip-lever component in concealed tub drainage; more than five prior plumbers reportedly could not remove it safely from above.',sources(['WATCO-TL','CSLB-Bids'])+flags(['F-01'])],['B','Preferred route','Ask for non-destructive tub-side assessment. Manufacturer instructions show linkage service through the overflow on specified models, but the actual model is unknown.',sources(['WATCO-TL'])+flags(['F-01','F-10'])],['C','Fallback route','Owner reports possible access from the storage-unit ceiling below. Heise’s published Ingleside job is the closest local access analogy found.',sources(['WEB-Heise-Ingleside'])+flags(['F-10'])],['D','Contract structure','Require one written scope naming the C-36 plumbing performer and the drywall/restoration performer. B + C-36 candidates are a screening group, not confirmed acceptance.',sources(['CSLB-B','CSLB-C36','CSLB-C9'])+flags(['F-03'])],['E','Cost comparison','Three different quote scopes were reported. No provider-issued amount or combined ceiling/restoration quote is confirmed; amount cells remain blank.',sources(['CSLB-Bids'])+flags(['F-02'])],['F','Occupied unit','Coordinate repair entry with the tenant and include protection, cleanup, debris removal and finish matching in the contract.',sources(['CA-1954','CSLB-Contracts'])+flags(['F-03'])],['G','Risk controls','Recheck licenses and insurance, review adverse statuses, request job-specific references and test sealing/drainage before sign-off.',sources(['CSLB-Bids','WATCO-TL'])+flags(['F-06','F-08','F-22'])]]
body+=sec('Important details',table(['#','Topic','Executive finding','Official / primary sources'],rows,'summary-table'))
body+=sec('What is not yet known',table(['Item','Value','Status','Source'],[['Exact failed component',blank(),'Unverified · no inspection/photos',sources(['WATCO-TL'])],['Combined contract price',blank(),'Unverified · no accepted quote',sources(['CSLB-Bids'])],['Availability / schedule',blank(),'Unverified · no provider contact',sources(['CSLB-Contracts'])],['Drywall opening dimensions',blank(),'Unverified · contractor determination needed',sources(['IAPMO-Access'])]],'summary-unknowns'))
page('executive-summary.html','Executive summary','The decision, evidence, shortlist and unresolved items in one place.',body)
# Requirements
rows=[]
for r in D['requirements']['rows']:rows.append([r['id'],cell(r['category']),cell(r['requirement']),cell(r['basis']),cell(r['verification'])+(' '+flags(r['flags']) if r['flags'] else ''),sources(r['source_ids'])])
body=note('Requirements are labeled by basis: owner request, official guidance or recommended safeguard. An official link supports the cited rule; it does not independently verify the owner’s description of the tub.')+sec('Full requirements register',table(['ID','Category','Requirement','Basis','Verification / limit','Source'],rows,'requirements-table'))
page('requirements.html','Requirements','A complete, categorized register of the repair, procurement, occupancy and publication requirements.',body)
# Estimates
rows=[]
for r in D['estimates']['rows']:rows.append([r['id'],cell(r['provider_as_quoted']),blank()+flags(['F-02']),cell(r['scope_owner_reported'])+'<br><small>Owner-reported wording; not a confirmed contract scope.</small>',blank(),blank(),sources(r['source_ids'])])
body=note('<strong>Amount policy:</strong> the supplied amounts are not repeated as verified prices. No provider-issued document or official published price was available, so amount, date and inclusion cells are blank and flagged. The CSLB source identifies a candidate business; it does not substantiate its quote.','warn')
body+=sec('Received quote scopes',table(['ID','Provider as quoted','Amount (USD)','Reported scope','Ceiling + restoration included?','Quote document confirmed?','Sources'],rows,'estimates-table'))
body+=sec('Unconfirmed commercial terms',table(['ID','Labor','Materials','Ceiling access','Drywall restoration','Paint','Dispatch fee','Valid until','Source'],[[r['id']]+[blank()+flags(['F-02']) for _ in range(7)]+[sources(r['source_ids'])] for r in D['estimates']['rows']],'estimate-terms'))
body+=sec('Line-by-line analysis',table(['ID','Comparison finding','Recommended clarification','Source'],[[r['id'],cell(r['analysis']),'Use one written specification covering diagnosis, access, parts, labor, protection, drywall, texture/paint, cleanup and exclusions.',sources(['CSLB-Bids','CSLB-Contracts'])] for r in D['estimates']['rows']],'estimate-analysis'))
page('estimates.html','Estimates & scope comparison','Three reported scopes, kept separate from verified prices and confirmed inclusions.',body)
# Providers
rows=[]
for p in prov:
 cls='<br>'.join(E(x) for x in p['classifications']) if p['classifications'] else blank()
 status=cell(p['status'])+('<br><span class="badge warn">'+E(p['additional_status'])+'</span>' if p['additional_status'] else '')
 rows.append([p['id'],f'<strong>{E(p["display_name"])}</strong><br><small>{E(p["legal_name"])}</small>',cell(p['license'])+'<br>'+sources(['CSLB-'+p['license']] if p['license'] else ['CSLB-Bids']),cls,status,cell(p['expire_date']),cell(p['phone']),cell(p['address']),flags(p['flags'])])
body='<div class="metrics">'+card(counts['active'],'active records','Point-in-time CSLB check')+card(counts['b_c36'],'B + C-36','Conditional multi-trade authority')+card(1,'C-9 + B specialist','Bernal Hill Drywall')+card(1,'suspended record','Excluded from active shortlist')+'</div>'
body+=note('License verification is not a workmanship guarantee. Company service claims are labeled as advertised; exact-job acceptance, current price, availability and review figures remain blank. Recheck the official record before signing.')
body+=sec('License and identity register', '<div class="toolbar"><label>Filter providers <input id="provider-filter" type="search" placeholder="Name, license, classification…"></label><span id="filter-count"></span></div>'+table(['ID','Business / legal name','License / official source','Classifications','Official status','Expiry','Business phone','Address of record','Flags'],rows,'providers-table'))
details=[]
for p in prov:
 links=sources(p['source_ids'])
 details.append([p['id'],cell(p['role']),cell(p['fit_evidence']),cell(p['workers_comp']),blank() if not p['review_url'] else a(p['review_url'],'Review discovery ↗'),blank(),links])
body+=sec('Fit, insurance and commercial unknowns',table(['ID','Screening role','Evidence / boundary','Workers-comp record','Review link','Accepted combined price','Sources'],details,'provider-fit'))
page('providers.html','Provider shortlist','Official license records, service evidence and explicit screening boundaries.',body)
# Technical
rows=[[r['id'],cell(r['category']),cell(r['statement']),cell(r['interpretation'])+' '+flags(r['flags']),sources(r['source_ids'])] for r in D['technical']['rows']]
body=note('This is procurement and technical background, not a repair instruction for an unidentified assembly. Do not force a seized linkage or apply another manufacturer’s tolerances to the actual tub.')+sec('Manufacturer, access and licensing findings',table(['ID','Category','Source-backed fact','Application / limit','Sources'],rows,'technical-table'))
page('technical.html','Technical approach','What the manufacturer and local job evidence support — and what they do not.',body)
# Analysis
rows=[[r['id'],cell(r['topic']),cell(r['finding']),cell(r['recommendation'])+' '+flags(r['flags']),sources(r['source_ids'])] for r in D['findings']['rows']]
page('analysis.html','Analysis & recommendations','Evidence-ranked screening advice, with no inferred price or booking claim.',sec('Findings and next actions',table(['ID','Topic','Finding','Recommendation','Sources'],rows,'analysis-table')))
# Sources
rows=[]
for r in S.values():
 badge='<span class="badge ok">Retrieved</span>' if r['retrieval_status']=='retrieved' else '<span class="badge warn">'+E(r['retrieval_status'])+'</span>'
 rows.append([r['id'],cell(r['title']),cell(r['publisher'])+'<br><small>'+E(r['kind'])+'</small>',a(r['url'],'Open source ↗'),badge+'<br><small>'+E(r['method'])+'</small>',cell(r['checked_utc'])])
page('sources.html','Source register','Official regulators, statutes, manufacturer instructions, company-published evidence and review-discovery links.',note('Government and manufacturer sources are distinguished from company claims and review platforms. Blocked or search-only sources never verify a numeric value.')+sec('All sources',table(['ID','Title','Publisher / type','Link','Retrieval','Checked'],rows,'sources-table')))
# Flags
rows=[[r['id'],cell(r['title']),cell(r['detail']),cell(r['action']),sources(r['source_ids'])] for r in D['flags']['rows']]
page('flagged-for-review.html','Flagged for review','Unverified values, source limitations and irregularities remain visible after publication.',note('These items do not block publication. They identify what must not be treated as confirmed, and what to review before contracting.','warn')+sec('Open review items',table(['ID','Issue','Evidence / irregularity','Treatment / next check','Sources'],rows,'flags-table')))
# Repository audit
inv=json.loads((HERE/'repository'/'inventory.json').read_text())
body='<div class="metrics">'+card(inv['files'],'tracked files inventoried','Baseline includes unrelated research')+card(inv['text_files'],'text files scanned','UTF-8 / JSON / Python checks')+card(inv['text_lines'],'text lines scanned','Structural, not scientific validation')+card(inv['issue_files'],'files with audit flags','Legacy unsupported amounts')+'</div>'
body+=note('The repository mixes an unrelated DOE GEMS project with multiple plumbing drafts. This audit preserves those artifacts and revalidates the plumbing evidence; it does not claim to reproduce geothermal experiments.')
rows=[]
for r in inv['rows']:
 if r['domain']=='current session':continue
 rows.append([str(len(rows)+1),a(r['source_url'],r['path']),cell(r['domain']),cell(r['check']),cell(r['lines']),flags(['F-05','F-22']) if not r['issues'] else flags(['F-02','F-05'])])
body+=sec('Tracked-file inventory',table(['#','File / official repository link','Domain','Structural check','Lines','Review'],rows,'inventory-table'))
page('repository.html','Repository audit','Line-by-line structural/provenance review with official repository links.',body)
# Verification placeholder updated by checker
page('verification.html','Verification & publication','Build gates, source discipline and the final deployment record.',note('Verification is running. The final report will replace this notice.')+sec('Checks','<p>See <a href="data/counts.json">computed dataset counts</a> and the source register.</p>'))
# Exec summary markdown
md='''# Executive summary — bathtub overflow trip lever

**Checked:** 2026-11-07. **Status:** source-checked screening brief; no booking or accepted quote.

## Important details
- Owner reports a stuck trip-lever component in concealed San Francisco tub drainage, with a tenant-occupied unit and possible storage-unit ceiling access below. This condition is not independently inspected.
- Prefer a model-specific, non-destructive tub-side assessment. Watco’s instructions demonstrate overflow-opening linkage service on specified families; they do not establish feasibility for this unknown assembly.
- Heise’s Plumbing publishes an Ingleside tub waste-and-overflow replacement using exterior-ceiling access. This is the closest local job analogy found, but drywall restoration and exact seized-part acceptance are not established.
- Screen Rapid Flow and Ace for a single plumbing-plus-restoration contract; both show active B + C-36 classifications. We Do Construction and Save-On-Interior are additional B + C-36 records. Bernal Hill Drywall shows C-9 + B and is a build-back specialist, not a C-36 plumber.
- The three reported quote scopes are not like-for-like. Amounts, dates and inclusion fields remain blank because no provider-issued confirmation was available. Require identical written specifications and explicit ceiling/finish/cleanup inclusions.
- Coordinate lawful repair entry, protection of belongings, dust containment, cleanup and acceptance testing. Recheck licenses, insurance and adverse statuses before contracting.

## Evidence boundaries
No photos, physical inspection, provider contact, availability confirmation or combined price were available. Yelp numeric review data is not published. The IAPMO access-panel spotlight is not a current local code determination. Suspended/adverse-status candidates are separately flagged.

## Official / primary links
'''+ '\n'.join('- '+S[i]['title']+': '+S[i]['url'] for i in ['CSLB-Bids','CSLB-B','CSLB-C36','CSLB-C9','CA-1954','WATCO-TL','WEB-Heise-Ingleside','CSLB-1115649','CSLB-829071','CSLB-995163','IAPMO-Access'])+'\n'
(HERE/'EXECUTIVE_SUMMARY.md').write_text(md)
print(json.dumps(counts,indent=2))

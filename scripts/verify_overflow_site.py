#!/usr/bin/env python3
"""Independent checks for the canonical overflow dashboard (stdlib only)."""
from __future__ import annotations
import json,pathlib,re,sys,datetime,html
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parent.parent
DATA=ROOT/'overflow-integration'/'data'
PAGES=['index.html','executive-summary.html','decision-analysis.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
checks=[]
def check(name,ok,detail=''):
 checks.append({'check':name,'ok':bool(ok),'detail':detail})
def load(n): return json.loads((DATA/n).read_text())
class Parse(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.ids=set();self.stack=[];self.errors=[];self.tables={};self.cur=None;self.inbody=False;self.row=None;self.rows=[];self.cell=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag not in {'meta','link','br','img','hr','input','source','area','base','col','embed','param','track','wbr'}: self.stack.append(tag)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
  if tag=='table':self.cur=a.get('id','');self.tables.setdefault(self.cur,[]);self.inbody=False
  elif tag=='tbody':self.inbody=True
  elif tag=='tr' and self.inbody:self.row=[]
  elif tag in ('td','th') and self.row is not None:self.cell=[]
 def handle_data(self,d):
  if self.cell is not None:self.cell.append(d)
 def handle_endtag(self,tag):
  if tag in {'meta','link','br','img','hr','input','source','area','base','col','embed','param','track','wbr'}:return
  if self.stack and self.stack[-1]==tag:self.stack.pop()
  else:self.errors.append(f'mismatch </{tag}>')
  if tag in ('td','th') and self.cell is not None:
   self.row.append(''.join(self.cell));self.cell=None
  elif tag=='tr' and self.row is not None:
   self.tables[self.cur].append(self.row);self.rows.append(self.row);self.row=None
  elif tag=='tbody':self.inbody=False
  elif tag=='table':self.cur=None
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.ext=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:
    u=a[k]
    if u.startswith('http'):self.ext.append(u)
    else:self.links.append(u)
def main():
 texts={p:(ROOT/p).read_text() for p in PAGES if (ROOT/p).exists()}
 check('all canonical pages present',len(texts)==len(PAGES),f'{len(texts)}/{len(PAGES)}')
 parsed={p:Parse() for p in texts}
 for p,t in texts.items():parsed[p].feed(t)
 check('HTML tag balance',all(not x.errors and not x.stack for x in parsed.values()),'; '.join(f'{p}:{x.errors or x.stack}' for p,x in parsed.items() if x.errors or x.stack))
 # nav completeness
 nav_ok=all(all(u in t for u,_ in [(p,p) for p in PAGES]) for t in texts.values())
 check('every page links every canonical page',nav_ok)
 # internal links/anchors in canonical pages
 broken=[]
 for p,t in texts.items():
  l=Links();l.feed(t)
  for u in l.links:
   if u.startswith(('mailto:','tel:','data:','#')):
    if u.startswith('#') and u[1:] and u[1:] not in parsed[p].ids:broken.append(f'{p}:{u}')
    continue
   path=u.split('#')[0]
   if not path:continue
   target=(ROOT/path).resolve()
   if not target.exists():broken.append(f'{p}:{u}')
   elif '#' in u:
    frag=u.split('#')[1]
    if target.suffix=='.html':
     q=Links();q.feed(target.read_text());
     if frag not in q.ids:broken.append(f'{p}:{u}')
 check('no broken internal links/anchors in canonical pages',not broken,'; '.join(broken[:20]))
 # row-source coverage: every tbody row must link a registered official-primary source.
 # Review platforms and repository records alone do not satisfy the official-source rule.
 srcs_for_rows={s['id']:s for s in load('sources.json')['rows']}
 official_ids={i for i,s in srcs_for_rows.items() if s['kind'] in {'official-government','official-company','official-manufacturer','official-code-publisher','official-tool'}}
 official_urls={srcs_for_rows[i]['url'] for i in official_ids}
 missing=[];rowcount=0
 for p,t in texts.items():
  for tbl in re.findall(r'<tbody>(.*?)</tbody>',t,re.S):
   for tr in re.findall(r'<tr>(.*?)</tr>',tbl,re.S):
    rowcount+=1
    hrefs=[html.unescape(u) for u in re.findall(r'href="([^"]+)"',tr)]
    if not any(u in official_urls for u in hrefs):missing.append(f'{p}:{tr[:80]}')
 check('every canonical table row has a registered official-primary source link',not missing,f'{rowcount} rows; offenders: '+'; '.join(missing[:10]))
 # data invariants
 prov=load('providers.json')['rows'];req=load('requirements.json')['rows'];est=load('estimates.json');rev=load('reviews.json')['rows'];flags=load('flags.json')['rows'];srcs={s['id']:s for s in load('sources.json')['rows']}
 check('provider count parity',len(parsed['providers.html'].tables.get('providers-table',[]))==len(prov),f"{len(parsed['providers.html'].tables.get('providers-table',[]))}/{len(prov)}")
 check('requirement count parity',len(parsed['requirements.html'].tables.get('requirements-table',[]))==len(req))
 check('estimate count parity',len(parsed['estimates.html'].tables.get('estimates-table',[]))==len(est['rows']))
 check('source count parity',len(parsed['sources.html'].tables.get('sources-table',[]))==len(srcs))
 check('flag count parity',len(parsed['flagged-for-review.html'].tables.get('flags-table',[]))==len(flags))
 bad=[]
 for p in prov:
  if p['license']:
   u=f"https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={p['license']}"
   if u not in texts['providers.html']:bad.append(p['license'])
  for i in p['source_ids']:
   if i not in srcs:bad.append(f"{p['id']}:{i}")
 check('CSLB link parity and provider source ids',not bad,'; '.join(bad))
 unresolved=[p for p in prov if not p['license']]
 check('unresolved identity fields blank',all(not p['license'] and not p['phone'] and not p['expiry'] and not p['status'] for p in unresolved),f'{len(unresolved)} unresolved')
 check('verified estimate amounts blank',all(x['amount_verified'] is None for x in est['rows']))
 check('review ratings/counts blank',all(v['rating'] is None and v['review_count'] is None for v in rev))
 check('owner amounts published as owner-reported',all(f"${x['amount_owner']}" in texts['estimates.html'] for x in est['rows']) and 'Owner-reported' in texts['estimates.html'])
 check('no numeric star ratings in canonical pages',not re.search(r'\d(?:\.\d)?\s*(?:stars|out of 5)',' '.join(texts.values()),re.I))
 # all source ids resolve and official urls are https
 bad=[]
 for name in ['requirements.json','technical.json','compliance.json','reviews.json','flags.json']:
  for r in load(name)['rows']:
   for i in r.get('source_ids',[]):
    if i not in srcs:bad.append(f'{name}:{r.get("id")}:{i}')
   if r.get('official_url') and not r['official_url'].startswith('https://'):bad.append(f'{name}:{r.get("id")}:official_url')
 check('all row source ids resolve and official urls are https',not bad,'; '.join(bad[:20]))
 # suspended not in priority shortlist table
 short=parsed['providers.html'].tables.get('',[])
 # first unnamed table is priority leads; ensure suspended name absent from its rows
 susp=[p['name'] for p in prov if p['status']=='Suspended']
 first_table=re.search(r'<tbody>(.*?)</tbody>',texts['providers.html'],re.S).group(1)
 check('suspended provider excluded from priority leads',all(n not in first_table for n in susp))
 # neutral public wording / no conflict markers / no placeholder literals
 banned=['<<<<<<<','>>>>>>>','=======','TODO','TBD','Lorem ipsum']
 sys.path.insert(0,str(ROOT/'scripts'));import wording_guard
 hits=[(p,w) for p,t in texts.items() for w in banned if w in t]
 hits+=[(p,f'wording:{d}') for p,t in texts.items() for _,d in wording_guard.scan_bytes(t.encode('utf-8'))]
 check('neutral public wording and no placeholders/conflict markers',not hits,str(hits))
 check('no None/nan literals in canonical pages',not re.search(r'>\s*(?:None|nan|NaN)\s*<',' '.join(texts.values())))
 # ranking is editorial, active-only in the hiring order, source-linked and weight-normalized
 rk=load('ranking.json');prov_by_id={p['id']:p for p in prov}
 check('ranking table parity',len(parsed['decision-analysis.html'].tables.get('ranking-table',[]))==len(rk['ranked']))
 check('ranking hiring order excludes suspended/unresolved identities',all(prov_by_id[r['provider_id']]['status']=='Current and active' for r in rk['ranked']+[rk['partner']]))
 check('ranking weights sum to one',abs(sum(w['weight'] for w in rk['weights'])-1.0)<1e-9)
 check('ranking rows have source ids and official urls',all(r.get('source_ids') and r.get('official_url','').startswith('https://') for r in rk['ranked']+[rk['partner']]+rk['not_recommended']))
 check('source kinds explicit',all(s.get('kind') for s in srcs.values()))
 # build report parity
 br=json.loads((ROOT/'overflow-integration'/'build-report.json').read_text())
 check('build report counts match data',br['counts']['providers']==len(prov) and br['counts']['requirements']==len(req) and br['counts']['flags']==len(flags) and br['counts']['sources']==len(srcs) and br['counts']['ranking']==len(rk['ranked']) and br['counts']['ranking_held']==len(rk['not_recommended']))
 # repo-wide tracked HTML internal link crawl (canonical + preserved stubs/docs)
 import subprocess
 tracked=subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT,text=True).splitlines()
 broken2=[];count=0
 for f in tracked:
  path=ROOT/f
  try:t=path.read_text()
  except:continue
  l=Links();l.feed(t)
  for u in l.links:
   if u.startswith(('mailto:','tel:','data:','#')):continue
   count+=1;target=(path.parent/u.split('#')[0]).resolve()
   if not target.exists():broken2.append(f'{f}:{u}')
 check('no broken internal links across tracked HTML',not broken2,f'{count} links; offenders: '+'; '.join(broken2[:20]))
 ok=all(c['ok'] for c in checks)
 report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS' if ok else 'FAIL','checks_run':len(checks),'checks_passed':sum(c['ok'] for c in checks),'checks_failed':sum(not c['ok'] for c in checks),'canonical_rows_checked':rowcount,'tracked_html_files':len(tracked),'checks':checks}
 (ROOT/'overflow-integration'/'verification-report.json').write_text(json.dumps(report,indent=2)+'\n')
 (ROOT/'site-data'/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 for c in checks:print(('PASS' if c['ok'] else 'FAIL'),c['check'],'—',c['detail'])
 print(f"\n{report['checks_passed']}/{report['checks_run']} checks passed — {report['result']}")
 return 0 if ok else 1
if __name__=='__main__':sys.exit(main())

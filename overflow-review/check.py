#!/usr/bin/env python3
"""Fail-closed data, source, HTML, link, script and responsive-layout checks."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; SITE=HERE/'site'; DATA=HERE/'data'
checks=[]; failures=[]
def check(name,ok,detail=''):
 checks.append({'name':name,'pass':bool(ok),'detail':detail})
 if not ok:failures.append(name)
def load(p):return json.loads(p.read_text())
D={p.stem:load(p) for p in DATA.glob('*.json')}; S={r['id']:r for r in D['sources']['rows']}
expected={'providers':24,'requirements':37,'estimates':3,'technical':10,'findings':12,'flags':22,'sources':58,'brief':5}
for k,n in expected.items():check('row count '+k,len(D[k]['rows'])==n,str(len(D[k]['rows'])))
ids=[]
for k,d in D.items():
 for r in d['rows']:
  ids.append(r['id']);check('source links '+r['id'],bool(r.get('source_ids',[r['url'] if k=='sources' else None])) and all(i in S for i in r.get('source_ids',[])))
check('unique row IDs',len(ids)==len(set(ids)))
flagids={r['id'] for r in D['flags']['rows']}
for k,d in D.items():
 for r in d['rows']:check('flags resolve '+r['id'],all(i in flagids for i in r.get('flags',[])))
for r in S.values():
 u=urlparse(r['url']);check('source URL scheme '+r['id'],u.scheme in ['https','http'] and bool(u.netloc))
 check('source provenance '+r['id'],bool(r['evidence_excerpt'] and r['method'] and r['checked_utc']))
 check('non-retrieved source explicitly limited '+r['id'],r['retrieval_status']=='retrieved' or r['retrieval_status'] in ['partial','search-excerpt','blocked-or-index-only'])
for p in D['providers']['rows']:
 for k in ['rating','review_count','current_quote','availability','exact_job_acceptance','combined_scope_confirmed']:check('unsupported field blank '+p['id']+' '+k,p[k]=='')
 check('no unverified reviews '+p['id'],not p['review_verified'])
 if p['license']:
  s=S['CSLB-'+p['license']]; ex=s['evidence_excerpt']
  check('CSLB URL '+p['id'],s['url'].endswith('LicNum='+p['license']) and s['retrieval_status']=='retrieved')
  check('license identity '+p['id'],p['license'] in s['url'] and p['legal_name'] in ex)
  check('license status '+p['id'],p['status'] in ex)
  check('license expiry '+p['id'],p['expire_date'] in ex)
  check('license phone '+p['id'],p['phone'] in ex)
  check('license classifications '+p['id'],all(c in ex for c in p['classifications']))
  check('address in evidence '+p['id'],all(part.strip() in ex for part in p['address'].split(',') if part.strip() not in ['CA']))
 else:check('unverified identity blank '+p['id'],not p['license'] and not p['address'] and not p['phone'] and not p['classifications'])
for r in D['estimates']['rows']:check('quote blank '+r['id'],all(r[k]=='' for k in ['amount_usd','quote_date','labor_included','materials_included','ceiling_access_included','drywall_restore_included','paint_included','dispatch_fee','valid_until']))
# HTML parse and link inventory
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.assets=[];self.text=[];self.rows=0;self.ids=[];self.stack=[];self.errors=[];self.inrow=False;self.rowlinks=[];self.rowtexts=[];self.table_rows=[];self.header=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t not in ['meta','link','br','hr','img','input','area','base','col','embed','param','source','track','wbr']:self.stack.append(t)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a' and 'href' in a:
   self.links.append(a['href'])
   if self.inrow:self.rowlinks.append(a['href'])
  if t in ['script','link','img']:
   u=a.get('src',a.get('href')); 
   if u:self.assets.append(u)
  if t=='thead':self.header=True
  if t=='tr':self.inrow=True;self.rowlinks=[];self.rowtexts=[]
 def handle_endtag(self,t):
  if t=='thead':self.header=False
  if t=='tr' and self.inrow:
   if self.rowtexts and not self.header:self.table_rows.append((' '.join(self.rowtexts),self.rowlinks[:]))
   self.inrow=False
  if t in self.stack:
   while self.stack:
    x=self.stack.pop()
    if x==t:break
 def handle_data(self,d):
  self.text.append(d)
  if self.inrow:self.rowtexts.append(d)
parsers={}
for p in SITE.glob('*.html'):
 q=P();q.feed(p.read_text());parsers[p.name]=q
 check('HTML balanced '+p.name,not q.stack,str(q.stack))
 check('unique HTML IDs '+p.name,len(q.ids)==len(set(q.ids)))
 check('no private/internal wording '+p.name,not re.search(r'private reason|permit background|owner-only|arena/[0-9a-f]{8}-korea8',p.read_text(),re.I))
 for href in q.links:
  u=urlparse(href)
  if u.scheme or u.netloc:check('external URL syntax '+p.name+' '+href,u.scheme in ['https','http'] and bool(u.netloc));continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  check('internal link '+p.name+' '+href,target.exists())
  if u.fragment and target.suffix=='.html':
   z=P();z.feed(target.read_text());check('fragment '+p.name+' '+href,u.fragment in z.ids)
 for asset in q.assets:check('self-contained asset '+p.name+' '+asset,not urlparse(asset).netloc and (p.parent/asset).exists())
 for row,links in q.table_rows:
  check('table row source '+p.name+' '+row[:65],any(urlparse(x).netloc or x=='sources.html' for x in links))
# exact dataset row parity on category pages
pairs={'providers.html':['providers-table','provider-fit'],'requirements.html':['requirements-table'],'estimates.html':['estimates-table','estimate-analysis'],'technical.html':['technical-table'],'analysis.html':['analysis-table'],'sources.html':['sources-table'],'flagged-for-review.html':['flags-table']}
for page,tables in pairs.items():
 text=(SITE/page).read_text()
 for tid in tables:
  block=re.search(r'<table id="'+re.escape(tid)+r'".*?</table>',text,re.S).group(0)
  key={'providers-table':'providers','provider-fit':'providers','requirements-table':'requirements','estimates-table':'estimates','estimate-analysis':'estimates','technical-table':'technical','analysis-table':'findings','sources-table':'sources','flags-table':'flags'}[tid]
  found=[x[len(tid)+1:] for x in re.findall(r'<tr id="([^"]+)"',block)]
  check('rendered IDs '+tid,found==[r['id'] for r in D[key]['rows']],str(len(found)))
# no unsupported amounts anywhere in served artifact
for p in SITE.rglob('*'):
 if p.is_file() and p.suffix in ['.html','.json','.js','.css','.md']:
  check('no unsupported amount '+str(p.relative_to(SITE)),not re.search(r'\$\s*(?:614|550|135)\b',p.read_text()))
# Responsive static checks + optional browser evidence supplied separately
css=(SITE/'assets/style.css').read_text();check('responsive CSS',('@media(max-width:760px)' in css and '.table-wrap{overflow:auto' in css));check('print CSS','@media print' in css)
js=(SITE/'assets/app.js').read_text();r=subprocess.run(['node','--check',str(SITE/'assets/app.js')],capture_output=True,text=True);check('JavaScript syntax',r.returncode==0,r.stderr)
# All JSON in site and source tree parse
for p in list(SITE.rglob('*.json'))+list(DATA.glob('*.json')):
 try:load(p);ok=True
 except Exception:ok=False
 check('JSON parse '+str(p.relative_to(ROOT)),ok)
report={'checked_utc':'2026-11-07','status':'PASS' if not failures else 'FAIL','checks':len(checks),'failures':failures,'results':checks,'pages':len(parsers),'table_rows':sum(len(p.table_rows) for p in parsers.values()),'scope':'Data provenance, row parity, HTML structure, internal links, self-contained assets, blank-value discipline, responsive CSS and JS syntax. External URLs are syntax-checked here; live retrievals are recorded separately in sources.json. Browser evidence is separate.'}
(HERE/'evidence').mkdir(exist_ok=True);(HERE/'evidence'/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','checks','failures','pages','table_rows']},indent=2))
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Check the integrated root and curated Pages artifact, including legacy redirects."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'overflow-review'/'public'
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.assets=[];self.ids=[];self.stack=[];self.text=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t not in ['meta','link','br','hr','img','input','area','base','col','embed','param','source','track','wbr']:self.stack.append(t)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a' and 'href' in a:self.links.append(a['href'])
  if t in ['script','link','img']:
   u=a.get('src',a.get('href'))
   if u:self.assets.append(u)
 def handle_endtag(self,t):
  if t in self.stack:
   while self.stack:
    x=self.stack.pop()
    if x==t:break
 def handle_data(self,d):self.text.append(d)
def P_ids(p):q=P();q.feed(p.read_text());return q.ids
fail=[];n=0
def ck(ok,msg):
 global n;n+=1
 if not ok:fail.append(msg)
for p in ART.rglob('*.html'):
 q=P();q.feed(p.read_text());ck(not q.stack,str(p)+' balance')
 for u in q.links+q.assets:
  z=urlparse(u)
  if z.scheme or z.netloc:ck(z.scheme in ['https','http'],str(p)+' external scheme '+u);continue
  t=(p.parent/unquote(z.path)).resolve() if z.path else p
  ck(t.exists() and t.is_relative_to(ART.resolve()),str(p)+' -> '+u)
  if z.fragment and t.suffix=='.html':ck(z.fragment in P_ids(t),str(p)+' fragment '+u)
 for u in q.assets:
  z=urlparse(u);ck(not z.netloc or (z.netloc=='karagemop466-tech.github.io' and z.path.startswith('/Korea8/')),str(p)+' remote asset '+u)
 txt=p.read_text();ck(not re.search(r'\$\s*(?:614|550|135)\b',txt),str(p)+' unsupported amount')
 ck(not re.search(r'private reason|permit background|owner-only|cannot pull a permit|cannot obtain a permit|without a permit for this week',txt,re.I),str(p)+' private wording')
# canonical parity
for p in (ROOT/'overflow-review'/'site').glob('*.html'):ck((ART/p.name).read_bytes()==p.read_bytes(),'canonical parity '+p.name)
# redirect manifest targets
for r in json.loads((ROOT/'overflow-review'/'repository'/'redirects.json').read_text())['redirects']:
 p=ART/r['path'];ck(p.exists(),'redirect exists '+r['path']);ck(('url='+r['target']) in p.read_text(),'redirect target '+r['path'])
report={'status':'PASS' if not fail else 'FAIL','checks':n,'failures':fail,'html_files':len(list(ART.rglob('*.html'))),'scope':'Curated public artifact: internal links/fragments/assets, canonical parity, redirect targets, unsupported amounts and private wording.'}
(ROOT/'overflow-review'/'evidence'/'public-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(bool(fail))

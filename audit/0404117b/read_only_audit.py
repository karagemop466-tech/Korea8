#!/usr/bin/env python3
"""Read-only canonical audit for session arena/0404117b-korea8.
Writes only under audit/0404117b; does not run the shared report-writing verifier.
"""
from __future__ import annotations
import json, pathlib, re, subprocess, datetime
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'audit'/'0404117b'
PAGES=['index.html','executive-summary.html','decision-analysis.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
OFFICIAL_SUFFIXES=('.gov','.gob','amlegal.com','watcomfg.com','iapmo.org','cslb.ca.gov','leginfo.legislature.ca.gov','sf.gov','heisesplumbing.com','eplumbingsolutions.com','bayareaplumbingsf.com','fastresponseplumbingsf.com','wedoconstructions.com','sfbuildinggroup.com','rapidflowbayarea.com','aceplumbingandrooter.com','ayoobpeery.com','bernalhilldrywall.com','fivestarplumbingsf.com','isacksonplumbing.com','atlasplumbingandrooter.com','inandoutplumbing.com','github.com','diamondcertified.org','bbb.org','yelp.com','angi.com','homeadvisor.com','yahoo.com')
def official(u):
 m=re.match(r'https?://([^/]+)',u); h=m.group(1).lower() if m else ''
 return any(h==s.lstrip('.') or h.endswith(s) for s in OFFICIAL_SUFFIXES)
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
def main():
 tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
 json_errors=[]; json_count=0
 for f in tracked:
  if f.endswith('.json'):
   json_count+=1
   try:json.loads((ROOT/f).read_text())
   except Exception as e:json_errors.append(f'{f}: {e}')
 broken=[]; link_count=0
 for f in tracked:
  if not f.endswith('.html'):continue
  p=ROOT/f; l=Links(); l.feed(p.read_text(errors='replace'))
  for u in l.links:
   if u.startswith(('mailto:','tel:','data:','#','http://','https://')):continue
   link_count+=1; target=(p.parent/u.split('#')[0]).resolve()
   if not target.exists():broken.append(f'{f}:{u}')
 row_total=0; row_official=0; row_gap=[]
 for page in PAGES:
  t=(ROOT/page).read_text()
  for ti,tbl in enumerate(re.findall(r'<tbody>(.*?)</tbody>',t,re.S)):
   for ri,tr in enumerate(re.findall(r'<tr>(.*?)</tr>',tbl,re.S)):
    row_total+=1; hrefs=re.findall(r'href="([^"]+)"',tr)
    if any(official(u) for u in hrefs):row_official+=1
    else:row_gap.append(f'{page} table#{ti} row#{ri}')
 data=ROOT/'overflow-integration'/'data'
 counts={n:len(json.loads((data/f'{n}.json').read_text())['rows']) for n in ['providers','requirements','sources','flags','reviews','technical','compliance']}
 counts['estimates']=len(json.loads((data/'estimates.json').read_text())['rows'])
 counts['ranked']=len(json.loads((data/'ranking.json').read_text())['ranked'])
 report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'tracked_files':len(tracked),'json_files_parsed':json_count,'json_errors':json_errors,'tracked_html_internal_links':link_count,'broken_internal_links':broken,'canonical_rows':row_total,'canonical_rows_with_recognized_official_primary_link':row_official,'strict_row_source_gaps':row_gap,'data_counts':counts,'note':'Read-only audit; shared build/verification reports were not rewritten.'}
 (OUT/'read-only-audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
 return 1 if json_errors or broken or row_gap else 0
if __name__=='__main__':raise SystemExit(main())

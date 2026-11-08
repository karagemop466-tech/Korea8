import json,pathlib,re,sys,unittest
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parent.parent
DATA=ROOT/'overflow-integration'/'data'
sys.path.insert(0,str(ROOT/'overflow-integration'))
from content_guard import has_restricted
def load(n):return json.loads((DATA/n).read_text())
class DataTests(unittest.TestCase):
 def test_source_ids_resolve(self):
  srcs={s['id'] for s in load('sources.json')['rows']}
  for name in ['providers.json','requirements.json','technical.json','compliance.json','reviews.json','flags.json']:
   for r in load(name)['rows']:
    for i in r.get('source_ids',[]):self.assertIn(i,srcs,f'{name}:{r.get("id")}')
 def test_estimates_owner_reported_verified_blank(self):
  e=load('estimates.json');self.assertEqual([r['amount_owner'] for r in e['rows']],[614,550,135]);self.assertTrue(all(r['amount_verified'] is None for r in e['rows']))
 def test_portola_blank(self):
  p=[x for x in load('providers.json')['rows'] if x['name']=='Portola Plumbing Services'][0]
  for k in ['license','phone','expiry','status','registered_city','workers_comp']:self.assertFalse(p[k])
 def test_suspended_flagged(self):
  p=[x for x in load('providers.json')['rows'] if x['license']=='1027286'][0];self.assertEqual(p['status'],'Suspended');self.assertIn('F-09',p['flags'])
 def test_no_numeric_reviews(self):
  self.assertTrue(all(v['rating'] is None and v['review_count'] is None for v in load('reviews.json')['rows']))
 def test_requirements_have_official_context(self):
  for r in load('requirements.json')['rows']:self.assertTrue(r['official_url'].startswith('https://'));self.assertTrue(r['source_ids'])
class SiteTests(unittest.TestCase):
 def test_pages_exist_and_nav(self):
  pages=['index.html','executive-summary.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
  for p in pages:
   t=(ROOT/p).read_text();self.assertIn('<!doctype html>',t)
   for q in pages:self.assertIn(f'href="{q}"',t)
 def test_owner_amounts_and_blank_verified(self):
  t=(ROOT/'estimates.html').read_text();self.assertIn('$614',t);self.assertIn('$550',t);self.assertIn('$135',t);self.assertIn('Owner-reported',t);self.assertIn('aria-label="blank"',t)
 def test_neutral_content_and_encoded_guard(self):
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertFalse(has_restricted(t),f'restricted digest in {p.name}')
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
 def test_ranked_provider_table(self):
  t=(ROOT/'providers.html').read_text();rank=load('ranking.json')
  self.assertIn('id="ranking-table"',t);self.assertIn('Verified amount:',t)
  for r in rank['rows']:
   if r['license']:self.assertIn(f'LicNum={r["license"]}',t)
   if r['phone']:self.assertIn(r['phone'],t)
  self.assertIn('Tier E',t);self.assertIn('Excluded',t)
 def test_every_canonical_row_has_official_link(self):
  srcs=load('sources.json')['rows']
  hosts={urlparse(s['url']).netloc.lower() for s in srcs if s['kind'].startswith('official-') or s['kind'] in {'repository-primary','official-tool'}}
  for name in ['providers.json','requirements.json','estimates.json','technical.json','compliance.json','reviews.json','flags.json','ranking.json']:
   obj=load(name)
   for r in obj.get('rows',[]):
    u=r.get('official_url')
    if u:hosts.add(urlparse(u).netloc.lower())
   if name=='estimates.json':
    for r in obj.get('official_fees',[]):
     u=r.get('official_url')
     if u:hosts.add(urlparse(u).netloc.lower())
  for p in ROOT.glob('*.html'):
   for body in re.findall(r'<tbody>(.*?)</tbody>',p.read_text(),re.S):
    for tr in re.findall(r'<tr>(.*?)</tr>',body,re.S):
     urls=re.findall(r'href="(https://[^"]+)"',tr)
     self.assertTrue(any(urlparse(u).netloc.lower() in hosts or urlparse(u).netloc.lower().endswith(('.gov','.ca.gov')) for u in urls),f'no official link in {p.name}: {tr[:100]}')
if __name__=='__main__':unittest.main()

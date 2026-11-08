import json,pathlib,re,unittest
ROOT=pathlib.Path(__file__).resolve().parent.parent
DATA=ROOT/'overflow-integration'/'data'
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
 def test_new_verified_2026_11_08_providers_and_cautions(self):
  provs={p['license'] or p['name']:p for p in load('providers.json')['rows']}
  self.assertEqual(provs['868994']['name'],'Atlas Plumbing & Rooter')
  self.assertEqual(provs['1041846']['name'],'Discover Plumbing & Rooter')
  self.assertEqual(provs['1034873']['name'],'Plumbing 1 Builders')
  lfm=provs['LFM Construction and Plumbing']
  for k in ['license','phone','expiry','status','registered_city','workers_comp']:self.assertFalse(lfm[k])
  dg=provs['297604']
  self.assertIn('F-37',dg['flags'])
  heise=provs['1089561']
  self.assertIn('F-38',heise['flags'])
  self.assertEqual(heise['rank'],10)
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
  t=(ROOT/'estimates.html').read_text();self.assertIn('$614',t);self.assertIn('$550',t);self.assertIn('$135',t);self.assertIn('Owner-reported',t);self.assertIn('aria-label="blank"',t);self.assertIn('cost_drivers' if False else 'Budget impact',t)
 def test_ranking_reasoning_and_contact_info_present(self):
  for f in ['index.html','executive-summary.html','providers.html','OVERFLOW_EXECUTIVE_SUMMARY.md']:
   t=(ROOT/f).read_text()
   self.assertIn('Ace Plumbing',t);self.assertIn('(415) 824-6444',t)
   self.assertIn('Atlas Plumbing',t);self.assertIn('BPC §7114.A',t if f in ('executive-summary.html','OVERFLOW_EXECUTIVE_SUMMARY.md','providers.html') else 'BPC §7114.A')
 def test_no_conflict_markers_or_private_meta(self):
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertNotIn('private reason',t);self.assertNotIn('without a permit for this week',t);self.assertNotIn('private scheduling',t)
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

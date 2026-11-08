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
 def test_no_numeric_reviews(self):
  self.assertTrue(all(v['rating'] is None and v['review_count'] is None for v in load('reviews.json')['rows']))
 def test_ranking_rows_complete_and_ordered(self):
  srcs={s['id'] for s in load('sources.json')['rows']}
  rk=load('ranking.json');rows=rk['rows']
  self.assertEqual([r['rank'] for r in rows],list(range(1,len(rows)+1)))
  for r in rows:
   self.assertTrue(r['official_url'].startswith('https://www.cslb.ca.gov/'),r['rank'])
   self.assertTrue(r['phone'],r['rank'])
   self.assertIsNone(r['cost_verified'],r['rank'])
   self.assertTrue(r['why'] and r['cost_basis'] and r['limits'],r['rank'])
   for i in r['source_ids']:self.assertIn(i,srcs,f"rank {r['rank']}:{i}")
 def test_ranking_covers_whole_register(self):
  prov={x['id'] for x in load('providers.json')['rows']}
  rk=load('ranking.json')
  covered={r['provider_id'] for r in rk['rows']}|{x['provider_id'] for x in rk['excluded_rows']}
  self.assertEqual(covered,prov)
  suspended={x['id'] for x in load('providers.json')['rows'] if x['status']=='Suspended'}
  self.assertFalse(suspended & {r['provider_id'] for r in rk['rows']})
 def test_requirements_have_official_context(self):
  for r in load('requirements.json')['rows']:self.assertTrue(r['official_url'].startswith('https://'));self.assertTrue(r['source_ids'])
class SiteTests(unittest.TestCase):
 def test_pages_exist_and_nav(self):
  pages=['index.html','executive-summary.html','decision-analysis.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
  for p in pages:
   t=(ROOT/p).read_text();self.assertIn('<!doctype html>',t)
   for q in pages:self.assertIn(f'href="{q}"',t)
 def test_decision_analysis_page_has_link_and_phone_per_row(self):
  t=(ROOT/'decision-analysis.html').read_text()
  rk=load('ranking.json')
  for r in rk['rows']:
   self.assertIn(f"LicNum={r['license']}",t)
   self.assertIn(r['phone'],t)
  self.assertIn('Owner-reported',t)
  for x in rk['excluded_rows']:self.assertIn(x['name'],t)
 def test_owner_amounts_and_blank_verified(self):
  t=(ROOT/'estimates.html').read_text();self.assertIn('$614',t);self.assertIn('$550',t);self.assertIn('$135',t);self.assertIn('Owner-reported',t);self.assertIn('aria-label="blank"',t)
 def test_no_conflict_markers_or_private_meta(self):
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertNotIn('private reason',t);self.assertNotIn('without a permit for this week',t)
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

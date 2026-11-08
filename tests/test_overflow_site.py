import html,json,pathlib,re,unittest
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
 def test_requirements_have_official_context(self):
  for r in load('requirements.json')['rows']:self.assertTrue(r['official_url'].startswith('https://'));self.assertTrue(r['source_ids'])
class CrosscheckTests(unittest.TestCase):
 def setUp(self):
  self.x=load('ranking-crosscheck.json');self.c=load('ranking.json')
 def test_scores_reproducible_and_ranked(self):
  self.assertEqual([r['rank'] for r in self.x['rows']],list(range(1,len(self.x['rows'])+1)))
  for r in self.x['rows']:
   c=r['criteria'];self.assertEqual(r['score'],c['scope_coverage']*3+c['adjacent_evidence']*2+c['small_job_fit']*1+c['written_price']*2-sum(d['points'] for d in r['deductions']),r['provider_id'])
 def test_every_row_has_contact_and_source(self):
  prov={p['id'] for p in load('providers.json')['rows']};srcs={s['id'] for s in load('sources.json')['rows']}
  for r in self.x['rows']:
   self.assertIn(r['provider_id'],prov);self.assertTrue(r['phone']);self.assertTrue(r['official_url'].startswith('https://'))
   for i in r['source_ids']:self.assertIn(i,srcs)
 def test_no_verified_amounts(self):
  for r in self.x['rows']:self.assertIsNone(r['cost']['verified_amount'])
 def test_page_publishes_crosscheck(self):
  t=(ROOT/'decision-analysis.html').read_text();self.assertIn('ranking-crosscheck',t)
  for r in self.x['rows']:self.assertIn(html.escape(r['name']),t)
 def test_canonical_ranking_has_official_contacts(self):
  for r in self.c['ranked']+[self.c['partner']]:
   self.assertTrue(r['phone']);self.assertTrue(r['official_url'].startswith('https://'))
class SiteTests(unittest.TestCase):
 def test_pages_exist_and_nav(self):
  pages=['index.html','executive-summary.html','decision-analysis.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
  for p in pages:
   t=(ROOT/p).read_text();self.assertIn('<!doctype html>',t)
   for q in pages:self.assertIn(f'href="{q}"',t)
 def test_owner_amounts_and_blank_verified(self):
  t=(ROOT/'estimates.html').read_text();self.assertIn('$614',t);self.assertIn('$550',t);self.assertIn('$135',t);self.assertIn('Owner-reported',t);self.assertIn('aria-label="blank"',t)
 def test_no_conflict_markers_or_private_meta(self):
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertNotIn('private reason',t);self.assertNotIn('without a permit for this week',t)
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

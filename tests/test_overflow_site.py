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
 def test_requirements_have_official_context(self):
  for r in load('requirements.json')['rows']:self.assertTrue(r['official_url'].startswith('https://'));self.assertTrue(r['source_ids'])
class SiteTests(unittest.TestCase):
 def test_pages_exist_and_nav(self):
  pages=['index.html','executive-summary.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
  for p in pages:
   t=(ROOT/p).read_text();self.assertIn('<!doctype html>',t)
   for q in pages:self.assertIn(f'href="{q}"',t)
 def test_unverified_owner_amounts_are_blank_in_public_site(self):
  pages=' '.join((ROOT/p).read_text() for p in ['estimates.html','executive-summary.html'])
  summary=(ROOT/'OVERFLOW_EXECUTIVE_SUMMARY.md').read_text()
  for amount in [614,550,135]:
   self.assertNotIn(f'${amount}',pages);self.assertNotIn(f'${amount}',summary)
  self.assertIn('aria-label="blank"',(ROOT/'estimates.html').read_text())
  self.assertTrue(all(r['amount_verified'] is None for r in load('estimates.json')['rows']))
 def test_ranked_shortlist_has_verified_contacts_and_official_sources(self):
  data=load('providers.json');sources={s['id']:s for s in load('sources.json')['rows']}
  self.assertEqual([r['rank'] for r in data['priority_candidates']],list(range(1,9)))
  for r in data['priority_candidates']:
   p=next(x for x in data['rows'] if x['id']==r['provider_id'])
   self.assertTrue(p['call_display']);self.assertTrue(p['call_tel'])
   self.assertTrue(r['source_ids'])
   self.assertTrue(all(sid in sources and sources[sid]['url'].startswith('https://') for sid in r['source_ids']))
  page=(ROOT/'providers.html').read_text()
  self.assertIn('844-BAY-FLOW',page);self.assertIn('(415) 824-6444',page);self.assertIn('Heise’s Plumbing',page)
 def test_no_conflict_markers_or_private_meta(self):
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertNotIn('private owner-only note',t)
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

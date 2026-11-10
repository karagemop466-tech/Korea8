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
 def test_ranking_active_and_source_linked(self):
  prov={p['id']:p for p in load('providers.json')['rows']};rk=load('ranking.json')
  for r in rk['ranked']+[rk['partner']]:
   self.assertEqual(prov[r['provider_id']]['status'],'Current and active');self.assertTrue(r['source_ids']);self.assertTrue(r['official_url'].startswith('https://'))
  self.assertAlmostEqual(sum(w['weight'] for w in rk['weights']),1.0)
 def test_requirements_have_official_context(self):
  for r in load('requirements.json')['rows']:self.assertTrue(r['official_url'].startswith('https://'));self.assertTrue(r['source_ids'])
class SiteTests(unittest.TestCase):
 def test_pages_exist_and_nav(self):
  pages=['index.html','executive-summary.html','decision-analysis.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
  for p in pages:
   t=(ROOT/p).read_text();self.assertIn('<!doctype html>',t)
   for q in pages:self.assertIn(f'href="{q}"',t)
 def test_owner_amounts_and_blank_verified(self):
  t=(ROOT/'estimates.html').read_text();self.assertIn('$614',t);self.assertIn('$550',t);self.assertIn('$135',t);self.assertIn('Owner-reported',t);self.assertIn('aria-label="blank"',t)
 def test_no_conflict_markers_and_neutral_wording(self):
  import sys;sys.path.insert(0,str(ROOT/'scripts'));import wording_guard
  for p in ROOT.glob('*.html'):
   t=p.read_text();self.assertNotIn('<<<<<<<',t);self.assertEqual(wording_guard.scan_bytes(t.encode('utf-8')),[],p.name)
 def test_heise_advertised_restoration_is_sourced_and_conditional(self):
  h=next(x for x in load('ranking.json')['ranked'] if x['provider_id']=='P-03')
  self.assertIn('HEISE-PATCH',h['source_ids']); self.assertIn('not independent proof',h['why'])
  self.assertIn('HEISE-PATCH',(ROOT/'sources.html').read_text())
 def test_watco_does_not_claim_complete_fill_test(self):
  r={x['id']:x for x in load('requirements.json')['rows']}
  self.assertNotIn('include fill/operate',r['R-40']['basis'])
  self.assertNotIn('include a fill/operate',r['R-02']['basis'])
 def test_dg_citation_substance_published(self):
  dg=next(x for x in load('ranking.json')['not_recommended'] if x['provider_id']=='P-21')
  self.assertIn('DG-CITATION',dg['source_ids']);self.assertIn('7114.A',dg['reason'])
  self.assertNotIn('substance is not published',dg['reason'])
 def test_sfbc_106a2_fire_resistive_documented(self):
  c=next(x for x in load('compliance.json')['rows'] if x['id']=='C-13')
  self.assertIn('SF-CODE-106',c['source_ids']);self.assertIn('fire-resistive',c['rule'].lower())
  r=next(x for x in load('requirements.json')['rows'] if x['id']=='R-12')
  self.assertIn('SF-CODE-106',r['source_ids'])
 def test_heise_dissolved_prior_license_distinguished(self):
  srcs={s['id']:s for s in load('sources.json')['rows']}
  self.assertIn('CSLB-787733',srcs)
  h=next(x for x in load('providers.json')['rows'] if x['id']=='P-03')
  self.assertIn('CSLB-787733',h['source_ids']);self.assertIn('1089561',h['additional_status'])
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

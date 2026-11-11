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
  pages=['index.html','executive-summary.html','decision-analysis.html','questions.html','requirements.html','providers.html','estimates.html','technical-approach.html','code-and-permit.html','sources.html','flagged-for-review.html','verification.html']
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
 def test_bpc_7059_and_city_sfpc_pdf_documented(self):
  srcs={s['id']:s for s in load('sources.json')['rows']}
  self.assertIn('BPC-7059',srcs);self.assertIn('CSLB-831',srcs);self.assertIn('SF-CODE-104-PDF',srcs)
  c2=next(x for x in load('compliance.json')['rows'] if x['id']=='C-02')
  self.assertIn('SF-CODE-104-PDF',c2['source_ids'])
  c15=next(x for x in load('compliance.json')['rows'] if x['id']=='C-15')
  self.assertIn('BPC-7059',c15['source_ids']);self.assertIn('incidental',c15['rule'].lower())
 def test_cost_drivers_on_estimates_without_inferred_prices(self):
  est=load('estimates.json')
  self.assertGreaterEqual(len(est.get('cost_drivers',[])),6)
  html_text=(ROOT/'estimates.html').read_text()
  self.assertIn('id="cost-drivers-table"',html_text)
 def test_sources_urls_fixed_and_unresolved_discovery_blank(self):
  srcs={s['id']:s for s in load('sources.json')['rows']}
  self.assertIn('/recent-jobs/projects/the-tub-waste-and-overflow-assembly-171358/',srcs['HEISE-PANHANDLE']['url'])
  self.assertIn('LicName=D+G+CONSTRUCTION+CO',srcs['DG-CITATION']['url'])
  for name in ("C J's Plumbing & Rooter Service",'Golden Gate Plumbing & Rooter Inc'):
   p=next(x for x in load('providers.json')['rows'] if x['name']==name)
   for k in ('license','phone','expiry','status','registered_city','workers_comp'):self.assertFalse(p[k])
 def test_gems_preserved(self):
  self.assertTrue((ROOT/'docs'/'index.html').exists());self.assertTrue((ROOT/'src').exists());self.assertTrue((ROOT/'vendor').exists())
if __name__=='__main__':unittest.main()

class FinalCurrentSourceTests(unittest.TestCase):
 def test_all_identified_providers_have_fresh_issue_and_source_dates(self):
  receipt=json.loads((ROOT/'audit/2026-11-10-4b81abe2/cslb-receipts.json').read_text())
  checked={r['license'] for r in receipt['rows']}
  self.assertEqual(len(checked),24)
  for p in load('providers.json')['rows']:
   if p['license'] not in checked: continue
   self.assertRegex(p['issue_date'],r'^\d{4}-\d{2}-\d{2}$',p['license'])
   self.assertIn('re-read 2026-11-11',p['source_timestamp'])
   self.assertNotIn('4:49 PM',p['source_timestamp'])
 def test_ranking_rubric_reproduces_corrected_order(self):
  rk=load('ranking.json'); weights={w['id']:w['weight'] for w in rk['weights']}
  self.assertEqual(weights,{'C1':.3,'C2':.2,'C3':.2,'C4':.15,'C5':.15})
  self.assertTrue(all(w.get('rubric') for w in rk['weights']))
  ordered=sorted(rk['ranked'],key=lambda r:(-sum(r['score_components'][k]*v for k,v in weights.items()),-r['score_components']['C2'],r['name']))
  self.assertEqual([r['provider_id'] for r in ordered[-2:]],['P-06','P-16'])
  self.assertEqual(ordered[-1]['score_components']['C1'],2)
  self.assertAlmostEqual(sum(ordered[-1]['score_components'][k]*v for k,v in weights.items()),1.70)
 def test_fdl_current_policy_not_stale_exemption(self):
  rk=load('ranking.json'); row=next(x for x in rk['not_recommended'] if x['provider_id']=='P-17')
  self.assertIn('current workers-compensation policy',row['reason'])
  self.assertNotIn('workers-compensation exemption, no building',row['reason'])
 def test_specialty_incidental_rule_is_sourced_and_conditional(self):
  sources={s['id']:s for s in load('sources.json')['rows']}
  self.assertIn('BPC-7059',sources)
  self.assertIn('incidental and supplemental',sources['BPC-7059']['supports'])
  c=next(x for x in load('compliance.json')['rows'] if x['id']=='C-15')
  self.assertIn('BPC-7059',c['source_ids'])
  r=next(x for x in load('requirements.json')['rows'] if x['id']=='R-15')
  self.assertIn('BPC-7059',r['source_ids'])
 def test_code_chunk_metadata_matches_direct_retrieval(self):
  sources={s['id']:s for s in load('sources.json')['rows']}
  self.assertIn('chunk 14',sources['SF-CODE-104']['supports'])
  self.assertIn('chunk 39',sources['SF-CODE-106']['supports'])
  self.assertNotIn('chunks 28–29',sources['SF-CODE-106']['supports'])
 def test_cost_drivers_have_sources_and_no_inferred_amounts(self):
  rows=load('estimates.json').get('cost_drivers',[])
  self.assertEqual(len(rows),6)
  for row in rows:
   self.assertTrue(row['source_ids']);self.assertTrue(row['official_url'].startswith('https://'))
   self.assertNotIn('amount',row);self.assertNotIn('amount_owner',row);self.assertNotIn('amount_verified',row)
  self.assertIn('cost-drivers-table',(ROOT/'estimates.html').read_text())
 def test_final_audit_and_traceability_are_linked(self):
  v=(ROOT/'verification.html').read_text()
  self.assertIn('audit/2026-11-10-4b81abe2/REPORT.md',v)
  self.assertIn('requirements-traceability.json',v)
  trace=json.loads((ROOT/'audit/2026-11-10-4b81abe2/requirements-traceability.json').read_text())
  self.assertEqual(trace['summary']['requirements'],len(trace['rows']))
  self.assertEqual(trace['summary']['satisfied']+trace['summary']['partially_satisfied'],len(trace['rows']))

class MergedReviewAndRequestTests(unittest.TestCase):
 def test_merged_review_request_features_preserved(self):
  self.assertEqual(len(load('reviews.json')['rows']),23)
  self.assertEqual(len(load('requests.json')['channels']),10)
  self.assertIn('request-script',(ROOT/'index.html').read_text())
  self.assertIn('partners_second_bid',load('ranking.json'))
 def test_no_unverified_yelp_numbers_in_narrative(self):
  f=next(x for x in load('flags.json')['rows'] if x['id']=='F-14')
  for value in ['4.7','4.2','1.4 thousand','278','283']:
   self.assertNotIn(value,f['detail'])
  self.assertNotIn('only two Yelp figures',(ROOT/'providers.html').read_text())
 def test_flag_ids_unique_and_new_range_does_not_replace_publication_flag(self):
  rows=load('flags.json')['rows'];ids=[x['id'] for x in rows]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertIn('F-52',ids)
  for i in range(65,70):self.assertIn(f'F-{i}',ids)

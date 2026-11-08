#!/usr/bin/env python3
"""Apply the remaining A6880 canonical corrections after an explicit handoff.

This script is stored in the independent audit scope. It is intentionally NOT
run while another session has an active canonical claim. It edits by stable row
ID and preserves unrelated fields/rows. Run from the repository root only after
K8-6880-3/K8-6880-4 are claimed by arena/6880fb12-korea8.
"""
from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / 'overflow-integration' / 'data'
CHECKED = '2026-11-08'

def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))

def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def row(rows, rid):
    for r in rows:
        if r.get('id') == rid:
            return r
    raise KeyError(rid)

def add_unique(lst, item):
    if item not in lst:
        lst.append(item)

def main():
    # Sources: new official-company service evidence and CSLB bid guidance.
    sources = load('sources.json')
    ids = {s['id'] for s in sources['rows']}
    if 'HEISE-DRYWALL' not in ids:
        sources['rows'].append({
            'id': 'HEISE-DRYWALL',
            'url': 'https://www.heisesplumbing.com/property-maintenance/paint-patch-and-drywall-repair/',
            'title': 'Heise’s Plumbing — Paint, Patch & Drywall Repair',
            'publisher': 'Heise’s Plumbing',
            'kind': 'official-company',
            'checked': CHECKED,
            'retrieval': 'direct',
            'supports': 'Company advertises drywall cutouts made during pipe/drain/valve maintenance, ceiling drywall repair after plumbing leaks are resolved, paint touch-up, occupied homes/apartment turnovers/multi-family properties, and tenant-schedule coordination.',
            'limitations': 'Company self-published service description; no exact-job acceptance, price, schedule, warranty or licensed restoration self-performance is confirmed. CSLB #1089561 has no B or C-9.',
            'official': True,
        })
    if 'CSLB-FINDING' not in ids:
        sources['rows'].append({
            'id': 'CSLB-FINDING',
            'url': 'https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx',
            'title': 'CSLB — Finding the Right Contractor',
            'publisher': 'California Contractors State License Board',
            'kind': 'official-government',
            'checked': CHECKED,
            'retrieval': 'direct',
            'supports': 'CSLB guidance: get at least three written bids and compare identical plans, specifications and scope of work; do not automatically accept the lowest bid.',
            'limitations': 'Consumer guidance, not a job-specific permit ruling or a verified contractor quote.',
            'official': True,
        })
    sources['as_of'] = CHECKED
    save('sources.json', sources)

    # Requirements: correct Watco attribution and provenance.
    req = load('requirements.json')
    r = row(req['rows'], 'R-02')
    r['basis'] = 'Proposed functional acceptance control. Watco step 7 supports remove/readjust so the drain stops water when closed; the retrieved sheet does not explicitly prescribe a fill/operate leak test.'
    r = row(req['rows'], 'R-40')
    r['basis'] = 'Proposed acceptance control: Watco step 7 supports closed-position water-stop adjustment, and DBI requires inspection before covering. Fill/leak testing before closure is a proposed control, not a quoted manufacturer test step.'
    r = row(req['rows'], 'R-03')
    r['origin'] = 'Proposed control'
    r['status'] = 'Proposed control; not yet accepted by a provider'
    r = row(req['rows'], 'R-36')
    r['origin'] = 'Proposed control'
    r['status'] = 'Proposed control; not yet accepted by a provider'
    r['basis'] = 'CSLB guidance recommends at least three written bids on identical plans, specifications and scope. The three supplied estimates cover different work and are not a comparable price range.'
    add_unique(r['source_ids'], 'CSLB-FINDING')
    r['official_url'] = 'https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx'
    save('requirements.json', req)

    # Compliance: complete §7057 count rule and add conditional §104.5 fee row.
    comp = load('compliance.json')
    c = row(comp['rows'], 'C-05')
    c['rule'] = 'BPC §7057 allows a B prime/subcontract for other trades when it requires at least two unrelated trades other than framing/carpentry, or the B holds the appropriate classification/subcontracts appropriately. Framing/carpentry cannot be counted in the two-trade calculation.'
    if not any(x.get('id') == 'C-13' for x in comp['rows']):
        comp['rows'].append({
            'id': 'C-13',
            'topic': 'Conditional permit-issuance-fee waiver',
            'rule': 'SF Plumbing Code §104.5 says replacement of a plumbing fixture or gas appliance without a change in drainage, piping or venting does not require payment of a permit issuance fee. A separate issuance fee is paid for each class of work, and final inspection requires outstanding fees to be paid.',
            'source_ids': ['SF-CODE-104', 'SF-FEES'],
            'official_url': 'https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830',
            'application': 'This is a conditional fee rule, not a permit exemption or an inspection-fee waiver. DBI must confirm whether the exact trip-lever/waste-and-overflow scope qualifies; do not subtract fees from a quote automatically.',
        })
    save('compliance.json', comp)

    # Flags: preserve licensing gate while recording advertised restoration service.
    flags = load('flags.json')
    f = row(flags['rows'], 'F-17')
    f['detail'] = 'The Ingleside/Mission/Marina project pages render project content but embed a “Page Not Found (404)” template block. The Ingleside page describes ceiling access; none proves drywall restoration. A separate official service page advertises post-plumbing drywall/ceiling/paint repair, but that advertisement is not job-specific restoration proof.'
    add_unique(f['source_ids'], 'HEISE-DRYWALL')
    f = row(flags['rows'], 'F-18')
    f['title'] = 'Heise’s license has no B or C-9 despite advertised drywall service'
    f['detail'] = '#1089561 shows A/C-10/C-20/C-36. The official Paint, Patch & Drywall Repair page advertises plumbing-access cutouts, ceiling patching, paint touch-up and tenant coordination, but the service page does not add a B or C-9 classification or confirm the restoration contracting party.'
    f['action'] = 'Name the properly licensed restoration party or lawful subcontract structure in writing before hiring; confirm who warrants the ceiling patch/texture/paint.'
    add_unique(f['source_ids'], 'HEISE-DRYWALL')
    save('flags.json', flags)

    # Ranking/provider narrative: new service evidence, no license inference.
    ranking = load('ranking.json')
    for w in ranking['weights']:
        if w['id'] == 'C4':
            w['source_ids'] = ['ACE', 'HEISE', 'HEISE-DRYWALL']
    for r in ranking['ranked']:
        if r.get('provider_id') == 'P-03':
            add_unique(r['source_ids'], 'HEISE-DRYWALL')
            r['score_components']['C4'] = 5
            r['why'] = 'The only provider with company-published San Francisco tub waste-and-overflow cases, including one that says the crew accessed the exterior ceiling to remove the old overflow. Its official Paint, Patch & Drywall Repair page also advertises plumbing-access cutout repair, ceiling water-stain patching, paint touch-up, occupied rentals and tenant-schedule coordination. That is the strongest conditional all-in-one service evidence, but the licence is C-36/C-10/A/C-20 with no B or C-9, so the restoration party and lawful contract structure must be named before hiring. The case page also embeds a 404 template block.'
            r['ask'] = 'Ask who performs and warrants the ceiling patch/texture/paint, under which license/contract structure, whether the same crew can do both paths, and for a written two-path price. Confirm whether the exterior-ceiling case resembles this storage-unit access and provide a direct reference.'
            r['short_why'] = 'published ceiling-access tub waste-and-overflow cases plus advertised plumbing-access drywall/ceiling/paint repair and tenant coordination; no B or C-9, so the restoration party must be named'
    save('ranking.json', ranking)

    providers = load('providers.json')
    p = row(providers['rows'], 'P-03')
    add_unique(p['source_ids'], 'HEISE-DRYWALL')
    p['fit'] = 'Strongest published adjacent case evidence: San Francisco tub waste-and-overflow replacements, including one described as using ceiling access. The official drywall service page advertises post-plumbing cutout/ceiling/paint repair and tenant coordination. No C-9/B on this license; the restoration party and contract structure remain unconfirmed.'
    save('providers.json', providers)

    # Generator narrative: keep hardcoded executive/dashboard text consistent.
    build = ROOT / 'scripts' / 'build_overflow_site.py'
    t = build.read_text(encoding='utf-8')
    replacements = [
        (
            "['Strongest adjacent technical case','Heise’s Ingleside','Company-published ceiling-access tub waste/overflow replacement; restoration unverified.',src_links(['HEISE-INGLESIDE','CSLB-1089561'])],",
            "['Strongest adjacent technical case','Heise’s Ingleside + drywall service','Company-published ceiling-access tub waste/overflow replacement; official page advertises post-plumbing drywall/ceiling/paint repair and tenant coordination; restoration party unverified.',src_links(['HEISE-INGLESIDE','HEISE-DRYWALL','CSLB-1089561'])],"
        ),
        (
            "2. Heise’s Plumbing #1089561, (415) 333-0704 — C-36/C-10/A/C-20; only company-published San Francisco ceiling-access tub waste-and-overflow case; no B or C-9, so the ceiling party must be named. No quote on file.",
            "2. Heise’s Plumbing #1089561, (415) 333-0704 — C-36/C-10/A/C-20; published ceiling-access tub waste-and-overflow case plus advertised plumbing-access drywall/ceiling/paint repair and tenant coordination; no B or C-9, so the restoration party/contract structure must be named. No quote on file."
        ),
        (
            "Heise’s ranks second because it is the only provider with a company-published San Francisco ceiling-access tub waste-and-overflow case, even though its licence has no B or C-9.",
            "Heise’s ranks second because it combines the only company-published San Francisco ceiling-access tub waste-and-overflow case with an official drywall/ceiling/paint service page and tenant-coordination statements, even though its licence has no B or C-9."
        ),
        (
            '<a href="audit/verification_3946905e/REPORT_2026-11-08_3946905e.md">Final source-verification audit</a></p>',
            '<a href="audit/verification_3946905e/REPORT_2026-11-08_3946905e.md">Final source-verification audit</a> · <a href="audit/REPORT_2026-11-08_6880fb12.md">Independent evidence audit</a></p>'
        ),
    ]
    for old, new in replacements:
        if old in t:
            t = t.replace(old, new, 1)
        elif new not in t:
            raise RuntimeError('generator replacement target missing: ' + old[:80])
    build.write_text(t, encoding='utf-8')

    # Regression tests for the evidence corrections.
    test = ROOT / 'tests' / 'test_overflow_evidence_6880fb12.py'
    test.write_text('''import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'overflow-integration' / 'data'
def load(name): return json.loads((DATA / name).read_text(encoding='utf-8'))
class EvidenceCorrections(unittest.TestCase):
    def test_new_primary_sources_registered(self):
        srcs = {s['id']: s for s in load('sources.json')['rows']}
        self.assertEqual(srcs['HEISE-DRYWALL']['kind'], 'official-company')
        self.assertEqual(srcs['CSLB-FINDING']['kind'], 'official-government')
    def test_watco_basis_is_proposed_control(self):
        rows = {r['id']: r for r in load('requirements.json')['rows']}
        for rid in ('R-02', 'R-40'):
            self.assertIn('step 7', rows[rid]['basis'])
            self.assertIn('Proposed', rows[rid]['basis'])
            self.assertNotIn('instructions include a fill/operate test', rows[rid]['basis'])
            self.assertNotIn('instructions include fill/operate testing', rows[rid]['basis'])
    def test_requirement_provenance(self):
        rows = {r['id']: r for r in load('requirements.json')['rows']}
        self.assertEqual(rows['R-03']['origin'], 'Proposed control')
        self.assertIn('CSLB-FINDING', rows['R-36']['source_ids'])
    def test_compliance_conditions(self):
        rows = {r['id']: r for r in load('compliance.json')['rows']}
        self.assertIn('framing/carpentry', rows['C-05']['rule'])
        self.assertIn('issuance fee', rows['C-13']['rule'])
        self.assertIn('not a permit exemption', rows['C-13']['application'])
    def test_heise_ranking_keeps_license_gate(self):
        rk = load('ranking.json')
        r = [x for x in rk['ranked'] if x['provider_id'] == 'P-03'][0]
        self.assertIn('HEISE-DRYWALL', r['source_ids'])
        self.assertIn('no B or C-9', r['why'])
        self.assertIn('tenant', r['short_why'])
    def test_rendered_pages_link_new_evidence(self):
        decision = (ROOT / 'decision-analysis.html').read_text(encoding='utf-8')
        self.assertIn('https://www.heisesplumbing.com/property-maintenance/paint-patch-and-drywall-repair/', decision)
        code = (ROOT / 'code-and-permit.html').read_text(encoding='utf-8')
        self.assertIn('Conditional permit-issuance-fee waiver', code)
if __name__ == '__main__': unittest.main()
''', encoding='utf-8')
    print('Remaining A6880 corrections applied. Run build, verifier, unit tests and strict audit next.')

if __name__ == '__main__':
    main()

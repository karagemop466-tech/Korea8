#!/usr/bin/env python3
"""Apply the 2026-11-10 verification corrections to the canonical data.

Every edit below is backed by a source re-read on 2026-11-10 and recorded in
`audit/2026-11-10-36eb26c3/`. The script is idempotent: running it twice leaves
the same data. It never deletes a prior row; it only re-stamps, appends or
corrects a field whose value was directly re-checked at source.
"""
from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'overflow-integration' / 'data'
TODAY = '2026-11-10'


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


changes = []


def note(msg):
    changes.append(msg)


# --------------------------------------------------------------------------
# 1. Sources: re-stamp every CSLB record, add the new directly-read sources.
# --------------------------------------------------------------------------
src = load('sources.json')
src['as_of'] = TODAY
by_id = {s['id']: s for s in src['rows']}
for s in src['rows']:
    if s['id'].startswith('CSLB-'):
        s['checked'] = TODAY
        s['retrieval'] = 'direct'
        s['limitations'] = ('Point-in-time official record re-read 2026-11-10 (the page showed "Data current as of '
                            '11/9/2026 4:49 PM"). Complaint disclosure is limited by law; active status is not an '
                            'endorsement or a complete background check.')

NEW_SOURCES = [
    dict(id='CSLB-787733',
         url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=787733',
         title="CSLB license detail #787733 — HEISE'S PLUMBING INC (expired)",
         publisher='California Contractors State License Board', kind='official-government', checked=TODAY,
         retrieval='direct',
         supports=('BBB records licence 787733 for "Heise\'s Plumbing, Inc.". CSLB shows that licence expired '
                   '03/31/2023, was cancelled after expiration and the Secretary of State recorded a dissolution '
                   'on 02/12/2025.'),
         limitations=('Expired record. It proves only that the licence number BBB publishes is not the active one; '
                      'it does not by itself establish the corporate relationship between the expired holder and '
                      'the active #1089561 holder.')),
    dict(id='CSLB-961936',
         url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=961936',
         title='CSLB license detail #961936 — BAY AREA PLUMBING BAP INC (inactive)',
         publisher='California Contractors State License Board', kind='official-government', checked=TODAY,
         retrieval='direct',
         supports=('A differently named entity, "BAY AREA PLUMBING BAP INC" (Concord), holds #961936, which CSLB '
                   'shows as inactive after a workers-compensation exemption cancellation on 09/14/2026. BBB '
                   'lists this licence number for a Pleasant Hill "Bay Area Plumbing BAP, Inc.".'),
         limitations=('No official record links this entity to the San Francisco #757796 quote provider. The two '
                      'businesses are similar in name only as far as the sources show.')),
    dict(id='BBB-ACE',
         url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/ace-plumbing-and-rooter-inc-1116-58941',
         title='BBB business profile — Ace Plumbing and Rooter, Inc.',
         publisher='Better Business Bureau', kind='review-platform', checked=TODAY, retrieval='direct',
         supports=('BBB Accreditation since 08/01/2004; A+ rating display; customer-review average 4.76/5 over 51 '
                   'reviews as displayed; licence 829071 recorded; 20 employees; business started 11/01/2003.'),
         limitations=('Platform display retrieved 2026-11-10. BBB ratings are BBB\'s opinion, not an independent '
                      'quality measure, and the page can change. Reviews are self-selected and none describes '
                      'this exact repair.')),
    dict(id='BBB-HEISE',
         url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/heises-plumbing-inc-1116-41584',
         title="BBB business profile — Heise's Plumbing, Inc.",
         publisher='Better Business Bureau', kind='review-platform', checked=TODAY, retrieval='direct',
         supports=('Not BBB accredited; B- rating display; 1 complaint filed in the last 3 years (in the last 12 '
                   'months) and reported as not responded to; 1 customer review (a negative service account); BBB '
                   'records licence 787733 and an address of 260 Ocean Ave.'),
         limitations=('Platform display retrieved 2026-11-10. Complaint text and business response were not read '
                      'in full, so the underlying facts are not verified here. BBB ratings are BBB\'s opinion.')),
    dict(id='BBB-EXPERT',
         url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492',
         title='BBB business profile — Expert Plumbing Solutions',
         publisher='Better Business Bureau', kind='review-platform', checked=TODAY, retrieval='direct',
         supports=('Not BBB accredited; "Not Rated"; licence 977638 recorded with an expiry of 10/31/2026; '
                   '1 employee; manager Mr. Pavel Bresker; business started locally 10/09/2012.'),
         limitations=('Platform display retrieved 2026-11-10. The licence expiry printed by BBB conflicts with '
                      'the CSLB record and is treated as a stale third-party field.')),
    dict(id='BBB-FAST',
         url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/fast-response-plumbing-rooter-1116-387063',
         title='BBB business profile — Fast Response Plumbing & Rooter',
         publisher='Better Business Bureau', kind='review-platform', checked=TODAY, retrieval='direct',
         supports=('Not BBB accredited; A+ display; licence 1024971 recorded with an expiry of 03/31/2027; 19 '
                   'employees; business started 09/15/2007; premises listed at 4444 Geary Blvd #203.'),
         limitations=('Platform display retrieved 2026-11-10. The listed premises differ from the CSLB registered '
                      'address. BBB ratings are BBB\'s opinion.')),
    dict(id='ANGI-ACE',
         url='https://www.angi.com/companylist/us/ca/san-francisco/ace-plumbing-and-rooter-inc-reviews-208758.htm',
         title='Angi profile — Ace Plumbing & Rooter',
         publisher='Angi', kind='review-platform', checked=TODAY, retrieval='direct',
         supports=('Angi displays "4.8 overall" and category sub-scores of quality 4.8, value 4.6, '
                   'professionalism 4.8, responsiveness 4.8 and punctuality 4.8.'),
         limitations=('Platform display retrieved 2026-11-10; review text includes both praise and a documented '
                      'dissatisfied account. Aggregation method is Angi\'s and is not comparable with BBB.')),
    dict(id='ANGI-ATLAS',
         url='https://www.angi.com/companylist/us/ca/san-francisco/atlas-plumbing-and-rooter-reviews-317113.htm',
         title='Angi profile — Atlas Plumbing & Rooter',
         publisher='Angi', kind='review-platform', checked=TODAY, retrieval='direct',
         supports='The Angi profile page for Atlas Plumbing & Rooter, San Francisco, resolves and is linked from BBB.',
         limitations='Page shell retrieved; no review text or numeric rating was captured, so nothing is asserted.'),
    dict(id='REDDIT-TL',
         url='https://www.reddit.com/r/Plumbing/comments/170tvds/stuck_trip_lever_old_bathtub_wouldnt_turn_up_or/',
         title='r/Plumbing — stuck trip lever on an old bathtub (community thread)',
         publisher='Reddit community thread', kind='community-forum', checked=TODAY, retrieval='direct',
         supports=('Field accounts describe seized or fused drop cylinders, linkages that break on removal, and '
                   'plumbers choosing to replace the waste-and-overflow rather than extract it.'),
         limitations=('Anonymous, unverified anecdotes about other tubs. Not an official source, not this unit, and '
                      'not treated as evidence about any named provider. It is cited only as context for the '
                      'difficulty the owner reports.')),
]
existing = {s['id'] for s in src['rows']}
for s in NEW_SOURCES:
    if s['id'] not in existing:
        src['rows'].append(s)
        note(f"sources.json: added {s['id']} ({s['kind']}, direct {TODAY})")
    else:
        src['rows'] = [s if x['id'] == s['id'] else x for x in src['rows']]
save('sources.json', src)

# --------------------------------------------------------------------------
# 2. Providers: re-stamp timestamps, add platform fields, record new notes.
# --------------------------------------------------------------------------
prov = load('providers.json')
prov['as_of'] = TODAY
for p in prov['rows']:
    if p.get('license'):
        p['source_timestamp'] = '11/9/2026 4:49 PM (CSLB page stamp); re-read 2026-11-10'
    p.setdefault('bbb_rating', None)
    p.setdefault('bbb_accredited', None)
    p.setdefault('bbb_url', None)
    p.setdefault('angi_rating_display', None)
    p.setdefault('angi_url', None)
    p.setdefault('platform_note', '')

PATCH = {
    'P-02': dict(bbb_rating='A+ (displayed)', bbb_accredited=True,
                 bbb_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/ace-plumbing-and-rooter-inc-1116-58941',
                 angi_rating_display='4.8/5 overall (displayed)',
                 angi_url='https://www.angi.com/companylist/us/ca/san-francisco/ace-plumbing-and-rooter-inc-reviews-208758.htm',
                 platform_note=('Directly retrieved 2026-11-10: BBB accredited since 08/01/2004 with an A+ display and '
                                'a 4.76/5 average over 51 reviews as displayed; Angi displays 4.8 overall. Reviews '
                                'describe water-heater, sewer and apartment-building work, not this repair.')),
    'P-03': dict(bbb_rating='B- (displayed)', bbb_accredited=False,
                 bbb_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/heises-plumbing-inc-1116-41584',
                 platform_note=('Directly retrieved 2026-11-10: BBB shows "Not accredited", a B- display, 1 complaint in '
                                'the last 3 years recorded as not responded to, and a single negative review. BBB also '
                                'publishes licence 787733, which CSLB shows as expired since 03/31/2023 (F-47).')),
    'P-04': dict(bbb_rating='Not Rated', bbb_accredited=False,
                 bbb_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492',
                 platform_note=('Directly retrieved 2026-11-10: BBB "Not Rated", not accredited, 1 employee. BBB '
                                'prints a licence expiry of 10/31/2026 while CSLB shows 10/31/2028; the CSLB record is '
                                'used and the difference is flagged (F-49).')),
    'P-06': dict(bbb_rating='A+ (displayed)', bbb_accredited=False,
                 bbb_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/fast-response-plumbing-rooter-1116-387063',
                 platform_note=('Directly retrieved 2026-11-10: BBB A+ display, not accredited, 19 employees, licence '
                                '1024971 with an expiry matching CSLB. BBB lists premises at 4444 Geary Blvd #203, not '
                                'the CSLB registered address.')),
    'P-25': dict(bbb_rating='A+ (displayed)', bbb_accredited=True,
                 bbb_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/atlas-plumbing-rooter-1116-116593',
                 angi_url='https://www.angi.com/companylist/us/ca/san-francisco/atlas-plumbing-and-rooter-reviews-317113.htm',
                 additional_status=('CSLB phone (650) 871-9863 differs from the company contact page (415) 849-2346 and '
                                    'from the BBB profile (415) 845-9199; all three are source-linked, none is silently '
                                    'substituted.'),
                 platform_note=('BBB profile directly re-read 2026-11-10: accredited since 06/03/2021, A+ display, '
                                'licence 868994 with an expiry of 3/31/2028 matching CSLB, business started 12/08/2005. '
                                'The BBB "About" text lists bathtub repair and replacement among its services.')),
}
for p in prov['rows']:
    if p['id'] in PATCH:
        p.update(PATCH[p['id']])
        note(f"providers.json: {p['id']} gained directly-retrieved BBB/Angi fields")

by_pid = {p['id']: p for p in prov['rows']}
by_pid['P-03']['flags'] = sorted(set(by_pid['P-03']['flags'] + ['F-47', 'F-50']))
by_pid['P-04']['flags'] = sorted(set(by_pid['P-04']['flags'] + ['F-49']))
by_pid['P-05']['flags'] = sorted(set(by_pid['P-05']['flags'] + ['F-48']))
by_pid['P-06']['flags'] = sorted(set(by_pid['P-06']['flags'] + ['F-50']))
by_pid['P-02']['flags'] = sorted(set(by_pid['P-02']['flags'] + ['F-50']))
by_pid['P-25']['flags'] = sorted(set(by_pid['P-25']['flags'] + ['F-51']))
by_pid['P-05']['fit'] = ('Owner-supplied estimate provider. Identity must be confirmed: the quoted "Bay Area Plumbing" '
                         'matches the active San Francisco sole ownership #757796, while a similarly named entity, '
                         '"BAY AREA PLUMBING BAP INC" #961936, is inactive and appears on a separate BBB profile (F-48).')
save('providers.json', prov)

# --------------------------------------------------------------------------
# 3. Reviews: keep numeric fields blank, add labelled platform displays.
# --------------------------------------------------------------------------
rev = load('reviews.json')
rev['as_of'] = TODAY
for r in rev['rows']:
    r.setdefault('display_rating', None)
    r.setdefault('retrieval', 'web-search excerpt only; business page not retrieved (Yelp HTTP 403)')
    r.setdefault('retrieved', '2026-11-08')

NEW_REVIEWS = [
    dict(id='RV-12', provider='Ace Plumbing & Rooter', platform='BBB',
         observation=('Accredited since 08/01/2004, A+ display, 4.76/5 average over 51 customer reviews as displayed. '
                      'Visible reviews describe water heaters, sewer traps and an apartment building.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/ace-plumbing-and-rooter-inc-1116-58941/customer-reviews',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071',
         source_ids=['BBB-ACE', 'CSLB-829071'], display_rating='4.76/5 (51 reviews, as displayed)',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit=('Platform display; reviews are self-selected and none describes a stuck trip lever or ceiling '
                'restoration. Not used as a ranking score.')),
    dict(id='RV-13', provider='Ace Plumbing & Rooter', platform='Angi',
         observation=('Angi displays 4.8 overall with quality 4.8, value 4.6, professionalism 4.8, responsiveness 4.8 '
                      'and punctuality 4.8. Review text includes praise and at least one documented dissatisfied account.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.angi.com/companylist/us/ca/san-francisco/ace-plumbing-and-rooter-inc-reviews-208758.htm',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071',
         source_ids=['ANGI-ACE', 'CSLB-829071'], display_rating='4.8/5 overall (as displayed)',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit='Aggregation method is Angi\'s; not comparable with BBB; not this exact job.'),
    dict(id='RV-14', provider="Heise’s Plumbing", platform='BBB',
         observation=('BBB shows "Not accredited", a B- display, 1 complaint in the last 3 years recorded as not '
                      'responded to, and 1 customer review describing an uncontained sewage spill.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/heises-plumbing-inc-1116-41584',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1089561',
         source_ids=['BBB-HEISE', 'CSLB-1089561', 'CSLB-787733'], display_rating='B- (as displayed)',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit=('Complaint and review were not read in full and the business response was not verified; the account '
                'is about a sewer job, not this repair. BBB rating is BBB\'s opinion.')),
    dict(id='RV-15', provider='Expert Plumbing Solutions', platform='BBB',
         observation=('BBB shows "Not Rated" and not accredited; licence 977638 is recorded with an expiry of '
                      '10/31/2026, which conflicts with the CSLB expiry of 10/31/2028.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638',
         source_ids=['BBB-EXPERT', 'CSLB-977638'], display_rating='Not Rated',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit='No review evidence; only licence and contact fields were captured (F-49).'),
    dict(id='RV-16', provider='Fast Response Plumbing & Rooter', platform='BBB',
         observation=('BBB shows an A+ display, not accredited, 19 employees, and licence 1024971 with an expiry '
                      'matching CSLB. Premises are listed at 4444 Geary Blvd #203.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/fast-response-plumbing-rooter-1116-387063',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971',
         source_ids=['BBB-FAST', 'CSLB-1024971'], display_rating='A+ (as displayed)',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit='No review text captured; A+ is BBB\'s display, not a quality finding about this job.'),
    dict(id='RV-17', provider='Atlas Plumbing & Rooter', platform='BBB',
         observation=('BBB shows accredited since 06/03/2021, an A+ display, 20 employees, business started '
                      '12/08/2005, and licence 868994 with an expiry of 3/31/2028 matching CSLB. Its service list '
                      'includes bathtub repair and replacement.'),
         rating=None, review_count=None, verified=False,
         review_url='https://www.bbb.org/us/ca/san-francisco/profile/plumber/atlas-plumbing-rooter-1116-116593',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=868994',
         source_ids=['BBB-ATLAS', 'CSLB-868994'], display_rating='A+ (as displayed)',
         retrieval='direct page retrieval', retrieved=TODAY,
         limit='Service list is a business category, not a completed-job record for this repair.'),
    dict(id='RV-18', provider='Atlas Plumbing & Rooter', platform='Angi',
         observation='The Angi profile page resolves and is linked from the BBB profile; no rating or review text was captured.',
         rating=None, review_count=None, verified=False,
         review_url='https://www.angi.com/companylist/us/ca/san-francisco/atlas-plumbing-and-rooter-reviews-317113.htm',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=868994',
         source_ids=['ANGI-ATLAS', 'CSLB-868994'], display_rating=None,
         retrieval='direct page retrieval', retrieved=TODAY, limit='Nothing asserted beyond page resolution.'),
    dict(id='RV-19', provider='Rapid Flow Plumbing & Rooter', platform='Angi',
         observation='The Angi profile URL pattern resolved to a generic template with no business-specific review content.',
         rating=None, review_count=None, verified=False,
         review_url='https://www.angi.com/companylist/us/ca/san-francisco/rapid-flow-plumbing-and-rooter-reviews-1.htm',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649',
         source_ids=['CSLB-1115649'], display_rating=None,
         retrieval='direct page retrieval', retrieved=TODAY,
         limit='No Angi record for this business was confirmed; absence of a profile is not evidence either way.'),
]
have = {r['id'] for r in rev['rows']}
for r in NEW_REVIEWS:
    if r['id'] not in have:
        rev['rows'].append(r)
        note(f"reviews.json: added {r['id']} ({r['platform']}, {r['retrieval']})")
for r in rev['rows']:
    if r['id'] == 'RV-01':
        r['retrieval'] = 'web-search excerpt only (Yelp HTTP 403 again on 2026-11-10)'
        r['retrieved'] = TODAY
save('reviews.json', rev)

# --------------------------------------------------------------------------
# 4. Flags: correct F-14/F-42 and add F-47..F-52.
# --------------------------------------------------------------------------
flags = load('flags.json')
flags['as_of'] = TODAY
fb = {f['id']: f for f in flags['rows']}
fb['F-14']['detail'] = ('Yelp business and search pages still returned HTTP 403 on 2026-11-10, so no Yelp rating, count '
                        'or review text is published. BBB and Angi, however, were retrieved directly on 2026-11-10, so '
                        'the earlier blanket statement that review platforms were blocked is narrowed to Yelp.')
fb['F-14']['action'] = ('Keep Yelp blank; publish BBB/Angi displays with the platform named, the retrieval date and a '
                        'clear "platform display, not independently verified" label; never convert them into a score.')
fb['F-14']['status'] = 'Partly resolved 2026-11-10 — Yelp still blocked, BBB/Angi now retrieved'
fb['F-14']['source_ids'] = sorted(set(fb['F-14']['source_ids'] + ['BBB-ACE', 'BBB-HEISE', 'ANGI-ACE']))
fb['F-42']['detail'] = ('Atlas publishes three different numbers: CSLB (650) 871-9863, its own contact page '
                        '(415) 849-2346, and the BBB profile (415) 845-9199. The CSLB number is the licensed record; '
                        'the others are business-supplied and none is silently substituted.')
fb['F-42']['source_ids'] = sorted(set(fb['F-42']['source_ids'] + ['BBB-ATLAS', 'ATLAS-CONTACT']))

NEW_FLAGS = [
    dict(id='F-47', severity='High', category='Provider identity', status='Open',
         title="Heise's BBB profile carries a different, expired licence number",
         detail=('BBB records licence 787733 for "Heise\'s Plumbing, Inc." at 260 Ocean Ave. CSLB shows #787733 '
                 'expired 03/31/2023, cancelled after expiration, with a Secretary of State dissolution recorded '
                 '02/12/2025. The active business is TARO GROUP INC dba HEISES PLUMBING #1089561, issued 04/06/2022. '
                 'BBB also conflicts with the company site on founding year (1950 vs "since 1954").'),
         action=('Ask the provider to name the exact legal entity and licence number that will appear on the '
                 'contract, and verify that number on CSLB on signing day. Do not rely on the BBB licence field.'),
         source_ids=['CSLB-787733', 'CSLB-1089561', 'BBB-HEISE', 'HEISE'],
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=787733'),
    dict(id='F-48', severity='High', category='Provider identity', status='Open',
         title='"Bay Area Plumbing" matches two different CSLB entities',
         detail=('The owner-supplied $550 estimate names "Bay Area Plumbing". CSLB #757796 is a San Francisco sole '
                 'ownership licence that is current and active; CSLB #961936 is "BAY AREA PLUMBING BAP INC" of '
                 'Concord, shown inactive after a workers-compensation exemption cancellation on 09/14/2026, and a '
                 'separate BBB profile in Pleasant Hill publishes that number.'),
         action=('Before relying on the $550 figure, require the quote to name the licence number and legal entity, '
                 'then verify that number on CSLB. Treat the estimate as unattributable until then.'),
         source_ids=['CSLB-757796', 'CSLB-961936', 'BBB-EXPERT'],
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=961936'),
    dict(id='F-49', severity='Low', category='Third-party data', status='Open',
         title='BBB licence-expiry field for Expert Plumbing Solutions is stale',
         detail=('BBB prints an expiry of 10/31/2026 for licence 977638; the CSLB record read on 2026-11-10 shows '
                 '10/31/2028. Third-party directory fields are secondary copies and can lag the regulator.'),
         action='Use the CSLB record as the authority for expiry and status; never quote a directory copy as the licence fact.',
         source_ids=['BBB-EXPERT', 'CSLB-977638'],
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638'),
    dict(id='F-50', severity='Medium', category='Reviews', status='Open',
         title='Platform-displayed ratings are not comparable and are excluded from scoring',
         detail=('Direct retrieval on 2026-11-10 produced BBB displays (Ace A+, 4.76/5 over 51; Heise B-; Fast A+; '
                 'Atlas A+; Expert Not Rated) and an Angi display for Ace (4.8 overall). The aggregation methods and '
                 'populations differ between platforms and the underlying reviews were not audited.'),
         action=('Publish them as labelled platform displays with the retrieval date, keep every numeric rating field '
                 'blank, and keep them out of the weighted hire order.'),
         source_ids=['BBB-ACE', 'BBB-HEISE', 'BBB-FAST', 'BBB-ATLAS', 'ANGI-ACE', 'CSLB-SEARCH'],
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
    dict(id='F-51', severity='Medium', category='Reviews', status='Open',
         title="No review anywhere confirms this exact stuck-lever extraction or ceiling restoration",
         detail=('All review evidence retrieved on 2026-11-10 concerns other work: water heaters, sewers, drains, '
                 'faucets and general apartment maintenance. The closest scope evidence remains Heise\'s '
                 'self-published Ingleside case, which is adjacent rather than this job.'),
         action=('Ask each shortlisted provider for a specific reference for a seized trip lever or a below-ceiling '
                 'waste-and-overflow replacement, including the restoration step.'),
         source_ids=['BBB-ACE', 'BBB-HEISE', 'HEISE-INGLESIDE', 'OWNER'],
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
    dict(id='F-52', severity='Medium', category='Permit', status='Open',
         title='A B-only licence may not obtain this plumbing permit on its own',
         detail=('SF.gov states that contractors with only a B licence get plumbing permits immediately only when the '
                 'permit is directly associated with a kitchen or bath permit; otherwise plumbing scope is approved '
                 'case by case. A standalone overflow repair is not a kitchen or bath remodel permit.'),
         action=('Confirm permit-holder eligibility for the exact scope before hiring; a B-only lead needs the C-36 '
                 'party named as permit holder, or written DBI approval.'),
         source_ids=['SF-REMODEL', 'SF-PERMIT', 'BPC-7057'],
         official_url='https://www.sf.gov/apply-kitchen-or-bath-remodel-permit'),
]
fh = {f['id'] for f in flags['rows']}
for f in NEW_FLAGS:
    if f['id'] not in fh:
        flags['rows'].append(f)
        note(f"flags.json: added {f['id']} — {f['title']}")
save('flags.json', flags)

# --------------------------------------------------------------------------
# 5. Compliance: quote the exemption text exactly and add two permit facts.
# --------------------------------------------------------------------------
comp = load('compliance.json')
comp['as_of'] = TODAY
cb = {c['id']: c for c in comp['rows']}
cb['C-02']['rule'] = ('SF Plumbing Code §104.2 "Exempt Work" lists: (1) repair of leaks not requiring cutting into or '
                      'removing piping; (2) unstopping of traps, sewers, vents or waste pipes not requiring cutting '
                      'into or removal of traps or piping; (3) replacement, repair or maintenance of faucets, angle '
                      'stops, hose bibbs or roof drain not requiring cutting into or removal of piping.')
cb['C-02']['application'] = ('A seized trip lever that cannot be freed from the overflow opening is not on this list; '
                             'the exemptions turn on not cutting into or removing piping, which is exactly the '
                             'condition in dispute here.')
cb['C-02']['source_ids'] = ['SF-CODE-104', 'SF-PERMIT']
NEW_COMP = [
    dict(id='C-13', topic='Fixture replacement without fee', source_ids=['SF-CODE-104'], official_url=None,
         rule=('SF Plumbing Code §104.5 provides that "the replacement of a plumbing fixture or a gas appliance '
               'without a change in drainage, piping or venting shall not require the payment of permit issuance fee."'),
         application=('Relevant only if the scope is a like-for-like fixture change with no drainage or piping change. '
                      'A stuck assembly behind the wall is unlikely to meet that condition, and the fee waiver is not '
                      'a permit exemption.')),
    dict(id='C-14', topic='B-licence plumbing permits', source_ids=['SF-REMODEL', 'SF-PERMIT'], official_url=None,
         rule=('SF.gov states that contractors with only a B licence get electrical and plumbing permits right away '
               'only when those permits are directly associated with a kitchen or bath permit; otherwise plumbing '
               'scope is approved based on the scope of work.'),
         application=('A standalone overflow repair is not a kitchen or bath remodel permit, so a B-only lead may need '
                      'the C-36 party or written DBI approval to be permit holder.')),
]
ch = {c['id'] for c in comp['rows']}
for c in NEW_COMP:
    c['official_url'] = 'https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830' if c['id'] == 'C-13' else 'https://www.sf.gov/apply-kitchen-or-bath-remodel-permit'
    if c['id'] not in ch:
        comp['rows'].append(c)
        note(f"compliance.json: added {c['id']} — {c['topic']}")
save('compliance.json', comp)

# --------------------------------------------------------------------------
# 6. Technical: one new row for the field-reported failure modes.
# --------------------------------------------------------------------------
tech = load('technical.json')
tech['as_of'] = TODAY
NEW_TECH = [dict(
    id='T-09', topic='Field-reported failure modes',
    statement=('Practitioner accounts of seized trip levers describe drop cylinders fused by mineral scale, linkages '
               'that break when forced, and plumbers who replace the waste-and-overflow instead of extracting it. '
               'This matches the owner report that several plumbers declined to force it from above.'),
    source_ids=['WATCO', 'REDDIT-TL'],
    official_url='https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf',
    status='Community field accounts; not this unit',
    limit=('Anonymous forum anecdotes, not official guidance and not evidence about any named provider. They explain '
           'why forcing is avoided; they do not establish that removal from above is impossible here.')),
]
th = {t['id'] for t in tech['rows']}
for t in NEW_TECH:
    if t['id'] not in th:
        tech['rows'].append(t)
        note('technical.json: added T-09 field-reported failure modes')
save('technical.json', tech)

# --------------------------------------------------------------------------
# 7. Requirements: five new checks drawn from the new evidence.
# --------------------------------------------------------------------------
req = load('requirements.json')
req['as_of'] = TODAY
NEW_REQ = [
    dict(id='R-43', category='Contracting entity', origin='Proposed control',
         requirement='The quote and contract must name the same legal entity and CSLB licence number that will do the work.',
         basis='BBB publishes licence 787733 for Heise\'s while CSLB shows that licence expired, and "Bay Area Plumbing" matches two different licence records.',
         acceptance_check='Licence number on the contract is verified current on CSLB on signing day and matches the legal entity on the contract.',
         source_ids=['CSLB-787733', 'CSLB-1089561', 'CSLB-961936', 'CSLB-757796'],
         status='Open — no provider has issued a document',
         legacy_ids='new 2026-11-10', official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
    dict(id='R-44', category='Reviews', origin='Proposed control',
         requirement='Request a specific reference for a seized trip lever or a below-ceiling waste-and-overflow replacement.',
         basis='No review retrieved on 2026-11-10 describes this exact extraction or the ceiling restoration.',
         acceptance_check='Provider supplies at least one reference matching the access route, or states in writing that it has none.',
         source_ids=['BBB-ACE', 'BBB-HEISE', 'HEISE-INGLESIDE'],
         status='Open', legacy_ids='new 2026-11-10',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
    dict(id='R-45', category='Reviews', origin='Proposed control',
         requirement='Any platform rating quoted to the owner must be evidenced by a directly retrieved platform page with its date.',
         basis='BBB and Angi displays differ in method and population and were only retrievable as displays, not audited reviews.',
         acceptance_check='Every rating shown in a provider\'s own material can be traced to a retrievable page, and no rating is used to rank.',
         source_ids=['BBB-ACE', 'ANGI-ACE', 'CSLB-SEARCH'],
         status='Open', legacy_ids='new 2026-11-10',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
    dict(id='R-46', category='Permit', origin='Official rule',
         requirement='Confirm who may hold the plumbing permit for a standalone overflow repair before scheduling.',
         basis='SF.gov ties immediate B-contractor plumbing permits to kitchen or bath permits; §104.5 also waives the issuance fee only for fixture swaps with no drainage or piping change.',
         acceptance_check='Written permit route names the permit holder and licence class, or a DBI determination for this address and scope.',
         source_ids=['SF-REMODEL', 'SF-PERMIT', 'SF-CODE-104'],
         status='Open — DBI determination not obtained', legacy_ids='new 2026-11-10',
         official_url='https://www.sf.gov/apply-plumbing-and-mechanical-permit'),
    dict(id='R-47', category='Licence standing', origin='Proposed control',
         requirement='Re-check licence status, bond and workers-compensation record within 30 days of the work date.',
         basis='CSLB records are point-in-time; one licence on this register carries a future-suspension warning and another is already suspended.',
         acceptance_check='A dated CSLB record for the contracting licence shows current-and-active status with bond and workers-compensation coverage at signing.',
         source_ids=['CSLB-1009195', 'CSLB-1027286', 'CSLB-SEARCH'],
         status='Open', legacy_ids='new 2026-11-10',
         official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
]
rh = {r['id'] for r in req['rows']}
for r in NEW_REQ:
    if r['id'] not in rh:
        req['rows'].append(r)
        note(f"requirements.json: added {r['id']} — {r['category']}")
save('requirements.json', req)

# --------------------------------------------------------------------------
# 8. Ranking: re-stamp, attach review evidence, add the date-stamped note.
# --------------------------------------------------------------------------
rk = load('ranking.json')
rk['as_of'] = TODAY
rk['method_note'] = ('Editorial decision support, not a verified performance or quality rating. Scores use only the fields '
                     'on the official CSLB records, company-published service statements and the owner-supplied quote '
                     'wording, each re-read on 2026-11-10. Platform ratings retrieved on 2026-11-10 are published '
                     'beside the ranking but are deliberately excluded from the score, because the platforms '
                     'aggregate different populations with different methods and the underlying reviews were not '
                     'audited. No provider was contacted, no reference was taken and no availability or price was '
                     'confirmed.')
rk['final_verification_note'] = ('2026-11-10 independent re-verification: all 24 CSLB records re-read (plus two newly '
                                 'identified records, #787733 expired and #961936 inactive), and the code, fee, company '
                                 'and manufacturer sources re-read. BBB and Angi profiles were retrieved directly for the '
                                 'first time; Yelp remained blocked. The weighted order is unchanged because no new '
                                 'evidence measured this exact job, and platform ratings are excluded from scoring. New '
                                 'flags F-47 to F-52 record the entity mismatches, the stale BBB licence field, the '
                                 'rating-comparability limit, the missing exact-job review and the B-licence permit limit.')
REVIEW_EVID = {
    'P-02': ('BBB A+ display, accredited since 2004, 4.76/5 over 51 reviews as displayed; Angi 4.8 overall. No review describes this repair.'),
    'P-03': ('BBB B- display, not accredited, 1 complaint in 3 years recorded as not responded to. Its BBB licence field (#787733) is expired on CSLB.'),
    'P-01': 'No BBB or Angi record was confirmed for this business in the 2026-11-10 retrieval.',
    'P-04': 'BBB "Not Rated", not accredited; no review evidence captured.',
    'P-05': 'No BBB or Angi record was confirmed for the San Francisco entity; a similarly named BAP Inc. profile publishes an inactive licence.',
    'P-06': 'BBB A+ display, not accredited; no review text describes this repair.',
    'P-25': 'BBB A+ display, accredited since 2021, licence field matches CSLB; service list includes bathtub repair.',
}
for r in rk['ranked'] + [rk['partner']] + rk['not_recommended']:
    pid = r.get('provider_id')
    r['review_evidence'] = REVIEW_EVID.get(pid, r.get('review_evidence', ''))
    if pid in by_pid:
        p = by_pid[pid]
        r['bbb_url'] = p.get('bbb_url')
        r['angi_url'] = p.get('angi_url')
        r['bbb_rating'] = p.get('bbb_rating')
save('ranking.json', rk)
note('ranking.json: re-stamped 2026-11-10, review evidence attached, scoring method note updated')

# --------------------------------------------------------------------------
# 9. Action plan (new page data).
# --------------------------------------------------------------------------
plan = {
    'as_of': TODAY,
    'intro': ('A sequenced plan that turns the research into one serviceable outcome. Each step names who does it, what '
              'must be true before moving on, and the official source behind the requirement. Steps are ordered; do not '
              'skip a gate.'),
    'steps': [
        dict(id='A-01', phase='Before you call', owner='Owner',
             action='Photograph the overflow plate, the tub shoe and the storage-unit ceiling, and note the building age if known.',
             why='Every provider asked so far had to guess the assembly; the model and access govern whether a tub-side attempt is even possible.',
             done_when='Photos exist and the assembly type is either identified or explicitly recorded as unknown.',
             source_ids=['OWNER', 'WATCO'],
             official_url='https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf'),
        dict(id='A-02', phase='Before you call', owner='Owner',
             action='Request the permit determination in writing from DBI for this address and scope, using the published permit line and §104.2 exemptions.',
             why='A permit is required before cutting into or replacing pipes; the exemptions turn on not cutting into or removing piping, which is the disputed point.',
             done_when='A written DBI answer states whether a permit is required and which fee category applies.',
             source_ids=['SF-PERMIT', 'SF-CODE-104', 'SF-DBI'],
             official_url='https://www.sf.gov/apply-plumbing-and-mechanical-permit'),
        dict(id='A-03', phase='Before you call', owner='Owner',
             action='Confirm authority over the storage unit and serve tenants the written entry notice required for necessary repairs.',
             why='Work on the ceiling below and entry to the occupied unit both need lawful access; notice must state date, approximate time and purpose.',
             done_when='Storage access is confirmed in writing and each affected tenancy has dated notice or recorded consent.',
             source_ids=['CIV-1954', 'OWNER'],
             official_url='https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.'),
        dict(id='A-04', phase='Shortlist', owner='Owner',
             action='Send one identical written scope to the top five leads, with the same access options and the same question set.',
             why='The three supplied prices cover three different scopes, so they cannot be compared. One scope is the only way to get comparable numbers.',
             done_when='Each lead has received the same scope text and a deadline for a written response.',
             source_ids=['OWNER', 'CSLB-CONTRACT', 'CSLB-829071'],
             official_url='https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx'),
        dict(id='A-05', phase='Shortlist', owner='Provider',
             action='Ask each lead to name the exact legal entity, licence number, permit holder and restoration party that will appear on the contract.',
             why='BBB publishes an expired licence for one lead and "Bay Area Plumbing" matches two different CSLB entities; the contract must be attributable.',
             done_when='A written answer names a licence number that is current and active on CSLB and matches the contracting entity.',
             source_ids=['CSLB-787733', 'CSLB-961936', 'CSLB-SEARCH'],
             official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
        dict(id='A-06', phase='Shortlist', owner='Provider',
             action='Ask for one specific reference for a seized trip lever or a below-ceiling waste-and-overflow replacement.',
             why='No retrieved review describes this exact repair; the nearest evidence is an adjacent published case.',
             done_when='A reference is provided that matches the access route, or the provider states in writing that it has none.',
             source_ids=['HEISE-INGLESIDE', 'BBB-ACE', 'BBB-HEISE'],
             official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
        dict(id='A-07', phase='Scope design', owner='Provider',
             action='Require a two-stage scope: tub-side attempt first, then below-ceiling access only with a written opening and restoration plan.',
             why='Manufacturer instructions support service from the overflow opening, while the stuck assembly may not release; the fallback must be priced and planned, not improvised.',
             done_when='The quote states both stages, the trigger for moving to stage two, and the price of each.',
             source_ids=['WATCO', 'REDDIT-TL', 'HEISE-INGLESIDE'],
             official_url='https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf'),
        dict(id='A-08', phase='Scope design', owner='Provider',
             action='Name the C-9 drywall party and price the patch, texture and paint as a line item.',
             why='C-9 covers gypsum board installation, taping and texturing; the plumbing classification does not by itself prove drywall self-performance.',
             done_when='The restoration party is named with its licence number and the finish scope is a priced line.',
             source_ids=['CSLB-C9', 'CSLB-C36', 'CSLB-995163'],
             official_url='https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9'),
        dict(id='A-09', phase='Occupied unit', owner='Provider',
             action='Agree the occupied-unit plan: working hours, dust containment, water shut-off window, contents protection and daily cleanup.',
             why='Tenants occupy the unit above the storage space and the finishes may be pre-1978; containment protects both the occupants and the work.',
             done_when='The plan is in the contract, with the notice dates attached.',
             source_ids=['CIV-1954', 'EPA-RRP', 'EPA-ASBESTOS'],
             official_url='https://www.epa.gov/lead/lead-renovation-repair-and-painting-program'),
        dict(id='A-10', phase='Occupied unit', owner='Owner',
             action='Screen the finishes for lead and asbestos before any cutting if the building predates 1978 or the material is suspect.',
             why='Federal lead-safe rules apply to paid paint-disturbing work in pre-1978 housing, and suspect asbestos should be sampled by accredited professionals rather than disturbed.',
             done_when='A screening result or a documented age exemption exists before demolition.',
             source_ids=['EPA-RRP', 'EPA-ASBESTOS'],
             official_url='https://www.epa.gov/lead/lead-renovation-repair-and-painting-program'),
        dict(id='A-11', phase='Award', owner='Owner',
             action='Verify the licence, bond and workers-compensation record on CSLB on the day of signing, and check the complaint disclosure link.',
             why='Records are point-in-time: one licence here carries a future-suspension warning and another is already suspended for a bond lapse.',
             done_when='A dated CSLB screenshot for the contracting licence is filed with the contract.',
             source_ids=['CSLB-SEARCH', 'CSLB-1009195', 'CSLB-1027286', 'DG-COMPLAINT'],
             official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx'),
        dict(id='A-12', phase='Award', owner='Owner',
             action='Sign a written contract with the lawful down payment, a completion date, written change orders and a leak/function test before closing.',
             why='A written contract is required over $500, the down payment is capped at the lesser of 10% or $1,000, and inspection must happen before pipes are covered.',
             done_when='Contract, payment schedule and change-order procedure are signed and the inspection step is scheduled.',
             source_ids=['CSLB-CONTRACT', 'BPC-7048', 'SF-PERMIT'],
             official_url='https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx'),
        dict(id='A-13', phase='Close-out', owner='Provider',
             action='Test the drain closed and open, document the repair with photos, and agree future service access.',
             why='The original failure is a seized linkage; a functional test and a recorded access route are what prevent a repeat.',
             done_when='A closed-drain water test holds, the ceiling is restored and photographed, and the access method is recorded.',
             source_ids=['WATCO', 'SF-CODE-104', 'CSLB-C9'],
             official_url='https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf'),
    ],
}
(DATA / 'action_plan.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
note(f"action_plan.json: created with {len(plan['steps'])} sequenced steps")

# Deployment record is regenerated by the build; keep it consistent with today.
dep = load('deployment.json')
dep['status'] = dep.get('status', '')
save('deployment.json', dep)

print('\n'.join(f'- {c}' for c in changes))
print(f"\n{len(changes)} data corrections applied for {TODAY}")
sys.exit(0)

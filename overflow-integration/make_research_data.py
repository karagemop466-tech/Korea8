"""One-time transcription of directly reviewed sources; not a live scraper.
Run from repo root. The JSON, not this script, is the reviewed source of record.
"""
import json, sys
from pathlib import Path
if (Path(__file__).parent/'data'/'providers.json').exists() and '--force' not in sys.argv:
 print('Final registers already exist; this one-time CSLB transcription helper is skipped. Use the JSON records as authoritative.'); sys.exit(0)
D=Path(__file__).parent/'data'
def save(name,obj): (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def cslb(n): return f'https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={n}'
sources=[]
def src(i,url,title,publisher,kind='official-government',method='direct',supports='',limits=''):
 sources.append(dict(id=i,url=url,title=title,publisher=publisher,kind=kind,checked='2026-11-07',retrieval=method,supports=supports,limitations=limits))
# Each tuple is transcribed from the corresponding directly retrieved CSLB page.
# number, legal name, classifications, city, phone, expiry, workers-comp summary, source time, extra
rows=[
('1115649','RAPID FLOW PLUMBING & ROOTER INC','B; C-36','SAN FRANCISCO','(415) 866-8401','2028-01-31','Exempt: certified no employees','12:18:31 PM',''),
('829071','ACE PLUMBING & ROOTER','C-36; A; C-4; C-16; B; C-10','SAN FRANCISCO','(415) 824-6444','2027-06-30','Policy recorded; expires 07/13/2027','12:18:55 PM',''),
('1089561','TARO GROUP INC · dba HEISES PLUMBING','C-36; C-10; A; C-20','SAN FRANCISCO','(415) 333-0704','2028-04-30','Policy recorded; expires 01/11/2027','12:17:58 PM',''),
('977638','EXPERT PLUMBING SOLUTIONS','C-36','SAN FRANCISCO','(415) 531-5340','2028-10-31','Policy recorded; expires 07/19/2027','12:17:23 PM',''),
('757796','BAY AREA PLUMBING','C-36','SAN FRANCISCO','(415) 668-8000','2027-01-31','Exempt: certified no employees','12:16:50 PM',''),
('1024971','JOSEPH TINSLEY · dba FAST RESPONSE PLUMBING AND ROOTER','C-36','SAN FRANCISCO','(415) 596-6115','2027-03-31','Policy recorded; expires 12/18/2026','12:18:12 PM',''),
('749536','SAVE - ON - INTERIOR','B; C-36','SAN FRANCISCO','(415) 668-8000','2028-05-31','Exempt: certified no employees','12:18:40 PM','CSLB miscellaneous entries: 11/06/2015 cash deposit letter $15,000; 01/14/2016 follow-up letter. No interpretation supplied.'),
('1096552','WE DO CONSTRUCTION INC','B; C-36','SAN FRANCISCO','(415) 416-5494','2028-09-30','Policy recorded; expires 11/14/2027','12:18:55 PM',''),
('392967','AYOOB & PEERY PLUMBING CO INC','B; C-4; C-16; C-36; C-20','SAN FRANCISCO','(415) 550-0975','2028-09-30','Policy recorded; expires 08/31/2027','12:18:38 PM',''),
('995163','BERNAL HILL DRYWALL INC','C-9; B','SAN FRANCISCO','(415) 533-8274','2028-07-31','Policy recorded; expires 03/10/2027','12:25:05 PM',''),
('1106131','SF BUILDING GROUP','B','SOUTH SAN FRANCISCO','(415) 297-2246','2027-06-30','Exempt: certified no employees','12:18:25 PM',''),
('1105133','HARP SERVICES · dba 24/7 SF HANDYMAN & REMODELING SERVICE','B-2','SAN FRANCISCO','(415) 304-1559','2027-05-31','Policy recorded; expires 04/11/2027','12:19:07 PM',''),
('1009195','ADVANCED PLUMBING AND DRAIN INC','C-36','SAN FRANCISCO','(415) 744-4944','2027-11-30','Policy recorded; expires 08/21/2027','12:18:38 PM','The license may be suspended at a future date for failure to resolve an outstanding final liability from the Franchise Tax Board, Department of Industrial Relations, Employment Development Department, or the Contractors State License Board.'),
('379364','JAMES CACCIA PLUMBING INC · dba CACCIA HOME SERVICES','C-36; C-31; C-34; C-10','BURLINGAME','(650) 342-5363','2027-04-30','Policy recorded; expires 10/01/2027','12:20:49 PM',''),
('966337','FLOW MASTERS PLUMBING INC','C-36; C-16; C-20','DALY CITY','(415) 751-1933','2027-10-31','Policy recorded; expires 06/01/2027','12:20:49 PM',''),
('1140843','DISCOUNT PLUMBING ROOTER SERVICES LLC','C-36; A','BURLINGAME','(650) 991-2100','2027-07-31','Policy recorded; expires 04/01/2027','12:19:02 PM','CSLB also records $2,000,000 liability insurance and a $100,000 LLC employee/worker bond.'),
('1086935','FDL PLUMBING INC','C-36','DALY CITY','(415) 678-9557','2028-10-31','Policy recorded; expires 01/21/2027','12:20:33 PM',''),
('961218','PRECISION ROOTER & DRAIN','C-36','SAN FRANCISCO','(415) 724-1824','2027-05-31','Exempt: certified no employees','12:20:35 PM',''),
('954385','CW PLUMBING INC · dba CITYWIDE PLUMBING','C-36','DALY CITY','(415) 716-1519','2028-07-31','Exempt: certified no employees','12:20:35 PM','License reissued to another entity 07/06/2026.'),
('300647','CAHILL CONTRACTORS INC','A; B','SAN FRANCISCO','(415) 986-0600','2027-11-30','Policy recorded; expires 07/01/2027','12:19:28 PM',''),
('297604','D G CONSTRUCTION CO','B; C-36','SAN FRANCISCO','(415) 308-0803','2027-04-30','Exempt: certified no employees','12:20:49 PM','CSLB links to complaint disclosure information; separate disclosure lists citation 2 2022 002099 dated 03/23/2023, for disclosure only per B&P 7124.6.'),
('1027286','KENNETH ASIRE PLUMBING','C-36','SAN FRANCISCO','(415) 913-8048','2027-05-31','Policy recorded; expires 08/30/2027','12:20:49 PM','License under Contractors Bond Suspension. Recorded bond cancellation date 08/16/2026. CSLB notes a received replacement bond may not yet be processed.'),
('1160613','CLEVER PLUMBING & ROOTER INC','C-36','SAN BRUNO','(650) 834-0821','2028-09-30','Exempt: certified no employees','12:21:30 PM','')]
providers=[]
for i,(n,legal,cls,city,phone,expiry,wc,tm,extra) in enumerate(rows,1):
 sid='CSLB-'+n; src(sid,cslb(n),f'CSLB license detail #{n}', 'California Contractors State License Board',supports='Legal name, classifications, status, expiry, registered city, phone and workers-compensation record.',limits='Point-in-time record. Complaint disclosure is limited by law; active status is not an endorsement or a complete background check.')
 providers.append(dict(id=f'P-{i:02}',name=legal.split(' · dba ')[-1].title().replace('Inc','Inc').replace('Llc','LLC'),legal_name=legal,license=n,classifications=cls.split('; '),registered_city=city.title().replace('San Francisco','San Francisco'),phone=phone,expiry=expiry,status='Suspended' if n=='1027286' else 'Current and active',workers_comp=wc,source_timestamp=f'11/7/2026 {tm}; timezone not stated',official_url=cslb(n),source_ids=[sid],website='',service_claim='',service_source='',service_verified=False,group='Additional registry candidate',fit='License record checked; exact job fit and service acceptance not established.',exact_job_confirmed=False,ceiling_restoration_confirmed=False,availability_confirmed=False,quote_confirmed=False,review_url='',review_source='',additional_status=extra,flags=[]))
# Prefer the exact business display name, without inferring a trading identity.
names={'1115649':'Rapid Flow Plumbing & Rooter','829071':'Ace Plumbing & Rooter','1089561':'Heise’s Plumbing','977638':'Expert Plumbing Solutions','757796':'Bay Area Plumbing','1024971':'Fast Response Plumbing & Rooter','749536':'Save-On-Interior','1096552':'We Do Construction','392967':'Ayoob & Peery','995163':'Bernal Hill Drywall','1106131':'SF Building Group','1105133':'24/7 SF Handyman & Remodeling Service','1009195':'Advanced Plumbing and Drain','379364':'Caccia Home Services','966337':'Flow Masters Plumbing','1140843':'Discount Plumbing Rooter Services','1086935':'FDL Plumbing','961218':'Precision Rooter & Drain','954385':'Citywide Plumbing','300647':'Cahill Contractors','297604':'D G Construction','1027286':'Kenneth Asire Plumbing','1160613':'Clever Plumbing & Rooter'}
by={p['license']:p for p in providers}
for n,name in names.items(): by[n]['name']=name
companies={
'1115649':('RF','https://www.rapidflowbayarea.com/','Rapid Flow — official home and service area','The company advertises San Francisco/Bay Area plumbing and general contracting, from a simple repair to a complete renovation.'),
'829071':('ACE','https://www.aceplumbingandrooter.com/','Ace Plumbing & Rooter — official site','The company advertises San Francisco residential plumbing and work for HOAs/property managers, including insurance requirements and purchase orders.'),
'1089561':('HEISE','https://www.heisesplumbing.com/','Heise’s Plumbing — official site','The company advertises San Francisco plumbing and property repairs, and says it handles jobs big or small.'),
'977638':('EXPERT','https://www.eplumbingsolutions.com/','Expert Plumbing Solutions — official site','The company advertises San Francisco residential repairs, drain work and fixture installation.'),
'757796':('BAY','https://www.bayareaplumbingsf.com/','Bay Area Plumbing — official site','The company advertises San Francisco residential/commercial plumbing, leak repair and kitchen/bathroom work.'),
'1024971':('FAST','https://www.fastresponseplumbingsf.com/','Fast Response — official site','The company advertises full-service residential plumbing for San Francisco houses, apartments and HOAs.'),
'1096552':('WEDO','https://www.wedoconstructions.com/services/general-contractor-in-san-francisco/','We Do Construction — official general-contracting page','The company advertises San Francisco design-build work, with B + C-36 and self-performed plumbing under one contract.'),
'392967':('AYOOB','https://www.ayoobpeery.com/','Ayoob & Peery — official site','The company describes itself as a San Francisco mechanical contractor focused on wet-side building systems and design/build solutions for commercial applications.'),
'995163':('BERNAL','https://www.bernalhilldrywall.com/','Bernal Hill Drywall — official site','The company advertises San Francisco drywall installation, patching, painting and texture matching, from small wall repairs to complete build-backs.'),
'1106131':('SFBG','https://sfbuildinggroup.com/','SF Building Group — official site','The company advertises all San Francisco neighborhoods, occupied-space work and trade coordination, but says it focuses on larger planned projects.')}
for n,(sid,url,title,claim) in companies.items():
 src(sid,url,title,names[n],kind='official-company',supports=claim,limits='Company self-description, not independent proof of performance, availability or acceptance of this scope.')
 p=by[n];p.update(website=url,service_claim=claim,service_source=sid,service_verified=True,source_ids=p['source_ids']+[sid])
updates={
'1115649':dict(group='Combined-scope lead',fit='First combined-scope inquiry: B + C-36 and a published simple-repair-to-renovation offer. A Yelp-indexed account describes a related tub-plug retrieval, not this exact trip-lever job.',review_url='https://www.yelp.com/search?find_desc=General+Contractors&find_loc=Excelsior%2C+San+Francisco%2C+CA',review_source='YELP-RF',flags=['F-06','F-07','F-08']),
'829071':dict(group='Combined-scope lead',fit='Combined-scope alternative: B + C-36 and published HOA/property-manager experience. Exact concealed trip-lever work and ceiling finishing remain unconfirmed.',review_url='https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco',review_source='YELP-ACE',flags=['F-06','F-08']),
'1089561':dict(group='Technical case-study lead',fit='Strongest published adjacent case evidence: San Francisco tub waste-and-overflow replacements, including one described as using ceiling access. No C-9/B on this license; ask who handles ceiling restoration.',review_url='https://www.yelp.com/biz/heises-plumbing-san-francisco',review_source='YELP-HEISE',flags=['F-06','F-09','F-10']),
'977638':dict(group='Existing estimate',fit='Requote the common scope. C-36 only on the checked license; a separately licensed restoration trade or properly structured prime contract is needed if the ceiling is opened.',flags=['F-03','F-04','F-06']),
'757796':dict(group='Existing estimate',fit='Requote the common scope. The supplied wording includes a spout/diverter, which is not automatically the waste-and-overflow assembly. Confirm the contracting entity and restoration trade.',flags=['F-03','F-04','F-06','F-07','F-11']),
'1024971':dict(group='Existing estimate',fit='Requote the common scope. A repair/adjustment price is not a replacement-plus-access price. C-36 only on the checked license.',flags=['F-03','F-04','F-06','F-12']),
'749536':dict(group='Additional registry candidate',fit='B + C-36 record shares a street address and phone with Bay Area Plumbing. Common ownership and use of this license on that quote are not established; confirm the legal contracting entity.',flags=['F-07','F-11','F-13']),
'1096552':dict(group='Conditional combined-scope lead',fit='B + C-36 and a one-contract offer, but the public positioning emphasizes larger renovations. Confirm willingness to take a small repair before prioritizing.',review_url='https://www.yelp.com/biz/we-do-construction-san-francisco',review_source='YELP-WEDO',flags=['F-06','F-14']),
'392967':dict(group='Additional registry candidate',fit='B + C-36, but the official site emphasizes commercial building systems. Small occupied-unit repair acceptance is unconfirmed.',flags=['F-06','F-15']),
'995163':dict(group='Restoration partner',fit='Drywall/patch/texture specialist with C-9 + B. A possible restoration partner under a properly structured combined contract; no C-36 on this license.',flags=['F-06','F-16']),
'1106131':dict(group='Conditional combined-scope lead',fit='B-only general contractor advertises occupied-space coordination, but focuses on larger projects. Plumbing must be self-performed only if appropriately licensed or subcontracted; identify the C-36 and C-9 parties.',flags=['F-06','F-07','F-17']),
'1105133':dict(group='Conditional registry candidate',fit='B-2 is not B or C-36. Statute requires at least three unrelated trades and restricts structural work and plumbing-system replacement; do not treat this as an automatic two-trade fit.',flags=['F-18']),
'1009195':dict(group='Additional registry candidate',fit='Active C-36 record carries a future-suspension warning for an outstanding final liability. Review the official record before any engagement.',flags=['F-19']),
'297604':dict(group='Additional registry candidate',fit='B + C-36 record has a complaint-disclosure link. The official disclosure lists a citation; review its details rather than treating active status as a clean history.',flags=['F-07','F-20']),
'1027286':dict(group='Not eligible — suspended',fit='Excluded from the active shortlist: CSLB reports a contractors-bond suspension. A replacement bond may be awaiting processing; recheck the official record.',flags=['F-21'])}
for n,u in updates.items(): by[n].update(u)
providers.append(dict(id='P-24',name='Portola Plumbing Services',legal_name='',license='',classifications=[],registered_city='',phone='',expiry='',status='',workers_comp='',source_timestamp='',official_url='https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx',source_ids=['CSLB-SEARCH'],website='',service_claim='',service_source='',service_verified=False,group='Identity unresolved',fit='Name appeared in prior research and Yelp search excerpts. No exact legal entity/license match was confirmed; license and contact fields are blank.',exact_job_confirmed=False,ceiling_restoration_confirmed=False,availability_confirmed=False,quote_confirmed=False,review_url='https://www.yelp.com/search?find_desc=Licensed+Plumber&find_loc=West+Portal%2C+San+Francisco%2C+CA',review_source='YELP-PORTOLA',additional_status='',flags=['F-22']))
src('CSLB-SEARCH','https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx','Check a contractor license','California CSLB',supports='Official lookup entry point for unresolved identities.',limits='An entry point does not verify any particular business.')
src('DG-COMPLAINT','https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=297604','D G Construction complaint disclosure','California CSLB',supports='Citation 2 2022 002099; 03/23/2023; disclosure status.',limits='Read the linked citation and CSLB disclosure rules; no inference about the underlying merits.')
by['297604']['source_ids'].append('DG-COMPLAINT')
save('providers.json',{'as_of':'2026-11-07','rows':providers})
save('sources.json',{'as_of':'2026-11-07','rows':sources})
print('Transcribed',len(providers),'provider identities;',len(sources),'sources so far')

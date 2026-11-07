#!/usr/bin/env python3
"""Real Chromium checks; requires playwright and an available Chromium executable."""
import json,os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parents[1]; base=os.environ.get('SITE_URL','http://127.0.0.1:8080/'); exe=os.environ.get('CHROMIUM_PATH') or None
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile')]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for name in ['index.html','executive-summary.html','requirements.html','estimates.html','providers.html','technical.html','analysis.html','sources.html','flagged-for-review.html','repository.html','verification.html']:
   r=page.goto(base+name,wait_until='networkidle');assert r.status==200,(name,r.status)
   assert page.locator('h1').count()==1
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),(label,name,'page overflow')
   results.append({'viewport':label,'page':name,'http':r.status,'page_overflow':False})
  page.goto(base+'providers.html',wait_until='networkidle');page.locator('#provider-filter').fill('1089561')
  assert page.locator('#providers-table tbody tr:visible').count()==1
  assert 'Heise' in page.locator('#providers-table tbody tr:visible').inner_text()
  page.locator('#provider-filter').fill('');assert page.locator('#providers-table tbody tr:visible').count()==24
  page.goto(base+'index.html',wait_until='networkidle');page.screenshot(path=str(HERE/'evidence'/f'{label}.png'),full_page=True)
  assert not errors,errors
  page.close()
 browser.close()
report={'status':'PASS','browser':'Chromium','base_url':base,'results':results,'filter_test':'PASS: license 1089561 -> one Heise row; reset -> 24 rows','javascript_errors':0}
(HERE/'evidence'/'browser.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

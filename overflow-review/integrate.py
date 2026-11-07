#!/usr/bin/env python3
"""Promote the checked namespace build to the canonical root and retire duplicate HTML routes."""
from pathlib import Path
import shutil,json,subprocess,html
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SITE=HERE/'site'
CANON=['index.html','executive-summary.html','requirements.html','providers.html','estimates.html','technical.html','analysis.html','sources.html','flagged-for-review.html','repository.html','verification.html']
for name in CANON:shutil.copyfile(SITE/name,ROOT/name)
for d in ['assets','data']:
 dest=ROOT/d;dest.mkdir(exist_ok=True)
 for p in (SITE/d).iterdir():
  if p.is_file():shutil.copyfile(p,dest/p.name)
# Root data now contains canonical JSON; unrelated GEMS template remains under data/templates.
shutil.copyfile(SITE/'assets'/'style.css',ROOT/'style.css')
# Preserve the old technical-approach URL as a redirect; code-and-permit is retired to neutral technical page.
aliases={'technical-approach.html':'technical.html','code-and-permit.html':'technical.html'}
prefixes=('bathtub/','bathtub-overflow/','bathroom-overflow/','trip-lever/','overflow-trip-lever/','docs/bathtub-')
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
redirects=[]
for name in tracked:
 if not name.endswith('.html') or name in CANON or name.startswith('overflow-review/'):continue
 if not (name.startswith(prefixes) or name in aliases):continue
 target=aliases.get(name)
 if not target:
  base=Path(name).name
  mapping={'providers.html':'providers.html','vendors.html':'providers.html','candidates.html':'providers.html','contractors.html':'providers.html','quotes.html':'estimates.html','estimates.html':'estimates.html','costs.html':'estimates.html','requirements.html':'requirements.html','scope.html':'requirements.html','sources.html':'sources.html','flagged.html':'flagged-for-review.html','flagged-for-review.html':'flagged-for-review.html','review.html':'flagged-for-review.html','findings.html':'analysis.html','analysis.html':'analysis.html','technical.html':'technical.html','background.html':'technical.html','rules.html':'technical.html','code.html':'technical.html','compliance.html':'technical.html','verification.html':'verification.html','methodology.html':'repository.html','executive-summary.html':'executive-summary.html','summary.html':'executive-summary.html','allinone.html':'providers.html'}
  target=mapping.get(base,'index.html')
 depth=len(Path(name).parent.parts);url=('../'*depth)+target
 doc=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={html.escape(url,quote=True)}"><link rel="canonical" href="{html.escape(url,quote=True)}"><title>Moved to the canonical repair brief</title></head><body><p>This earlier brief has been consolidated. <a href="{html.escape(url,quote=True)}">Open the current source-checked repair brief</a>.</p></body></html>\n'
 (ROOT/name).write_text(doc);redirects.append({'path':name,'target':url})
(HERE/'repository'/'redirects.json').write_text(json.dumps({'canonical':CANON,'redirects':redirects},indent=2)+'\n')
print(json.dumps({'canonical_pages':len(CANON),'redirects':len(redirects)},indent=2))

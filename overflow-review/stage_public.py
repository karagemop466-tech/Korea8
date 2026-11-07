#!/usr/bin/env python3
"""Stage only public, neutral repair pages and preserved GEMS public docs/downloads."""
from pathlib import Path
import shutil,json,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'overflow-review'/'public'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir(parents=True)
canon=json.loads((ROOT/'overflow-review'/'repository'/'redirects.json').read_text())['canonical']
for n in canon:shutil.copyfile(ROOT/n,OUT/n)
for d in ['assets','data']:
 shutil.copytree(ROOT/d,OUT/d,ignore=shutil.ignore_patterns('templates','bridge','raw','external','mirror'))
# Preserve unrelated public GEMS docs and their linked downloads, without repository internals.
shutil.copytree(ROOT/'docs',OUT/'docs')
shutil.copytree(ROOT/'downloads',OUT/'downloads')
for r in json.loads((ROOT/'overflow-review'/'repository'/'redirects.json').read_text())['redirects']:
 q=OUT/r['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/r['path'],q)
(OUT/'.nojekyll').write_text('')
print(len(list(OUT.rglob('*'))))

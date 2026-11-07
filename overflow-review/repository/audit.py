#!/usr/bin/env python3
"""Structural/provenance audit of tracked files; not a scientific validation."""
import ast, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
rows=[]
for name in sorted(filter(None,files)):
 p=ROOT/name; b=p.read_bytes(); row={'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'lines':None,'check':'binary inventory only','issues':[]}
 if name.startswith('overflow-review/'):
  row['check']='current-session output; excluded from baseline audit'
 elif b'\0' in b:
  row['check']='binary inventory only'
 else:
  try: text=b.decode('utf-8'); row['lines']=len(text.splitlines())
  except UnicodeDecodeError: row['check']='non-UTF-8 inventory only'
  else:
   row['check']='UTF-8 text scanned'
   if name.endswith('.json'):
    try: json.loads(text); row['check']='JSON parsed; UTF-8 text scanned'
    except Exception as e: row['issues'].append('JSON parse: '+str(e))
   if name.endswith('.py'):
    try: ast.parse(text,filename=name); row['check']='Python syntax parsed; UTF-8 text scanned'
    except Exception as e: row['issues'].append('Python syntax: '+str(e))
   if any(x in name.lower() for x in ['bathtub','trip-lever','overflow']) or name.startswith(('project/','site-data/')):
    row['domain']='plumbing dossier / shared output'
   elif name.startswith(('docs/','evidence/','registry/','vendor/','src/','data/templates/','submissions/','downloads/')) or name in ['README.md','AGENTS.md','PROJECT_PROMPT.md','EXECUTIVE_SUMMARY.md','HYPOTHESES.md','RUN_CARD.json','run_card.json']:
    row['domain']='unrelated or mixed legacy research'
   else: row['domain']='repository infrastructure / other'
   # Flag public legacy numeric quote values without reproducing them in this report.
   if name.endswith(('.html','.json','.md')) and row.get('domain')=='plumbing dossier / shared output':
    if any(v in text for v in ['$614','$550','$135']): row['issues'].append('Legacy unsupported quote amount present; superseded public routes must not expose it')
 if 'domain' not in row: row['domain']='current session' if name.startswith('overflow-review/') else 'binary legacy artifact'
 row['source_url']='https://github.com/karagemop466-tech/Korea8/blob/'+subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()+'/'+name
 rows.append(row)
report={'scope':'Every tracked file inventoried; every decodable text file scanned line-by-line for encoding and applicable JSON/Python syntax. External factual claims only revalidated where official plumbing sources were retrieved. Unrelated GEMS scientific claims are not validated.','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'files':len(rows),'text_files':sum(r['lines'] is not None for r in rows),'text_lines':sum(r['lines'] or 0 for r in rows),'issue_files':sum(bool(r['issues']) for r in rows),'rows':rows}
(Path(__file__).parent/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))

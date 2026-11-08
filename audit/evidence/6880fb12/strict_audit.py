#!/usr/bin/env python3
"""Independent, read-only audit of the canonical bathtub dashboard.

Session arena/6880fb12-korea8. Does not import or modify the site's verifier.
Checks every canonical tbody row for a recognized primary-source link, using the
source register's own kind labels rather than a hostname allowlist. Review-platform
links alone do not satisfy the requirement. Also checks internal links, owner-amount
labels, ranking arithmetic, and restricted private phrasing in served text/data.
"""
from __future__ import annotations
import json, pathlib, re, subprocess, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / 'overflow-integration' / 'data'
PRIMARY_KINDS = {'official-government', 'official-company', 'official-manufacturer', 'official-code-publisher', 'official-tool', 'owner-record', 'repository-primary'}
SOURCES = {s['url']: s for s in json.loads((DATA / 'sources.json').read_text())['rows']}

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.in_body=False; self.row=None; self.table=''
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='table': self.table=a.get('id','')
        elif tag=='tbody': self.in_body=True
        elif tag=='tr' and self.in_body: self.row={'table':self.table,'hrefs':[],'text':[]}
        elif tag=='a' and self.row is not None and 'href' in a: self.row['hrefs'].append(a['href'])
    def handle_data(self, data):
        if self.row is not None: self.row['text'].append(data)
    def handle_endtag(self, tag):
        if tag=='tr' and self.row is not None:
            self.row['text']=' '.join(''.join(self.row['text']).split()); self.rows.append(self.row); self.row=None
        elif tag=='tbody': self.in_body=False
        elif tag=='table': self.table=''

class LinkParser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for k in ('href','src'):
            if k in a: self.links.append(a[k])

def primary_links(hrefs):
    out=[]
    for h in hrefs:
        s=SOURCES.get(h)
        if s and s.get('kind') in PRIMARY_KINDS: out.append(h)
    return out

def main():
    index=(ROOT/'index.html').read_text()
    nav=re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', index, re.S)
    pages=re.findall(r'href="([^"]+\.html)"', nav.group(1)) if nav else []
    problems=[]; rows_total=0; rows_primary=0; row_details=[]
    for page in pages:
        p=ROOT/page
        if not p.exists(): problems.append(f'missing canonical page: {page}'); continue
        tp=TableParser(); tp.feed(p.read_text())
        for i,row in enumerate(tp.rows,1):
            rows_total+=1; pl=primary_links(row['hrefs'])
            if pl: rows_primary+=1
            else: problems.append(f'{page} row {i} table={row["table"] or "(unnamed)"}: no recognized primary-source link :: {row["text"][:160]}')
            row_details.append({'page':page,'row':i,'table':row['table'],'primary_links':pl,'all_links':row['hrefs']})
    # Internal links across all tracked HTML, including redirects and legacy docs.
    tracked=subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT,text=True).splitlines()
    internal=0; broken=[]
    for f in tracked:
        p=ROOT/f; lp=LinkParser(); lp.feed(p.read_text())
        for u in lp.links:
            if u.startswith(('http:','https:','mailto:','tel:','data:')): continue
            if u.startswith('#'):
                if u[1:] and u[1:] not in lp.ids: broken.append(f'{f}:{u}')
                continue
            path=unquote(urlsplit(u).path)
            if not path: continue
            internal+=1; target=(p.parent/path).resolve()
            if not target.exists(): broken.append(f'{f}:{u}')
    problems += [f'broken internal link: {x}' for x in broken]
    # Owner amounts must be labeled within the same table row, or nearby in prose.
    amount_hits=[]
    for page in pages:
        t=(ROOT/page).read_text(); tp=TableParser(); tp.feed(t)
        for row in tp.rows:
            for m in re.finditer(r'\$(614|550|135)\b',row['text']):
                if not re.search(r'owner[- ]reported|owner[- ]supplied|unverified',row['text'],re.I):
                    amount_hits.append(f'{page}:{m.group(0)}')
        prose=re.sub(r'<table.*?</table>','',t,flags=re.S)
        for m in re.finditer(r'\$(614|550|135)\b',prose):
            ctx=prose[max(0,m.start()-300):m.end()+220]
            if not re.search(r'owner[- ]reported|owner[- ]supplied|unverified',ctx,re.I):
                amount_hits.append(f'{page}:{m.group(0)}')
    problems += [f'unlabeled owner amount: {x}' for x in amount_hits]
    # Ranking arithmetic and contiguous rendered order.
    rk=json.loads((DATA/'ranking.json').read_text()); weights={w['id']:w['weight'] for w in rk['weights']}
    scored=sorted(rk['ranked'],key=lambda r:(-sum(r['score_components'][k]*weights[k] for k in weights),-r['score_components']['C2'],r['name']))
    import html as html_module
    decision=html_module.unescape((ROOT/'decision-analysis.html').read_text()) if (ROOT/'decision-analysis.html').exists() else ''
    rank_order_ok=all(decision.find(r['name'])>=0 for r in scored)
    positions=[decision.find(r['name']) for r in scored]
    rank_order_ok=rank_order_ok and positions==sorted(positions)
    if not rank_order_ok: problems.append('ranking page order does not match recomputed score/tie-break order')
    # Restricted phrasing in served HTML and canonical/legacy JSON; detector scripts are excluded.
    privacy=re.compile(r'cannot pull a permit|cannot obtain a permit|permit for this week|stay private|private reason|off the record|under the table|skip the permit|avoid the permit',re.I)
    privacy_hits=[]
    files=list(ROOT.glob('*.html'))+list((ROOT/'overflow-integration').rglob('*.json'))+list((ROOT/'bathtub').rglob('*.json'))+list((ROOT/'data').rglob('*.json'))+list((ROOT/'project').glob('*.json'))+list((ROOT/'site-data').glob('*.json'))
    for p in files:
        if not p.exists(): continue
        for m in privacy.finditer(p.read_text(errors='replace')): privacy_hits.append(f'{p.relative_to(ROOT)}:{m.group(0)}')
    problems += [f'privacy hit: {x}' for x in privacy_hits]
    report={'session':'arena/6880fb12-korea8','canonical_pages':pages,'canonical_pages_count':len(pages),'rows_total':rows_total,'rows_with_recognized_primary_link':rows_primary,'tracked_html_files':len(tracked),'internal_links_checked':internal,'broken_internal_links':broken,'unlabeled_owner_amounts':amount_hits,'privacy_hits':privacy_hits,'ranking_order_matches_recomputed':rank_order_ok,'problems':problems,'row_details':row_details}
    out=pathlib.Path(__file__).with_name('strict-audit-report.json'); out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'row_details','problems'}},indent=2))
    for x in problems: print('PROBLEM:',x)
    return 1 if problems else 0
if __name__=='__main__': sys.exit(main())

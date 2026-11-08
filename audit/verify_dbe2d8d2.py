#!/usr/bin/env python3
"""Independent line-by-line verification of the canonical dashboard.

Session arena/dbe2d8d2-korea8. This parser deliberately does NOT import the
site's own build/verifier modules. It re-reads the published HTML and the
source registry, and enforces the strict rule: every table row must carry a
link to a host registered as an official/primary source; unconfirmable values
must be blank and flagged.
"""
from __future__ import annotations
import json, pathlib, re, sys, datetime, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'overflow-integration' / 'data'
PAGES = [
    'index.html', 'executive-summary.html', 'requirements.html', 'providers.html',
    'decision-analysis.html', 'estimates.html', 'technical-approach.html',
    'code-and-permit.html', 'sources.html', 'flagged-for-review.html',
    'verification.html',
]

def host_of(url):
    try:
        return (urllib.parse.urlparse(url).hostname or '').lower()
    except ValueError:
        return ''

def main():
    problems = []
    stats = {'pages': 0, 'tables': 0, 'rows': 0, 'rows_with_registered_official_link': 0,
             'internal_links': 0, 'rank_rows': 0, 'rank_rows_with_cslb_and_phone': 0,
             'privacy_hits': 0, 'amount_occurrences': 0}

    sources = json.loads((DATA / 'sources.json').read_text())['rows']
    official_kinds = {
        'official-government', 'official-company', 'official-manufacturer',
        'official-code-publisher', 'official-tool', 'repository-primary', 'owner-record',
    }
    official_hosts = {host_of(s['url']) for s in sources if s['kind'] in official_kinds}
    official_hosts.discard('')
    registered_urls = {s['url'] for s in sources}

    html_text = {}
    for page in PAGES:
        p = ROOT / page
        if not p.exists():
            problems.append(f'MISSING PAGE {page}')
            continue
        html_text[page] = p.read_text(encoding='utf-8')
        stats['pages'] += 1

    # 1. Navigation completeness and conflict markers
    for page, text in html_text.items():
        for target in PAGES:
            if f'href="{target}"' not in text:
                problems.append(f'{page}: missing nav link to {target}')
        for marker in ('<<<<<<<', '>>>>>>>', '=======', 'TODO', 'TBD', 'Lorem ipsum'):
            if marker in text:
                problems.append(f'{page}: placeholder/conflict marker {marker!r}')
        if re.search(r'>\s*(?:None|nan|NaN)\s*<', text):
            problems.append(f'{page}: literal None/nan in a cell')

    # 2. Strict row-level source check
    for page, text in html_text.items():
        for ti, tbl in enumerate(re.findall(r'<table\b.*?</table>', text, re.S)):
            body = re.search(r'<tbody\b.*?</tbody>', tbl, re.S)
            if not body:
                continue
            stats['tables'] += 1
            for ri, row in enumerate(re.findall(r'<tr\b.*?</tr>', body.group(), re.S)):
                stats['rows'] += 1
                hrefs = re.findall(r'href="([^"]+)"', row)
                official = [u for u in hrefs if host_of(u) in official_hosts]
                if official:
                    stats['rows_with_registered_official_link'] += 1
                else:
                    plain = re.sub(r'<[^>]*>', ' ', row)
                    problems.append(f'{page} table#{ti} row#{ri}: NO registered official link :: {plain.strip()[:160]}')

    # 3. Ranked decision analysis: every rank row must show an official CSLB detail and a phone
    dt = html_text.get('decision-analysis.html', '')
    rank_table = re.search(r'<table[^>]*id="ranking-table".*?</table>', dt, re.S)
    if not rank_table:
        problems.append('decision-analysis.html: ranking-table missing')
    else:
        for ri, row in enumerate(re.findall(r'<tr\b.*?</tr>', rank_table.group(), re.S)):
            if '<th' in row:
                continue
            stats['rank_rows'] += 1
            has_cslb = 'www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=' in row
            has_phone = bool(re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', row))
            if has_cslb and has_phone:
                stats['rank_rows_with_cslb_and_phone'] += 1
            else:
                problems.append(f'decision-analysis.html ranking row#{ri}: cslb={has_cslb}, phone={has_phone}')
    if stats['rank_rows'] != 12:
        problems.append(f'ranking rows = {stats["rank_rows"]} (expected 12)')

    # 4. Internal links and anchors
    ids_by_page = {p: set(re.findall(r'id="([^"]+)"', t)) for p, t in html_text.items()}
    for page, text in html_text.items():
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
                continue
            if href.startswith('#'):
                stats['internal_links'] += 1
                if href[1:] and href[1:] not in ids_by_page[page]:
                    problems.append(f'{page}: broken anchor {href}')
                continue
            path, _, frag = href.partition('#')
            stats['internal_links'] += 1
            target = (ROOT / path.split('?')[0]).resolve() if path else ROOT / page
            if not target.exists():
                problems.append(f'{page}: broken internal link {href}')
            elif frag and target.suffix == '.html':
                resolved = target.relative_to(ROOT).as_posix()
                if resolved in ids_by_page and frag not in ids_by_page[resolved]:
                    problems.append(f'{page}: broken anchor {href}')

    # 5. Blank / unverified discipline for owner-supplied amounts
    banned_privacy = re.compile(
        r'cannot pull a permit|cannot obtain a permit|permit for this week|'
        r'must stay private|private reason|off the record|under the table|'
        r'skip the permit|avoid the permit|without a permit for this week', re.I)
    scan_globs = [
        ROOT.glob('*.html'), ROOT.glob('*.md'),
        DATA.glob('*.json'), (ROOT / 'site-data').glob('*.json'),
        (ROOT / 'project').glob('*.json'), (ROOT / 'bathtub' / 'data').glob('*.json'),
        (ROOT / 'data' / 'bathtub').glob('*.json'),
    ]
    for group in scan_globs:
        for f in group:
            text = f.read_text(encoding='utf-8', errors='replace')
            for m in banned_privacy.finditer(text):
                problems.append(f'PRIVACY hit in {f.relative_to(ROOT)}: {m.group(0)!r}')
                stats['privacy_hits'] += 1
    for page, text in html_text.items():
        for m in re.finditer(r'\$(614|550|135)\b', text):
            stats['amount_occurrences'] += 1
            ctx = text[max(0, m.start() - 300):m.end() + 220]
            if not re.search(r'owner[- ]reported|owner[- ]supplied|unverified|not verified', ctx, re.I):
                problems.append(f'{page}: owner amount {m.group(0)} lacks unverified label nearby')

    # 6. Every row's source ids in the data files resolve, and official URLs are https
    src_ids = {s['id'] for s in sources}
    for name in ['providers.json', 'requirements.json', 'technical.json', 'compliance.json',
                 'reviews.json', 'flags.json', 'ranking.json']:
        doc = json.loads((DATA / name).read_text())
        rows = doc.get('rows') or (doc.get('ranks', []) + doc.get('criteria', []) + doc.get('excluded', []))
        for r in rows:
            for sid in r.get('source_ids', []):
                if sid not in src_ids:
                    problems.append(f'{name}: unresolved source id {sid}')
            ou = r.get('official_url', '')
            if ou and not ou.startswith('https://'):
                problems.append(f'{name}: non-https official_url {ou}')
    for sid in json.loads((DATA / 'ranking.json').read_text())['cost_note_source_ids']:
        if sid not in src_ids:
            problems.append(f'ranking.json cost_note_source_ids: unresolved {sid}')

    # 7. Report
    report = {
        'session': 'arena/dbe2d8d2-korea8',
        'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'result': 'PASS' if not problems else 'FAIL',
        'stats': stats,
        'registered_official_hosts': sorted(official_hosts),
        'problems': problems,
    }
    out = ROOT / 'audit' / 'verification_dbe2d8d2.json'
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'pages={stats["pages"]} tables={stats["tables"]} rows={stats["rows"]} '
          f'rows_with_official_link={stats["rows_with_registered_official_link"]} '
          f'rank_rows={stats["rank_rows"]} internal_links={stats["internal_links"]} '
          f'privacy_hits={stats["privacy_hits"]} problems={len(problems)} — {report["result"]}')
    for p in problems:
        print('PROBLEM:', p)
    return 0 if not problems else 1

if __name__ == '__main__':
    sys.exit(main())

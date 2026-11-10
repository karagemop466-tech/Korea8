#!/usr/bin/env python3
"""Stage only the public HTML link closure, never the repository wholesale."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import shutil

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(v for k, v in attrs if k in ('href', 'src') and v)


def public_files(root=ROOT):
    root = root.resolve()
    pending = [Path('index.html')]
    found = set()
    allowed = {'.html', '.css', '.json', '.md', '.png', '.jpg', '.jpeg', '.svg', '.pdf', '.txt', '.csv', '.js', '.ico'}
    while pending:
        relative = pending.pop()
        source = (root / relative).resolve()
        if not source.is_relative_to(root):
            raise ValueError(f'Link escapes publication root: {relative}')
        relative = source.relative_to(root)
        if relative in found:
            continue
        if any(part.startswith('.') for part in relative.parts) or source.suffix not in allowed:
            raise ValueError(f'Non-public link target: {relative}')
        if not source.is_file():
            raise ValueError(f'Missing public target: {relative}')
        found.add(relative)
        if source.suffix == '.html':
            parser = Links()
            parser.feed(source.read_text())
            for url in parser.urls:
                parsed = urlsplit(url)
                # tel:, data:, mailto: and any other scheme are not files to stage
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                if parsed.path.startswith('data:'):
                    continue
                path = unquote(parsed.path)
                target = root / path.lstrip('/') if path.startswith('/') else source.parent / path
                if path.endswith('/'):
                    target /= 'index.html'
                pending.append(target.relative_to(root))
    return found


def stage(destination=ROOT / 'build' / 'pages'):
    files = public_files()
    destination = destination.resolve()
    if destination != ROOT / 'build' / 'pages':
        raise ValueError('Staging destination must be build/pages')
    if destination.exists():
        shutil.rmtree(destination)
    for relative in sorted(files):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    (destination / '.nojekyll').touch()
    print(f'Staged {len(files)} linked public files in {destination}')

if __name__ == '__main__':
    stage()

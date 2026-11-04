#!/usr/bin/env python3
"""Restore only public, hash-pinned research inputs; no credentials or protected data."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
from urllib.parse import quote
ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest', type=Path, default=ROOT/'registry/inputs.json')
    args = ap.parse_args()
    if not shutil.which('gh'):
        raise SystemExit('GitHub CLI (gh) is required; no credential is stored by this project.')
    manifest = json.loads(args.manifest.read_text())
    results = []
    for entry in manifest['files']:
        dest = ROOT / entry['dest']
        if not dest.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError('manifest destination escapes repository')
        if dest.exists():
            if sha256(dest) != entry['sha256']:
                raise ValueError(f'{dest}: existing file differs from pin; refusing to overwrite')
            status = 'present-hash-verified'
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            partial = dest.with_suffix(dest.suffix + '.partial')
            resource = f"repos/{entry['repo']}/contents/{quote(entry['path'], safe='/')}?ref={entry['ref']}"
            try:
                with partial.open('wb') as out:
                    subprocess.run(['gh','api',resource,'-H','Accept: application/vnd.github.raw'],
                                   stdout=out, stderr=subprocess.PIPE, check=True)
                got = sha256(partial)
                if got != entry['sha256']:
                    raise ValueError(f"{entry['dest']}: SHA-256 mismatch {got} != {entry['sha256']}")
                partial.replace(dest)
            finally:
                partial.unlink(missing_ok=True)
            status = 'restored-hash-verified'
        results.append({'dest':entry['dest'],'status':status,'sha256':entry['sha256'],'bytes':dest.stat().st_size})
        print(status, entry['dest'], flush=True)
    receipt = ROOT/'data/restore_receipt.json'
    receipt.write_text(json.dumps({'schema':'korea8.restore-receipt.v1','manifest':str(args.manifest.relative_to(ROOT)),
                                   'provenance_warning':manifest['note'],'files':results},indent=2)+'\n')
    print(f'Verified {len(results)} files; receipt: {receipt.relative_to(ROOT)}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

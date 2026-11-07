#!/usr/bin/env python3
"""Retire the duplicate briefs published by earlier parallel sessions.

Each earlier session published its own copy of the same brief under its own
directory.  The project protocol makes the root dashboard the single
authoritative copy, and the 2026-11-06 review asked for the duplicates to be
retired.  This script replaces every page of a retired brief with a small
redirect stub that forwards to the canonical page built by
scripts/build_project_site.py.

Nothing is deleted: the original pages stay in Git history (see the commit
recorded in COORDINATION.md), and the redirect stubs keep every previously
published URL working, which is what a search engine or an old bookmark needs.

Run:  python scripts/build_redirects.py
      python scripts/build_redirects.py --check     (verify only, writes nothing)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Retired brief directory -> how deep it sits relative to the repo root.
RETIRED = {
    "bathtub": ".",
    "bathtub-overflow": ".",
    "bathroom-overflow": ".",
    "trip-lever": ".",
    "docs": "docs",
    "docs/bathtub-overflow": "docs",
}

# Filename fragment -> canonical page at the repository root.
TARGETS = [
    ("executive-summary", "executive-summary.html"),
    ("summary", "executive-summary.html"),
    ("requirements", "requirements.html"),
    ("scope", "requirements.html"),
    ("estimates", "estimates.html"),
    ("costs", "estimates.html"),
    ("quotes", "estimates.html"),
    ("providers", "providers.html"),
    ("contractors", "providers.html"),
    ("vendors", "providers.html"),
    ("candidates", "providers.html"),
    ("allinone", "providers.html"),
    ("technical", "technical-approach.html"),
    ("background", "technical-approach.html"),
    ("findings", "technical-approach.html"),
    ("analysis", "technical-approach.html"),
    ("compliance", "technical-approach.html"),
    ("code", "technical-approach.html"),
    ("methodology", "technical-approach.html"),
    ("verification", "verification.html"),
    ("flagged", "flagged-for-review.html"),
    ("review", "flagged-for-review.html"),
    ("sources", "sources.html"),
    ("index", "index.html"),
]

STUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={href}">
<link rel="canonical" href="https://karagemop466-tech.github.io/Korea8/{target}">
<title>Consolidated — Bathtub Overflow Trip Lever Project</title>
<style>body{{font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
margin:0;background:#f6f7f9;color:#16212e}}main{{max-width:640px;margin:14vh auto;padding:28px;background:#fff;
border:1px solid #e3e8ee;border-radius:12px}}a{{color:#0b5cad}}</style>
</head>
<body>
<main>
<h1 style="font-size:22px;margin:0 0 8px">This page has moved</h1>
<p>The separate brief that used to live here has been consolidated into the single authoritative site
for this project. You are being forwarded to the matching page.</p>
<p><a href="{href}">Continue to the consolidated page</a>.</p>
<p style="color:#5b6b7c;font-size:14px">Retired copy: <code>{original}</code> — kept in the
repository history, no longer published as a separate version.</p>
</main>
</body>
</html>
"""


def target_for(filename):
    stem = filename[:-5].lower() if filename.endswith(".html") else filename.lower()
    for fragment, target in TARGETS:
        if fragment in stem:
            return target
    return "index.html"


def pages():
    out = []
    for rel in RETIRED:
        absdir = os.path.join(ROOT, rel)
        if not os.path.isdir(absdir):
            continue
        for name in sorted(os.listdir(absdir)):
            if not name.endswith(".html"):
                continue
            if rel == "docs" and not (name.startswith("bathtub") or name == "index.html"):
                # The preserved DOE GEMS archive pages (executive-summary, submit*, limitations,
                # sources) stay untouched. docs/index.html was overwritten by a parallel
                # bathtub session and is retired like the other duplicates.
                continue
            if rel == "docs/bathtub-overflow":
                pass
            elif rel != "docs" and name == "index.html":
                pass
            depth = rel.count("/") + 1
            href = "../" * depth + target_for(name)
            out.append((rel, name, href, target_for(name)))
    return out


def main():
    check_only = "--check" in sys.argv
    rows = pages()
    problems = []
    for rel, name, href, target in rows:
        target_path = os.path.join(ROOT, target)
        if not os.path.isfile(target_path):
            problems.append(f"{rel}/{name}: canonical target {target} does not exist")
        path = os.path.join(ROOT, rel, name)
        stub = STUB.format(href=href, target=target, original=f"{rel}/{name}")
        if check_only:
            if not os.path.isfile(path):
                problems.append(f"{rel}/{name}: missing")
                continue
            text = open(path, encoding="utf-8").read()
            if 'http-equiv="refresh"' not in text:
                problems.append(f"{rel}/{name}: not retired (no redirect)")
            elif f'url={href}' not in text:
                problems.append(f"{rel}/{name}: redirects to the wrong target")
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(stub)
    if problems:
        for p in problems:
            print("REDIRECT PROBLEM:", p)
        return 1
    print(("checked" if check_only else "wrote") + f" {len(rows)} redirect pages across "
          f"{len({r[0] for r in rows})} retired directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())

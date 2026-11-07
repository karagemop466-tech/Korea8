#!/usr/bin/env python3
"""Independent checks over the built project site.

The build script (scripts/build_project_site.py) enforces source links while it
renders.  This script re-checks the *written* pages, the redirect stubs and the
data-to-page agreement, then records the result in site-data/verification.json.

Checks
  1. internal links   — every relative href/src on a canonical page resolves
  2. retired briefs   — every page of a retired brief is a redirect to a real page
  3. data = page      — each data page renders exactly as many table rows as its
                        JSON has records
  4. licence links    — every provider row links to its own CSLB licence page
  5. no out-of-scope  — the built pages contain none of the phrases that would
                        indicate private, confidential or off-record material
  6. nav integrity    — every canonical page carries the full navigation and
                        the navigation targets exist

Run: python scripts/verify_project_site.py
Exit code 0 = all checks passed.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "project")

CANONICAL = [
    "index.html", "executive-summary.html", "requirements.html", "estimates.html",
    "providers.html", "technical-approach.html", "sources.html", "verification.html",
    "flagged-for-review.html",
]

FORBIDDEN = [
    "without a permit", "no permit", "cannot pull", "private reason", "keep private",
    "keeps private", "confidential", "internal use", "internal scoping",
    "intentionally excluded", "off the record", "do not publish", "stay private",
    "this week", "under the table",
]

problems = []


def load(name):
    with open(os.path.join(PROJ, name), encoding="utf-8") as fh:
        return json.load(fh)


def check_links():
    pages = [f for f in sorted(os.listdir(ROOT)) if f.endswith(".html")]
    checked = 0
    for page in pages:
        text = open(os.path.join(ROOT, page), encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if url.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = url.split("#")[0]
            if not target:
                continue
            checked += 1
            if not os.path.exists(os.path.join(ROOT, target)):
                problems.append(f"{page}: broken relative link {url}")
    return checked


def check_redirects():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_redirects.py"), "--check"],
                         capture_output=True, text=True, cwd=ROOT)
    if out.returncode != 0:
        problems.append("redirect check failed: " + (out.stdout + out.stderr).strip()[:400])
    return out.stdout.strip()


def count_rows(page):
    text = open(os.path.join(ROOT, page), encoding="utf-8").read()
    return len(re.findall(r"<tr>", text))


def check_row_counts():
    expected = {
        "requirements.html": ("requirements.json", "requirements"),
        "providers.html": ("providers.json", "providers"),
        "technical-approach.html": ("technical.json", "findings"),
        "sources.html": ("sources.json", "sources"),
    }
    checked = 0
    for page, (fname, key) in expected.items():
        data = load(fname)[key]
        rows = count_rows(page)
        # one <tr> per row plus one header row per table; sources renders several tables
        header_rows = 1 if fname != "sources.json" else None
        checked += 1
        if fname == "sources.json":
            types = len({s["type"] for s in data})
            if rows != len(data) + types:
                problems.append(f"{page}: {rows} rows rendered, expected {len(data)} + {types} header rows")
        elif rows != len(data) + header_rows:
            problems.append(f"{page}: {rows} rows rendered, expected {len(data) + header_rows}")
    return checked


def check_licence_links():
    prov = load("providers.json")["providers"]
    text = open(os.path.join(ROOT, "providers.html"), encoding="utf-8").read()
    for p in prov:
        lic = p["license_number"]
        if f"LicNum={lic}" not in text:
            problems.append(f"providers.html: no CSLB link for licence {lic}")
    return len(prov)


def check_forbidden():
    hits = 0
    for page in CANONICAL:
        text = open(os.path.join(ROOT, page), encoding="utf-8").read().lower()
        for term in FORBIDDEN:
            if term in text:
                problems.append(f"{page}: contains out-of-scope phrase '{term}'")
                hits += 1
    return len(CANONICAL) * len(FORBIDDEN), hits


def check_nav():
    for page in CANONICAL:
        text = open(os.path.join(ROOT, page), encoding="utf-8").read()
        if '<nav class="nav">' not in text:
            problems.append(f"{page}: navigation block missing")
        for target in CANONICAL:
            if f'href="{target}"' not in text:
                problems.append(f"{page}: navigation link to {target} missing")
    return len(CANONICAL)


def main():
    if not os.path.isfile(os.path.join(ROOT, "verification.html")):
        problems.append("verification.html missing — run scripts/build_project_site.py first")

    links = check_links()
    redirects = check_redirects()
    rows = check_row_counts()
    licences = check_licence_links()
    terms, _ = check_forbidden()
    nav = check_nav()

    report = {
        "checks": {
            "internal_links_checked": links,
            "redirect_check": redirects,
            "data_pages_row_counted": rows,
            "provider_licence_links_checked": licences,
            "forbidden_phrase_scans": terms,
            "pages_nav_checked": nav,
        },
        "problems": problems,
        "result": "pass" if not problems else "fail",
    }
    path = os.path.join(ROOT, "site-data", "verification.json")
    if os.path.isfile(path):
        try:
            existing = json.load(open(path, encoding="utf-8"))
            existing["independent_checks"] = report
            json.dump(existing, open(path, "w", encoding="utf-8"), indent=2)
        except Exception as exc:  # pragma: no cover - defensive
            print("could not update verification.json:", exc)

    if problems:
        for p in problems:
            print("FAIL:", p)
        print(f"\n{len(problems)} problem(s)")
        return 1
    print(f"PASS — internal links {links}, redirects checked, {rows} data pages row-counted, "
          f"{licences} licence links, {terms} phrase scans, {nav} pages with navigation")
    return 0


if __name__ == "__main__":
    sys.exit(main())

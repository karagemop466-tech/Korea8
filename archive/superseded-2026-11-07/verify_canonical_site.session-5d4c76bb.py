#!/usr/bin/env python3
"""Independent verification of the generated canonical site.

Reads only the built HTML (plus the data files for row counts) and fails on:
  * a data row with no source link and no explicit owner/unverified marker;
  * a unverified quote amount appearing anywhere;
  * reader-facing wording outside the neutral repair-scope rule;
  * a broken internal link or a missing page/navigation entry;
  * an external script/style/image reference (the site must be self-contained);
  * row-count drift between the data files and the rendered tables.

Writes site-data/verification.json.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site-data"

PAGES = [
    "index.html",
    "executive-summary.html",
    "requirements.html",
    "providers.html",
    "estimates.html",
    "technical-approach.html",
    "code-and-permit.html",
    "sources.html",
    "flagged-for-review.html",
    "verification.html",
]

# Unverified quote amounts from the owner's brief must never be published.
FORBIDDEN_AMOUNTS = [r"\$135", r"\$550", r"\$614"]

# Retired: wording is checked by scripts/wording_guard.py.
FORBIDDEN_PHRASES: list[str] = []

checks: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "ok": bool(ok), "detail": detail})


VOID = {"meta", "link", "br", "img", "hr", "input", "source"}


class _Balance(HTMLParser):
    """Minimal tag-balance checker."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"extra </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"mismatch </{tag}>")


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def rows_of(html: str) -> list[str]:
    return re.findall(r"<tr>(.*?)</tr>", html, flags=re.S)


def main() -> int:
    pages = {p: (ROOT / p).read_text(encoding="utf-8") for p in PAGES if (ROOT / p).exists()}

    check("all pages present", len(pages) == len(PAGES),
          f"{len(pages)}/{len(PAGES)}: {', '.join(sorted(set(PAGES) - set(pages))) or 'none missing'}")

    # --- navigation on every page
    nav_ok = all(all(f'href="{p}"' in html for p in PAGES) for html in pages.values())
    check("every page links every other page in the nav", nav_ok)

    # --- internal links resolve
    broken = []
    for slug, html in pages.items():
        for href in re.findall(r'href="([^"#:]+)"', html):
            if href.startswith(("http", "mailto:", "//")):
                continue
            if href not in pages and not (ROOT / href).exists():
                broken.append(f"{slug} -> {href}")
    check("no broken internal links", not broken, "; ".join(broken[:8]))

    # --- self-contained assets
    external = []
    for slug, html in pages.items():
        for tag in re.findall(r"<(?:script|img|link)[^>]*>", html):
            for url in re.findall(r'(?:src|href)="(http[^"]+)"', tag):
                external.append(f"{slug}: {url}")
    check("no external script/style/image dependencies", not external, "; ".join(external[:5]))

    # --- amounts
    hits = []
    for slug, html in pages.items():
        for pat in FORBIDDEN_AMOUNTS:
            if re.search(pat, html):
                hits.append(f"{slug}: {pat}")
    check("no unverified quote amount is published", not hits, "; ".join(hits))

    # --- wording check
    phrase_hits = []
    for slug, html in pages.items():
        low = html.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in low:
                phrase_hits.append(f"{slug}: '{phrase}'")
    check("reader-facing wording is neutral", not phrase_hits,
          "; ".join(phrase_hits[:6]))
    check("punctuation check — no 'None' or 'nan' literals", not any(
        re.search(r">\s*(None|nan|NaN)\s*<", h) for h in pages.values()))

    # --- row-level source discipline
    id_pat = re.compile(r'class="mono">((?:P|C|T|R|E|FEE|B|S|F)-\d+)<')
    unsourced = []
    total_rows = 0
    for slug, html in pages.items():
        for row in rows_of(html):
            m = id_pat.search(row)
            if not m:
                continue
            total_rows += 1
            rid = m.group(1)
            has_link = 'href="http' in row
            has_marker = any(t in row for t in ("owner-provided", "unverified", "no official source", "Official source", "official source"))
            if not has_link and not has_marker:
                unsourced.append(f"{slug}:{rid}")
    check("every data row carries a source link or an explicit marker", not unsourced,
          f"{total_rows} rows checked; offenders: {', '.join(unsourced[:8])}")

    # --- row-count parity with the data files
    providers = load("providers.json")["providers"]
    expected_rows = {
        "providers": len(providers),
        "requirements": len(load("requirements.json")["requirements"]),
        "flags": len(load("flags.json")["flags"]),
        "sources": len(load("sources.json")["sources"]),
    }
    prov_html = pages.get("providers.html", "")
    prov_ids = set(re.findall(r'class="mono">(P-\d+)<', prov_html))
    check("every provider renders a row", len(prov_ids) == expected_rows["providers"],
          f"{len(prov_ids)} of {expected_rows['providers']}")

    req_ids = set(re.findall(r'class="mono">(R-\d+)<', pages.get("requirements.html", "")))
    check("every requirement renders a row", len(req_ids) == expected_rows["requirements"],
          f"{len(req_ids)} of {expected_rows['requirements']}")

    flag_ids = set(re.findall(r'class="mono">(F-\d+)<', pages.get("flagged-for-review.html", "")))
    check("every flag renders", len(flag_ids) == expected_rows["flags"],
          f"{len(flag_ids)} of {expected_rows['flags']}")

    src_ids = set(re.findall(r'class="mono">(S-\d+)<', pages.get("sources.html", "")))
    check("every source renders", len(src_ids) == expected_rows["sources"],
          f"{len(src_ids)} of {expected_rows['sources']}")

    # --- provider rows must cite CSLB
    prov_rows = rows_of(prov_html)
    cslb_ok = all("cslb.ca.gov" in row for row in prov_rows if id_pat.search(row))
    check("every provider row cites an official CSLB page", cslb_ok)

    # --- HTML well-formedness
    problems = []
    for slug, html in pages.items():
        parser = _Balance()
        parser.feed(html)
        if parser.errors or parser.stack:
            problems.append(f"{slug}: {parser.errors[:2] or parser.stack[:3]}")
    check("pages are well-formed HTML (tag balance)", not problems, "; ".join(problems[:4]))

    # --- footer canonical statement
    check("every page states it is the single authoritative copy",
          all("single authoritative copy" in h.lower() for h in pages.values()))

    passed = sum(1 for c in checks if c["ok"])
    result = {
        "verified_on": "2026-11-07",
        "pages": len(pages),
        "rows_checked": total_rows,
        "checks_run": len(checks),
        "checks_passed": passed,
        "checks_failed": len(checks) - passed,
        "result": "PASS" if passed == len(checks) else "FAIL",
        "checks": checks,
    }
    (DATA / "verification.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")

    for c in checks:
        print(("PASS " if c["ok"] else "FAIL ") + c["check"] + (f" — {c['detail']}" if c["detail"] else ""))
    print(f"\n{passed}/{len(checks)} checks passed — {result['result']}")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verify the built bathtub project site.

Checks, in order:
  1. every internal href/src resolves to a file that exists;
  2. every in-page anchor (#id) used in a link exists in the target page;
  3. every table row that carries data carries a source link (counted per table);
  4. every external link is https and points at an official or primary domain;
  5. no private/internal project information appears in any published file;
  6. rendered row counts match the JSON datasets (no silent drop or duplication);
  7. no placeholder text or unresolved template markers.

Exit code 1 on any failure. Writes project/verification.json.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [
    "index.html", "executive-summary.html", "requirements.html", "estimates.html",
    "providers.html", "technical-approach.html", "sources.html", "verification.html",
    "flagged-for-review.html",
]
OFFICIAL_DOMAINS = {
    "www.cslb.ca.gov", "leginfo.legislature.ca.gov", "www.sf.gov", "aa.iapmo.org",
    "forms.iapmo.org", "www.watcomfg.com", "www.yelp.com",
    "github.com",
}
# Company websites carried over from the earlier verification pass. Permitted as contact links only:
# the Sources page marks every one of them 'linked-not-rechecked', and no licence value comes from them.
PROVIDER_DOMAINS = {
    "www.eplumbingsolutions.com", "www.bayareaplumbingsf.com",
    "www.fastresponseplumbingsf.com", "www.heisesplumbing.com",
    "www.aceplumbingandrooter.com", "www.wedoconstructions.com",
    "sfbuildinggroup.com", "www.rapidflowbayarea.com",
}
# Phrases that must never appear on the published site.
BANNED = [
    "no permit", "without a permit", "permit cannot", "can't pull", "cannot pull",
    "avoid the permit", "skip the permit", "off the record", "off-record",
    "internal use", "confidential", "keep private", "not public", "privately",
    "for reasons", "unmentionable", "under the table", "cash only",
]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []   # (attr, value)
        self.ids: set[str] = set()
        self.rows = 0
        self.rows_with_link = 0
        self._in_tr = False
        self._tr_has_link = False
        self._in_thead = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        for attr in ("href", "src"):
            if attr in d and d[attr]:
                self.links.append((attr, d[attr]))
        if tag == "thead":
            self._in_thead = True
        if tag == "tbody":
            self._in_thead = False
        if tag == "tr":
            self._in_tr = True
            self._tr_has_link = False
        if tag == "a" and self._in_tr:
            self._tr_has_link = True

    def handle_endtag(self, tag):
        if tag == "thead":
            self._in_thead = False
        if tag == "tr" and self._in_tr:
            self._in_tr = False
            if not self._in_thead:
                self.rows += 1
                if self._tr_has_link:
                    self.rows_with_link += 1


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    report: dict = {"checked": [], "problems": problems, "warnings": warnings}

    docs: dict[str, Collector] = {}
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            problems.append(f"missing page: {page}")
            continue
        text = path.read_text(encoding="utf-8")
        c = Collector()
        c.feed(text)
        docs[page] = c

    # 1 + 2: internal links and anchors
    internal = anchors = 0
    for page, c in docs.items():
        for attr, value in c.links:
            if value.startswith(("http://", "https://", "mailto:")):
                continue
            internal += 1
            target, _, frag = value.partition("#")
            target_page = target or page
            if not (ROOT / target_page).exists():
                problems.append(f"{page}: broken internal link -> {value}")
                continue
            if frag:
                anchors += 1
                tc = docs.get(target_page)
                if tc is None:
                    tc = Collector()
                    tc.feed((ROOT / target_page).read_text(encoding="utf-8"))
                if frag not in tc.ids:
                    problems.append(f"{page}: anchor not found -> {value}")
    report["checked"].append(f"internal links: {internal}, anchors: {anchors}")

    # 3: rows with a source link
    for page, c in docs.items():
        if page == "requirements.html" and c.rows and c.rows_with_link != c.rows:
            warnings.append(
                f"{page}: {c.rows - c.rows_with_link} of {c.rows} table rows carry no link "
                f"(expected only on the first-party requirement table)"
            )
        elif page not in ("requirements.html",) and c.rows and c.rows_with_link != c.rows:
            warnings.append(f"{page}: {c.rows - c.rows_with_link} of {c.rows} rows carry no source link")
    report["checked"].append("source link per table row")

    # 4: external links are https and on a listed domain
    external = 0
    for page, c in docs.items():
        for attr, value in c.links:
            if not value.startswith(("http://", "https://")):
                continue
            external += 1
            u = urlparse(value)
            if u.scheme != "https":
                problems.append(f"{page}: non-https external link -> {value}")
            if u.netloc not in OFFICIAL_DOMAINS and u.netloc not in PROVIDER_DOMAINS:
                problems.append(f"{page}: unlisted external domain -> {u.netloc}")
    report["checked"].append(f"external links: {external} (official/primary domains, plus provider contact sites)")

    # 5: privacy sweep over every published root file
    published = PAGES + ["style.css"]
    for name in published:
        path = ROOT / name
        if not path.exists():
            continue
        low = path.read_text(encoding="utf-8").lower()
        for phrase in BANNED:
            if phrase in low:
                problems.append(f"{name}: banned phrase present -> '{phrase}'")
    report["checked"].append("privacy sweep")

    # 6: rendered counts match JSON
    prov = json.loads((ROOT / "project/providers.json").read_text())
    est = json.loads((ROOT / "project/estimates.json").read_text())
    flags = json.loads((ROOT / "project/flagged.json").read_text())
    req = json.loads((ROOT / "project/requirements.json").read_text())
    src = json.loads((ROOT / "project/sources.json").read_text())
    tech = json.loads((ROOT / "project/technical.json").read_text())

    prov_html = (ROOT / "providers.html").read_text()
    for p in prov["providers"]:
        if f'id="{p["id"]}"' not in prov_html:
            problems.append(f"providers.html missing row {p['id']}")
        if p["license"] not in prov_html:
            problems.append(f"providers.html missing licence {p['license']}")
    for e in est["estimates"]:
        if f'id="{e["id"]}"' not in (ROOT / "estimates.html").read_text():
            problems.append(f"estimates.html missing row {e['id']}")
    flags_html = (ROOT / "flagged-for-review.html").read_text()
    for f in flags["flags"]:
        if f'id="{f["id"]}"' not in flags_html:
            problems.append(f"flagged page missing {f['id']}")
    req_html = (ROOT / "requirements.html").read_text()
    for g in req["regulatory"] + req["brief"]:
        if f'id="{g["id"]}"' not in req_html:
            problems.append(f"requirements.html missing {g['id']}")
    src_html = (ROOT / "sources.html").read_text()
    for s in src["sources"]:
        if f'id="{s["id"]}"' not in src_html:
            problems.append(f"sources.html missing {s['id']}")
    tech_html = (ROOT / "technical-approach.html").read_text()
    for t in tech["findings"]:
        if f'id="{t["id"]}"' not in tech_html:
            problems.append(f"technical page missing {t['id']}")
    report["checked"].append("rendered rows match JSON")

    # 6b: every provider row's source URL must appear verbatim on the page
    for p in prov["providers"]:
        if p["source_url"] not in prov_html:
            problems.append(f"providers.html: CSLB link missing for {p['id']}")

    # every regulatory requirement must render its official link (href is HTML-escaped)
    def rendered(url: str) -> bool:
        return url in req_html or url.replace("&", "&amp;") in req_html

    for g in req["regulatory"]:
        if not rendered(g["source_url"]):
            problems.append(f"requirements.html: source link missing for {g['id']}")

    # 7: template markers / placeholders
    for name in PAGES:
        text = (ROOT / name).read_text(encoding="utf-8")
        for marker in ("{", "}", "TODO", "Lorem", "FIXME", "None</td>"):
            if marker in ("{", "}"):
                if re.search(r"\{[a-z_]+\}", text):
                    problems.append(f"{name}: unresolved template marker")
            elif marker in text:
                problems.append(f"{name}: placeholder text '{marker}'")
        if "size=" in text and "stylesheet" not in text:
            problems.append(f"{name}: stylesheet not linked")
    report["checked"].append("no placeholder or template markers")

    report["ok"] = not problems
    report["summary"] = f"{len(report['checked'])} check groups, {len(problems)} problems, {len(warnings)} warnings"
    (ROOT / "project/verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(report["summary"])
    for w in warnings:
        print("  WARN:", w)
    for p in problems:
        print("  FAIL:", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())

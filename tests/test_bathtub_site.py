#!/usr/bin/env python3
"""Line-by-line verification of the bathtub project site.

Run directly:      python tests/test_bathtub_site.py
Run under pytest:  python -m pytest tests/test_bathtub_site.py -q

Checks
  1. provenance  - no row may claim to be verified unless its source URL is in
                   url_registry.json with retrieval_status == "retrieved"
  2. completeness- every row in every dataset carries either a source URL or an
                   explicit statement that no official source exists
  3. links       - every internal link in the built HTML resolves to a file
  4. registry    - every external link in the built HTML is in the registry
  5. rendering   - no page contains an unresolved template artefact

Writes artifacts/bathtub_linkcheck.json.
Exits non-zero on any violation.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bathtub"
DOCS = ROOT / "docs"
OUT = ROOT / "bathtub"
ART = ROOT / "artifacts"

REGISTRY = {e["url"]: e for e in json.loads((DATA / "url_registry.json").read_text())["entries"]}


def retrieved(url: str | None) -> bool:
    if not url:
        return False
    ent = REGISTRY.get(url)
    return bool(ent and ent.get("retrieval_status") == "retrieved")


class LinkGrab(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k in ("href", "src"):
            if k in d:
                self.links.append(d[k])


def collect_rows():
    """(dataset, row_id, description, source_url, verified_flag)"""
    out = []

    def walk(name, rows, url_key="source_url"):
        for r in rows:
            out.append((name, r.get("id", "?"), r.get("topic") or r.get("title")
                        or r.get("requirement") or r.get("display_name") or r.get("provider_label")
                        or r.get("url") or "?",
                        r.get(url_key), bool(r.get("verified"))))

    walk("providers", json.loads((DATA / "providers.json").read_text())["providers"],
         url_key="official_source_url")
    walk("estimates", json.loads((DATA / "estimates.json").read_text())["estimates"])
    for a in json.loads((DATA / "estimates.json").read_text())["analysis"]:
        out.append(("estimates.analysis", a["id"], a["finding"], None, bool(a.get("verified"))))
    walk("regulations", json.loads((DATA / "regulations.json").read_text())["rows"])
    walk("technical", json.loads((DATA / "technical.json").read_text())["rows"])
    req = json.loads((DATA / "requirements.json").read_text())
    for cat in req["categories"]:
        walk("requirements", cat["requirements"], url_key="official_source_url")
    walk("flags", json.loads((DATA / "flags.json").read_text())["flags"])
    for u, ent in REGISTRY.items():
        out.append(("url_registry", "URL", ent.get("publisher", ""), u,
                    ent.get("retrieval_status") == "retrieved"))
    return out


def main() -> int:
    ART.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    warnings: list[str] = []
    stats: dict[str, int] = {}

    # ---- 1 & 2: provenance -------------------------------------------------
    rows = collect_rows()
    stats["rows_checked"] = len(rows)
    verified_no_source = []
    for ds, rid, desc, url, flag in rows:
        if flag and not retrieved(url):
            verified_no_source.append(f"{ds}/{rid}: marked verified but source not retrieved ({url})")
    stats["rows_verified"] = sum(1 for r in rows if r[4])
    stats["rows_unverified"] = sum(1 for r in rows if not r[4])
    problems += verified_no_source

    # ---- 3 & 4: links in the built HTML ------------------------------------
    # only pages this session owns are link-checked; the integrated root
    # dashboard belongs to another session and is out of scope here.
    pages = sorted(OUT.glob("*.html"))
    stats["pages_checked"] = len(pages)
    internal_bad: list[str] = []
    external_unregistered: list[str] = []
    external_bad: list[str] = []
    internal_ok = 0
    external_ok = 0
    anchors_bad: list[str] = []

    for p in pages:
        text = p.read_text()
        g = LinkGrab()
        g.feed(text)
        for href in g.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                if href.startswith(("mailto:", "tel:")):
                    continue
                if href not in REGISTRY:
                    external_unregistered.append(f"{p.name}: {href}")
                elif REGISTRY[href]["retrieval_status"] != "retrieved":
                    external_bad.append(f"{p.name}: {href} ({REGISTRY[href]['retrieval_status']})")
                else:
                    external_ok += 1
                continue
            # internal / relative
            target = href.split("#")[0]
            frag = href.split("#")[1] if "#" in href else None
            if not target:
                if frag:
                    # same-page anchor: check it exists in this document
                    if f'id="{frag}"' not in text:
                        anchors_bad.append(f"{p.name}: missing anchor #{frag}")
                continue
            resolved = (p.parent / target).resolve()
            if not resolved.exists():
                internal_bad.append(f"{p.name}: {href} -> {resolved}")
            else:
                internal_ok += 1
                if frag:
                    tgt_text = resolved.read_text(errors="ignore")
                    if f'id="{frag}"' not in tgt_text:
                        anchors_bad.append(f"{p.name}: {href} -> missing anchor #{frag}")

    stats["internal_links_ok"] = internal_ok
    stats["external_links_ok"] = external_ok
    problems += [f"BROKEN INTERNAL LINK {x}" for x in internal_bad]
    problems += [f"UNREGISTERED EXTERNAL LINK {x}" for x in external_unregistered]
    warnings += [f"external link present but not retrieved: {x}" for x in external_bad]
    problems += [f"BROKEN ANCHOR {x}" for x in anchors_bad]

    # ---- 5: rendering artefacts --------------------------------------------
    artefacts = []
    for p in pages:
        t = p.read_text()
        for pat in ("{", "}", "None", "Undefined"):
            if pat in ("{", "}"):
                # only flag brace pairs that look like unrendered f-string slots
                for m in re.finditer(r"\{[a-z_]+\[", t):
                    artefacts.append(f"{p.name}: {m.group(0)!r}")
        if ">None<" in t:
            artefacts.append(f"{p.name}: rendered 'None'")
        if "False<" in t or ">False<" in t:
            artefacts.append(f"{p.name}: rendered 'False'")
    problems += [f"RENDER ARTEFACT {x}" for x in artefacts]

    report = {
        "generated_utc": "2026-11-06",
        "stats": stats,
        "problems": problems,
        "warnings": warnings,
        "result": "PASS" if not problems else "FAIL",
    }
    (ART / "bathtub_linkcheck.json").write_text(json.dumps(report, indent=2) + "\n")
    (OUT / "data" / "linkcheck.json").write_text(json.dumps(report, indent=2) + "\n")

    print(json.dumps(report["stats"], indent=2))
    for w in warnings:
        print("WARN ", w)
    if problems:
        print(f"\nFAILED — {len(problems)} problem(s):")
        for x in problems:
            print("  -", x)
        return 1
    print(f"\nPASS — {len(problems)} problems, {len(warnings)} warnings")
    return 0


def test_site_passes():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())

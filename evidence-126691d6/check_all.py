#!/usr/bin/env python3
"""Final-integration verification (session arena/126691d6-korea8, 2026-11-07).

Two passes over every published HTML file in the repository tree:

1. Internal link check — every relative href/src on any published page must
   resolve to a file that exists on disk (anchors are not checked; GitHub Pages
   serves directories' index.html, so directory links resolve to index.html).

2. Privacy sweep — the published pages must not contain phrases that identify or
   describe material the owner asked to keep out of public records. Public-law
   statements (e.g. the CSLB general rule that no structure may be repaired
   "without a permit unless exempt", or the BPC 7048 statute text) are
   allow-listed as official-source quotes; the phrases below target meta-copy
   that discusses the excluded material itself.

Outputs JSON reports under evidence-126691d6/.
"""
import html.parser
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUBLISH_DIRS = ["", "trip-lever", "bathroom-overflow", "bathtub-overflow", "bathtub", "docs"]
STATIC_EXTS = {".html", ".htm"}

FORBIDDEN = [
    "keep private",
    "never become public",
    "never be mentioned",
    "private constraints",
    "scheduling and permit",
    "scheduling and background",
    "permit background",
    "internal scheduling",
    "internal-use constraint",
    "no private content",
    "private case details",
    "no private or sensitive information is published",
    "private or sensitive information is published on this site",
    "deliberately excluded",
    "must never be added",
    "standing instruction",
    "off-record workaround",
    "off the record",
    "work to be done without a permit",
    "without a permit for reasons",
    "cannot pull a permit",
    "Internal use only.",
]
# phrases that are legitimate official-source quotes (do not flag):
ALLOW = [
    "without a permit unless exempt",          # CSLB-published general rule quote
    "does not require a building permit",      # BPC 7048 statute text
    "no structure may be altered or repaired", # CSLB-published general rule quote
]


class LinkGrabber(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


def html_files():
    out = []
    for base in PUBLISH_DIRS:
        d = os.path.join(ROOT, base) if base else ROOT
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames if x not in {".git", "node_modules", "__pycache__"}]
            for fn in filenames:
                if os.path.splitext(fn)[1] in STATIC_EXTS:
                    out.append(os.path.join(dirpath, fn))
    return sorted(out)


def link_check():
    broken = []
    checked = 0
    for path in html_files():
        rel_dir = os.path.dirname(os.path.relpath(path, ROOT))
        text = open(path, encoding="utf-8", errors="replace").read()
        p = LinkGrabber()
        p.feed(text)
        for ref in p.refs:
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            target = ref.split("#")[0].split("?")[0]
            if not target:
                continue
            checked += 1
            fs_target = os.path.normpath(os.path.join(ROOT, rel_dir, target))
            ok = os.path.isfile(fs_target)
            if not ok and os.path.isdir(fs_target):
                ok = os.path.isfile(os.path.join(fs_target, "index.html"))
            if not ok:
                broken.append({"file": os.path.relpath(path, ROOT), "ref": ref})
    return {"internal_links_checked": checked, "broken": broken}


def privacy():
    hits = []
    for path in html_files():
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8", errors="replace").read()
        plain = re.sub(r"\s+", " ", text)
        for phrase in FORBIDDEN:
            if phrase.lower() in plain.lower():
                if any(a.lower() in plain.lower() for a in ALLOW) and phrase in {
                    "work to be done without a permit",
                }:
                    continue
                idx = plain.lower().find(phrase.lower())
                hits.append({"file": rel, "phrase": phrase,
                             "context": plain[max(0, idx - 90): idx + len(phrase) + 90]})
    return {"phrases_checked": FORBIDDEN, "hits": hits}


def main():
    out_dir = os.path.join(ROOT, "evidence-126691d6")
    os.makedirs(out_dir, exist_ok=True)
    lc = link_check()
    pv = privacy()
    with open(os.path.join(out_dir, "linkcheck_all_20261107.json"), "w") as fh:
        json.dump(lc, fh, indent=1)
    with open(os.path.join(out_dir, "privacy_sweep_20261107.json"), "w") as fh:
        json.dump(pv, fh, indent=1)
    print(f"internal links checked: {lc['internal_links_checked']}; broken: {len(lc['broken'])}")
    for b in lc["broken"][:25]:
        print("  BROKEN:", b)
    print(f"privacy phrases checked: {len(pv['phrases_checked'])}; hits: {len(pv['hits'])}")
    for h in pv["hits"][:25]:
        print("  HIT:", h["file"], "::", h["phrase"])
    return 1 if (lc["broken"] or pv["hits"]) else 0


if __name__ == "__main__":
    sys.exit(main())

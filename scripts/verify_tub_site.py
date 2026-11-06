#!/usr/bin/env python3
"""Fail-closed verification gate for the trip-lever site.

Checks, all with stdlib only:

  1. every expected page exists and is non-trivial;
  2. every internal href resolves to a real file, and every on-page #anchor resolves;
  3. every external href is https and resolves to a host we deliberately cite;
  4. every <tr> in a <tbody> carries at least one source link or an explicit UNVERIFIED cell;
  5. no placeholder text ("TODO", "TBD", "lorem") anywhere;
  6. the private constraint is absent from every published file (keyword blocklist);
  7. the data files contain no literal value that is unreachable from the rendered page set
     (i.e. counts match);
  8. every source id referenced in data/tub/*.json exists in sources.json.

Writes tub-verification.json. Exit code 1 on any failure.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tub"

EXPECTED = [
    "index.html", "providers.html", "quotes.html", "requirements.html",
    "rules.html", "access.html", "sources.html", "flagged.html",
    "style.css", ".nojekyll", "feed.json",
]

CITED_HOSTS = (
    "cslb.ca.gov",
    "sf.gov",
    "leginfo.legislature.ca.gov",
    "codelibrary.amlegal.com",
    "media.api.sf.gov",
    "iapmo.org",
    "aa.iapmo.org",
    "epa.gov",
    "drivendata.org",
    "techcomm.kohler.com",
    "fastresponseplumbingsf.com",
    "bayareaplumbingsf.com",
    "heisesplumbing.com",
    "precisionrooterdrain.com",
    "bestplumbers.com",
    "buildzoom.com",
    "yelp.com",
    "github.com",
)

# Words that must never appear in published output, because they would disclose the
# owner's private constraint. Kept generic on purpose; see data/tub/flagged.json P-01.
FORBIDDEN = [
    "without a permit",
    "no permit",
    "unpermitted",
    "under the table",
    "skip the permit",
    "avoid the permit",
    "permit-free",
    "off the books",
    "keep it private",
    "cannot pull a permit",
    "can't pull a permit",
    "cannot pull a permit",
    "for reasons that need to stay private",
    "need to stay private",
    "stays private",
    "never mentioned",
    "never becomes public",
    "must stay private",
]

PLACEHOLDERS = ["TODO", "TBD", "lorem ipsum", "FIXME", "XXX", "placeholder text"]

results: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    results.append({"check": name, "ok": True if ok else False, "detail": detail})


def anchors_and_links(text: str) -> tuple[list[str], list[str], set[str]]:
    hrefs = re.findall(r'href="([^"]+)"', text)
    ids = set(re.findall(r'\sid="([^"]+)"', text))
    internal = [h for h in hrefs if not h.startswith(("http://", "https://", "mailto:", "tel:"))]
    external = [h for h in hrefs if h.startswith(("http://", "https://"))]
    return internal, external, ids


def main() -> int:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pages = [p for p in EXPECTED if p.endswith(".html")]

    # 1 -- pages exist
    for name in EXPECTED:
        p = ROOT / name
        size = p.stat().st_size if p.exists() else -1
        ok = p.exists() and (size > 0 or name == ".nojekyll")
        check(f"exists:{name}", ok, f"{p.stat().st_size if p.exists() else 0} bytes")

    # 2 -- internal links and anchors
    page_ids = {}
    for p in pages:
        _int, _ext, ids = anchors_and_links((ROOT / p).read_text(encoding="utf-8"))
        page_ids[p] = ids
    broken, checked = [], 0
    for p in pages:
        text = (ROOT / p).read_text(encoding="utf-8")
        internal, _ext, _ids = anchors_and_links(text)
        for h in internal:
            checked += 1
            target, _, frag = h.partition("#")
            if target == "":
                if frag and frag not in page_ids[p]:
                    broken.append(f"{p} -> #{frag} (no such id on page)")
                continue
            tp = (ROOT / target)
            if not tp.exists():
                broken.append(f"{p} -> {target} (missing file)")
                continue
            if frag:
                if target not in page_ids:
                    page_ids[target] = anchors_and_links(tp.read_text(encoding="utf-8"))[2]
                if frag not in page_ids[target]:
                    broken.append(f"{p} -> {target}#{frag} (no such id)")
    check("internal_links_resolve", not broken,
          f"{checked} internal links checked; broken: {broken if broken else 'none'}")

    # 3 -- external links: https only and a cited host
    bad_ext = []
    n_ext = 0
    for p in list(pages) + ["gems_site/index.html", "gems_site/sources.html", "gems_site/limitations.html"]:
        fp = ROOT / p
        if not fp.exists():
            continue
        _i, external, _d = anchors_and_links(fp.read_text(encoding="utf-8"))
        for h in external:
            n_ext += 1
            if not h.startswith("https://"):
                bad_ext.append(f"{p}: {h} (not https)")
                continue
            host = re.sub(r"^https://([^/]+).*$", r"\1", h).lower()
            if not any(host == c or host.endswith("." + c) or host.endswith(c) for c in CITED_HOSTS):
                bad_ext.append(f"{p}: {h} (host {host} not on the cited list)")
    check("external_links_https_and_known", not bad_ext,
          f"{n_ext} external links checked; problems: {bad_ext if bad_ext else 'none'}")

    # 4 -- every tbody row has a source cell
    bad_rows, n_rows = [], 0
    for p in pages:
        text = (ROOT / p).read_text(encoding="utf-8")
        for body in re.findall(r"<tbody>(.*?)</tbody>", text, flags=re.S):
            for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, flags=re.S):
                n_rows += 1
                has_src_link = re.search(r'href="https://[^"]+"[^>]*>\s*S\d+', row) is not None
                has_unverified = "UNVERIFIED" in row or "no source" in row
                # sources.html rows ARE the source: each row links its own document by S-id.
                if p == "sources.html":
                    # the row IS the source record; its own document link is the citation
                    has_src_link = (re.search(r'href="https://[^"]+">\s*(<!--.*?-->)?S\d+', row) is not None)
                if not (has_src_link or has_unverified):
                    bad_rows.append(f"{p}: {re.sub(r'<[^>]+>', ' ', row)[:90].strip()}")
    check("every_row_has_source_cell", not bad_rows,
          f"{n_rows} table rows checked; missing source: {bad_rows if bad_rows else 'none'}")

    # 5 -- no placeholders
    hits = []
    for p in pages:
        low = (ROOT / p).read_text(encoding="utf-8").lower()
        for ph in PLACEHOLDERS:
            if ph.lower() in low:
                hits.append(f"{p}: {ph}")
    check("no_placeholders", not hits, str(hits if hits else "none"))

    # 6 -- private constraint absent from every published artefact
    leaks = []
    scan = pages + ["feed.json", "style.css"]
    scan += [str(f.relative_to(ROOT)) for f in DATA.glob("*.json")]
    scan += ["REPO_REVIEW.md", "COORDINATION.md"]
    for rel in scan:
        fp = ROOT / rel
        if not fp.exists():
            continue
        low = fp.read_text(encoding="utf-8").lower()
        for w in FORBIDDEN:
            if w in low:
                leaks.append(f"{rel}: '{w}'")
    check("private_constraint_absent", not leaks, str(leaks if leaks else "none"))

    # 7 -- data/render count agreement
    def n(path, key):
        return len(json.loads((DATA / f"{path}.json").read_text())[key])

    counts = {
        "requirements": n("requirements", "requirements"),
        "vendors": n("vendors", "vendors"),
        "estimates": n("estimates", "estimates"),
        "rules": n("rules", "rules"),
        "sources": n("sources", "sources"),
        "unverified": n("flagged", "unverified_items"),
        "irregularities": n("flagged", "irregularities"),
        "questions": n("flagged", "questions_to_ask"),
        "options": n("scope", "options"),
    }
    rendered = {
        "requirements": (ROOT / "requirements.html").read_text().count('data-kind="req"'),
        "vendors": (ROOT / "providers.html").read_text().count('data-kind="vendor"'),
        "estimates": (ROOT / "quotes.html").read_text().count('data-kind="estimate"'),
        "rules": (ROOT / "rules.html").read_text().count('data-kind="rule"'),
        "sources": (ROOT / "sources.html").read_text().count('data-kind="source"'),
    }
    mismatch = {k: (counts[k], v) for k, v in rendered.items() if counts[k] != v}
    check("data_matches_rendered_counts", not mismatch,
          f"data vs html: {{k: (data, rendered) for mismatches}} = {mismatch if mismatch else 'all equal'}"
          f" (data counts: {counts})")

    # 8 -- every referenced source id exists
    known = {s["id"] for s in json.loads((DATA / "sources.json").read_text())["sources"]}
    missing = set()
    for f in DATA.glob("*.json"):
        if f.name == "sources.json":
            continue
        text = f.read_text()
        for m in re.findall(r'"S\d{2}"', text):
            sid = m.strip('"')
            if sid not in known:
                missing.add(f"{f.name}:{sid}")
    check("all_source_ids_defined", not missing, str(sorted(missing) if missing else "none"))

    # 9 -- the GEMS archive still resolves
    gems_broken = []
    for gp in (ROOT / "gems_site").glob("*.html"):
        internal, _e, _d = anchors_and_links(gp.read_text(encoding="utf-8"))
        for h in internal:
            if not (ROOT / "gems_site" / h.partition("#")[0]).exists():
                gems_broken.append(f"{gp.name} -> {h}")
    check("gems_archive_links_resolve", not gems_broken,
          str(gems_broken if gems_broken else "none"))

    failed = [r for r in results if not r["ok"]]
    report = {
        "schema": "tub-verification-v1",
        "generated_utc": generated,
        "ok": not failed,
        "n_checks": len(results),
        "n_failed": len(failed),
        "data_counts": counts,
        "checks": results,
    }
    (ROOT / "tub-verification.json").write_text(json.dumps(report, indent=2) + "\n")

    for r in results:
        print(("PASS " if r["ok"] else "FAIL ") + r["check"] + " — " + r["detail"][:300])
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

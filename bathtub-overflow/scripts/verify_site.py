#!/usr/bin/env python3
"""Fail-closed verification of the bathtub-overflow dataset and the generated site.

Checks that can be made without human inspection:
  * every table row carries at least one source link;
  * every source reference resolves to a real entry in sources.json (or to an https URL);
  * every licence record points at an official CSLB page;
  * every value that could not be confirmed is flagged, and every flag id exists;
  * the rendered HTML row counts match the JSON row counts;
  * no internal link is broken;
  * no placeholder text survives;
  * no private/internal content leaked into the published files.

Exit code 0 only if every check passes. Writes bathtub-overflow/evidence/verification.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SITE = ROOT  # published subtree root
EVID = ROOT / "evidence"

DATA_FILES = ["sources.json", "vendors.json", "requirements.json", "costs.json",
              "code_facts.json", "findings.json", "flagged.json"]

PAGES = ["index.html", "scope.html", "vendors.html", "costs.html", "code.html",
         "findings.html", "flagged.html", "sources.html"]

# Phrases that would disclose internal, non-public project information in a published file.
FORBIDDEN = [
    "proceed without a permit",
    "performed without a permit",
    "work without a permit",
    "without a permit, and",
    "no permit required",
    "unpermitted work",
    "skip the permit",
    "private reason",
]
PLACEHOLDERS = ["TODO", "TBD", "FIXME", "lorem ipsum", "XXX", "<placeholder>"]

CSLB_LICENSE_BASE = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/"

checks: list[dict] = []


def check(cid: str, desc: str, ok: bool, detail: str = "") -> bool:
    checks.append({"id": cid, "description": desc, "ok": bool(ok), "detail": detail})
    return bool(ok)


def load(name: str):
    return json.loads((DATA / name).read_text())


def main() -> int:
    data = {}
    ok_all = True
    for name in DATA_FILES:
        try:
            data[name] = load(name)
            check(f"DATA-{name}", f"{name} parses as JSON", True)
        except Exception as exc:  # pragma: no cover - defensive
            ok_all = False
            check(f"DATA-{name}", f"{name} parses as JSON", False, str(exc))
            return finish(0)

    sources = data["sources.json"]["sources"]
    sources_by_id = {s["id"]: s for s in sources}
    flagged_ids = {i["id"] for i in data["flagged.json"]["items"]}
    vendors = data["vendors.json"]["vendors"]
    requirements = data["requirements.json"]["requirements"]
    findings = data["findings.json"]["findings"]
    costs = data["costs.json"]
    code_facts = data["code_facts.json"]["facts"]

    # --- sources ------------------------------------------------------------
    bad = [s["id"] for s in sources if not s.get("url", "").startswith("https://")]
    ok_all &= check("SRC-SCHEME", "every source URL is https", not bad, ", ".join(bad))
    bad = [s["id"] for s in sources if not s.get("verifies", "").strip()]
    ok_all &= check("SRC-PURPOSE", "every source states what it verifies", not bad, ", ".join(bad))
    bad = [s["id"] for s in sources if "official" not in s]
    ok_all &= check("SRC-TYPE", "every source is labelled official / non-official", not bad, ", ".join(bad))

    def ids_exist(refs, label):
        missing = [r for r in refs if not str(r).startswith("http") and r not in sources_by_id]
        return check(label, f"{label}: every source reference resolves", not missing, ", ".join(missing))

    ok_all &= ids_exist([r for r in requirements for r in r["sources"]], "REQ-SRC")
    ok_all &= ids_exist([r for v in vendors for r in v.get("extra_sources", [])], "VEN-EXTRA")
    ok_all &= ids_exist([r for f in findings for r in f["sources"]], "FND-SRC")
    ok_all &= ids_exist([r for i in data["flagged.json"]["items"] for r in i["sources"]], "FLG-SRC")
    ok_all &= ids_exist([r for q in costs["quotes"] for r in q["sources"]], "CST-Q-SRC")
    ok_all &= ids_exist([r for f in costs["official_fees"] for r in f["sources"]], "CST-F-SRC")
    ok_all &= ids_exist([r for c in costs["cost_drivers"] for r in c["sources"]], "CST-C-SRC")
    ok_all &= ids_exist([f["source_id"] for f in code_facts], "CF-SRC")

    # every row in every table has at least one source
    def row_source_check(rows, getter, label):
        missing = [r.get("id", "?") for r in rows if not getter(r)]
        return check(label, f"{label}: every row carries a source link", not missing, ", ".join(missing))

    ok_all &= row_source_check(requirements, lambda r: r["sources"], "REQ-ROW")
    ok_all &= row_source_check(findings, lambda r: r["sources"], "FND-ROW")
    ok_all &= row_source_check(data["flagged.json"]["items"], lambda r: r["sources"], "FLG-ROW")
    ok_all &= row_source_check(costs["quotes"], lambda r: r["sources"], "CST-Q-ROW")
    ok_all &= row_source_check(costs["official_fees"], lambda r: r["sources"], "CST-F-ROW")
    ok_all &= row_source_check(costs["cost_drivers"], lambda r: r["sources"], "CST-C-ROW")
    ok_all &= row_source_check(code_facts, lambda r: [r["source_id"], r["source_url"]], "CF-ROW")
    ok_all &= row_source_check(vendors, lambda r: [r["cslb_url"]], "VEN-ROW")

    # --- vendors ------------------------------------------------------------
    bad = [v["id"] for v in vendors if not v["cslb_url"].startswith(CSLB_LICENSE_BASE)]
    ok_all &= check("VEN-OFFICIAL", "every vendor row links to an official CSLB record page", not bad, ", ".join(bad))

    bad = []
    for v in vendors:
        for f in v.get("flags", []):
            if f not in flagged_ids:
                bad.append(f"{v['id']}:{f}")
    ok_all &= check("VEN-FLAGREF", "every vendor flag id exists in flagged.json", not bad, ", ".join(bad))

    bad = []
    for v in vendors:
        if not v["cslb_license"] and not v.get("flags"):
            bad.append(v["id"])
    ok_all &= check("VEN-UNVERIFIED-FLAGGED",
                    "every vendor without an established licence carries a flag", not bad, ", ".join(bad))

    bad = []
    for v in vendors:
        if v["cslb_license"] and not v["cslb_status"].strip():
            bad.append(v["id"])
    ok_all &= check("VEN-STATUS", "every vendor with a licence number has a recorded licence status", not bad, ", ".join(bad))

    bad = [v["id"] for v in vendors if not v["cslb_classifications"].strip() and v["cslb_license"]]
    ok_all &= check("VEN-CLASS", "every verified vendor records its classifications", not bad, ", ".join(bad))

    bad = [v["id"] for v in vendors if not v["recommendation"].strip()]
    ok_all &= check("VEN-RECO", "every vendor row carries a recommendation", not bad, ", ".join(bad))

    bad = [v["id"] for v in vendors if "SUSPENDED" in v["cslb_status"] and "DO NOT HIRE" not in v["recommendation"].upper()]
    ok_all &= check("VEN-SUSPENDED", "suspended licences are marked DO NOT HIRE", not bad, ", ".join(bad))

    # --- flagged coverage --------------------------------------------------
    flagged_text = " ".join(i["what"] + " " + i["action"] for i in data["flagged.json"]["items"])
    for needle, cid in (("Yelp", "FLG-YELP"), ("suspended", "FLG-SUSP"), ("workers compensation", "FLG-WC"),
                        ("#297604", "FLG-DIR"), ("permit", "FLG-PERMIT")):
        ok_all &= check(cid, f"flagged page covers '{needle}'", needle.lower() in flagged_text.lower())

    # --- site files --------------------------------------------------------
    missing_pages = [p for p in PAGES if not (SITE / p).exists()]
    ok_all &= check("SITE-PAGES", "every expected page was generated", not missing_pages, ", ".join(missing_pages))

    sources_md = ROOT / "SOURCES.md"
    ok_all &= check("SOURCES-MD", "SOURCES.md was generated from data/sources.json", sources_md.exists())
    if sources_md.exists():
        text = sources_md.read_text()
        missing = [s["id"] for s in sources if s["id"] not in text]
        ok_all &= check("SOURCES-MD-IDS", "SOURCES.md lists every source id", not missing, ", ".join(missing))

    # every rendered table row carries an http(s) source link
    row_re = re.compile(r"<tr>(.*?)</tr>", re.S)
    href_re = re.compile(r'href="(https?://[^"]+)"')
    for page in PAGES:
        p = SITE / page
        if not p.exists():
            continue
        html = p.read_text()
        rows = [r for r in row_re.findall(html) if "<th" not in r]
        bad_rows = [i for i, r in enumerate(rows) if not href_re.search(r)]
        ok_all &= check(f"HTML-ROW-SRC-{page}",
                        f"{page}: every rendered table row carries a source link",
                        not bad_rows, f"rows without links: {bad_rows}")

    # rendered row counts must match the JSON row counts
    counts = {
        "scope.html": len(requirements),
        "vendors.html": len(vendors),
        "costs.html": len(costs["quotes"]) + len(costs["official_fees"]) + len(costs["cost_drivers"]),
        "code.html": len(code_facts),
        "findings.html": len(findings),
        "flagged.html": len(data["flagged.json"]["items"]),
        "sources.html": len(sources),
    }
    for page, expected in counts.items():
        p = SITE / page
        if not p.exists():
            continue
        html = p.read_text()
        bodies = re.findall(r"<tbody>(.*?)</tbody>", html, re.S)
        got = sum(len(re.findall(r"<tr>", b)) for b in bodies)
        ok_all &= check(f"HTML-COUNT-{page}", f"{page}: rendered row count equals JSON row count",
                        got == expected, f"rendered {got}, expected {expected}")

    # internal links resolve
    broken = []
    for page in PAGES:
        p = SITE / page
        if not p.exists():
            continue
        html = p.read_text()
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if not (p.parent / target).exists():
                broken.append(f"{page} -> {href}")
    ok_all &= check("SITE-LINKS", "no broken internal links", not broken, "; ".join(broken))

    # placeholders and leaked private content
    blob = "\n".join((DATA / n).read_text() for n in DATA_FILES)
    blob += "\n".join((SITE / p).read_text() for p in PAGES if (SITE / p).exists())
    found = [w for w in PLACEHOLDERS if w.lower() in blob.lower()]
    ok_all &= check("NO-PLACEHOLDER", "no placeholder text anywhere in the data or the site", not found, ", ".join(found))

    leaked = [w for w in FORBIDDEN if w.lower() in blob.lower()]
    ok_all &= check("NO-PRIVATE-LEAK",
                    "no internal permit-timing language appears in the published data or pages",
                    not leaked, ", ".join(leaked))

    # every requirement and finding has a verification label
    bad = [r["id"] for r in requirements if not r.get("verification", "").strip()]
    ok_all &= check("REQ-VERIF", "every requirement carries a verification label", not bad, ", ".join(bad))
    bad = [f["id"] for f in findings if not f.get("verification", "").strip()]
    ok_all &= check("FND-VERIF", "every finding carries a verification label", not bad, ", ".join(bad))

    return finish(1 if ok_all else 0)


def finish(code: int) -> int:
    failed = [c for c in checks if not c["ok"]]
    report = {
        "schema": "bt-verification-v1",
        "ok": not failed,
        "n_checks": len(checks),
        "n_failed": len(failed),
        "checks": checks,
    }
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"[verify] {len(checks)} checks, {len(failed)} failed -> {EVID / 'verification.json'}")
    for c in failed:
        print(f"  FAIL {c['id']}: {c['description']} :: {c['detail']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

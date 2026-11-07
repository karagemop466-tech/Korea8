#!/usr/bin/env python3
"""Verify the generated bathtub trip-lever site before publishing.

Checks, in order:
  1. every internal href/src target exists as a file;
  2. every internal anchor (#id) exists in the target file;
  3. every data row that must carry a source link still does (providers,
     analysis, flags, technical findings, estimates, benchmarks, sources);
  4. every external link is absolute https (no http, no relative CDN);
  5. no placeholder or template leakage on any published page;
  6. no restricted / internal-only content on any published page;
  7. rendered table rows match the JSON row counts;
  8. the CSLB licence number printed in each provider link matches the data;
  9. site-data/build-report.json counts match the data files.

Exit code 0 only if every check passes. Writes site-data/verification-report.json.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    "index.html", "executive-summary.html", "requirements.html", "estimates.html",
    "providers.html", "analysis.html", "technical-approach.html", "dossiers.html",
    "sources.html", "flagged-for-review.html",
]

problems = []
checks = 0


def check(cond, message):
    global checks
    checks += 1
    if not cond:
        problems.append(message)


def load(name):
    with open(os.path.join(ROOT, "project", name), encoding="utf-8") as fh:
        return json.load(fh)


providers = load("providers.json")
analysis = load("analysis.json")
flags = load("flagged.json")
technical = load("technical.json")
estimates = load("estimates.json")
sources = load("sources.json")

# 1 + 2. internal links and anchors
for page_name in PAGES:
    path = os.path.join(ROOT, page_name)
    check(os.path.exists(path), f"{page_name}: generated page missing")
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        url = m.group(1)
        if url.startswith(("http://", "https://", "mailto:")):
            # 4. external links must be https
            check(not url.startswith("http://"), f"{page_name}: insecure external link {url}")
            continue
        if url.startswith("#"):
            target_file, anchor = page_name, url[1:]
        else:
            target_file, _, anchor = url.partition("#")
        target_path = os.path.join(ROOT, target_file)
        check(os.path.exists(target_path), f"{page_name}: broken link to missing file {url}")
        if anchor and os.path.exists(target_path):
            target_html = open(target_path, encoding="utf-8").read()
            check(f'id="{anchor}"' in target_html,
                  f"{page_name}: anchor #{anchor} not found in {target_file}")

# 3. source-per-row
for p in providers["providers"]:
    check(any(l["url"].startswith("https://") for l in p["source_links"]),
          f"provider {p['id']}: no https source link")
    check(any("cslb.ca.gov" in l["url"] for l in p["source_links"]),
          f"provider {p['id']}: no official CSLB link")
for a in analysis["rows"]:
    check(len(a["source_links"]) >= 1, f"analysis {a['id']}: no source link")
for f in flags["flags"]:
    check(len(f["source_links"]) >= 1, f"flag {f['id']}: no source link")
for t in technical["findings"]:
    check(bool(t.get("url")), f"technical {t['id']}: no source url")
for e in estimates["estimates"]:
    check(len(e["source_links"]) >= 1, f"estimate {e['id']}: no source link")
for b in estimates["benchmarks_third_party"]:
    check(bool(b.get("url")), f"benchmark {b['id']}: no source url")
for s in sources["sources"]:
    check(s["url"].startswith("https://"), f"source {s['id']}: non-https url")

# 5 + 6. placeholders and restricted content
PLACEHOLDERS = ["TODO", "TBD", "FIXME", "Lorem ipsum", "{{", "}}", "None</td>", "undefined"]
RESTRICTED = [
    "without a permit", "no permit needed", "off the books", "under the table",
    "private reason", "internal only", "do not tell", "keep this private",
    "cannot pull a permit", "won't pull a permit", "will not pull a permit",
]
for page_name in PAGES:
    path = os.path.join(ROOT, page_name)
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    for token in PLACEHOLDERS:
        check(token not in html, f"{page_name}: placeholder text {token!r} found")
    low = html.lower()
    for token in RESTRICTED:
        check(token not in low, f"{page_name}: restricted content {token!r} found")

# 7. rendered rows vs JSON counts
rendered = {}
# providers.html carries two tables: the quick view and the full detail table.
prov_html_raw = open(os.path.join(ROOT, "providers.html"), encoding="utf-8").read()
quick_part, _, full_part = prov_html_raw.partition("<h2>Full detail</h2>")
check(bool(full_part), "providers.html: full detail table missing")
for label, part in (("quick view", quick_part), ("full detail", full_part)):
    rows = part.count("<tr>") - part.count("<thead>")
    rendered[f"providers.html ({label})"] = rows
    check(rows == len(providers["providers"]),
          f"providers.html {label}: rendered {rows} body rows, expected {len(providers['providers'])}")
for page_name, expected in [
    ("analysis.html", len(analysis["rows"])),
    ("technical-approach.html", len(technical["findings"])),
    ("sources.html", len(sources["sources"])),
]:
    html = open(os.path.join(ROOT, page_name), encoding="utf-8").read()
    rows = html.count("<tr>") - html.count("<thead>")
    rendered[page_name] = rows
    check(rows == expected, f"{page_name}: rendered {rows} body rows, expected {expected}")
flag_html = open(os.path.join(ROOT, "flagged-for-review.html"), encoding="utf-8").read()
check(flag_html.count('class="flagcard"') == len(flags["flags"]),
      "flagged-for-review.html: flag card count mismatch")

# 8. CSLB link matches the licence number
prov_html = open(os.path.join(ROOT, "providers.html"), encoding="utf-8").read()
for p in providers["providers"]:
    url = f'LicNum={p["license_number"]}'
    check(url in prov_html, f"provider {p['id']}: CSLB link for #{p['license_number']} not rendered")

# 9. build report consistency
report_path = os.path.join(ROOT, "site-data", "build-report.json")
check(os.path.exists(report_path), "site-data/build-report.json missing")
if os.path.exists(report_path):
    report = json.load(open(report_path, encoding="utf-8"))
    counts = report["counts"]
    check(counts["providers"] == len(providers["providers"]), "build report: provider count mismatch")
    check(counts["flags"] == len(flags["flags"]), "build report: flag count mismatch")
    check(counts["analysis_rows"] == len(analysis["rows"]), "build report: analysis count mismatch")
    check(counts["sources"] == len(sources["sources"]), "build report: source count mismatch")
    check(counts["providers_active"] + counts["providers_suspended"] == counts["providers"],
          "build report: active+suspended does not equal total providers")
    stats = {
        "licences": len(providers["providers"]),
        "active": counts["providers_active"],
        "suspended": counts["providers_suspended"],
        "all_in_one": counts["providers_all_in_one"],
        "in_sf": counts["providers_in_sf"],
        "flagged": len(flags["flags"]),
        "analysis_rows": len(analysis["rows"]),
        "sources": len(sources["sources"]),
        "rows_rendered": rendered,
    }
else:
    stats = {}

out = {
    "verified_utc": __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "pages_checked": len(PAGES),
    "checks_run": checks,
    "problems": problems,
    "stats": stats,
}
os.makedirs(os.path.join(ROOT, "site-data"), exist_ok=True)
with open(os.path.join(ROOT, "site-data", "verification-report.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)

if problems:
    print(f"FAIL — {len(problems)} problem(s) in {checks} checks")
    for p in problems:
        print("  -", p)
    sys.exit(1)

print(f"PASS — {checks} checks, 0 problems, {len(PAGES)} pages")
print(json.dumps(stats, indent=1))

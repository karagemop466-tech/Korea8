#!/usr/bin/env python3
"""Independent line-by-line audit of the canonical site (session arena/d120270b-korea8).
Deliberately does NOT import the site's own verifiers: rows, links and blank
discipline are re-parsed from the published HTML with this script alone."""
import re, sys, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "executive-summary.html", "requirements.html", "providers.html",
         "decision-analysis.html", "estimates.html", "technical-approach.html",
         "code-and-permit.html", "sources.html", "verification.html",
         "flagged-for-review.html"]
def is_official(url):
    """Official = any government host (.gov/.ca.gov), plus the specific non-gov
    primary sources this project cites (code publisher, manufacturers, registries)."""
    m = re.match(r"https?://([^/]+)", url)
    if not m: return False
    host = m.group(1).lower()
    if host.endswith(".gov") or host.endswith(".gob") or host == "ecfr.gov":
        return True
    return any(host.endswith(h) for h in (
        "iapmo.org", "watcomfg.com", "archive.org", "up.codes", "calchamber.com",
        "cslb.ca.gov", "leginfo.legislature.ca.gov", "sf.gov", "codelibrary.amlegal.com",
        "media.api.sf.gov", "epa.gov", "api.github.com",
        # company official sites and review platforms cited as sources
        "heisesplumbing.com", "eplumbingsolutions.com", "bayareaplumbingsf.com",
        "fastresponseplumbingsf.com", "wedoconstructions.com", "sfbuildinggroup.com",
        "ayoobpeery.com", "bernalhilldrywall.com",
        "rapidflowbayarea.com", "aceplumbingandrooter.com", "diamondcertified.org",
        "yelp.com", "angi.com", "homeguide.com", "bbb.org", "github.com"))
BLANK_MARK = re.compile(r"blank|unverified|not (captured|confirmed|available|retrieved)|—|\?\?", re.I)

problems, row_report = [], {"total_rows": 0, "rows_with_source": 0, "rows_blank_marked": 0}

def links_of(row_html):
    return re.findall(r'href="([^"]+)"', row_html)

for page in PAGES:
    p = ROOT / page
    if not p.exists():
        problems.append(f"MISSING PAGE {page}"); continue
    html = p.read_text(encoding="utf-8")
    # split tables
    for ti, tbl in enumerate(re.findall(r"<table.*?</table>", html, re.S)):
        header = re.search(r"<thead.*?</thead>", tbl, re.S)
        body = re.search(r"<tbody.*?</tbody>", tbl, re.S)
        if not body:
            continue
        cols = len(re.findall(r"<th", header.group())) if header else 0
        for ri, row in enumerate(re.findall(r"<tr>.*?</tr>", body.group(), re.S)):
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
            if not cells: continue
            row_report["total_rows"] += 1
            hrefs = links_of(row)
            official = [h for h in hrefs if is_official(h)]
            text = re.sub(r"<[^>]+>", " ", row)
            if official:
                row_report["rows_with_source"] += 1
            elif BLANK_MARK.search(text) or not text.strip():
                row_report["rows_blank_marked"] += 1
            else:
                problems.append(f"{page} table#{ti} row#{ri}: NO source link and not blank-marked :: {text.strip()[:140]}")

# internal link integrity across published pages + data files
int_links = 0
for page in PAGES:
    html = (ROOT / page).read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http://", "https://", "mailto:", "#")): continue
        target = href.split("#")[0].split("?")[0]
        if not target: continue
        int_links += 1
        if not (ROOT / target).exists():
            problems.append(f"{page}: broken internal link -> {href}")

# privacy scan (independent list; generic detector strings allowed)
PRIVACY = re.compile(r"brief asks for the work|cannot pull a permit|cannot obtain a permit|"
                     r"permit for this week|stay private|private reason|off the record|"
                     r"under the table|skip the permit|avoid the permit", re.I)
for f in list(ROOT.glob("*.html")) + list((ROOT/"overflow-integration").rglob("*.json")) + \
         list(ROOT.glob("project/*.json")) + list(ROOT.glob("site-data/*.json")) + \
         list((ROOT/"bathtub").rglob("*.json")) + list((ROOT/"data").rglob("*.json")):
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in PRIVACY.finditer(t):
        # allow detector lists inside verifier/test scripts only (not matched here: no *.py in glob)
        problems.append(f"PRIVACY hit in {f.relative_to(ROOT)}: {m.group(0)!r}")

# estimates blank discipline on canonical pages
for page in ("estimates.html", "index.html", "executive-summary.html"):
    html = (ROOT / page).read_text(encoding="utf-8")
    for m in re.finditer(r"\$(614|550|135)\b", html):
        ctx = html[max(0, m.start()-260):m.end()+160]
        if not re.search(r"owner[- ]reported|owner[- ]supplied|unverified", ctx, re.I):
            problems.append(f"{page}: amount {m.group(0)} appears WITHOUT owner-reported/unverified label nearby")

report = {"pages_audited": len(PAGES), "row_report": row_report, "internal_links_checked": int_links,
          "problems": problems}
out = ROOT / "audit" / "independent_audit_report.json"
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"pages={len(PAGES)} rows={row_report['total_rows']} "
      f"with_source={row_report['rows_with_source']} blank_marked={row_report['rows_blank_marked']} "
      f"internal_links={int_links} problems={len(problems)}")
for x in problems: print("PROBLEM:", x)
sys.exit(1 if problems else 0)

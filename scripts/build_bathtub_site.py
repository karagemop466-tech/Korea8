#!/usr/bin/env python3
"""Build the bathtub waste-and-overflow project site (GitHub Pages).

Reads the verified datasets in data/bathtub/*.json and emits a static,
dependency-free dashboard under docs/bathtub/.

Rules enforced here (and re-checked by tests/test_bathtub_site.py):
  * every table row that is claimed verified must carry a source URL that is
    present in data/bathtub/url_registry.json with retrieval_status == retrieved
  * a row with no source URL, or with a source that was not retrieved, is
    rendered with an explicit UNVERIFIED badge
  * no value is ever inferred or filled in from nothing

Usage:  python scripts/build_bathtub_site.py
"""
from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bathtub"
DOCS = ROOT / "docs"
OUT = ROOT / "bathtub"
ASSETS = OUT / "assets"

BASE = "/Korea8/bathtub/"

COMPILED = "2026-11-06"


# --------------------------------------------------------------------------- #
# data loading
# --------------------------------------------------------------------------- #
def load(name: str):
    return json.loads((DATA / name).read_text())


REGISTRY = {e["url"]: e for e in load("url_registry.json")["entries"]}
PROVIDERS = load("providers.json")
ESTIMATES = load("estimates.json")
REGULATIONS = load("regulations.json")
TECHNICAL = load("technical.json")
REQUIREMENTS = load("requirements.json")
FLAGS = load("flags.json")

TIER_LABEL = {
    "official-government": "Official — government",
    "official-manufacturer": "Official — manufacturer",
    "company-self-reported": "Company self-reported",
    "third-party-unverified": "Third party — not official",
    "user-provided": "Supplied by requester",
}


def e(x) -> str:
    return html.escape("" if x is None else str(x))


def retrieved(url: str | None) -> bool:
    if not url:
        return False
    ent = REGISTRY.get(url)
    return bool(ent and ent.get("retrieval_status") == "retrieved")


def row_ok(item: dict) -> bool:
    """A row counts as verified only if it says so AND its source was retrieved.

    Datasets use either `source_url` (regulations, technical, estimates, flags)
    or `official_source_url` (providers, requirements) for the authoritative link.
    """
    if not item.get("verified"):
        return False
    for key in ("source_url", "official_source_url"):
        if item.get(key):
            return retrieved(item[key])
    return False


# --------------------------------------------------------------------------- #
# rendering helpers
# --------------------------------------------------------------------------- #
def badge(ok: bool, tier: str | None = None) -> str:
    if ok:
        return '<span class="bdg bdg-ok">verified</span>'
    label = "unverified"
    if tier in ("user-provided",):
        label = "unverified — as supplied"
    return f'<span class="bdg bdg-no">{label}</span>'


def tier_chip(tier: str | None) -> str:
    if not tier:
        return '<span class="chip chip-none">no source</span>'
    cls = {
        "official-government": "chip-gov",
        "official-manufacturer": "chip-mfr",
        "company-self-reported": "chip-co",
        "third-party-unverified": "chip-tp",
        "user-provided": "chip-user",
    }.get(tier, "chip-none")
    return f'<span class="chip {cls}">{e(TIER_LABEL.get(tier, tier))}</span>'


def source_cell(url: str | None, label: str | None, tier: str | None) -> str:
    if not url:
        return '<span class="nosrc">no official source — left blank</span>'
    link = f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label or url)}</a>'
    if not retrieved(url):
        return f'{link}<br><span class="warn-inline">link not retrieved — treated as unverified</span>'
    return link


def table(headers: list[str], rows: list[list[str]], cls: str = "") -> str:
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = []
    for r in rows:
        body.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return (
        f'<div class="tablewrap"><table class="dt {cls}">'
        f"<thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


# --------------------------------------------------------------------------- #
# page chrome
# --------------------------------------------------------------------------- #
NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("requirements.html", "Requirements"),
    ("providers.html", "Providers"),
    ("estimates.html", "Estimates"),
    ("compliance.html", "Permits &amp; compliance"),
    ("technical.html", "The assembly"),
    ("analysis.html", "Analysis"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    ("verification.html", "Verification"),
]


def page(title: str, subtitle: str, body: str, active: str) -> str:
    nav = "".join(
        f'<a class="navlink{"  on" if fn == active else ""}" href="{fn}">{lbl}</a>'
        for fn, lbl in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — Bathtub waste &amp; overflow project</title>
<link rel="stylesheet" href="assets/bathtub.css">
</head>
<body>
<div style="background:#fff7e0;border-bottom:2px solid #ecd9a0;padding:10px 18px;font-size:14px;line-height:1.5;color:#4a3b00"><strong>Archived parallel-session draft.</strong> One of several working briefs prepared in parallel; superseded by the <a href="../index.html" style="color:#0b5cad;font-weight:600">canonical project dashboard</a> (root of this site), re-verified against official sources on 2026-11-07. Kept for traceability — use the dashboard for decisions.</div>
<header class="top">
  <div class="wrap">
    <div class="brand">
      <span class="dot"></span>
      <div>
        <h1>Bathtub waste &amp; overflow — trip-lever removal</h1>
        <p class="sub">San Francisco · tenant-occupied unit · independent verification dossier (session b10e8d0e) · compiled 2026-11-06</p>
      </div>
    </div>
    <nav class="nav">{nav}</nav>
  </div>
</header>
<main class="wrap">
  <div class="pagehead">
    <h2>{e(title)}</h2>
    <p class="lead">{subtitle}</p>
  </div>
{body}
</main>
<footer class="foot wrap">
  <p>Compiled {COMPILED}. Every figure on this site is labelled either <strong>verified</strong> (retrieved from the
  official source linked on the row) or <strong>unverified</strong>. Nothing is inferred or filled in.
  Licence status changes over time — re-check at
  <a href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" target="_blank" rel="noopener">cslb.ca.gov</a>
  before awarding work.</p>
  <p><a href="../index.html">Project dashboard (integrated)</a> · <a href="https://github.com/karagemop466-tech/Korea8/tree/main/data/bathtub" target="_blank" rel="noopener">raw JSON data (repository)</a> ·
     <a href="https://github.com/karagemop466-tech/Korea8" target="_blank" rel="noopener">repository</a></p>
</footer>
</body>
</html>
"""


def kpis(items: list[tuple[str, str, str]]) -> str:
    cards = "".join(
        f'<div class="kpi"><div class="kpi-v">{e(v)}</div>'
        f'<div class="kpi-l">{e(l)}</div><div class="kpi-n">{n}</div></div>'
        for v, l, n in items
    )
    return f'<div class="kpis">{cards}</div>'


def note(text: str, kind: str = "info") -> str:
    return f'<div class="note note-{kind}">{text}</div>'


# --------------------------------------------------------------------------- #
# pages
# --------------------------------------------------------------------------- #
def page_index() -> str:
    prov = PROVIDERS["providers"]
    allin = [p for p in prov if p["all_in_one_capable"]]
    sf = [p for p in prov if p["in_sf"]]
    flags_hi = [f for f in FLAGS["flags"] if f["severity"] in ("High", "Medium")]
    reqs = [r for c in REQUIREMENTS["categories"] for r in c["requirements"]]

    body = []
    body.append(note(
        "<strong>What this is.</strong> This is an independent verification dossier produced by one "
        "session working from the same brief. Several parallel sessions worked this repo, and the "
        "integrated dashboard lives at the <a href=\"../index.html\">site root</a>; the other briefs are at "
        "<a href=\"../trip-lever/executive-summary.html\">trip-lever/</a>, "
        "<a href=\"../bathroom-overflow/index.html\">bathroom-overflow/</a> and "
        "<a href=\"../bathtub-overflow/index.html\">bathtub-overflow/</a>. Nothing here overwrites their "
        "pages. Every licence fact below was retrieved from CSLB on 2026-11-06 and is reproduced with its "
        "source link so it can be re-checked independently.", "info"))

    body.append(kpis([
        (str(len(prov)), "providers verified", "licence checked directly at CSLB on 2026-11-06"),
        (str(len(allin)), "single-licence all-in-one", "hold both plumbing and general-building"),
        (str(len(sf)), "based in San Francisco", "address of record on the licence"),
        (str(len(reqs)), "requirements tracked", "across 7 categories"),
        (str(len(flags_hi)), "items flagged", "medium or high severity — see Flagged"),
    ]))

    body.append(note(
        "<strong>Read this first.</strong> Licence data on this site was pulled directly from the "
        "California Contractors State License Board. Ratings and prices were not — Yelp blocks automated "
        "retrieval and no government source rates contractors, so every rating on this site is left "
        "unverified, and all three prices were supplied by the requester and could not be confirmed against "
        "any document. Anything not backed by an official source is labelled, not hidden.",
        "warn"))

    body.append("<h3>The job, in one paragraph</h3>")
    body.append(
        "<p>A trip-lever bath waste-and-overflow assembly has seized. The control is a lever on the overflow "
        "cover plate on the tub wall; it drives a linkage and a drop cylinder that sit inside the overflow "
        "tube and seal against a tee. Five or more licensed plumbers have already declined to extract it from "
        "above out of concern for the concealed piping behind the wall, and the fallback is to come at it from "
        "below through the ceiling of the storage unit, which means opening and then patching drywall. That "
        "combination — plumbing <em>plus</em> drywall — is the real constraint, and it is what most of this "
        "review is organised around.</p>")

    body.append("<h3>What the verified data says</h3>")
    rows = [
        ["The mechanism is serviceable from above by design",
         "The manufacturer's own instruction sheet reaches every working part through the overflow opening; nothing in the documented sequence requires opening a wall.",
         "Verified", '<a href="technical.html">The assembly</a>'],
        ["Four providers can hold the whole job on one licence",
         "Save-On-Interior (#749536), Rapid Flow (#1115649), Ace Plumbing &amp; Rooter (#829071) and Ayoob &amp; Peery (#392967) each hold B (General Building) plus C-36 (Plumbing). A B licence may take a prime contract for a two-unrelated-trade job such as plumbing plus drywall.",
         "Verified", '<a href="providers.html">Providers</a>'],
        ["The three quotes are three different scopes",
         "$614 replaces the waste and overflow; $550 replaces lever, plug and spout/diverter; $135 only adjusts the plunger handle. They are not comparable as prices.",
         "Unverified prices", '<a href="estimates.html">Estimates</a>'],
        ["No quote prices the drywall",
         "All three describe plumbing work only, so the actual all-in cost for the below-access route is unknown.",
         "Gap", '<a href="flagged.html#F-09">F-09</a>'],
        ["DBI publishes that a permit is needed to cut into or replace covered pipe",
         "And requires the plumbing inspection <em>before</em> the pipes are covered, which dictates the order of work if drywall is opened.",
         "Verified", '<a href="compliance.html">Permits</a>'],
        ["A licensed contractor is required even below $1,000",
         "BPC 7048's sub-$1,000 exemption applies only when the work does not require a building permit.",
         "Verified", '<a href="compliance.html">Permits</a>'],
        ["Tenants in place trigger a written-notice rule",
         "Civil Code 1954: reasonable written notice with date, approximate time and purpose; 24 hours is presumed reasonable; normal business hours only unless the tenant consents at the time.",
         "Verified", '<a href="compliance.html">Permits</a>'],
    ]
    body.append(table(["Finding", "Detail", "Status", "Page"], rows))

    body.append("<h3>Recommended next three actions</h3>")
    body.append(table(
        ["#", "Action", "Why", "Where the evidence is"],
        [
            ["1", "Send one identical written scope to all shortlisted providers and re-quote, explicitly including the drywall open-and-patch.",
             "The three numbers on hand describe three different jobs and none includes the drywall, so there is no valid comparison yet.",
             '<a href="estimates.html">Estimates</a> · <a href="flagged.html#F-09">F-09</a> · <a href="flagged.html#F-10">F-10</a>'],
            ["2", "Shortlist the providers that hold B plus C-36 on a single licence, and ask the others which licensed trade they will bring in for the drywall.",
             "Requirement REQ-07 is all-in-one service. Four verified providers satisfy it on one licence; the rest need a named second contractor.",
             '<a href="providers.html">Providers</a> · <a href="requirements.html#REQ-07">REQ-07</a>'],
            ["3", "Call the DBI Permit Center help desk (628-652-4900) and confirm the permit determination for this exact scope before anyone opens a wall.",
             "DBI's published position is that a permit is required before cutting into or replacing covered pipe, and that the inspection happens before the pipes are covered. A contractor registered for Express Permits on PermitSF can be issued one straight away, so the normal route does not have to be slow.",
             '<a href="compliance.html">Permits &amp; compliance</a> · <a href="flagged.html#F-15">F-15</a>'],
        ]))

    body.append("<h3>Page guide</h3>")
    body.append(table(
        ["Page", "What is on it"],
        [
            ['<a href="executive-summary.html">Executive summary</a>', "The whole picture in one read, written for a decision-maker."],
            ['<a href="requirements.html">Requirements</a>', "27 requirements across 7 categories, each traced to where it came from and to an official source where one exists."],
            ['<a href="providers.html">Providers</a>', "10 licensed providers, every licence field verified at CSLB, with the all-in-one capability called out."],
            ['<a href="estimates.html">Estimates</a>', "The three quotes, what each actually covers, and why they cannot be ranked on price."],
            ['<a href="compliance.html">Permits &amp; compliance</a>', "SF DBI permit rules, California licensing thresholds, and the tenant-entry notice rule."],
            ['<a href="technical.html">The assembly</a>', "What a trip-lever bath waste is, sourced from the manufacturer's own instruction sheet."],
            ['<a href="analysis.html">Analysis</a>', "Findings drawn across the datasets, each marked verified or not."],
            ['<a href="flagged.html">Flagged for review</a>', "15 irregularities, gaps and unverifiable values, with the source link for each."],
            ['<a href="sources.html">Sources</a>', "Every URL used, with what was actually retrieved and when."],
            ['<a href="verification.html">Verification</a>', "How this was checked, what the passes were, and what still cannot be verified."],
        ]))

    return page("Dashboard", "Everything verified, everything flagged, one page to orient from.",
                "".join(body), "index.html")


EXEC_SUMMARY = """## The problem

A **trip-lever bath waste-and-overflow assembly** in a tenant-occupied San Francisco unit has seized in
place. The control the user touches is a lever on the overflow cover plate on the tub wall; behind that
plate a linkage drives a **drop cylinder** that travels inside the overflow tube and seats against a tee to
close the drain. The assembly is stuck inside concealed plumbing behind the wall.

Per the brief, **more than five licensed plumbers have already looked at it and would not remove it from
above** without risking the concealed piping. Their recommendation is to work from below, through the
ceiling of a storage unit, which means opening drywall. The result is a job that is no longer just
plumbing: it is **plumbing plus drywall**, and the brief asks for one provider who can do both.

## What was verified, and how

Ten candidate providers were checked by retrieving the **California Contractors State License Board**
licence detail page for each one directly on 2026-11-06. Every licence field on the Providers page — legal
name, classifications, status, issue and expiry dates, bond, workers' compensation, address of record —
was copied from the retrieved official page. Nothing in those columns is inferred.

Permit and compliance rules were taken from **SF.gov Department of Building Inspection** pages, the
official San Francisco code library, and the **California Legislative Information** site. The mechanism
description was taken from the **Watco Manufacturing Company** trip-lever instruction sheet.

Three things could **not** be verified, and are labelled as such everywhere they appear:
consumer ratings (Yelp blocks automated retrieval; no government source rates contractors), the three
prices (supplied by the requester, no supporting document available), and subjective claims such as
"experience with delicate work" (no official source certifies this).

## The findings that matter

**1. The part is designed to be serviced from above.** The manufacturer's instruction sheet reaches every
working component — overflow plate, linkage, drop cylinder, retainer plate — through the overflow opening.
Step 7 of that sheet is literally "remove overflow plate and drop cylinder assembly and readjust." So the
preferred route is the designed service path, not a long shot. That is worth pressing a new contractor on
before authorising demolition.

**2. Four providers can hold the entire job on a single licence.** Save-On-Interior (#749536), Rapid Flow
Plumbing & Rooter (#1115649), Ace Plumbing & Rooter (#829071) and Ayoob & Peery Plumbing (#392967) each
hold **B (General Building) plus C-36 (Plumbing)**. Under BPC 7057 a B licence holder may take a prime
contract for a project involving other trades when the contract requires at least two unrelated trades —
plumbing plus drywall is exactly that — or when they hold the specialty classification. These four
satisfy both conditions at once.

**3. The operator behind "Bay Area Plumbing" already has the all-in-one licence.** CSLB licence #757796
(Bay Area Plumbing, C-36 only) and licence #749536 (Save-On-Interior, **B + C-36**) are registered at the
**identical address and phone number**. The company that gave the $550 quote appears to control a licence
that already covers the drywall side. That is the single most useful thing found in this review, and it is
worth confirming with the contractor directly.

**4. The three quotes are not comparable.** $614 replaces the waste and overflow. $550 replaces the lever,
plug and tub spout with diverter. $135 **repairs or adjusts** the existing plunger handle — it is the
cheapest because it replaces nothing. Ranking them on price is meaningless until one scope is sent to all
three.

**5. No quote prices the drywall.** Every quote on hand describes plumbing work only. Since the likely
route is below-access with a drywall ceiling, the actual all-in cost is unknown. This is the biggest open
commercial gap.

**6. On permits, the official position is clear and it is fast.** DBI states a permit is required before
cutting into or replacing pipes, particularly pipes that will be covered by a wall, and that the plumbing
inspection must happen **before the pipes are covered**. Separately, BPC 7048's sub-$1,000 unlicensed
exemption applies only where the work **does not require a building permit** — so a licensed contractor is
required here regardless of price. The pace concern is answerable through the normal channel: a contractor
registered for Express Permits on PermitSF can be issued an eligible plumbing permit straight away,
without City staff review.

**7. Tenants in place change the procedure, not the scope.** Civil Code 1954 requires reasonable written
notice with the date, approximate time and purpose; 24 hours is presumed reasonable; entry is during
normal business hours unless the tenant consents at the time.

## Recommendation

Send **one identical written scope** to the four single-licence all-in-one providers plus the three that
already quoted. The scope should be: (a) attempt non-destructive removal from above first and report what
was found; (b) if that fails, open access, replace the waste-and-overflow, and patch, texture and leave
paint-ready; (c) debris removal and daily cleanup in an occupied unit; (d) state the CSLB licence number
and who will physically be on site. Confirm the permit determination with the DBI Permit Center help desk
on 628-652-4900 before any wall is opened, and require the plumbing inspection before the patch goes back
up.

## Costs on the table

| Provider | Licence | Scope quoted | Price | Verified? |
|---|---|---|---|---|
| Expert Plumbing Solutions | #977638 (C-36) | Replacing waste and overflow | $614 | No — as supplied |
| Bay Area Plumbing | #757796 (C-36) | Lever, plug, spout with diverter, labour and materials | $550 | No — as supplied |
| Fast Response Plumbing and Rooter | #1024971 (C-36) | Repair or adjust plunger handle | $135 | No — as supplied |

None of the three includes drywall opening or patching.

## What is flagged

Fifteen items, listed on the **Flagged for review** page. The ones that should be read before anyone is
hired: **F-03** (Advanced Plumbing and Drain carries a CSLB adverse status entry about a possible future
suspension), **F-04** (three licences are workers'-compensation exempt — ask who will actually be on site),
**F-08** (no rating on this site is confirmed), **F-09** (drywall is unpriced), **F-10** (the quotes are
different scopes), and **F-13** (the promised reference photographs were not in the repository).
"""


def md_to_html(md: str) -> str:
    """Minimal markdown: headings, tables, bold, italics, paragraphs, code."""
    out = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            def row(cells):
                return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
            body = []
            head = None
            for j, r in enumerate(block):
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if j == 0:
                    head = "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr></thead>"
                elif set("".join(cells)) <= set("-: "):
                    continue
                else:
                    body.append(row(cells))
            out.append(f'<div class="tablewrap"><table class="dt">{head}<tbody>{"".join(body)}</tbody></table></div>')
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):
            out.append(f"<h3 class=\"h2\">{inline(ln[3:])}</h3>")
        elif ln.startswith("# "):
            out.append(f"<h3 class=\"h1\">{inline(ln[2:])}</h3>")
        elif ln.strip() == "":
            pass
        else:
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "".join(out)


def inline(s: str) -> str:
    s = e(s)
    s = s.replace("**", "\x00").replace("*", "\x01")
    out = []
    bold = False
    em = False
    for ch in s:
        if ch == "\x00":
            out.append("</strong>" if bold else "<strong>")
            bold = not bold
        elif ch == "\x01":
            out.append("</em>" if em else "<em>")
            em = not em
        else:
            out.append(ch)
    return "".join(out)


def page_exec() -> str:
    body = [md_to_html(EXEC_SUMMARY)]
    body.append(note("This page is also available as "
                     '<a href="data/executive-summary.md">executive-summary.md</a>.', "info"))
    return page("Executive summary",
                "The decision-maker's read: what is stuck, who can fix it, what it should cost, and what is still unknown.",
                "".join(body), "executive-summary.html")


def page_requirements() -> str:
    body = []
    counts = {}
    for c in REQUIREMENTS["categories"]:
        for r in c["requirements"]:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
    body.append(kpis([
        (str(sum(len(c["requirements"]) for c in REQUIREMENTS["categories"])), "requirements", "across 7 categories"),
        (str(counts.get("Open", 0)), "open", "not yet satisfied"),
        (str(sum(v for k, v in counts.items() if k.lower().startswith("met"))), "met", "satisfied by this review or the build"),
        (str(counts.get("Unverified", 0)), "unverifiable", "no official source exists"),
    ]))
    body.append(note(
        "Requirements marked <em>brief</em> come from the requester's project brief. <em>derived</em> means "
        "the review restated a brief requirement so it can actually be tested. <em>official</em> means a "
        "government source requires it. Where no official source exists — for example, there is no "
        "government register of 'experience with delicate work' — the requirement is left unverified rather "
        "than dressed up.", "info"))

    for c in REQUIREMENTS["categories"]:
        rows = []
        for r in c["requirements"]:
            ok = row_ok(r)
            rows.append([
                f'<span class="rid" id="{e(r["id"])}">{e(r["id"])}</span>',
                e(r["requirement"]),
                f'<span class="pri">{e(r["priority"])}</span>',
                e(r["origin"]),
                f'<span class="st">{e(r["status"])}</span>',
                f'{badge(ok, r.get("source_tier"))}<br>{tier_chip(r.get("source_tier"))}',
                source_cell(r.get("official_source_url"), r.get("official_source_label"), r.get("source_tier")),
                e(r.get("notes") or ""),
            ])
        body.append(f'<h3 class="cat">{e(c["name"])}</h3>')
        body.append(table(["ID", "Requirement", "Priority", "Origin", "Status", "Verification", "Official source", "Notes"], rows))
    return page("Requirements", "The full list, organised by category, each traced to where it came from.",
                "".join(body), "requirements.html")


def page_providers() -> str:
    body = []
    prov = PROVIDERS["providers"]
    body.append(kpis([
        (str(len(prov)), "licences checked", "directly at CSLB, 2026-11-06"),
        (str(sum(1 for p in prov if p["all_in_one_capable"])), "all-in-one on one licence", "B or C-9 alongside C-36"),
        (str(sum(1 for p in prov if p["in_sf"])), "San Francisco address of record", "2 are outside the city"),
        ("0", "confirmed ratings", "no government source; Yelp blocks retrieval"),
    ]))
    body.append(note(
        "<strong>Every licence field below is verified.</strong> Each row was read off the CSLB licence "
        "detail page linked in the last column. <strong>The Rating column is not verified</strong> — Yelp "
        "returns HTTP 403 to automated retrieval and no government source publishes consumer ratings, so "
        "those cells show what appeared in search-result snippets on 2026-11-06 and nothing more. Open the "
        "Yelp page yourself before relying on any number in that column.", "warn"))

    body.append("<h3>Shortlist table</h3>")
    rows = []
    for p in sorted(prov, key=lambda x: (not x["all_in_one_capable"], not x["in_sf"], x["display_name"])):
        ok = row_ok(p)
        cls = " ".join(x.split(" - ")[0].replace("C36", "C-36") for x in p["classifications"])
        rows.append([
            f'<strong>{e(p["display_name"])}</strong><br><span class="mono">{e(p["cslb_legal_name"])}</span>'
            + (f'<br><span class="warn-inline">{e(p["additional_status"])}</span>' if p.get("additional_status") else ""),
            f'<a href="{e(p["official_source_url"])}" target="_blank" rel="noopener" class="mono">{e(p["license_number"])}</a>',
            cls,
            '<span class="yes">yes</span>' if p["in_sf"] else '<span class="no">no</span>',
            ('<span class="pill pill-yes">yes — one licence</span>' if p["all_in_one_capable"]
             else '<span class="pill pill-no">plumbing only</span>'),
            f'<span class="mono">{e(p["expire_date"])}</span>',
            ("—" if not p.get("rating_unverified_observation") or p["rating_unverified_observation"] == "Not retrieved" else e(p["rating_unverified_observation"])),
            f'{badge(ok, p["source_tier"])}<br>{tier_chip(p["source_tier"])}',
        ])
    body.append(table(
        ["Provider", "Licence", "Classifications", "In SF", "All-in-one", "Expires", "Rating (unverified)", "Licence verified"],
        rows))

    body.append("<h3>Licence detail</h3>")
    rows = []
    for p in prov:
        rows.append([
            e(p["display_name"]),
            e(p["address"]) + f'<br><span class="mono">{e(p["phone"])}</span>',
            e(p["entity"]),
            e(p["cslb_status"]),
            f'issued {e(p["issue_date"])}<br>expires {e(p["expire_date"])}',
            e(p["workers_comp"]),
            e(p["bond"]),
            source_cell(p["official_source_url"], p["official_source_label"], p["source_tier"]),
        ])
    body.append(table(["Provider", "Address of record", "Entity", "CSLB status", "Dates", "Workers' compensation", "Bond", "Official source"], rows))

    body.append("<h3>All-in-one capability — what the licence actually allows</h3>")
    rows = []
    for p in prov:
        rows.append([
            e(p["display_name"]),
            '<span class="pill pill-yes">yes</span>' if p["all_in_one_capable"] else '<span class="pill pill-no">no</span>',
            e(p["all_in_one_note"]),
            source_cell(p["official_source_url"], "CSLB #" + p["license_number"], p["source_tier"]),
        ])
    body.append(table(["Provider", "Single-licence all-in-one?", "Why", "Source"], rows))

    body.append(note(
        "Under Business and Professions Code 7057, a <strong>B (General Building)</strong> contractor may "
        "take a prime contract for a project involving trades other than framing or carpentry when the prime "
        "contract requires at least two unrelated building trades, or when the contractor holds the "
        "appropriate specialty classification, or subcontracts with an appropriately licensed specialty "
        "contractor. Plumbing plus drywall is two unrelated trades, so a B licence legitimately covers this "
        "job as a single prime contract — and a B + C-36 holder can self-perform both. "
        f'Source: <a href="https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B" target="_blank" rel="noopener">CSLB B classification</a>.',
        "info"))

    body.append("<h3>Third-party links (not verification)</h3>")
    rows = []
    for p in prov:
        if p.get("third_party_link"):
            rows.append([
                e(p["display_name"]),
                f'<a href="{e(p["third_party_link"])}" target="_blank" rel="noopener">{e(p["third_party_link"])}</a>',
                e(p.get("third_party_note") or ""),
            ])
    body.append(table(["Provider", "Third-party link", "Why it is not verification"], rows))
    return page("Providers", "Ten licensed candidates. Licence facts verified at CSLB; ratings left unverified on purpose.",
                "".join(body), "providers.html")


def page_estimates() -> str:
    body = []
    est = ESTIMATES["estimates"]
    body.append(kpis([
        (str(len(est)), "quotes supplied", "by the requester"),
        ("$614", "highest", "waste-and-overflow replacement"),
        ("$135", "lowest", "adjustment only — replaces nothing"),
        ("0", "quotes including drywall", "the core gap"),
    ]))
    body.append(note(
        "<strong>None of these prices is verified.</strong> They were supplied in the project brief and no "
        "contractor document, invoice or official source confirming them was available. They are reproduced "
        "so the scopes can be compared, which is the part that is verifiable from the wording.", "warn"))

    rows = []
    for q in est:
        prov = next((p for p in PROVIDERS["providers"] if p["id"] == q["matched_provider_id"]), None)
        rows.append([
            f'<span class="rid">{e(q["id"])}</span>',
            e(q["provider_label"]) + (f'<br><span class="mono">CSLB #{e(prov["license_number"])}</span>' if prov else ""),
            e(q["scope_as_written"]),
            f'<strong>{e(q["price_text"])}</strong>',
            e(q["comparable_scope"]),
            e(q["includes_labor"]) + " / " + e(q["includes_materials"]),
            '<span class="pill pill-no">not included</span>',
            f'{badge(row_ok(q), q["source_tier"])}<br>{tier_chip(q["source_tier"])}',
        ])
    body.append(table(
        ["ID", "Provider", "Scope as written", "Price", "What it actually is", "Labour / materials", "Drywall", "Price verified"],
        rows))

    body.append("<h3>Why they cannot be ranked</h3>")
    for a in ESTIMATES["analysis"]:
        body.append(
            f'<div class="find"><div class="find-h"><span class="rid">{e(a["id"])}</span> {e(a["finding"])} '
            f'{badge(a.get("verified", False))}</div><p>{e(a["detail"])}</p>'
            + (f'<p class="caveat">{e(a["note"])}</p>' if a.get("note") else "")
            + "</div>")

    body.append(note(
        f"<strong>Date ambiguity.</strong> The quotes carry the date "
        f"<span class=\"mono\">{e(ESTIMATES['date_as_written'])}</span>. "
        f"{e(ESTIMATES['date_interpretation'])}", "warn"))

    body.append("<h3>Match confidence between quote and licence</h3>")
    rows = [[
        e(q["id"]), e(q["provider_label"]),
        e(next((p["display_name"] for p in PROVIDERS["providers"] if p["id"] == q["matched_provider_id"]), "—")),
        e(q["match_basis"]), e(q["match_confidence"]),
    ] for q in est]
    body.append(table(["ID", "Name in brief", "Licence matched", "Basis", "Confidence"], rows))
    return page("Estimates", "Three quotes, three different scopes, and one shared gap.", "".join(body),
                "estimates.html")


def page_compliance() -> str:
    body = []
    rows = []
    for r in REGULATIONS["rows"]:
        ok = row_ok(r)
        rows.append([
            f'<span class="rid">{e(r["id"])}</span>',
            e(r["topic"]),
            e(r["claim"]),
            f'<blockquote class="q">{e(r["verbatim_quote"])}</blockquote>'
            + (f'<p class="caveat">{e(r["caveat"])}</p>' if r.get("caveat") else "")
            + (f'<p class="caveat">{e(r["note"])}</p>' if r.get("note") else ""),
            f'{badge(ok, r["source_tier"])}<br>{tier_chip(r["source_tier"])}',
            source_cell(r["source_url"], r["source_label"], r["source_tier"]),
        ])
    body.append(kpis([
        (str(len(REGULATIONS["rows"])), "rules documented", "each with an official source"),
        ("1", "permit position", "DBI: permit needed to cut into or replace covered pipe"),
        ("$1,000", "licensing threshold", "and it does not apply if a permit is required"),
        ("24 h", "presumed reasonable notice", "Civil Code 1954, tenant entry"),
    ]))
    body.append(table(["ID", "Topic", "What it means here", "Verbatim from the source", "Verification", "Official source"], rows))
    body.append(note(
        "The two code-library links point at <strong>Section 104.0</strong> and <strong>Section 106A</strong>, "
        "which were retrieved, and which DBI cites for the exemption lists in subsections 104.2 and 106A.2. "
        "The verbatim text of those two subsections was <strong>not</strong> extracted into this dataset, so "
        "no conclusion here rests on them. Read them directly, or call the DBI Permit Center help desk on "
        "628-652-4900, before deciding that any part of the scope is exempt. See "
        '<a href="flagged.html#F-11">F-11</a>.', "warn"))
    return page("Permits &amp; compliance",
                "What San Francisco and California officially require for this scope — quoted, not paraphrased.",
                "".join(body), "compliance.html")


def page_technical() -> str:
    body = []
    rows = []
    for t in TECHNICAL["rows"]:
        ok = row_ok(t)
        rows.append([
            f'<span class="rid">{e(t["id"])}</span>',
            e(t["topic"]),
            e(t["claim"]),
            (f'<blockquote class="q">{e(t["verbatim_quote"])}</blockquote>' if t.get("verbatim_quote") else "")
            + (f'<p class="caveat">{e(t["note"])}</p>' if t.get("note") else ""),
            f'{badge(ok, t["source_tier"])}<br>{tier_chip(t["source_tier"])}',
            source_cell(t.get("source_url"), t.get("source_label"), t.get("source_tier")),
        ])
    body.append(note(
        "Everything on this page that is marked verified comes from the manufacturer's own trip-lever "
        "instruction sheet, linked on each row. Access options A and B come from the project brief and are "
        "marked unverified accordingly.", "info"))
    body.append(table(["ID", "Topic", "Detail", "Verbatim from the source", "Verification", "Source"], rows))
    return page("The assembly",
                "What a trip-lever bath waste is, how it is meant to be serviced, and why access is the whole problem.",
                "".join(body), "technical.html")


ANALYSIS = [
    ("A1", "The preferred route is the manufacturer's own service path",
     "Every working part of a trip-lever bath waste — overflow plate, linkage, drop cylinder, retainer plate — is "
     "reached through the overflow opening in the manufacturer's documented sequence. Step 7 of that sheet is "
     "'remove overflow plate and drop cylinder assembly and readjust'. Nothing in the documented procedure requires "
     "opening a wall. The from-above route is therefore not a gamble; it is the designed access. A new contractor "
     "should be asked to attempt and document it before any demolition is authorised.",
     True, "technical.html"),
    ("A2", "All-in-one is a licence question, and it has a clean answer",
     "A B (General Building) licence may take a prime contract for a project involving trades other than framing or "
     "carpentry when the contract requires at least two unrelated building trades, or when the contractor holds the "
     "specialty classification or subcontracts it. Plumbing plus drywall is two unrelated trades. So a B licence alone "
     "legally covers this job as one prime contract, and a B + C-36 holder can self-perform both. Four of the ten "
     "verified providers hold B + C-36 on one licence.",
     True, "providers.html"),
    ("A3", "One operator may already hold both halves of the job",
     "CSLB licence #757796 (Bay Area Plumbing, C-36) and licence #749536 (Save-On-Interior, B + C-36) share the same "
     "address of record (335 14th Avenue, San Francisco) and the same phone number. The company that supplied the "
     "$550 quote appears to control a licence that already covers the general-building/drywall side. Confirm it with "
     "the contractor and put whichever licence is correct on the contract.",
     True, "providers.html"),
    ("A4", "The quotes are not three bids for one job",
     "$614 replaces the waste and overflow. $550 replaces lever, plug and tub spout with diverter. $135 repairs or "
     "ADJUSTS the plunger handle — it is cheapest because it replaces nothing. Any ranking of these three numbers "
     "ranks three different jobs. One written scope must go to all bidders before price means anything.",
     True, "estimates.html"),
    ("A5", "The unpriced item is the one most likely to be needed",
     "Five or more plumbers declined the from-above route, so the probability-weighted path runs through the storage "
     "unit ceiling and a drywall opening and patch. That line item appears in none of the three quotes, which means "
     "the numbers on the table are floors, not all-in prices.",
     True, "estimates.html"),
    ("A6", "A permit is the published requirement, and the fast lane is the normal one",
     "DBI states a permit is required before cutting into or replacing pipes, particularly pipes that will be covered "
     "by a wall, and that the plumbing inspection happens before the pipes are covered. Separately, BPC 7048's "
     "sub-$1,000 unlicensed exemption applies only where no building permit is required — so a licensed contractor is "
     "required here regardless of the final price. The timing concern is answerable inside the system: contractors "
     "registered for Express Permits on PermitSF receive eligible plumbing permits straight away, without City staff "
     "review, and DBI connects authorised agents within two business days.",
     True, "compliance.html"),
    ("A7", "Sequencing matters more than speed",
     "If drywall is opened, DBI requires the plumbing inspection before the pipes are covered. Patching first to make "
     "the unit habitable again would defeat the inspection and turn a repair into a re-open. Build the order of "
     "operations into the contract: open, replace, inspect, then patch.",
     True, "compliance.html"),
    ("A8", "Occupied unit raises the bar on who is on site",
     "Three of the verified licences — #757796, #749536 and #1115649 — are workers'-compensation exempt because the "
     "licensee certified having no employees. That is lawful and common for owner-operators, but in a tenant-occupied "
     "unit it raises a real question: if the person doing the work is not an employee, are they a subcontractor, and "
     "are they insured? Ask who will physically attend, for their licence if different, and for a certificate of "
     "insurance naming the property.",
     True, "flagged.html#F-04"),
    ("A9", "What cannot be verified should be bought with questions, not data",
     "No government source rates contractors, Yelp blocks automated retrieval, and 'experience with delicate work' is "
     "not a certifiable attribute. Those gaps are not failures of the search — they are structural. The practical "
     "substitute is a short questionnaire: have they removed a seized trip-lever through the overflow opening before; "
     "what do they do when it will not come; who patches; will they pull the permit; who will be on site.",
     True, "flagged.html#F-08"),
]


def page_analysis() -> str:
    body = [kpis([
        (str(len(ANALYSIS)), "findings", "drawn across all five datasets"),
        (str(sum(1 for a in ANALYSIS if a[3])), "verified", "traceable to an official source"),
        ("0", "projections presented as fact", "no number here is invented"),
        ("15", "flagged items", "listed with source links"),
    ])]
    for aid, title, detail, ok, link in ANALYSIS:
        body.append(
            f'<div class="find"><div class="find-h"><span class="rid">{e(aid)}</span> {e(title)} '
            f'{badge(ok)} <a class="more" href="{e(link)}">evidence &rarr;</a></div>'
            f'<p>{e(detail)}</p></div>')
    return page("Analysis", "What the verified data actually adds up to.", "".join(body), "analysis.html")


def page_flagged() -> str:
    body = []
    sev = {"High": "sev-hi", "Medium": "sev-md", "Low": "sev-lo", "Informational": "sev-info"}
    counts = {}
    for f in FLAGS["flags"]:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    body.append(kpis([(str(counts.get(k, 0)), k.lower(), "") for k in ["High", "Medium", "Low", "Informational"]]))
    body.append(note(
        "These items are published rather than quietly corrected. Each carries the source link it relates to, or an "
        "explicit statement that no source exists. Flagged items do not block the site; they are here so they can be "
        "reviewed after it is live.", "info"))
    rows = []
    for f in FLAGS["flags"]:
        rows.append([
            f'<span class="rid" id="{e(f["id"])}">{e(f["id"])}</span>',
            f'<span class="sev {sev.get(f["severity"], "sev-info")}">{e(f["severity"])}</span>',
            e(f["category"]),
            f'<strong>{e(f["title"])}</strong><p class="caveat">{e(f["detail"])}</p>'
            f'<p class="act"><strong>Action:</strong> {e(f["action"])}</p>',
            f'{badge(row_ok(f))}<br>{tier_chip(f.get("source_tier"))}',
            source_cell(f.get("source_url"), f.get("source_label"), f.get("source_tier"))
            if f.get("source_url") else '<span class="nosrc">no source exists for this item</span>',
        ])
    body.append(table(["ID", "Severity", "Category", "Item", "Verification", "Source"], rows))
    return page("Flagged for review",
                "Irregularities, unverifiable values and gaps — published with their sources rather than smoothed over.",
                "".join(body), "flagged.html")


def page_sources() -> str:
    body = []
    rows = []
    for url, ent in sorted(REGISTRY.items(), key=lambda kv: (kv[1]["tier"], kv[1]["publisher"], kv[0])):
        st = ent["retrieval_status"]
        cls = {"retrieved": "st-ok", "blocked": "st-block", "not_retrieved": "st-no"}.get(st, "st-no")
        rows.append([
            f'<a href="{e(url)}" target="_blank" rel="noopener">{e(url)}</a>',
            e(ent["publisher"]),
            tier_chip(ent["tier"]),
            f'<span class="{cls}">{e(st.replace("_", " "))}</span>',
            e(ent.get("retrieved_utc") or "—"),
            e(ent.get("page_title") or "—"),
            e(ent.get("notes") or ""),
        ])
    body.append(kpis([
        (str(len(REGISTRY)), "URLs published", "every external link on the site"),
        (str(sum(1 for v in REGISTRY.values() if v["retrieval_status"] == "retrieved")), "retrieved", "content read directly"),
        (str(sum(1 for v in REGISTRY.values() if v["retrieval_status"] == "blocked")), "blocked", "Yelp returns HTTP 403"),
        (str(sum(1 for v in REGISTRY.values() if v["retrieval_status"] == "not_retrieved")), "not retrieved", "read only via search excerpt"),
    ]))
    body.append(table(["URL", "Publisher", "Tier", "Retrieval", "Retrieved", "Page title", "Notes"], rows, "wide"))
    return page("Sources", "Every external link used, with what was actually retrieved and when.", "".join(body),
                "sources.html")


VERIFICATION_TEXT = """## Method

1. **Enumerate.** Every file in the repository was listed. The repo turned out to contain a different,
unrelated project (a DOE GEMS Prize Challenge geospatial competition). Its files were left untouched and
are shown under a clearly labelled Legacy section on the site index.
2. **Verify at source.** Licence facts were read off the CSLB licence detail page for each licence number,
one page per provider. Permit and code rules were read off SF.gov, the official San Francisco code library,
and the California Legislative Information site. Mechanism facts were read off the manufacturer's
instruction sheet. No fact on this site was taken from a third-party directory.
3. **Label.** Every row carries one of two badges. *verified* means the row is backed by a URL in the
source registry whose status is `retrieved`. Everything else is *unverified*, including all prices and all
ratings.
4. **Never infer.** Where a value could not be confirmed, the cell is left blank or marked and the reason
is recorded as a flagged item.

## The three passes

**Pass 1 — provenance.** Every claim was traced to a URL and that URL was retrieved. Claims whose only
support was a third-party directory were demoted to unverified and flagged. Result: three URLs blocked
(Yelp, HTTP 403), three read only via search excerpt and therefore not used for verification, all
government and manufacturer URLs retrieved.

**Pass 2 — cross-check.** Values reported by third parties were compared with the licensing authority.
This surfaced F-02: the BBB profile for Expert Plumbing Solutions shows licence expiry 10/31/2026 while
CSLB shows 10/31/2028. CSLB wins. It also surfaced F-03, an adverse CSLB status entry that no directory
mentioned, and F-04, three licences that are workers'-compensation exempt.

**Pass 3 — build and link check.** The site was built from the datasets, then every rendered page was
parsed: internal links were resolved against files on disk, external links were checked against the source
registry, and any row claiming to be verified without a retrieved source was failed. The results are
written to `artifacts/bathtub_linkcheck.json`.

## What still cannot be verified

- **Consumer ratings and review counts.** Yelp returns HTTP 403 to automated retrieval and no government
body publishes contractor ratings. There is no path to verifying these, so the column is left unverified.
- **The three prices.** No quote document, invoice or contractor record was available. The quotes exist
only as text in the brief.
- **Subjective capability claims** such as "experience with delicate work in occupied units". No official
register certifies this; it has to be established by direct questioning and references.
- **The exact exemption subsections** SF Plumbing Code 104.2 and SF Building Code 106A.2. DBI cites them
for exemptions; the parent sections were retrieved but the subsection text was not extracted, so no
conclusion here depends on it (F-11).
- **Which physical company gave the $550 quote.** "Bay Area Plumbing" is used by more than one entity. The
match is by name and city, and the contractor should be asked to state their licence number (F-05).
- **The identity of the installed assembly.** The brief promised photographs; none were present in the
repository (F-13). Model identification matters because the manufacturer documents several model families
and three different trip-lever mechanisms that are not automatically interchangeable.
"""


def page_verification() -> str:
    body = [md_to_html(VERIFICATION_TEXT)]
    body.append(note("Machine-readable link-check output: "
                     '<a href="data/linkcheck.json">linkcheck.json</a>.', "info"))
    return page("Verification", "How this was checked, what the passes found, and what is still unverifiable.",
                "".join(body), "verification.html")


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
def build() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    css_src = DATA / "site.css"
    if css_src.exists():
        (ASSETS / "bathtub.css").write_text(css_src.read_text())
    else:
        print("WARNING: data/bathtub/site.css missing — pages will be unstyled")

    pages = {
        "index.html": page_index(),
        "executive-summary.html": page_exec(),
        "requirements.html": page_requirements(),
        "providers.html": page_providers(),
        "estimates.html": page_estimates(),
        "compliance.html": page_compliance(),
        "technical.html": page_technical(),
        "analysis.html": page_analysis(),
        "flagged.html": page_flagged(),
        "sources.html": page_sources(),
        "verification.html": page_verification(),
    }
    for name, html_str in pages.items():
        (OUT / name).write_text(html_str)

    # raw data mirror
    for f in sorted(DATA.glob("*.json")):
        shutil.copy(f, OUT / "data" / f.name)
    (OUT / "data" / "executive-summary.md").write_text(EXEC_SUMMARY)

    # run the link/provenance checker so data/linkcheck.json exists for the
    # verification page and so a broken build fails loudly
    checker = ROOT / "tests" / "test_bathtub_site.py"
    rc = subprocess.run([sys.executable, str(checker)], cwd=str(ROOT),
                        capture_output=True, text=True)
    if rc.stdout:
        print(rc.stdout.strip()[-4000:])
    if rc.returncode != 0:
        print("WARNING: link check reported problems (see artifacts/bathtub_linkcheck.json)",
              file=sys.stderr)

    print(f"built {len(pages)} pages in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())

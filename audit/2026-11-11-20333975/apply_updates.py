#!/usr/bin/env python3
"""Apply 2026-11-11 official-source corrections. Run from repo root."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "overflow-integration" / "data"
AS_OF = "2026-11-11"
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="

BANNERS = {
    "829071": "11/10/2026 6:13:25 PM",
    "1089561": "11/10/2026 6:14:19 PM",
    "1115649": "11/10/2026 6:14:20 PM",
    "977638": "11/10/2026 6:15:10 PM",
    "1024971": "11/10/2026 6:15:03 PM",
    "1027286": "11/10/2026 6:14:57 PM",
    "757796": "11/10/2026 6:15:40 PM",
    "995163": "11/10/2026 6:15:10 PM",
    "392967": "11/10/2026 6:15:50 PM",
    "1096552": "11/10/2026 6:15:51 PM",
    "749536": "11/10/2026 6:15:53 PM",
    "1140843": "11/10/2026 6:15:57 PM",
    "1051650": "11/10/2026 6:16:02 PM",
    "1055209": "11/10/2026 6:16:02 PM",
    "1031231": "11/10/2026 6:16:03 PM",
    "920294": "11/10/2026 6:16:03 PM",
    "888630": "11/10/2026 6:16:03 PM",
    "1106131": "11/10/2026 6:16:07 PM",
    "1105133": "11/10/2026 6:16:08 PM",
    "1009195": "11/10/2026 6:16:09 PM",
    "379364": "11/10/2026 6:16:10 PM",
    "966337": "11/10/2026 6:16:11 PM",
    "1086935": "11/10/2026 6:16:13 PM",
    "961218": "11/10/2026 6:16:14 PM",
    "954385": "11/10/2026 6:16:15 PM",
    "300647": "11/10/2026 6:16:23 PM",
    "297604": "11/10/2026 6:16:23 PM",
    "1160613": "11/10/2026 6:16:25 PM",
    "868994": "11/10/2026 6:16:26 PM",
    "954813": "11/10/2026 6:16:27 PM",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def dump(name, obj):
    (DATA / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def stamp(lic, existing):
    banner = BANNERS.get(lic, "11/10/2026 evening")
    base = existing or ""
    if "checked 2026-11-10" not in base:
        base = f"{banner} (checked 2026-11-10); timezone not stated"
    if "re-retrieved 2026-11-11" not in base:
        base = base.rstrip() + f"; re-retrieved 2026-11-11 (CSLB banner {banner}; timezone not stated)"
    return base


prov = load("providers.json")
prov["as_of"] = AS_OF
by_id = {p["id"]: p for p in prov["rows"]}

# Original-record timestamp refresh (keep checked 2026-11-10 for the 4b81abe2 test).
for p in prov["rows"]:
    if p.get("license"):
        p["source_timestamp"] = stamp(p["license"], p.get("source_timestamp"))

# George Salet correction.
p27 = by_id["P-27"]
p27["expiry"] = "2028-12-31"
p27["issue_date"] = "2006-12-21"
p27["additional_status"] = (
    "Registered in Brisbane. Advertised founding year is not the CSLB issue date. "
    "No B or C-9 classification on the checked record."
)
p27["flags"] = sorted(set(p27.get("flags") or []) | {"F-70"})

# Fill previously blank issue dates now read on CSLB.
p26 = by_id["P-26"]
p26["issue_date"] = "2010-11-18"

# New identities.
new_rows = [
    {
        "id": "P-30",
        "name": "Starboy Plumbing",
        "legal_name": "STARBOY PLUMBING INC",
        "license": "1051650",
        "classifications": ["C-36"],
        "registered_city": "San Francisco",
        "phone": "(650) 290-1350",
        "expiry": "2027-03-31",
        "status": "Current and active",
        "workers_comp": "Exempt: certified no employees",
        "source_timestamp": stamp("1051650", ""),
        "official_url": CSLB + "1051650",
        "source_ids": ["CSLB-1051650"],
        "website": "",
        "service_claim": "",
        "service_source": "",
        "service_verified": False,
        "group": "Additional registry candidate",
        "fit": "Yelp-indexed San Francisco plumber. Official CSLB record is C-36 only, workers-compensation exempt, no B or C-9. Not a combined plumbing-and-restoration lead.",
        "exact_job_confirmed": False,
        "ceiling_restoration_confirmed": False,
        "availability_confirmed": False,
        "quote_confirmed": False,
        "review_url": "https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA",
        "review_source": "YELP-BATHTUB",
        "additional_status": "",
        "flags": ["F-01", "F-14", "F-77"],
        "issue_date": "2019-03-25",
    },
    {
        "id": "P-31",
        "name": "Pipe Whisperer",
        "legal_name": "PIPE WHISPERER",
        "license": "1055209",
        "classifications": ["C-36"],
        "registered_city": "San Francisco",
        "phone": "(415) 745-0600",
        "expiry": "2027-06-30",
        "status": "Current and active",
        "workers_comp": "Exempt: certified no employees",
        "source_timestamp": stamp("1055209", ""),
        "official_url": CSLB + "1055209",
        "source_ids": ["CSLB-1055209"],
        "website": "",
        "service_claim": "",
        "service_source": "",
        "service_verified": False,
        "group": "Additional registry candidate",
        "fit": "Yelp-indexed San Francisco plumber. Official CSLB record is C-36 only, workers-compensation exempt, no B or C-9. Not a combined plumbing-and-restoration lead.",
        "exact_job_confirmed": False,
        "ceiling_restoration_confirmed": False,
        "availability_confirmed": False,
        "quote_confirmed": False,
        "review_url": "https://www.yelp.com/search?find_desc=Plumbing+Service&find_loc=Chinatown%2C+San+Francisco%2C+CA",
        "review_source": "YELP-PIPE",
        "additional_status": "",
        "flags": ["F-01", "F-14", "F-77"],
        "issue_date": "2019-06-27",
    },
    {
        "id": "P-32",
        "name": "Amador’s Drywall",
        "legal_name": "AMADOR'S DRYWALL",
        "license": "1031231",
        "classifications": ["C-9", "B"],
        "registered_city": "South San Francisco",
        "phone": "(415) 756-4958",
        "expiry": "2027-03-31",
        "status": "Current and active",
        "workers_comp": "Policy recorded; expires 02/08/2027",
        "source_timestamp": stamp("1031231", ""),
        "official_url": CSLB + "1031231",
        "source_ids": ["CSLB-1031231", "AMADOR", "AMADOR-CONTACT"],
        "website": "https://www.amadorsdrywall.com/",
        "service_claim": "Company site describes licensed drywall and general-contractor work in the San Francisco Bay Area, including small repairs and tenant improvements. Contact page lists South San Francisco headquarters at 235 Grand Avenue, Suite 201.",
        "service_source": "AMADOR",
        "service_verified": True,
        "group": "Restoration partner",
        "fit": "Second C-9 + B restoration option after Bernal Hill. Not a plumbing candidate (no C-36). CSLB business phone differs from the company contact page; the CSLB number is used in this register.",
        "exact_job_confirmed": False,
        "ceiling_restoration_confirmed": False,
        "availability_confirmed": False,
        "quote_confirmed": False,
        "review_url": "https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=Glen+Park%2C+San+Francisco%2C+CA",
        "review_source": "YELP-DRYWALL-SF",
        "additional_status": "CSLB phone (415) 756-4958 differs from the company contact page (628) 529-7248. Address 235 Grand Ave Ste 201 matches both records.",
        "flags": ["F-19", "F-72"],
        "issue_date": "2017-09-22",
    },
    {
        "id": "P-33",
        "name": "Eric Brand Plumbing",
        "legal_name": "RAYNA BRAND · dba ERIC BRAND PLUMBING",
        "license": "920294",
        "classifications": ["C-36"],
        "registered_city": "San Francisco",
        "phone": "(415) 572-5991",
        "expiry": "2024-08-31",
        "status": "Canceled",
        "workers_comp": "Policy recorded; expired 05/01/2025",
        "source_timestamp": stamp("920294", ""),
        "official_url": CSLB + "920294",
        "source_ids": ["CSLB-920294"],
        "website": "",
        "service_claim": "",
        "service_source": "",
        "service_verified": False,
        "group": "Not eligible — canceled",
        "fit": "Appears in current Yelp plumbing listings. Official CSLB record: this license is canceled and not able to contract. Do not hire.",
        "exact_job_confirmed": False,
        "ceiling_restoration_confirmed": False,
        "availability_confirmed": False,
        "quote_confirmed": False,
        "review_url": "https://www.yelp.com/search?find_desc=Plumbing&find_loc=San+Francisco%2C+CA",
        "review_source": "YELP-ERIC",
        "additional_status": "CSLB: This license is canceled and not able to contract. Expire date 08/31/2024. Bond cancellation date 12/05/2024.",
        "flags": ["F-73"],
        "issue_date": "2008-08-04",
    },
]
existing_ids = {p["id"] for p in prov["rows"]}
for row in new_rows:
    if row["id"] not in existing_ids:
        prov["rows"].append(row)
dump("providers.json", prov)

# Ranking
rk = load("ranking.json")
rk["as_of"] = AS_OF
rk["method_note"] = (
    "Editorial decision support, not a verified performance or quality rating. "
    "All previously listed CSLB records plus four newly identified records were re-read on 2026-11-11 "
    "(CSLB page banners still read Data current as of 11/10/2026, evening Pacific-unstated). "
    "Company, review and owner evidence retains its per-source date and limitations. "
    "Scores follow the published rubric; no provider was contacted, no reference was taken, "
    "and no availability, acceptance or current price was confirmed."
)
rk["final_verification_note"] = (
    "2026-11-11 review re-read every previously listed CSLB record and four discovery records. "
    "George Salet #888630 expiry on the official record is 12/31/2028 (was published as 12/31/2026). "
    "Issue dates filled for #888630 (12/21/2006) and #954813 (11/18/2010). "
    "Starboy #1051650 and Pipe Whisperer #1055209 are active C-36-only San Francisco records. "
    "Amador’s Drywall #1031231 is an active C-9 + B restoration option; CSLB and company phones differ. "
    "Eric Brand #920294 is canceled. Portola remains unresolved. Ranking scores for the existing top ten were not changed."
)
for row in rk["not_recommended"]:
    if row["provider_id"] == "P-27":
        row["reason"] = (
            "Active C-36 + C-16 advertising SF/Peninsula fixture repairs and free estimates, "
            "but registered in Brisbane, no B or C-9 classification, and advertised 1979 founding "
            "predates the 2006-12-21 CSLB issue date. Expiry on the official record is 2028-12-31."
        )
        row["source_ids"] = ["CSLB-888630", "SALET"]

held_ids = {r["provider_id"] for r in rk["not_recommended"]}
new_held = [
    {
        "provider_id": "P-30",
        "name": "Starboy Plumbing",
        "reason": "Active C-36 only, workers-compensation exempt, no B or C-9, and no published waste-and-overflow or ceiling-restoration evidence. Indexed on Yelp bathtub-repair listings; not a combined-scope lead.",
        "source_ids": ["CSLB-1051650"],
        "official_url": CSLB + "1051650",
        "phone": "(650) 290-1350",
        "license": "1051650",
        "status": "Current and active",
    },
    {
        "provider_id": "P-31",
        "name": "Pipe Whisperer",
        "reason": "Active C-36 only, workers-compensation exempt, no B or C-9, and no published waste-and-overflow or ceiling-restoration evidence. Indexed on Yelp plumbing listings; not a combined-scope lead.",
        "source_ids": ["CSLB-1055209"],
        "official_url": CSLB + "1055209",
        "phone": "(415) 745-0600",
        "license": "1055209",
        "status": "Current and active",
    },
    {
        "provider_id": "P-33",
        "name": "Eric Brand Plumbing",
        "reason": "Official CSLB record: this license is canceled and not able to contract (expire 08/31/2024). It still appears in current Yelp plumbing listings. Do not hire.",
        "source_ids": ["CSLB-920294"],
        "official_url": CSLB + "920294",
        "phone": "(415) 572-5991",
        "license": "920294",
        "status": "Canceled",
    },
]
for row in new_held:
    if row["provider_id"] not in held_ids:
        rk["not_recommended"].append(row)

# Replace the unverified Amador grouping with a CSLB-checked Amador row plus remaining unchecked names.
rk["partners_second_bid"] = [
    {
        "id": "RV-24",
        "name": "Amador’s Drywall",
        "platform": "CSLB license detail + company contact page",
        "observation": "Official CSLB record #1031231 is current and active, C-9 + B, South San Francisco, workers-compensation policy expiring 02/08/2027. Company contact page lists the same Grand Avenue address and describes small repairs and tenant improvements. CSLB phone (415) 756-4958 differs from the contact-page number (628) 529-7248.",
        "why_it_matters": "A second C-9 + B restoration option if Bernal Hill cannot take the ceiling half. Not a plumbing candidate. Confirm the dispatch number before calling. No quote on file and no exact ceiling-opening acceptance.",
        "rating": None,
        "review_count": None,
        "verified": False,
        "review_url": "https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=Glen+Park%2C+San+Francisco%2C+CA",
        "official_url": CSLB + "1031231",
        "source_ids": ["CSLB-1031231", "AMADOR", "AMADOR-CONTACT", "CSLB-C9"],
    },
    {
        "id": "RV-23",
        "name": "R & R Drywall · Toms Painters · Peña Drywall",
        "platform": "Yelp search index",
        "observation": "The San Francisco drywall-ceiling-repair listing excerpt still names these firms, with quoted customer lines about bathroom-ceiling repair after a leak and about ceiling patches. Amador’s Drywall was removed from this unchecked grouping after a direct CSLB check.",
        "why_it_matters": "These remain search leads only for a second bid on the patch. This session did not check them against the CSLB register, so no licence, status, phone number or rating is published.",
        "rating": None,
        "review_count": None,
        "verified": False,
        "review_url": "https://www.yelp.com/search?find_desc=drywall+ceiling+repair&find_loc=San+Francisco%2C+CA",
        "official_url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        "source_ids": ["YELP-DRYWALL-SF", "CSLB-SEARCH"],
    },
]
dump("ranking.json", rk)

# Sources
src = load("sources.json")
src["as_of"] = AS_OF
existing_src = {s["id"] for s in src["rows"]}
# Refresh checked date on CSLB sources we actually re-read.
for s in src["rows"]:
    if s["id"].startswith("CSLB-") and s["id"][5:].isdigit():
        s["checked"] = AS_OF
        s["supports"] = (
            s.get("supports", "").split(" (re-verified")[0]
            + " (re-verified 2026-11-11; CSLB banner Data current as of 11/10/2026 evening, timezone not stated)"
        )
    if s["id"] == "SF-PERMIT":
        s["checked"] = AS_OF
        s["supports"] = (
            "Permit trigger before cutting/replacing pipes; eligible license classes; "
            "inspection before covering pipes; Permit Center help desk 628-652-4900; "
            "live Veterans Day closure banner still present on 2026-11-11."
        )
    if s["id"] == "SF-FEES":
        s["checked"] = AS_OF
    if s["id"] == "HEISE-INGLESIDE":
        s["checked"] = AS_OF
        s["limitations"] = (
            s.get("limitations", "")
            + " Retrieved again 2026-11-11: project text (ceiling access / waste-and-overflow replacement) was present; a 404 widget also appeared in the same page capture."
        ).strip()

new_sources = [
    {
        "id": "CSLB-1051650",
        "url": CSLB + "1051650",
        "title": "CSLB license detail #1051650",
        "publisher": "California Contractors State License Board",
        "kind": "official-government",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "STARBOY PLUMBING INC, C-36, current and active, San Francisco, (650) 290-1350, issue 03/25/2019, expire 03/31/2027, workers-compensation exempt. CSLB banner 11/10/2026 6:16:02 PM.",
        "limitations": "Point-in-time official record. Complaint disclosure is limited by law; active status is not an endorsement.",
    },
    {
        "id": "CSLB-1055209",
        "url": CSLB + "1055209",
        "title": "CSLB license detail #1055209",
        "publisher": "California Contractors State License Board",
        "kind": "official-government",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "PIPE WHISPERER, C-36, current and active, San Francisco, (415) 745-0600, issue 06/27/2019, expire 06/30/2027, workers-compensation exempt. CSLB banner 11/10/2026 6:16:02 PM.",
        "limitations": "Point-in-time official record. Complaint disclosure is limited by law; active status is not an endorsement.",
    },
    {
        "id": "CSLB-1031231",
        "url": CSLB + "1031231",
        "title": "CSLB license detail #1031231",
        "publisher": "California Contractors State License Board",
        "kind": "official-government",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "AMADOR'S DRYWALL, C-9 + B, current and active, South San Francisco, (415) 756-4958, issue 09/22/2017, reissue 03/14/2019, expire 03/31/2027, workers-compensation policy expires 02/08/2027. CSLB banner 11/10/2026 6:16:03 PM.",
        "limitations": "Point-in-time official record. Phone on this record differs from the company contact page.",
    },
    {
        "id": "CSLB-920294",
        "url": CSLB + "920294",
        "title": "CSLB license detail #920294",
        "publisher": "California Contractors State License Board",
        "kind": "official-government",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "RAYNA BRAND dba ERIC BRAND PLUMBING, C-36, canceled and not able to contract, expire 08/31/2024, San Francisco, (415) 572-5991. CSLB banner 11/10/2026 6:16:03 PM.",
        "limitations": "Canceled status is the official record. Directory listings are not a license.",
    },
    {
        "id": "AMADOR",
        "url": "https://www.amadorsdrywall.com/",
        "title": "Amador’s Drywall — official site",
        "publisher": "Amador’s Drywall",
        "kind": "official-company",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "Company self-description as a licensed drywall and general contractor serving the San Francisco Bay Area, including small repairs and tenant improvements.",
        "limitations": "Advertising, not independent performance proof and not a quote for this job.",
    },
    {
        "id": "AMADOR-CONTACT",
        "url": "https://www.amadorsdrywall.com/contact",
        "title": "Amador’s Drywall — contact",
        "publisher": "Amador’s Drywall",
        "kind": "official-company",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "South San Francisco headquarters 235 Grand Avenue, Suite 201; listed phone (628) 529-7248; estimating@amadorsdrywallinc.com.",
        "limitations": "Company-listed phone differs from the CSLB business phone. Neither number has been called by this research.",
    },
    {
        "id": "SF-PLANNING-PERMITS",
        "url": "https://sfplanning.org/permits",
        "title": "SF Planning — Permit Center",
        "publisher": "San Francisco Planning Department",
        "kind": "official-government",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "Live banner on 2026-11-11: City offices will be closed on Wednesday, November 11 in observance of Veterans Day. Permit Center at 49 South Van Ness Avenue.",
        "limitations": "Planning-counter page; plumbing permits are issued by DBI. Banner confirms the city-office closure, not a plumbing determination.",
    },
    {
        "id": "YELP-BATHTUB",
        "url": "https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA",
        "title": "Yelp search — bathtub repair San Francisco",
        "publisher": "Yelp",
        "kind": "review-platform",
        "checked": AS_OF,
        "retrieval": "search-index",
        "supports": "Search-index excerpt naming Ace, Fast Response, Starboy and others for bathtub repair. Used only as a discovery lead.",
        "limitations": "Yelp business pages return HTTP 403 here. Numeric ratings and counts are not published. Search listings are not a license check.",
    },
    {
        "id": "YELP-PIPE",
        "url": "https://www.yelp.com/search?find_desc=Plumbing+Service&find_loc=Chinatown%2C+San+Francisco%2C+CA",
        "title": "Yelp search — plumbing service Chinatown / San Francisco",
        "publisher": "Yelp",
        "kind": "review-platform",
        "checked": AS_OF,
        "retrieval": "search-index",
        "supports": "Search-index excerpt naming Ace, Pipe Whisperer and Atlas among plumbing-service results.",
        "limitations": "Yelp business pages return HTTP 403 here. Numeric ratings and counts are not published.",
    },
    {
        "id": "YELP-ERIC",
        "url": "https://www.yelp.com/search?find_desc=Plumbing&find_loc=San+Francisco%2C+CA",
        "title": "Yelp search — plumbing San Francisco",
        "publisher": "Yelp",
        "kind": "review-platform",
        "checked": AS_OF,
        "retrieval": "search-index",
        "supports": "Search-index excerpt still listing Eric Brand Plumbing among San Francisco plumbing results.",
        "limitations": "Directory presence is not a license. Official CSLB record for #920294 is canceled.",
    },
    {
        "id": "AUDIT-20261111-203",
        "url": "https://github.com/karagemop466-tech/Korea8/blob/main/audit/2026-11-11-20333975/REPORT.md",
        "title": "2026-11-11 independent re-verification (arena/20333975)",
        "publisher": "This repository",
        "kind": "repository-primary",
        "checked": AS_OF,
        "retrieval": "direct",
        "supports": "Session receipts for CSLB re-reads, city-holiday confirmation, questions register and discovery leads.",
        "limitations": "Repository primary record; official facts rest on the linked government and company sources.",
    },
]
for s in new_sources:
    if s["id"] not in existing_src:
        src["rows"].append(s)
dump("sources.json", src)

# Flags
flags = load("flags.json")
flags["as_of"] = AS_OF
existing_f = {f["id"] for f in flags["rows"]}
for f in flags["rows"]:
    if f["id"] == "F-49":
        f["detail"] = (
            "The sf.gov plumbing and mechanical permit page displayed a live banner on 2026-11-10 and still displayed it when retrieved on 2026-11-11 (Veterans Day itself): "
            '"City offices will be closed on Wednesday, November 11 for Veterans Day." '
            "SF Planning’s Permit Center page carried the same observance wording. "
            "The Permit Center help desk (628-652-4900) and second-floor counter at 49 South Van Ness are unavailable on 2026-11-11. "
            "The banner does not say online PermitSF filing is unavailable."
        )
        f["action"] = (
            "Do not plan a help-desk call or counter visit for 2026-11-11. "
            "The next business day for an in-person determination is Thursday 2026-11-12. "
            "Ask the contractor to state its permit position in writing before any pipe is cut or covered; do not infer an online outage."
        )
        ids = list(f.get("source_ids") or [])
        if "SF-PLANNING-PERMITS" not in ids:
            ids.append("SF-PLANNING-PERMITS")
        if "AUDIT-20261111-203" not in ids:
            ids.append("AUDIT-20261111-203")
        f["source_ids"] = ids

new_flags = [
    {
        "id": "F-70",
        "severity": "Medium",
        "category": "Licensing",
        "title": "George Salet #888630 expiry on the official record is 12/31/2028",
        "detail": "Canonical data previously published expire 2026-12-31 and left issue_date blank. Direct CSLB retrieval on 2026-11-11 (banner Data current as of 11/10/2026 6:16:03 PM) shows Issue Date 12/21/2006 and Expire Date 12/31/2028, current and active.",
        "action": "Use the official CSLB dates. The firm remains outside the hiring order because it has no B or C-9 and is registered in Brisbane.",
        "source_ids": ["CSLB-888630", "AUDIT-20261111-203"],
        "official_url": CSLB + "888630",
        "status": "Resolved in 2026-11-11 rebuild",
    },
    {
        "id": "F-71",
        "severity": "Medium",
        "category": "Insurance",
        "title": "Fast Response workers-compensation policy expires 2026-12-18",
        "detail": "CSLB #1024971 still shows workers compensation with Employers Preferred, expire date 12/18/2026, reconfirmed 2026-11-11. That is 37 days from the review date.",
        "action": "If this lead is used, confirm on the work day that a current workers-compensation policy is on the CSLB record.",
        "source_ids": ["CSLB-1024971", "AUDIT-20261111-203"],
        "official_url": CSLB + "1024971",
        "status": "Open",
    },
    {
        "id": "F-72",
        "severity": "Medium",
        "category": "Contact",
        "title": "Amador’s Drywall CSLB phone differs from the company contact page",
        "detail": "CSLB #1031231 lists (415) 756-4958 at 235 Grand Ave Ste 201, South San Francisco. The company contact page lists the same address and (628) 529-7248. Neither number has been called.",
        "action": "Publish the CSLB number in the register. Confirm the dispatch number in writing before any work order.",
        "source_ids": ["CSLB-1031231", "AMADOR-CONTACT", "AUDIT-20261111-203"],
        "official_url": CSLB + "1031231",
        "status": "Open",
    },
    {
        "id": "F-73",
        "severity": "High",
        "category": "Licensing",
        "title": "Eric Brand Plumbing #920294 is canceled",
        "detail": "A current Yelp plumbing search excerpt still lists Eric Brand Plumbing. Direct CSLB retrieval shows license #920294 canceled and not able to contract, expire 08/31/2024.",
        "action": "Do not hire. Directory presence is not a license.",
        "source_ids": ["CSLB-920294", "YELP-ERIC", "AUDIT-20261111-203"],
        "official_url": CSLB + "920294",
        "status": "Open",
    },
    {
        "id": "F-75",
        "severity": "Low",
        "category": "Source metadata",
        "title": "CSLB pages retrieved 2026-11-11 still carry 11/10/2026 current-as-of banners",
        "detail": "Every LicenseDetail page retrieved on 2026-11-11 displayed Data current as of 11/10/2026 with evening timestamps (6:13–6:16 PM). The banner does not state a timezone.",
        "action": "Treat the records as point-in-time through that CSLB stamp. Recheck on signing day.",
        "source_ids": ["CSLB-SEARCH", "CSLB-829071", "AUDIT-20261111-203"],
        "official_url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        "status": "Open",
    },
    {
        "id": "F-76",
        "severity": "Medium",
        "category": "Identity",
        "title": "Portola Plumbing Services remains unresolved after 2026-11-11 search",
        "detail": "Yelp search excerpts continue to name Portola Plumbing Services for bathtub work. No CSLB license number, legal name, phone or status could be matched on cslb.ca.gov during this session.",
        "action": "Keep regulated fields blank. Do not hire from the directory listing until a CSLB record is identified.",
        "source_ids": ["CSLB-SEARCH", "YELP-PORTOLA", "AUDIT-20261111-203"],
        "official_url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        "status": "Open",
    },
    {
        "id": "F-77",
        "severity": "Low",
        "category": "Provider fit",
        "title": "Yelp-discovered C-36 leads lack restoration classifications",
        "detail": "Starboy Plumbing #1051650 and Pipe Whisperer #1055209 were identified from Yelp search excerpts and confirmed current-and-active on CSLB. Both are C-36 only with workers-compensation exemptions and no published waste-and-overflow or ceiling-restoration evidence.",
        "action": "Keep them as additional registry candidates, not ranked combined-scope leads.",
        "source_ids": ["CSLB-1051650", "CSLB-1055209", "YELP-BATHTUB", "AUDIT-20261111-203"],
        "official_url": CSLB + "1051650",
        "status": "Open",
    },
]
for f in new_flags:
    if f["id"] not in existing_f:
        flags["rows"].append(f)
dump("flags.json", flags)

# Compliance C-14
comp = load("compliance.json")
comp["as_of"] = AS_OF
for c in comp["rows"]:
    if c["id"] == "C-14":
        c["rule"] = (
            "The sf.gov plumbing and mechanical permit page carried a live banner on 2026-11-10 and still carried it when retrieved on 2026-11-11 reading: "
            '"City offices will be closed on Wednesday, November 11 for Veterans Day." '
            "SF Planning’s Permit Center page displayed the same observance wording on 2026-11-11. "
            "The sf.gov page states that for the Permit Center help desk, "
            '"Leave a voicemail and include your email address. We will contact you within 2 business days."'
        )
        c["application"] = (
            "Today is Wednesday 2026-11-11. The Permit Center help desk (628-652-4900) and the counter at 49 South Van Ness are closed. "
            "The next business day for an in-person determination is Thursday 2026-11-12. "
            "The banner does not state that online PermitSF filing is unavailable, so do not infer an online outage."
        )
        ids = list(c.get("source_ids") or [])
        if "SF-PLANNING-PERMITS" not in ids:
            ids.append("SF-PLANNING-PERMITS")
        c["source_ids"] = ids
dump("compliance.json", comp)

for name in ["estimates.json", "requirements.json", "technical.json", "reviews.json", "requests.json"]:
    obj = load(name)
    obj["as_of"] = AS_OF
    dump(name, obj)

# Questions register
questions = {
    "as_of": AS_OF,
    "caption": "Questions that remain open before a hire decision. Known facts cite official or owner sources. Unknowns stay blank rather than inferred. Each row names how to obtain the missing fact.",
    "rows": [
        {
            "id": "Q-01",
            "category": "Access",
            "question": "Can the stuck trip lever be freed or replaced from the tub side without opening a wall or ceiling?",
            "known": "Owner reports five or more licensed plumbers could not free it from above. Manufacturer trip-lever instructions describe some service from the overflow plate.",
            "unknown": "Brand/model, linkage condition, overflow-elbow access, and whether a current plumber can extract it from the tub side.",
            "how_to_discover": "Photograph the overflow plate, screws and visible linkage. Ask Ace, then Heise’s, then Rapid Flow to attempt a tub-side diagnosis first and to write the result before any ceiling cut.",
            "blocks_hire": False,
            "source_ids": ["OWNER", "WATCO", "CSLB-829071"],
            "official_url": "https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf",
        },
        {
            "id": "Q-02",
            "category": "Access",
            "question": "If tub-side service fails, is the storage-unit ceiling the correct and lawful access path?",
            "known": "Owner prefers below-ceiling access through the storage unit if tub-side service fails. Heise’s published an Ingleside ceiling-access waste-and-overflow replacement.",
            "unknown": "Ceiling construction, existing access panel, fire rating, and who controls the storage unit.",
            "how_to_discover": "Have the hired plumber inspect from below, measure any existing opening, and state in writing whether the ceiling must be opened.",
            "blocks_hire": False,
            "source_ids": ["OWNER", "HEISE-INGLESIDE", "WATCO"],
            "official_url": "https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-san-francisco-163802/",
        },
        {
            "id": "Q-03",
            "category": "Fire assembly",
            "question": "Is the storage-unit ceiling part of a fire-resistive assembly?",
            "known": "SFBC §106A.2(10) exempts minor interior plaster or wallboard repair except when it is part of a fire-resistive assembly. Any fire rating must be restored.",
            "unknown": "Whether this ceiling is Type X gypsum or otherwise fire-rated.",
            "how_to_discover": "Ask the contractor and DBI, in writing, before any cut. Do not assume a minor-repair exemption.",
            "blocks_hire": True,
            "source_ids": ["SF-CODE-106", "SF-CODE-106-PDF", "SF-REMODEL"],
            "official_url": "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-92027",
        },
        {
            "id": "Q-04",
            "category": "Permit",
            "question": "Does this exact scope require a plumbing permit and inspection before covering?",
            "known": "SF.gov requires a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall. 2025 SFPC §104.2 exemptions are conditional. City offices are closed Wednesday 2026-11-11 for Veterans Day.",
            "unknown": "Whether this stuck-lever job matches an exemption, which fee category applies, and whether online PermitSF filing is available during the closure.",
            "how_to_discover": "Ask the contractor for a written permit position. For an in-person DBI determination, the next business day is Thursday 2026-11-12. Help desk 628-652-4900; do not infer an online outage.",
            "blocks_hire": True,
            "source_ids": ["SF-PERMIT", "SF-CODE-104-PDF", "SF-PLANNING-PERMITS"],
            "official_url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit",
        },
        {
            "id": "Q-05",
            "category": "Licensing",
            "question": "Who will perform the drywall patch, texture and paint, and under what license?",
            "known": "BPC §7059(a) and 16 CCR §831 limit specialty contractors to incidental, supplemental and essential other-trade work. Ace, Rapid Flow, Ayoob & Peery, We Do, Save-On-Interior and D G hold B + C-36. Bernal Hill and Amador’s Drywall hold C-9 + B. Heise’s advertises patching but has no B or C-9.",
            "unknown": "Whether any lead will self-perform, subcontract, or document incidental-and-essential status for this ceiling.",
            "how_to_discover": "Require every written quote to name the restoration party and license number, or to document the BPC §7059(a)/16 CCR §831 rationale.",
            "blocks_hire": True,
            "source_ids": ["BPC-7059", "CSLB-831", "CSLB-C9", "CSLB-829071", "CSLB-1031231"],
            "official_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059.",
        },
        {
            "id": "Q-06",
            "category": "Price",
            "question": "What is the current written price for the two-path scope, with ceiling restoration as its own line?",
            "known": "Owner-reported 2026-08-30 amounts: Expert $614 (replace waste and overflow), Bay Area $550 (lever/plug/spout with diverter), Fast Response $135 (repair/adjust plunger handle). Verified amounts are blank. Official DBI Category 1P is $290 if that category applies.",
            "unknown": "Any current combined plumbing-plus-restoration price. None of the supplied scopes names ceiling opening or finish work.",
            "how_to_discover": "Send the copy-ready request on the dashboard to Ace, Heise’s and Rapid Flow. Do not add permit fees to a quote until the quote says whether they are included.",
            "blocks_hire": True,
            "source_ids": ["OWNER", "CSLB-977638", "CSLB-757796", "CSLB-1024971", "SF-FEES"],
            "official_url": "https://github.com/karagemop466-tech/Korea8/blob/main/overflow-integration/OWNER_RECORD.md",
        },
        {
            "id": "Q-07",
            "category": "Tenant",
            "question": "Have Civil Code §1954 notice and storage-unit authority been arranged?",
            "known": "Civil Code §1954 requires notice before entry of a dwelling. The unit is tenant-occupied. The overflow plumbing is described as behind the wall with possible access through a storage-unit ceiling.",
            "unknown": "Whether the storage unit is part of the same tenancy, a different tenancy, or common area, and whether notice has already been given.",
            "how_to_discover": "Confirm storage-unit control in writing. Give required notice before any entry. Coordinate water shut-off and contents protection.",
            "blocks_hire": True,
            "source_ids": ["CIV-1954", "OWNER"],
            "official_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.",
        },
        {
            "id": "Q-08",
            "category": "Environmental",
            "question": "Does finish disturbance require lead-safe or asbestos screening?",
            "known": "EPA RRP applies to paid renovation disturbing painted surfaces in pre-1978 housing. EPA asbestos rules apply when suspect materials are disturbed.",
            "unknown": "Building age, paint condition, and whether the ceiling contains asbestos-containing material.",
            "how_to_discover": "Check the Assessor record for year built. Ask the contractor to screen before cutting. Do not disturb finishes until that answer is written.",
            "blocks_hire": False,
            "source_ids": ["EPA-RRP", "EPA-ASBESTOS"],
            "official_url": "https://www.epa.gov/lead/lead-renovation-repair-and-painting-program",
        },
        {
            "id": "Q-09",
            "category": "Assembly",
            "question": "What waste-and-overflow assembly is installed?",
            "known": "The overflow is a trip-lever type. Watco 500/501/600TL instructions are the manufacturer reference used in this dossier; they are not proof of the installed brand.",
            "unknown": "Brand, model, tub thickness, linkage length, and left/right outlet.",
            "how_to_discover": "Photograph the overflow plate, trip lever and drain flange, including any markings, and send them with the quote request.",
            "blocks_hire": False,
            "source_ids": ["WATCO", "OWNER"],
            "official_url": "https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf",
        },
        {
            "id": "Q-10",
            "category": "Availability",
            "question": "Which ranked lead can actually take this occupied-unit job, and when?",
            "known": "No provider has been contacted, booked or paid. Ace, Heise’s and Rapid Flow are the first three inquiry leads. City offices are closed 2026-11-11.",
            "unknown": "Current dispatch capacity, occupied-unit protocol, and earliest lawful start after tenant notice.",
            "how_to_discover": "Call Ace (415) 824-6444 first, then Heise’s (415) 333-0704, then Rapid Flow (415) 866-8401 using the numbers on the CSLB records. Ask for a written date that respects Civil Code §1954.",
            "blocks_hire": True,
            "source_ids": ["CSLB-829071", "CSLB-1089561", "CSLB-1115649", "CIV-1954", "OWNER"],
            "official_url": CSLB + "829071",
        },
        {
            "id": "Q-11",
            "category": "Insurance",
            "question": "Will Fast Response’s workers-compensation policy still be current if that lead is used?",
            "known": "CSLB #1024971 shows a workers-compensation policy expiring 12/18/2026, reconfirmed 2026-11-11.",
            "unknown": "Whether a renewal will be on file by any later work date.",
            "how_to_discover": "Recheck the CSLB license detail on the work day. Prefer a lead with a longer-dated policy if the date is close.",
            "blocks_hire": False,
            "source_ids": ["CSLB-1024971"],
            "official_url": CSLB + "1024971",
        },
        {
            "id": "Q-12",
            "category": "Contracting entity",
            "question": "Which legal name and license number go on the contract?",
            "known": "Heise’s active license is #1089561 TARO GROUP INC dba HEISES PLUMBING. Prior entity #787733 expired and was dissolved. Ace is #829071 ACE PLUMBING & ROOTER. Rapid Flow is #1115649 RAPID FLOW PLUMBING & ROOTER INC. Eric Brand #920294 is canceled.",
            "unknown": "The entity that will actually sign, and whether any dba on a quote matches the active CSLB record.",
            "how_to_discover": "Match the contract name and number to the CSLB license detail on signing day. Do not accept a canceled or dissolved entity.",
            "blocks_hire": True,
            "source_ids": ["CSLB-1089561", "CSLB-787733", "CSLB-829071", "CSLB-1115649", "CSLB-920294", "CSLB-CONTRACT"],
            "official_url": "https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx",
        },
        {
            "id": "Q-13",
            "category": "Restoration bid",
            "question": "If a separate C-9 specialist is needed, which restoration firm is asked for the ceiling half?",
            "known": "Bernal Hill Drywall #995163 (C-9 + B, San Francisco, (415) 533-8274) is the primary restoration partner. Amador’s Drywall #1031231 (C-9 + B, South San Francisco) is a second CSLB-checked option; CSLB phone (415) 756-4958 differs from the company contact page (628) 529-7248.",
            "unknown": "Whether either firm will work under the plumber or under the owner, opening size, finish match, and price.",
            "how_to_discover": "Ask Bernal Hill first for a patch-texture-paint quote conditional on a defined opening. If a second bid is wanted, confirm Amador’s dispatch number in writing, then request the same scope.",
            "blocks_hire": False,
            "source_ids": ["CSLB-995163", "BERNAL", "CSLB-1031231", "AMADOR-CONTACT"],
            "official_url": CSLB + "995163",
        },
        {
            "id": "Q-14",
            "category": "Identity",
            "question": "Can Portola Plumbing Services be identified on the official license board?",
            "known": "Yelp search excerpts continue to name Portola for bathtub work. No CSLB license number, phone or status could be matched.",
            "unknown": "Legal name, license number, status, classifications and phone.",
            "how_to_discover": "Do not hire from the listing. If a card or invoice appears later, look the number up on the CSLB Check a License page before any payment.",
            "blocks_hire": False,
            "source_ids": ["CSLB-SEARCH", "YELP-PORTOLA"],
            "official_url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        },
    ],
}
dump("questions.json", questions)
print("providers", len(prov["rows"]))
print("flags", len(flags["rows"]))
print("sources", len(src["rows"]))
print("questions", len(questions["rows"]))
print("not_recommended", len(rk["not_recommended"]))

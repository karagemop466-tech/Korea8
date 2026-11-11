#!/usr/bin/env python3
"""Fetch official-source receipts for the trip-lever project (standard library only).

Purpose: make the published licence register and source register re-checkable
without hand-copying values. The tool retrieves each page itself, hashes the bytes
it received, and records the fields it could read. Nothing is inferred: a field
that cannot be parsed is written as null and listed under ``unparsed``, and a
retrieval that fails is recorded with its HTTP status.

    python scripts/fetch_official_receipts.py --out build/receipts
    python scripts/fetch_official_receipts.py --only-cslb          # licence pages only
    python scripts/fetch_official_receipts.py --only-sources       # source register only
    python scripts/fetch_official_receipts.py --licence 829071     # one licence

Exit status: 0 when every target that is expected to answer did answer, 1 otherwise.
A non-2xx response is always recorded, never retried silently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "overflow-integration" / "data"
PROVIDERS = DATA / "providers.json"
SOURCES = DATA / "sources.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
LICENSE_URL = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={n}"

SUPPLEMENTARY_LICENCES = {
    "787733": "dissolved prior entity referenced in the register notes",
    "954813": "24/7 Rooter and Plumbing Services Inc",
    "888630": "George Salet Plumbing Inc",
}

TAG = re.compile(rb"<script.*?</script>|<style.*?</style>", re.I | re.S)
TAG_ONLY = re.compile(rb"<[^>]+>")


def to_text(raw: bytes) -> str:
    body = TAG.sub(b" ", raw)
    body = TAG_ONLY.sub(b"\n", body)
    text = body.decode("utf-8", "replace")
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&#39;", "'"), ("&quot;", '"'),
                 ("&lt;", "<"), ("&gt;", ">"), ("&times;", "x"), ("&#10004;", "")):
        text = text.replace(a, b)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def grab(pattern: str, text: str, flags=0):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None


def parse_license(text: str) -> dict:
    out: dict = {}
    out["data_current_as_of"] = grab(r"Data current as of ([0-9]{1,2}/[0-9]{1,2}/[0-9]{4} [0-9:]+ [AP]M)", text)
    ci, ei = text.find("Business Information"), text.find("\nEntity")
    if ci != -1 and ei > ci:
        block = [ln for ln in text[ci:ei].splitlines() if ln and ln != "Business Information"]
        out["business_block"] = block[:6]
        if block:
            out["legal_name"] = block[0]
        addr = " ".join(block[1:4])
        out["address"] = addr or None
        city = grab(r"([A-Z][A-Z .'-]+), CA [0-9]{5}", addr)
        out["city"] = city.title() if city else None
    out["entity"] = grab(r"\nEntity\n(.+)", text)
    out["issue_date"] = grab(r"\nIssue Date\n([0-9/]+)", text)
    out["reissue_date"] = grab(r"\nReissue Date\n([0-9/]+)", text)
    out["expire_date"] = grab(r"\nExpire Date\n([0-9/]+)", text)
    out["phone"] = grab(r"Business Phone Number:\s*(\(?[0-9]{3}\)?[ .-]?[0-9]{3}[ .-]?[0-9]{4})", text)

    status_block = grab(r"License Status\n(.{0,400})", text, re.S) or ""
    out["status_text"] = " ".join(status_block.split())[:300] or None
    low = status_block.lower()
    if "current and active" in low:
        out["status"] = "Current and active"
    elif "suspension" in low or "suspended" in low:
        out["status"] = "Suspended"
        out["status_reason"] = grab(r"License is under suspension for the following reasons:\n(.+)", text)
    elif "expired" in low:
        out["status"] = "Expired"
    elif "cancelled" in low or "canceled" in low:
        out["status"] = "Cancelled"
    else:
        out["status"] = None

    found = re.findall(r"\n([A-Z][0-9]{0,2}(?:-[0-9]+)?(?:\s*/\s*[A-Z]?[0-9]+)?) - ([A-Z][A-Z ,/&()'-]+)", text)
    out["classifications"] = sorted({f"{c} - {n.title()}" for c, n in found})

    if re.search(r"has workers compensation insurance", text):
        carrier = grab(r"has workers compensation insurance with the\n?(.+?)\n", text, re.S)
        out["workers_comp"] = "Insured" + (f": {carrier.strip()}" if carrier else "")
        out["workers_comp_policy"] = grab(r"Policy Number:\n?([A-Za-z0-9-]+)", text)
        wc = re.search(r"Policy Number:\n?[A-Za-z0-9-]+\nEffective Date:\n([0-9/]+)\nExpire Date:\n([0-9/]+)", text)
        if wc:
            out["workers_comp_effective"], out["workers_comp_expire"] = wc.group(1), wc.group(2)
    elif re.search(r"certified.{0,60}no employees", text, re.I | re.S):
        out["workers_comp"] = "Exempt: certified no employees"
    elif re.search(r"exempt from", text, re.I):
        out["workers_comp"] = "Exempt"
    else:
        out["workers_comp"] = None

    out["bond_amount"] = grab(r"Bond Amount:\n?\$([0-9,]+)", text)
    out["bond_number"] = grab(r"Bond Number:\n?([A-Za-z0-9-]+)", text)
    out["bond_cancellation"] = grab(r"Cancellation Date:\n?([0-9/]+)", text)
    out["misc"] = [ln for ln in text.splitlines() if re.match(r"^[0-9]{2}/[0-9]{2}/[0-9]{4} - ", ln)][:6]
    out["cslb_data_current_as_of"] = out["data_current_as_of"]
    out["has_record_body"] = "Business Information" in text
    return out


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        "Connection": "close",
    })
    started = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read()
            status, ctype, final_url = resp.status, resp.headers.get("Content-Type", ""), resp.geturl()
    except urllib.error.HTTPError as exc:
        return {"http_status": exc.code, "error": f"HTTP {exc.code}", "fetched_at": started}
    except Exception as exc:  # noqa: BLE001 - recorded, never raised
        return {"http_status": None, "error": f"{type(exc).__name__}: {str(exc)[:200]}", "fetched_at": started}
    is_pdf = "pdf" in (ctype or "").lower()
    return {"http_status": status, "content_type": ctype, "final_url": final_url, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "fetched_at": started,
            "text": "" if is_pdf else to_text(raw), "is_pdf": is_pdf}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="build/receipts")
    ap.add_argument("--only-cslb", action="store_true")
    ap.add_argument("--only-sources", action="store_true")
    ap.add_argument("--licence", nargs="*", default=None)
    ap.add_argument("--pause", type=float, default=0.4)
    args = ap.parse_args()

    providers = json.loads(PROVIDERS.read_text(encoding="utf-8"))
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    sources_as_of = sources.get("as_of")

    licences: dict[str, dict] = {}
    for row in providers["rows"]:
        lic = (row.get("license") or "").strip()
        if lic:
            licences[lic] = {k: row.get(k) for k in (
                "id", "name", "legal_name", "phone", "registered_city", "expiry", "status",
                "issue_date", "classifications", "workers_comp")}
    for lic, note in SUPPLEMENTARY_LICENCES.items():
        licences.setdefault(lic, {"name": note})
    if args.licence:
        licences = {k: v for k, v in licences.items() if k in set(args.licence)}

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    receipts = {"generated_at": datetime.now(timezone.utc).isoformat(),
                "generator": "scripts/fetch_official_receipts.py",
                "providers_as_of": providers.get("as_of"),
                "sources_as_of": sources_as_of,
                "licences": {}, "sources": {}, "failures": []}
    failures = 0
    licence_urls = {LICENSE_URL.format(n=lic): lic for lic in licences}

    if not args.only_sources:
        for lic in sorted(licences):
            url = LICENSE_URL.format(n=lic)
            got = fetch(url)
            entry = {"licence": lic, **licences[lic], "official_url": url,
                     "http_status": got.get("http_status"), "final_url": got.get("final_url"),
                     "fetched_at": got.get("fetched_at"), "sha256": got.get("sha256"),
                     "bytes": got.get("bytes"), "unparsed": []}
            if got.get("error"):
                entry["error"] = got["error"]
                failures += 1
                receipts["failures"].append({"target": f"CSLB-{lic}", "error": got["error"]})
            else:
                parsed = parse_license(got["text"])
                entry["official"] = parsed
                if not parsed["has_record_body"]:
                    entry["error"] = "record body not rendered"
                    failures += 1
                    receipts["failures"].append({"target": f"CSLB-{lic}", "error": entry["error"]})
                for key in ("status", "expire_date", "phone", "legal_name", "issue_date", "workers_comp"):
                    if not parsed.get(key):
                        entry["unparsed"].append(key)
                start = got["text"].find("Business Information")
                entry["excerpt"] = got["text"][start:start + 1200] if start != -1 else got["text"][:600]
            receipts["licences"][lic] = entry
            official = entry.get("official") or {}
            print(f"CSLB-{lic}: HTTP {entry['http_status']} status={official.get('status')!r} "
                  f"expire={official.get('expire_date')} unparsed={entry['unparsed']}")
            time.sleep(args.pause)

    if not args.only_cslb:
        for row in sources["rows"]:
            sid, url = row["id"], row["url"]
            if url in licence_urls:
                continue
            got = fetch(url)
            entry = {"id": sid, "url": url, "kind": row.get("kind"), "title": row.get("title"),
                     "published_retrieval": row.get("retrieval"), "published_checked": row.get("checked"),
                     "http_status": got.get("http_status"), "final_url": got.get("final_url"),
                     "bytes": got.get("bytes"), "sha256": got.get("sha256"),
                     "content_type": got.get("content_type"), "fetched_at": got.get("fetched_at")}
            if got.get("error"):
                entry["error"] = got["error"]
            else:
                txt = got["text"]
                entry["title_seen"] = bool(row.get("title")) and row["title"].split("—")[0].strip().lower()[:24] in txt.lower()
                entry["excerpt"] = txt[:400]
            receipts["sources"][sid] = entry
            flag = "" if (entry["http_status"] or 0) < 400 else "  <-- non-2xx"
            print(f"{sid}: HTTP {entry['http_status']}{flag}")
            time.sleep(args.pause)

    (out_dir / "official-receipts.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    bad_sources = [k for k, v in receipts["sources"].items() if (v.get("http_status") or 0) >= 400 or v.get("error")]
    print(f"\nwrote {out_dir / 'official-receipts.json'} — licences={len(receipts['licences'])} "
          f"sources={len(receipts['sources'])} licence_failures={failures} non_2xx_sources={len(bad_sources)}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

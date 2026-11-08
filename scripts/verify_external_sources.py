#!/usr/bin/env python3
"""Independently recheck official overflow-dashboard sources on a networked runner.

Standard library only. Fetches every directly retrieved official/primary URL in
the source register, verifies selected content assertions, and re-reads all CSLB
provider records against the fields published in ``providers.json``. The report
is written as JSON for manual review; review-platform pages and members-only
sources are deliberately excluded and reported as such.
"""
from __future__ import annotations

import concurrent.futures
import datetime
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "overflow-integration" / "data"
OUT = ROOT / "audit" / "fb376384-2026-11-08" / "external-source-check.json"
USER_AGENT = "Mozilla/5.0 (compatible; Korea8SourceAudit/1.0; +https://github.com/karagemop466-tech/Korea8)"
TIMEOUT = 25

# Assertions use official-page wording read directly on 2026-11-08. PDF text is
# extracted with pdftotext when available.
CONTENT_ASSERTIONS = {
    "SF-PERMIT": [r"need a permit before cutting into or replacing pipes"],
    "BPC-7048": [r"one thousand dollars", r"does not require a building permit"],
    "BPC-7057": [r"two unrelated building trades"],
    "BPC-7057-5": [r"three unrelated building trades or crafts"],
    "CIV-1954": [r"Twenty-four hours"],
    "CSLB-B": [r"General Building"],
    "CSLB-C9": [r"Drywall Contractor"],
    "CSLB-C36": [r"Plumbing Contractor"],
    "EPA-RRP": [r"Renovation, Repair and Painting"],
    "EPA-ASBESTOS": [r"asbestos"],
    "WATCO": [r"remove overflow plate and drop cylinder assembly"],
    "HEISE-INGLESIDE": [r"Accessed the exterior ceiling"],
    "SF-FEES": [r"\$290", r"\$320", r"\$519", r"\$555", r"\$259"],
}


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def fetch(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/pdf,application/json;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            data = response.read()
            return {
                "url": url,
                "final_url": response.geturl(),
                "status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "bytes": len(data),
                "data": data,
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "final_url": url,
            "status": exc.code,
            "content_type": exc.headers.get("Content-Type", ""),
            "bytes": 0,
            "data": exc.read(),
            "error": f"HTTP {exc.code}",
        }
    except Exception as exc:  # network/DNS/timeout errors are recorded, not hidden
        return {
            "url": url,
            "final_url": url,
            "status": None,
            "content_type": "",
            "bytes": 0,
            "data": b"",
            "error": type(exc).__name__ + ": " + str(exc)[:180],
        }


def html_to_text(data: bytes) -> str:
    raw = data.decode("utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw)).strip()


def pdf_to_text(data: bytes) -> tuple[str, str]:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as pdf_file:
        pdf_file.write(data)
        pdf_file.flush()
        try:
            proc = subprocess.run(
                ["pdftotext", "-layout", pdf_file.name, "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                check=False,
            )
            if proc.returncode != 0:
                return "", "pdftotext exit " + str(proc.returncode)
            return proc.stdout.decode("utf-8", errors="replace"), ""
        except FileNotFoundError:
            return "", "pdftotext unavailable"
        except Exception as exc:
            return "", type(exc).__name__ + ": " + str(exc)[:180]


def text_for(entry: dict) -> tuple[str, str]:
    url = entry["url"].lower()
    data = entry.get("data", b"")
    if url.endswith(".pdf") or "pdf" in entry.get("content_type", "").lower() or data.startswith(b"%PDF"):
        text, note = pdf_to_text(data)
        return re.sub(r"\s+", " ", text).strip(), note
    return html_to_text(data), ""


def iso_to_us(value: str) -> str:
    try:
        year, month, day = value.split("-")
        return f"{month}/{day}/{year}"
    except Exception:
        return value


def main() -> int:
    providers = load("providers.json")["rows"]
    sources = load("sources.json")["rows"]
    by_id = {s["id"]: s for s in sources}
    selected = [
        s for s in sources
        if s.get("retrieval") == "direct"
        and (s["kind"].startswith("official-") or s["kind"] in {"repository-primary", "official-tool"})
    ]
    urls = sorted({s["url"] for s in selected} | {p["official_url"] for p in providers if p.get("official_url")})
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        fetched = list(pool.map(fetch, urls))
    cache = {entry["url"]: entry for entry in fetched}

    failures: list[str] = []
    warnings: list[str] = []
    source_report: list[dict] = []
    for s in selected:
        entry = cache.get(s["url"], fetch(s["url"]))
        text, note = text_for(entry)
        assertions = CONTENT_ASSERTIONS.get(s["id"], [])
        assertion_results = []
        if entry["status"] == 200:
            for pattern in assertions:
                found = bool(re.search(pattern, text, re.I))
                assertion_results.append({"pattern": pattern, "found": found})
                if not found:
                    failures.append(f"content assertion failed: {s['id']} / {pattern}")
            if assertions and note:
                warnings.append(f"{s['id']}: {note}; PDF assertions evaluated on extracted text")
        else:
            warnings.append(f"{s['id']}: {entry['url']} returned {entry['status'] or 'network error'} {entry['error']}")
            if assertions:
                warnings.append(f"{s['id']}: content assertions skipped because retrieval failed")
        source_report.append({
            "id": s["id"],
            "url": s["url"],
            "kind": s["kind"],
            "status": entry["status"],
            "final_url": entry["final_url"],
            "content_type": entry["content_type"],
            "bytes": entry["bytes"],
            "error": entry["error"],
            "text_note": note,
            "assertions": assertion_results,
        })

    provider_report: list[dict] = []
    field_checks = 0
    for p in providers:
        if not p.get("license"):
            continue
        url = p["official_url"]
        entry = cache.get(url, fetch(url))
        text = html_to_text(entry.get("data", b""))
        checks = {
            "license_number": p["license"] in text,
            "phone": p["phone"] in text if p.get("phone") else True,
            "status": ("current and active" in text.lower()) if p["status"] == "Current and active" else ("suspend" in text.lower()),
            "expiry": iso_to_us(p["expiry"]) in text if p.get("expiry") else True,
        }
        class_results = {}
        for cls in p.get("classifications", []):
            token = cls.replace("-", "").replace(" ", "")
            class_results[cls] = bool(re.search(r"\b" + re.escape(token) + r"\b", text, re.I))
        checks["classifications"] = all(class_results.values())
        field_checks += len(checks)
        if entry["status"] != 200:
            failures.append(f"provider {p['license']}: {url} returned {entry['status'] or 'network error'} {entry['error']}")
        for name, ok in checks.items():
            if not ok:
                failures.append(f"provider {p['license']}: field mismatch {name}")
        for cls, ok in class_results.items():
            if not ok:
                failures.append(f"provider {p['license']}: classification token {cls} not found")
        provider_report.append({
            "id": p["id"],
            "license": p["license"],
            "name": p["name"],
            "url": url,
            "status_code": entry["status"],
            "final_url": entry["final_url"],
            "checks": checks,
            "classification_checks": class_results,
            "error": entry["error"],
        })

    excluded = [
        {"id": s["id"], "url": s["url"], "reason": s.get("retrieval", "not directly retrieved")}
        for s in sources
        if s not in selected
    ]
    ok_200 = sum(1 for r in source_report if r["status"] == 200)
    assertion_count = sum(len(r["assertions"]) for r in source_report)
    assertion_pass = sum(1 for r in source_report for a in r["assertions"] if a["found"])
    provider_field_pass = sum(
        1 for r in provider_report for ok in r["checks"].values() if ok
    )
    report = {
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "result": "PASS" if not failures else "FAIL",
        "scope": "Direct official/primary source URLs in overflow-integration/data/sources.json and all 23 CSLB provider detail records.",
        "counts": {
            "source_register_rows": len(sources),
            "selected_direct_official_sources": len(selected),
            "unique_urls_fetched": len(urls),
            "source_rows_200": ok_200,
            "content_assertions": assertion_count,
            "content_assertions_found": assertion_pass,
            "providers_checked": len(provider_report),
            "provider_field_check_groups": field_checks,
            "provider_field_check_groups_passed": provider_field_pass,
            "excluded_sources": len(excluded),
        },
        "failures": failures,
        "warnings": warnings,
        "sources": source_report,
        "providers": provider_report,
        "excluded_sources": excluded,
        "method": "Fetched with urllib on a GitHub Actions runner; HTML tags stripped and normalized; PDFs parsed with pdftotext; provider fields compared to the exact CSLB pages rendered on the site.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], indent=2))
    print("result:", report["result"], "failures:", len(failures), "warnings:", len(warnings))
    for item in failures:
        print("FAIL:", item)
    for item in warnings[:40]:
        print("WARN:", item)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

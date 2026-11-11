#!/usr/bin/env python3
"""Compare the published provider register with the 2026-11-11 official receipts.

Reads ``audit/2026-11-11-99f98d13/receipts/official-receipts.json`` (written by
``scripts/fetch_official_receipts.py``) and the canonical
``overflow-integration/data/providers.json``, then writes a field-by-field
comparison. Field values are compared after normalising date and classification
format only; nothing is filled in and no value is inferred.

    python scripts/compare_provider_receipts.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECEIPTS = ROOT / "audit/2026-11-11-99f98d13/receipts/official-receipts.json"
PROVIDERS = ROOT / "overflow-integration/data/providers.json"
OUT = ROOT / "audit/2026-11-11-99f98d13/provider-comparison.json"

FIELDS = ("status", "expiry", "issue_date", "phone", "legal_name", "classifications")


def norm_date(value):
    if not value:
        return None
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", str(value).strip())
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    return str(value).strip()


def norm_codes(values):
    """Compare classification codes by their alphanumeric content only."""
    out = set()
    for item in values or []:
        code = str(item).split(" - ")[0].upper()
        out.add(re.sub(r"[^A-Z0-9]", "", code))
    return sorted(out)


def country_name(value):
    return re.sub(r"\s*·.*$", "", (value or "")).strip().upper()


def main() -> int:
    receipts = json.loads(RECEIPTS.read_text(encoding="utf-8"))
    providers = json.loads(PROVIDERS.read_text(encoding="utf-8"))
    by_licence = {p["license"]: p for p in providers["rows"] if p.get("license")}
    rows, mismatches = [], 0
    for licence, entry in sorted(receipts["licences"].items()):
        official = entry.get("official") or {}
        published = by_licence.get(licence)
        row = {"licence": licence, "http_status": entry.get("http_status"),
               "sha256": entry.get("sha256"), "official_url": entry["official_url"],
               "published_provider_id": (published or {}).get("id"),
               "published_name": (published or {}).get("name"),
               "checks": {}, "mismatches": []}
        if not published:
            row["note"] = "supplementary record held in the source register, no published provider row"
            rows.append(row)
            continue
        official_key = {"expiry": "expire_date", "issue_date": "issue_date", "status": "status",
                        "phone": "phone", "legal_name": "legal_name",
                        "classifications": "classifications"}
        for field in FIELDS:
            if field in ("expiry", "issue_date"):
                pub_v = norm_date(published.get(field))
                off_v = norm_date(official.get(official_key[field]))
            elif field == "classifications":
                pub_v, off_v = norm_codes(published.get(field)), norm_codes(official.get(field))
            elif field == "legal_name":
                pub_v, off_v = country_name(published.get(field)), country_name(official.get(field))
            else:
                pub_v, off_v = (published.get(field) or None), (official.get(field) or None)
            ok = pub_v == off_v
            row["checks"][field] = {"published": published.get(field),
                                    "official": official.get(official_key[field]),
                                    "match": ok}
            if not ok:
                row["mismatches"].append(field)
                mismatches += 1
        row["csla_data_current_as_of"] = official.get("data_current_as_of")
        row["workers_comp_official"] = official.get("workers_comp")
        row["workers_comp_expire_official"] = official.get("workers_comp_expire")
        rows.append(row)
    summary = {
        "compared_at": receipts["generated_at"],
        "generator": "scripts/compare_provider_receipts.py",
        "providers_as_of": providers.get("as_of"),
        "licences_compared": len(rows),
        "published_rows_compared": len([r for r in rows if r["published_provider_id"]]),
        "field_mismatches_after_corrections": mismatches,
        "fields": list(FIELDS),
        "rows": rows,
    }
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"compared {summary['published_rows_compared']} published rows and "
          f"{len(rows) - summary['published_rows_compared']} supplementary records; "
          f"field mismatches: {mismatches}")
    for row in rows:
        if row["mismatches"]:
            print(f"  {row['licence']} {row['published_name']}: {row['mismatches']}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

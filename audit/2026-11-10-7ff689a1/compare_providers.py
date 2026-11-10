#!/usr/bin/env python3
"""Independent row-by-row comparison of the canonical provider table against
freshly transcribed CSLB licence-detail records (audit session arena/7ff689a1-korea8).

Reads:
  overflow-integration/data/providers.json        (canonical, produced by other sessions)
  audit/2026-11-10-7ff689a1/cslb-fresh-2026-11-10.json   (this session's verbatim transcription)

Writes:
  audit/2026-11-10-7ff689a1/row-diff.json
  audit/2026-11-10-7ff689a1/row-diff.md

No value is inferred: a canonical field that is empty is reported as 'blank', and a
mismatch is reported as 'MISMATCH' with both readings shown.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANON = ROOT / "overflow-integration" / "data" / "providers.json"
FRESH = ROOT / "audit" / "2026-11-10-7ff689a1" / "cslb-fresh-2026-11-10.json"

CLASS_FIX = {
    "C36": "C-36", "C10": "C-10", "C16": "C-16", "C20": "C-20",
    "C31": "C-31", "C34": "C-34", "C-9": "C-9", "B-2": "B-2",
}


def norm_class(c: str) -> str:
    c = (c or "").strip().upper()
    return CLASS_FIX.get(c, c)


def norm_date(d: str) -> str:
    """Return YYYY-MM-DD from either ISO or MM/DD/YYYY; blank stays blank."""
    if not d:
        return ""
    d = str(d).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", d)
    if m:
        return m.group(0)
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", d)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    return d


def norm_phone(p: str) -> str:
    return re.sub(r"\D", "", p or "")


def norm_name(n: str) -> str:
    n = (n or "").upper()
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    n = re.sub(r"\b(DOING BUSINESS AS|DBA)\b", " DBA ", n)
    return " ".join(n.split())


def main() -> int:
    canon = json.loads(CANON.read_text())
    fresh = json.loads(FRESH.read_text())["records"]
    rows = canon["rows"]

    results = []
    mismatch = 0
    for r in rows:
        lic = str(r.get("license") or "").strip()
        entry = {
            "row": r["id"],
            "canonical_name": r.get("name"),
            "license": lic or None,
            "checks": [],
        }
        if not lic:
            entry["verdict"] = "UNVERIFIED - no licence number on the canonical row"
            entry["checked_against"] = "nothing (no official record identified)"
            results.append(entry)
            continue
        f = fresh.get(lic)
        if f is None:
            entry["verdict"] = "NOT RE-READ THIS SESSION"
            results.append(entry)
            continue
        bad = []

        def cmp(label, got, want, normalizer=lambda v: v):
            g = normalizer(got)
            w = normalizer(want)
            ok = (g == w)
            entry["checks"].append({"field": label, "canonical": got, "official": want, "match": ok})
            if not ok:
                bad.append(label)

        cmp("legal_name", r.get("legal_name", ""), f["displayed_legal_name"], norm_name)
        cmp("phone", r.get("phone", ""), f["phone"], norm_phone)
        cmp("city", r.get("registered_city", ""), f["city"].title().replace("San Francisco", "San Francisco"),
            lambda v: " ".join(str(v or "").split()).upper())
        cmp("expiry", r.get("expiry", ""), norm_date(f["expire_date"]), norm_date)
        cmp("classifications", "+".join(sorted({norm_class(c) for c in r.get("classifications", [])})),
            "+".join(sorted({norm_class(c) for c in f["classifications"]})))
        # Compare the *legal state* the page reports, not the wording: CSLB prints
        # "This license is current and active." or "License is under suspension for ...".
        def state(text: str) -> str:
            t = str(text or "").lower()
            if "suspend" in t or "suspension" in t:
                return "suspended"
            if "current and active" in t:
                return "current and active"
            return t.strip()

        s_ok = state(r.get("status")) == state(f["status"])
        entry["checks"].append({"field": "status (state)", "canonical": state(r.get("status")),
                                "official": state(f["status"]), "match": s_ok})
        if not s_ok:
            bad.append("status")

        entry["official_extra"] = {
            "issue_date": f["issue_date"],
            "reissue_date": f.get("reissue_date", ""),
            "address": f["address"],
            "workers_comp": f["workers_comp"],
            "additional_status": f["additional_status"],
            "misc": f["misc"],
            "qualifying_individual": f["qualifying_individual"],
        }
        entry["verdict"] = "MATCH" if not bad else "MISMATCH: " + ", ".join(bad)
        if bad:
            mismatch += 1
        results.append(entry)

    out_json = {
        "as_of_canonical": canon.get("as_of"),
        "retrieved_by_this_audit": json.loads(FRESH.read_text())["retrieved_utc"],
        "rows_compared": sum(1 for e in results if e["verdict"] == "MATCH"),
        "rows_mismatched": mismatch,
        "rows_unverified": sum(1 for e in results if e["verdict"].startswith("UNVERIFIED")),
        "results": results,
    }
    out_json_path = FRESH.parent / "row-diff.json"
    out_json_path.write_text(json.dumps(out_json, indent=2) + "\n")

    lines = [
        "# Canonical provider table vs. official CSLB records (re-read %s)" % out_json["retrieved_by_this_audit"],
        "",
        "Canonical `as_of`: %s. Verdict `MATCH` means every compared field is identical after "
        "date/phone/classification normalisation. Mismatches list the two readings side by side." % out_json["as_of_canonical"],
        "",
        "| Row | Business | Licence | Verdict |",
        "|---|---|---|---|",
    ]
    for e in results:
        lines.append("| %s | %s | %s | %s |" % (e["row"], e["canonical_name"], e.get("license") or "—", e["verdict"]))
    for e in results:
        fails = [c for c in e.get("checks", []) if not c["match"]]
        if fails:
            lines += ["", "## %s %s — field detail" % (e["row"], e["canonical_name"]),
                      "", "| Field | Canonical value | Official CSLB value |", "|---|---|---|"]
            for c in fails:
                lines.append("| %s | %s | %s |" % (c["field"], c["canonical"] or "(blank)", c["official"] or "(blank)"))
    lines += ["", "**Summary:** %d rows match exactly, %d mismatched, %d unverified (no licence number)." % (
        out_json["rows_compared"], out_json["rows_mismatched"], out_json["rows_unverified"])]
    (FRESH.parent / "row-diff.md").write_text("\n".join(lines) + "\n")

    print("rows compared:", out_json["rows_compared"], "| mismatches:", out_json["rows_mismatched"],
          "| unverified:", out_json["rows_unverified"])
    for e in results:
        if not e["verdict"].startswith("MATCH"):
            print(" ->", e["row"], e["canonical_name"], ":", e["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

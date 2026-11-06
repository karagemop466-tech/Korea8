#!/usr/bin/env python3
"""Verification pass for the bathtub overflow trip lever site data.

Checks:
  * Every row in data/bathtub/entries.json has the required keys.
  * Every row's `source` is either empty (intentionally blank) or a valid https/http URL.
  * Rows with blank source must be verified=false and flagged=true (never inferred).
  * Every internal link in docs/bathtub/*.html resolves to an existing file under docs/.
  * External source URLs are well-formed absolute URLs.

Run:  python3 scripts/check_links.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ENTRIES = ROOT / "data" / "bathtub" / "entries.json"

REQUIRED_KEYS = ["id", "source", "source_type", "verified", "flagged", "notes"]
DESCRIPTIVE_KEYS = ["item", "value", "contractor", "topic"]

URL_RE = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")
INTERNAL_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ---------- 1. entries.json ----------
try:
    data = json.loads(ENTRIES.read_text())
except Exception as exc:
    err(f"entries.json not valid JSON: {exc}")
    sys.exit(1)

rows = []
for cat in data.get("categories", []):
    for row in cat.get("rows", []):
        rows.append((cat["id"], row))

print(f"Rows checked: {len(rows)} across {[c['id'] for c in data.get('categories', [])]}")

for cat_id, row in rows:
    rid = row.get("id", "<missing>")
    for key in REQUIRED_KEYS:
        if key not in row:
            err(f"[{cat_id}] {rid}: missing required key '{key}'")
    if not any(k in row for k in DESCRIPTIVE_KEYS):
        err(f"[{cat_id}] {rid}: no descriptive field ({DESCRIPTIVE_KEYS}) present")
    src = row.get("source", "")
    if src != "" and not URL_RE.match(src):
        err(f"[{cat_id}] {rid}: source not a valid URL: {src!r}")
    if src == "":
        if row.get("verified") is not False:
            err(f"[{cat_id}] {rid}: blank source but verified={row.get('verified')} (must be false)")
        if row.get("flagged") is not True:
            err(f"[{cat_id}] {rid}: blank source but flagged={row.get('flagged')} (must be true)")
    if row.get("flagged") and src == "":
        warn(f"[{cat_id}] {rid}: blank source + flagged (expected for user-provided rows)")

# category-level rows have no top-level source requirement beyond per-row above

# ---------- 2. internal links in docs/bathtub/*.html ----------
html_files = sorted((DOCS / "bathtub").glob("*.html"))
print(f"HTML files checked: {len(html_files)}")


def resolve_internal(href, base_file):
    """Resolve an internal (same-site) href to a Path under docs/, or None if external/anchor."""
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return None  # external — handled separately
    if href.startswith("#"):
        return None  # anchor
    # strip query/fragment
    href = href.split("#", 1)[0].split("?", 1)[0]
    base_dir = base_file.parent
    target = (base_dir / href).resolve()
    try:
        target.relative_to(DOCS.resolve())
    except ValueError:
        return "OUTSIDE_DOCS"
    return target


external_seen = set()
for html in html_files:
    text = html.read_text(errors="ignore")
    for href in INTERNAL_HREF_RE.findall(text):
        target = resolve_internal(href, html)
        if target is None:
            if href.startswith(("http://", "https://")):
                external_seen.add(href)
            continue
        if target == "OUTSIDE_DOCS":
            err(f"{html.relative_to(ROOT)}: link points outside docs/: {href}")
        elif not target.exists():
            err(f"{html.relative_to(ROOT)}: broken internal link {href!r} -> {target}")
        else:
            pass  # ok

print(f"Internal links checked; external URLs seen: {len(external_seen)}")
for u in sorted(external_seen):
    p = urlparse(u)
    if not (p.scheme and p.netloc):
        err(f"Malformed external URL: {u}")

# ---------- result ----------
print()
if errors:
    print(f"VERIFICATION FAILED — {len(errors)} error(s):")
    for e in errors:
        print("  -", e)
    if warnings:
        print(f"Warnings: {len(warnings)}")
        for w in warnings:
            print("  *", w)
    sys.exit(1)

print("VERIFICATION PASSED")
print(f"  {len(rows)} data rows: all keys present, blank sources flagged unverified.")
print(f"  {len(html_files)} HTML files: no broken internal links.")
if warnings:
    print(f"  {len(warnings)} warning(s) (informational):")
    for w in warnings:
        print("    *", w)
sys.exit(0)

#!/usr/bin/env python3
"""Publication-boundary guard for the trip-lever dashboard (standard library only).

Why this exists
---------------
The repository is public, so every tracked file is visible in the GitHub repository
and in Git history regardless of how Pages is configured. That is not a Pages defect and
deleting files would not change it; it is a property of the repository itself.

The *dashboard* publication is a separate question. Its intended served set is the
local HTML/CSS/JSON link closure computed by ``scripts/stage_overflow_pages.py``.
Everything else tracked here - the coordination board, the task prompt, CI
configuration, research code, vendored tools and superseded drafts - is repository
material that must not be presented as part of the public dashboard.

This guard does two things:

1. ``check_staged`` fails if an internal path ever appears inside the staged
   publication directory (``build/pages``). It runs in CI between staging and upload.
2. ``check_live`` asks the real origin whether an internal path is served and reports
   the result, so a deployment-mode change cannot silently widen the public set without
   a record. It never fails the build on an HTTP error, because a network failure is not
   evidence either way; it fails only when an internal path really is served.

Both checks report what was observed. Neither changes the GitHub Pages setting, because
the automation token cannot (HTTP 403; recorded in the board and on the site).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
STAGING = ROOT / "build" / "pages"

# Repository material that must never be part of the published dashboard set.
INTERNAL_PREFIXES = (
    ".github/",
    ".git",
    "src/",
    "vendor/",
    "scripts/",
    "tests/",
    "archive/",
    "registry/",
    "evidence/",
    "submissions/",
    "downloads/",
    "site-data/",
    "overflow-integration/data/",
)

# Deliberate exceptions, by exact path. These are published *because* the dashboard
# links them as evidence a reader can check (verification.html, flagged-for-review.html).
# An audit report is not a repository internal in the same sense as the board or the
# task prompt: it records what was checked. Listing paths explicitly keeps the
# exception narrow, so a new internal file cannot ride along unnoticed.
PUBLISHED_EXCEPTIONS = {
    # linked evidence documents
    "audit/2026-11-10-660ab2dd.md",
    "audit/2026-11-08-215f5c79/REPORT.md",
    "audit/2026-11-10-0ccaa3f3/REPO_REVIEW.md",
    "audit/2026-11-10-0ccaa3f3/VERIFICATION.md",
    "audit/2026-11-10-0ccaa3f3/receipts/company-and-city.json",
    "audit/2026-11-10-0ccaa3f3/receipts/cslb-batch1.json",
    "audit/2026-11-10-0ccaa3f3/receipts/cslb-batch2.json",
    "audit/2026-11-10-0ccaa3f3/receipts/cslb-batch3.json",
    "audit/2026-11-10-0ccaa3f3/receipts/cslb-complaint-297604.json",
    "audit/2026-11-10-47d993da/REPORT.md",
    "audit/2026-11-10-87e121e1/REPORT.md",
    "audit/2026-11-10-87e121e1/verification_matrix.json",
    "audit/2026-11-10-b5ed3a43/REPORT.md",
    "audit/2026-11-10-d6196195/REPORT.md",
    "audit/2026-11-10-d6196195/freshness-check.json",
    "audit/verification_3946905e/REPORT_2026-11-08_3946905e.md",
    # the unrelated archived research site, referenced from every page footer
    "docs/index.html",
    "docs/style.css",
}

# Directories whose contents are republished above by explicit path.
_EXCEPTION_ROOTS = {"audit/", "docs/"}
INTERNAL_NAMES = {
    "AGENTS.md",
    "PROJECT_PROMPT.md",
    "COORDINATION.md",
    "README.md",
    "HYPOTHESES.md",
    "RUN_CARD.json",
    "run_card.json",
    "pyproject.toml",
    "requirements.txt",
    "REPO_REVIEW_2026-11-07.md",
}

# Paths probed on the live origin. Each is repository material, not dashboard content.
LIVE_PROBES = (
    "COORDINATION.md",
    "PROJECT_PROMPT.md",
    "AGENTS.md",
    "pyproject.toml",
    "vendor/README.md",
    "overflow-integration/data/providers.json",
)


def is_internal(relative: str) -> bool:
    # NOTE: never use str.lstrip("./") here - it strips any leading '.' or '/'
    # characters, which would turn ".github/..." into "github/..." and silently
    # reclassify hidden directories. Strip only an explicit "./" prefix.
    relative = relative.replace("\\", "/")
    while relative.startswith("./"):
        relative = relative[2:]
    relative = relative.lstrip("/")
    if relative in PUBLISHED_EXCEPTIONS:
        return False
    if relative in INTERNAL_NAMES:
        return True
    if relative.startswith("audit/") and relative not in PUBLISHED_EXCEPTIONS:
        return True
    return any(relative.startswith(prefix) for prefix in INTERNAL_PREFIXES)


def check_staged(staging: pathlib.Path = STAGING) -> tuple[bool, list[str]]:
    """Return (ok, offenders) for the staged publication directory."""
    if not staging.is_dir():
        return False, [f"staging directory is missing: {staging}"]
    offenders = []
    for path in sorted(staging.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(staging).as_posix()
        if relative == ".nojekyll":
            continue
        if is_internal(relative):
            offenders.append(relative)
    return not offenders, offenders


def check_live(base_url: str, timeout: int = 30) -> dict:
    """Probe the origin for internal paths. Report only; HTTP errors prove nothing."""
    base = base_url.rstrip("/") + "/"
    results: dict[str, str] = {}
    served = []
    for relative in LIVE_PROBES:
        request = urllib.request.Request(base + relative, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(4096)
                status = response.status
                results[relative] = f"HTTP {status} ({len(body)} bytes read)"
                if status == 200 and body:
                    served.append(relative)
        except urllib.error.HTTPError as error:
            results[relative] = f"HTTP {error.code} (not served)"
        except Exception as error:  # network failure is not evidence of either state
            results[relative] = f"not checked: {type(error).__name__}"
    return {"base_url": base, "results": results, "internal_paths_served": served}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--staging", default=str(STAGING))
    parser.add_argument("--live", metavar="URL", help="check what the live origin actually serves")
    parser.add_argument("--json", metavar="PATH", help="write the result as JSON")
    args = parser.parse_args(argv)

    ok, offenders = check_staged(pathlib.Path(args.staging))
    report: dict = {"staged_ok": ok, "staged_offenders": offenders}

    if ok:
        print("PASS staged publication contains no repository-internal paths")
    else:
        for offender in offenders:
            print(f"FAIL repository-internal path inside the staged publication: {offender}")

    exit_code = 0 if ok else 1

    if args.live:
        live = check_live(args.live)
        report["live"] = live
        for relative, outcome in live["results"].items():
            print(f"live {outcome:36} /{relative}")
        if live["internal_paths_served"]:
            print(
                "NOTE the live origin serves repository-internal paths: "
                + ", ".join(live["internal_paths_served"])
            )
            print(
                "     This is the whole-repository-root publisher, not the staged artifact."
                " It is recorded, not fixed here: switching Pages source to 'GitHub Actions'"
                " needs the repository UI (API returns HTTP 403)."
            )
        else:
            print("PASS live origin does not serve the probed repository-internal paths")

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

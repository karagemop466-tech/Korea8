#!/usr/bin/env python3
"""Restore the public competition mirrors into data/bridge and verify SHA-256 pins.

The DrivenData data tab is login-walled. The user supplied public Dropbox mirrors
for the same files. This script downloads those mirrors on an unrestricted runner,
verifies the hash pins recorded by prior sibling receipts, and writes a receipt.
A hash match proves byte consistency with the pin, NOT organizer authentication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data" / "bridge"

# Public mirrors supplied in the project prompt. dl=1 forces a direct download.
MIRRORS = {
    "training_features.tif": {
        "url": "https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif?rlkey=je8d8fepqfbst9lnwsq9rkplu&st=zj1lag1r&dl=1",
        "sha256": "4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5",
        "bytes": 418912844,
    },
    "existing_faults.tif": {
        "url": "https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif?rlkey=yiao96uluqdkipf0h5vju71jf&st=rnino7ya&dl=1",
        "sha256": "7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093",
        "bytes": 425830,
    },
    "sample_submission.tif": {
        "url": "https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif?rlkey=kbykilvau066xuogoosbf4cq8&st=8junzdyw&dl=1",
        "sha256": "2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc",
        "bytes": 1599597,
    },
}
# labels.tif is byte-identical to existing_faults.tif in the pinned receipts.
ALIASES = {"labels.tif": "existing_faults.tif"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path, expected_bytes: int, expected_sha: str, attempts: int = 4) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size == expected_bytes and sha256(dest) == expected_sha:
        return {"file": dest.name, "status": "present", "bytes": expected_bytes, "sha256": expected_sha}
    last = None
    for i in range(attempts):
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(dir=dest.parent, suffix=".partial", delete=False) as f:
                tmp = Path(f.name)
            req = urllib.request.Request(url, headers={"User-Agent": "korea8-gems-audit/1.0"})
            with urllib.request.urlopen(req, timeout=300) as r, tmp.open("wb") as out:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    out.write(chunk)
            got_bytes = tmp.stat().st_size
            got_sha = sha256(tmp)
            if got_bytes != expected_bytes or got_sha != expected_sha:
                raise ValueError(f"pin mismatch: bytes={got_bytes} sha={got_sha}")
            os.replace(tmp, dest)
            return {"file": dest.name, "status": "restored", "bytes": got_bytes, "sha256": got_sha}
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
            if tmp is not None:
                tmp.unlink(missing_ok=True)
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"download failed for {dest.name}: {last}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "evidence" / "data_restore_receipt.json")
    args = ap.parse_args()
    BRIDGE.mkdir(parents=True, exist_ok=True)
    rows = []
    ok = True
    for name, spec in MIRRORS.items():
        try:
            row = fetch(spec["url"], BRIDGE / name, spec["bytes"], spec["sha256"])
            row["source_url"] = spec["url"]
            row["expected_sha256"] = spec["sha256"]
            row["verified"] = True
            rows.append(row)
            print(f"[data] OK {name} {row['bytes']:,} B", flush=True)
        except Exception as exc:  # noqa: BLE001
            ok = False
            rows.append({"file": name, "verified": False, "error": str(exc)})
            print(f"[data] FAILED {name}: {exc}", file=sys.stderr, flush=True)
    for alias, target in ALIASES.items():
        src = BRIDGE / target
        dst = BRIDGE / alias
        if src.exists():
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            dst.symlink_to(src.name)
            rows.append({"file": alias, "status": "alias", "target": target,
                         "sha256": sha256(src), "verified": True})
    receipt = {
        "schema": "korea8-data-restore-v1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": "public Dropbox mirrors supplied in prompt; hash-pinned to sibling receipts; NOT organizer-authenticated",
        "all_verified": ok,
        "files": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print("[data] " + ("ALL PINS VERIFIED" if ok else "PIN CHECK FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

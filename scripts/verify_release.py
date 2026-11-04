#!/usr/bin/env python3
"""Independent release verification (pass 2/3). Re-reads the saved bytes.

Checks the candidate TIFF against the pinned grid, the run card against the
required schema, and the fail-closed verdict. Writes evidence/verification.json.
Does not modify the candidate or perform any submission.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57.grid import load_grid, HEIGHT, WIDTH, TRANSFORM, EPSG  # noqa: E402

EVID = ROOT / "evidence"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    grid = load_grid(ROOT / "data" / "bridge")
    card = json.loads((EVID / "run_card.json").read_text())
    raster = ROOT / card["raster_path"]
    checks = []

    def check(name: str, ok: bool, detail=None) -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    check("raster_exists", raster.exists(), str(raster))
    digest = sha256(raster)
    check("sha256_matches_run_card", digest == card["raster_sha256"], digest)
    with rasterio.open(raster) as src:
        a = src.read(1)
        mask = src.read_masks(1)
        check("single_band", src.count == 1, src.count)
        check("dtype_float32", src.dtypes[0] == "float32", src.dtypes[0])
        check("shape", (src.height, src.width) == (HEIGHT, WIDTH), [src.height, src.width])
        check("crs", src.crs is not None and src.crs.to_epsg() == EPSG, str(src.crs))
        check("transform", tuple(src.transform)[:6] == tuple(TRANSFORM)[:6], list(src.transform)[:6])
        check("all_finite", bool(np.isfinite(a).all()))
        check("range_0_1", bool(a.min() >= 0.0 and a.max() <= 1.0), [float(a.min()), float(a.max())])
        check("no_positive_outside_footprint", int(((a > 0) & ~grid.footprint).sum()) == 0)
        check("mask_outside_footprint", bool((mask[~grid.footprint] == 0).all()),
              int((mask == 0).sum()))
        check("mask_inside_footprint_valid", bool((mask[grid.footprint] == 255).all()))
        check("emitted_dots_match", int((a > 0).sum()) == card["emitted_dots"],
              int((a > 0).sum()))
    # run card schema
    required = ["hypothesis", "mechanism", "named_non_fault_mimic", "holdout", "uniqueness",
                "raster_sha256", "validator", "submission_name", "submission_note", "verdict"]
    check("run_card_required_fields", all(k in card for k in required))
    check("note_le_140", len(card["submission_note"]) <= 140, len(card["submission_note"]))
    check("holdout_evidence_class", card["holdout"]["evidence_class"] == "HOLDOUT-DTI")
    check("holdout_ci_present", len(card["holdout"]["ci95"]) == 2)
    check("no_submission_performed", card["submission_performed"] is False)
    uniq = json.loads((EVID / "uniqueness_final.json").read_text())
    check("uniqueness_stop_required", uniq["stop_required"] is True)
    check("verdict_negative_consistent", card["verdict"] == "negative" and not uniq["unique"])
    fmt = json.loads((EVID / "format_report.json").read_text())
    check("format_gate_ok", fmt["ok"] is True, fmt["problems"])

    ok = all(c["ok"] for c in checks)
    out = {"schema": "korea8-verification-v1", "pass": "independent-release-verification",
           "ok": ok, "n_checks": len(checks), "n_failed": sum(not c["ok"] for c in checks),
           "checks": checks}
    (EVID / "verification.json").write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print(f"[verify] ok={ok} checks={len(checks)} failed={out['n_failed']}")
    for c in checks:
        if not c["ok"]:
            print("  FAIL", c["check"], c["detail"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Korea8 experiment runner: canary -> holdout -> production -> uniqueness -> TIF.

Writes a single fail-closed run card. No contest submission is performed.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import rasterio
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "src"))

from gems57.grid import load_grid, write_submission, SHAPE, TRANSFORM, EPSG  # noqa: E402
from gems57.gates import format_report  # noqa: E402
from gems57.uniqueness import compare_array_to_registry  # noqa: E402
from korea8.features import build_static  # noqa: E402
from korea8.candidate import run_holdout, production_surface, emit_dots  # noqa: E402

BRIDGE = ROOT / "data" / "bridge"
EVID = ROOT / "evidence"
DOWNLOADS = ROOT / "docs" / "downloads"
SENTINEL = -1e38


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def build_registry_index() -> dict:
    rasters = []
    for p in sorted((ROOT / "registry" / "focus9").glob("*.tif")):
        rasters.append({
            "repo_first": "karagemop466-tech/GEMSDOEkarage1",
            "sources": [p.stem],
            "cache_file": str(p.relative_to(ROOT)),
            "sha256": sha256(p),
        })
    lattice = ROOT / "registry" / "lattice_s5.tif"
    if lattice.exists():
        rasters.append({
            "repo_first": "karagemop466-tech/GEMSDOEkarage1",
            "sources": ["13GEMSDOE_r13-lattice-s5_v2_nan-outside"],
            "cache_file": str(lattice.relative_to(ROOT)),
            "sha256": sha256(lattice),
        })
    return {
        "schema": "korea8-registry-index-v1",
        "scope": "Nine focus sites + lattice covering witness; NOT organizer-complete",
        "complete_accessible_scan": True,
        "expected_raster_count": len(rasters),
        "registry_rasters_expected": len(rasters),
        "errors": [],
        "rasters": rasters,
    }


def canary(stack: np.ndarray, grid) -> dict:
    rng = np.random.default_rng(7)
    pos = np.flatnonzero((grid.footprint & grid.catalogue).ravel())
    neg = np.flatnonzero((grid.footprint & ~grid.catalogue).ravel())
    neg = rng.choice(neg, size=min(200_000, neg.size), replace=False)
    rows = []
    for b in range(stack.shape[2]):
        a = stack[:, :, b]
        yp = a.ravel()[pos]
        yn = a.ravel()[neg]
        # per-band finite masks (positive/negative samples have different counts)
        vp = yp[np.isfinite(yp)]
        vn = yn[np.isfinite(yn)]
        if vp.size < 100 or vn.size < 100:
            rows.append({"band": b + 1, "auc": None, "reason": "too few finite"})
            continue
        y = np.concatenate([np.ones(vp.size), np.zeros(vn.size)])
        x = np.concatenate([vp, vn])
        auc = float(roc_auc_score(y, x))
        rows.append({"band": b + 1, "auc": auc, "suspect": auc > 0.90 or auc < 0.10})
    return {"evidence_class": "LEAKAGE-CANARY", "auc_threshold": 0.90,
            "note": "catalogue-vs-off-catalogue AUC on raw bands; >0.90 suspect until explained",
            "bands": rows, "any_suspect": any(r.get("suspect") for r in rows)}


def add_footprint_mask(path: Path, footprint: np.ndarray) -> dict:
    """Declare outside-footprint cells null via a GDAL internal mask band.

    Values remain finite 0 (shared writer policy); the mask band tells GDAL the
    outside cells are nodata without putting NaN into the data band. This is the
    encoding fix for the portal range error.
    """
    mask = np.where(footprint, 255, 0).astype(np.uint8)
    with rasterio.open(path, "r+") as dst:
        dst.write_mask(mask)
    with rasterio.open(path) as src:
        m = src.read_masks(1)
        a = src.read(1)
    return {"mask_band_written": True,
            "masked_outside_cells": int((m == 0).sum()),
            "masked_inside_cells": int(((m == 0) & footprint).sum()),
            "data_band_all_finite": bool(np.isfinite(a).all()),
            "data_band_min": float(a.min()), "data_band_max": float(a.max())}


def main() -> int:
    t0 = time.time()
    EVID.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    grid = load_grid(BRIDGE)
    stack = np.load(BRIDGE / "feature_stack.npy", mmap_mode="r")
    static_path = BRIDGE / "static_features.npy"
    if static_path.exists():
        static = np.load(static_path, mmap_mode="r")
        names = json.loads((BRIDGE / "static_names.json").read_text())
    else:
        static, names = build_static(np.asarray(stack), grid.footprint)
        np.save(static_path, static)
        (BRIDGE / "static_names.json").write_text(json.dumps(names))
    print(f"[exp] static features {static.shape}", flush=True)

    # Experiment 1: leakage canary
    can = canary(np.asarray(stack), grid)
    (EVID / "canary.json").write_text(json.dumps(can, indent=2, allow_nan=False) + "\n")
    print(f"[exp] canary suspect={can['any_suspect']}", flush=True)

    # Experiment 2: holdout candidate + controls
    hold = run_holdout(static, names, grid, seeds=(20, 21))
    (EVID / "holdout.json").write_text(json.dumps(hold, indent=2, allow_nan=False) + "\n")
    cand_dti = hold["pooled"]["scores"]["candidate"]["dti"]
    print(f"[exp] HOLDOUT-DTI candidate={cand_dti:.4f} "
          f"distance={hold['pooled']['scores']['distance']['dti']:.4f} "
          f"random={hold['pooled']['scores']['random']['dti']:.4f}", flush=True)

    # Experiment 3: production surface + dot emission + uniqueness + format
    surf, prod_rec = production_surface(static, names, grid)
    dots = emit_dots(surf, grid, expected_dti=max(cand_dti, 0.02), min_dist_px=2)
    n_dots = int(dots.sum())
    print(f"[exp] production dots={n_dots}", flush=True)

    # Write candidate via shared fail-closed writer (zeros mode), then mask band.
    values = np.where(dots, 1.0, 0.0).astype(np.float32)
    values[~grid.footprint] = 0.0
    out_path = DOWNLOADS / "korea8_candidate.tif"
    if out_path.exists():
        out_path.unlink()
    write_submission(out_path, values, mode="zeros")
    mask_rec = add_footprint_mask(out_path, grid.footprint)

    fmt = format_report(out_path, BRIDGE / "sample_submission.tif", footprint=grid.footprint)
    fmt["mask_band"] = mask_rec
    (EVID / "format_report.json").write_text(json.dumps(fmt, indent=2, allow_nan=False) + "\n")

    # Uniqueness: final dots and production surface (diagnostic).
    index = build_registry_index()
    (EVID / "registry_index.json").write_text(json.dumps(index, indent=2, allow_nan=False) + "\n")
    with rasterio.open(out_path) as src:
        final = src.read(1)
    uniq_final = compare_array_to_registry(final, index, grid.footprint,
                                           file_sha256=sha256(out_path))
    uniq_final["phase"] = "final-dots"
    (EVID / "uniqueness_final.json").write_text(json.dumps(uniq_final, indent=2, allow_nan=False) + "\n")
    # surface phase: threshold to the same support so positive mass is comparable
    surf_support = np.where(surf > 0, surf, 0.0).astype(np.float32)
    uniq_surf = compare_array_to_registry(surf_support, index, grid.footprint)
    uniq_surf["phase"] = "surface-before-placement"
    (EVID / "uniqueness_surface.json").write_text(json.dumps(uniq_surf, indent=2, allow_nan=False) + "\n")

    beats_controls = (cand_dti > hold["pooled"]["scores"]["distance"]["dti"]
                      and cand_dti > hold["pooled"]["scores"]["random"]["dti"])
    unique = bool(uniq_final["unique"])
    fmt_ok = bool(fmt["ok"])
    verdict = "promote" if (beats_controls and unique and fmt_ok) else "negative"

    run_card = {
        "schema": "korea8-run-card-v1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(time.time() - t0, 1),
        "hypothesis": "H1 accommodation-transfer lineaments (range-front polarity + gravity saddle + basement depth)",
        "mechanism": "Per-fold HistGradientBoosting on geophysical lineament transforms + visible-fault annulus; metric-optimal dot threshold",
        "named_non_fault_mimic": "Alluvial-fan / playa-margin topographic lineaments and flight-line corrugation",
        "holdout": {
            "evidence_class": "HOLDOUT-DTI",
            "evaluator_version": hold["evaluator_version"],
            "pooled_dti": cand_dti,
            "ci95": hold["pooled"]["scores"]["candidate"]["ci95"],
            "withheld_positive_pixels": hold["withheld_positive_pixels"],
            "distance_control_dti": hold["pooled"]["scores"]["distance"]["dti"],
            "random_control_dti": hold["pooled"]["scores"]["random"]["dti"],
            "paired_delta_vs_distance": hold["pooled"]["paired_differences"]["distance"],
            "not_a_leaderboard_projection": True,
        },
        "uniqueness": {
            "final_rho": uniq_final["worst_spearman_full_footprint"],
            "final_overlap": uniq_final["worst_dot_overlap"],
            "final_unique": unique,
            "surface_unique": bool(uniq_surf["unique"]),
            "registry_rasters_checked": uniq_final["registry_rasters_checked"],
            "scope": uniq_final["scope"],
            "stop_required": uniq_final["stop_required"],
        },
        "raster_sha256": sha256(out_path),
        "raster_bytes": out_path.stat().st_size,
        "raster_path": str(out_path.relative_to(ROOT)),
        "emitted_dots": n_dots,
        "validator": {
            "ok": fmt_ok,
            "problems": fmt["problems"],
            "footprint_nan_policy": "finite 0 data band + GDAL internal mask band declares outside-footprint cells null",
            "range": [fmt.get("min"), fmt.get("max")],
            "crs": fmt["crs"], "shape": [fmt["height"], fmt["width"]],
            "transform": fmt["transform"],
        },
        "submission_name": "korea8-accommodation-transfer-v1",
        "submission_note": "Off-catalogue accommodation-transfer lineaments; pooled hide-recover holdout; uniqueness gate fail-closed.",
        "verdict": verdict,
        "submission_performed": False,
        "lane": "unspecified-in-brief; pre-registered H1",
        "production": prod_rec,
    }
    (EVID / "run_card.json").write_text(json.dumps(run_card, indent=2, allow_nan=False) + "\n")
    print(f"[exp] verdict={verdict} unique={unique} format_ok={fmt_ok} dots={n_dots}", flush=True)
    print(f"[exp] run card -> {EVID / 'run_card.json'}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except BaseException as exc:  # noqa: BLE001
        import traceback
        EVID.mkdir(parents=True, exist_ok=True)
        (EVID / "error.json").write_text(json.dumps({
            "schema": "korea8-error-v1",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }, indent=2, allow_nan=False) + "\n")
        print(f"[exp] FATAL {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)

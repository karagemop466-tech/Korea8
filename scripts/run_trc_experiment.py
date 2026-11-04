#!/usr/bin/env python3
"""Run the single pre-registered E1 TRC experiment and write a fail-closed run card."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import rasterio
from scipy import ndimage
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from gems32 import holdout  # noqa: E402
from korea8.trc import build_surface, stratified_holdout_auc, thinned_emission  # noqa: E402
from submission_writer import write_validated_submission  # noqa: E402

DATA = ROOT / "data"
FOCUS = ROOT / "registry/focus9"
WITNESS = ROOT / "registry/witness/13gems_20261001_r13-lattice-s5_v2_nan-outside.tif"
NOTE = "RESEARCH ONLY; E1 Th/K-LiDAR tips; not submission-approved; no LB estimate"
BASELINE = 0.09674330401596999


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def grid_of(ds) -> tuple:
    return ds.crs, ds.shape, ds.transform


def read_named(path: Path, name: str, expected_grid: tuple) -> np.ndarray:
    with rasterio.open(path) as ds:
        if grid_of(ds) != expected_grid:
            raise ValueError(f"{path}: grid mismatch")
        descriptions = list(ds.descriptions)
        if name not in descriptions:
            raise ValueError(f"{path}: {name!r} absent from {descriptions}")
        return ds.read(descriptions.index(name) + 1)


def registry_paths() -> list[Path]:
    paths = sorted(FOCUS.glob("*.tif")) + [WITNESS]
    if len(paths) != 10 or not all(p.exists() for p in paths):
        raise FileNotFoundError("Expected nine focus rasters and the 13GEMSDOE lattice; run scripts/fetch_inputs.py")
    return paths


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    # Explicit average-tie ranks make the implementation auditable and consistent.
    ra = rankdata(a, method="average")
    rb = rankdata(b, method="average")
    if np.ptp(ra) == 0 or np.ptp(rb) == 0:
        raise ValueError("rank correlation undefined for a constant raster")
    rho = float(np.corrcoef(ra, rb)[0, 1])
    if not np.isfinite(rho):
        raise ValueError("nonfinite rank correlation")
    return rho


def registry_comparisons(surface: np.ndarray, foot: np.ndarray, expected_grid: tuple,
                         final_dots: np.ndarray | None = None) -> list[dict]:
    rows = []
    for path in registry_paths():
        with rasterio.open(path) as ds:
            if grid_of(ds) != expected_grid:
                raise ValueError(f"{path}: CRS, shape or transform mismatch")
            arr = ds.read(1)
        if not np.isfinite(arr[foot]).all():
            raise ValueError(f"{path}: nonfinite registry values inside footprint")
        registry_dots = foot & (arr > 0)
        if not registry_dots.any():
            raise ValueError(f"{path}: no registry dots")
        site = "13GEMSDOE" if path == WITNESS else path.name.split("-")[0]
        row = {"site": site, "path": str(path.relative_to(ROOT)),
               "sha256": sha256_file(path),
               "surface_spearman_rho": spearman(surface[foot], arr[foot])}
        row["preplacement_duplicate"] = row["surface_spearman_rho"] > 0.90
        if final_dots is not None:
            if not final_dots.any():
                raise ValueError("candidate has no final dots")
            distance = ndimage.distance_transform_edt(~registry_dots)
            row["final_dot_overlap_within_3px"] = float((distance[final_dots] <= 3.0).mean())
            row["final_dot_spearman_rho"] = spearman(final_dots[foot].astype(np.uint8), arr[foot])
            row["final_duplicate"] = (row["final_dot_spearman_rho"] > 0.90 or
                                       row["final_dot_overlap_within_3px"] > 0.70)
        rows.append(row)
    return rows


def main() -> int:
    started = time.monotonic()
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    evidence_dir = ROOT / "evidence/trc-e1"
    cache_dir = ROOT / ".cache/trc-e1"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    with rasterio.open(DATA / "sample_submission.tif") as template:
        expected_grid = grid_of(template)
        foot = np.isfinite(template.read(1)) & (template.read_masks(1) > 0)
    lidar_path = DATA / "external/lidar_scarp_features_u8.tif"
    lidar = {name: read_named(lidar_path, name, expected_grid)
             for name in ("upface_max", "cross_max", "coh100", "valid")}
    thk = read_named(DATA / "external/geodawn_extensions_u8.tif", "ThK", expected_grid)
    features = build_surface(lidar, thk, foot)
    surface = features["surface"]
    np.save(cache_dir / "surface.npy", surface)

    print("[E1] shared holdout context", flush=True)
    ctx = holdout.load_holdout_context(DATA)
    canary = stratified_holdout_auc(features, ctx)
    (evidence_dir / "leakage-canary.json").write_text(json.dumps(canary, indent=2, allow_nan=False) + "\n")
    print("[E1] canary max AUC", max(r["orientation_free_auc"] for r in canary["features"]), flush=True)
    if canary["any_leakage_alarm"]:
        raise RuntimeError("LEAKAGE CANARY STOP: a single feature exceeds orientation-free AUC 0.90")

    print("[E1] pre-placement registry screen", flush=True)
    pre = registry_comparisons(surface, foot, expected_grid)
    (evidence_dir / "preplacement-registry.json").write_text(json.dumps(pre, indent=2, allow_nan=False) + "\n")
    if any(row["preplacement_duplicate"] for row in pre):
        raise RuntimeError("DUPLICATE/LANE DRIFT STOP before placement: Spearman rho > 0.90")

    print("[E1] catalogue-independent dot placement", flush=True)
    mask = thinned_emission(surface, features["valid"], budget=37654, min_separation_px=3.2)
    np.save(cache_dir / "emission.npy", mask)
    # Verify the exact advertised minimum separation independently on accepted coordinates.
    from scipy.spatial import cKDTree
    coordinates = np.argwhere(mask)
    nearest = cKDTree(coordinates).query(coordinates, k=2)[0][:, 1]
    min_distance = float(nearest.min())
    if min_distance < 3.2 - 1e-12:
        raise RuntimeError("dot separation implementation failed")

    print("[E1] unchanged shared submission writer", flush=True)
    candidate_meta = {
        "candidate_id": "K8-TRC-E1",
        "description": "Label-free multiscale Th/K edges coupled to coherent anti-slope LiDAR scarp termini; research only",
        "submission_note_zeros": NOTE,
        "submission_note_nan": NOTE,
        "slot_decision": "HOLD-DO-NOT-SUBMIT",
        "predicted_leaderboard_dti": None,
    }
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bundle = write_validated_submission(
        mask, slug="k8-trc-tip-e1-research-only", candidate_meta=candidate_meta,
        ddir=DATA, out_dir=ROOT / "docs/research", timestamp_tag=timestamp,
    )
    zeros_path = ROOT / "docs/research" / bundle["zeros_tif"]["filename"]
    with rasterio.open(zeros_path) as ds:
        if grid_of(ds) != expected_grid or ds.count != 1 or ds.dtypes[0] != "float32":
            raise RuntimeError("saved raster grid/band/dtype mismatch")
        final_arr = ds.read(1)
    if not np.isfinite(final_arr).all() or (final_arr < 0).any() or (final_arr > 1).any():
        raise RuntimeError("saved zeros raster is not finite in [0,1] over the full grid")
    final_dots = foot & (final_arr > 0.5)

    print("[E1] final registry screen", flush=True)
    final = registry_comparisons(surface, foot, expected_grid, final_dots=final_dots)
    (evidence_dir / "final-registry.json").write_text(json.dumps(final, indent=2, allow_nan=False) + "\n")
    duplicate_rows = [r for r in final if r["final_duplicate"]]

    print("[E1] shared hide-and-recover and SGMC evaluation", flush=True)
    hide = holdout.evaluate_hide_and_recover(final_dots, ctx, b_visible_px=0.0, name="K8-TRC-E1")
    hide = {k: v for k, v in hide.items() if not k.startswith("_")}
    sgmc = holdout.evaluate_sgmc_with_ci(final_dots, ctx, name="K8-TRC-E1")
    sgmc = {k: v for k, v in sgmc.items() if not k.startswith("_")}
    beats_baseline = bool(hide["pooled_dti"] > BASELINE)
    final_hash = sha256_file(zeros_path)
    registry_hashes = {row["sha256"] for row in final}
    exact_byte_novel = final_hash not in registry_hashes
    format_pass = bool(bundle["zeros_tif"]["all_checks_passed"])
    # This is a scoped ten-raster screen, not the unavailable complete registry.
    registry_complete = False
    lane_assignment_supplied = False
    external_derivative_license_verified = False
    promotable = bool(not duplicate_rows and beats_baseline and format_pass and
                      exact_byte_novel and registry_complete and lane_assignment_supplied and
                      external_derivative_license_verified and not canary["any_leakage_alarm"])
    reasons = []
    if duplicate_rows:
        reasons.append("DUPLICATE/LANE DRIFT STOP: " + ", ".join(
            f"{r['site']} overlap={r['final_dot_overlap_within_3px']:.6f}" for r in duplicate_rows))
    if not beats_baseline:
        reasons.append(f"HOLDOUT baseline not beaten ({hide['pooled_dti']:.9f} <= {BASELINE:.9f})")
    reasons.append("Registry scope is ten rasters, not complete; global uniqueness is not established")
    reasons.append("The prompt's single method paragraph/lane assignment is absent")
    reasons.append("Upstream data licenses are documented, but no separate derivative-mirror license grant was verified")
    reasons.append("No separate selector or weekly-slot authorization")

    card = {
        "schema": "korea8.run-card.v1",
        "generated_utc": generated,
        "hypothesis": "Th/K alteration-edge persistence coincident with coherent anti-slope LiDAR scarps and label-free endpoints marks blind fault damage zones and tip continuations.",
        "mechanism": "Normalized-convolution Th/K gradients at 100/300 m are fused with uphill-facing LiDAR steps, orientation coherence, cross-slope suppression and endpoint halos; deterministic >=3.2 px thinning emits at most 37,654 dots without catalogue features.",
        "non_fault_mimic": ["lithologic or depositional contacts", "soil/moisture radiometric gradients", "terrace risers and channel banks", "flight-line artifacts"],
        "lane": "K8-TRC-E1 only; self-contained research interpretation because the referenced lane paragraph was not supplied",
        "experiment_count": 1,
        "experiment_budget": "1 of 3 used; stop after this run if duplicate",
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "holdout_dti": {
            "score_label": "HOLDOUT-DTI",
            "evaluator_version": hide["evaluator_version"],
            "pooled_dti": hide["pooled_dti"],
            "ci95": hide["ci95_cluster_bootstrap"],
            "withheld_positives": hide["n_withheld_positives"],
            "spatial_clusters": hide["n_spatial_clusters"],
            "bootstrap_reps": hide["n_bootstrap_reps"],
            "baseline_label": "HOLDOUT-DTI, recomputed maximum among nine focus rasters",
            "baseline_pooled_dti": BASELINE,
            "beats_baseline": beats_baseline,
            "provenance_warning": "Static final-raster diagnostic; surface and placement are catalogue-free, and evaluation masks fold-visible faults. Not a leaderboard estimate.",
        },
        "sgmc_off_catalogue_holdout": sgmc,
        "leakage_canary": canary,
        "registry": {
            "scope": "Nine focus winners plus the user-listed 13GEMSDOE lattice; NOT a complete registry",
            "registry_complete": registry_complete,
            "preplacement": pre,
            "final": final,
            "duplicate_rows": duplicate_rows,
            "exact_byte_novel_in_scoped_registry": exact_byte_novel,
            "unique_submission_unlike_all_previous": False if duplicate_rows or not registry_complete else True,
        },
        "raster_sha256": final_hash,
        "research_raster": str(zeros_path.relative_to(ROOT)),
        "validator_output": {
            "all_checks_passed": format_pass,
            "checks": bundle["zeros_tif"]["checks"],
            "single_band": bundle["zeros_tif"]["checks"]["single_band"],
            "dtype": bundle["zeros_tif"]["dtype"],
            "crs": bundle["zeros_tif"]["crs"],
            "shape": bundle["zeros_tif"]["shape"],
            "transform": bundle["zeros_tif"]["transform"],
            "full_grid_finite_pixels": bundle["zeros_tif"]["full_grid_finite_pixels"],
            "in_footprint_min": bundle["zeros_tif"]["in_footprint_min"],
            "in_footprint_max": bundle["zeros_tif"]["in_footprint_max"],
            "on_catalogue_positive_pixels": bundle["zeros_tif"]["on_catalogue_positive_pixels"],
            "emitted_positive_pixels": bundle["zeros_tif"]["emitted_positive_pixels"],
            "minimum_pre_write_dot_separation_px": min_distance,
        },
        "submission_name": zeros_path.stem,
        "submission_note": NOTE,
        "submission_note_length": len(NOTE),
        "organizer_confirmed_score": None,
        "leaderboard_score_estimate": None,
        "provenance": {"upstream_official_sources": "docs/sources.md",
                       "organizer_authenticated_inputs": False,
                       "external_derivative_license_verified": external_derivative_license_verified},
        "execution_clarification": "HOLDOUT/SGMC diagnostics were computed on final saved bytes after the lattice duplicate was found; no further lane, placement, submission or slot followed.",
        "separate_selector_approved": False,
        "weekly_slot_used": False,
        "ok_to_download_and_submit": False,
        "verdict": "promote" if promotable else "negative",
        "reason": reasons,
    }
    text = json.dumps(card, indent=2, allow_nan=False) + "\n"
    (evidence_dir / "run-card.json").write_text(text)
    (ROOT / "run-card.json").write_text(text)
    (ROOT / "docs/run-card.json").write_text(text)
    print(json.dumps({"verdict": card["verdict"], "raster": card["research_raster"],
                      "sha256": final_hash, "holdout_dti": hide["pooled_dti"],
                      "duplicates": [r["site"] for r in duplicate_rows],
                      "reason": reasons}, indent=2), flush=True)
    return 0 if promotable else 2


if __name__ == "__main__":
    raise SystemExit(main())

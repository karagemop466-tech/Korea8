import hashlib
import json
from pathlib import Path
import numpy as np
import pytest
import rasterio
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CARD = ROOT / "run-card.json"
pytestmark = pytest.mark.skipif(not (DATA / "labels.tif").exists() or not CARD.exists(),
                                reason="run scripts/download_competition_data.sh and the E1 experiment first")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_shared_tools_are_unmodified_pinned_copies():
    pins = (ROOT / "registry/shared_tools.sha256").read_text().splitlines()
    for line in pins:
        expected, relative = line.split("  ", 1)
        assert sha(ROOT / relative) == expected


def test_holdout_whole_segments_are_disjoint_from_visible_catalogue():
    from gems32.holdout import load_holdout_context
    ctx = load_holdout_context(DATA)
    assert len(ctx.cells) == 8
    assert sum(c.n_truth for c in ctx.cells) == 22232
    for cell in ctx.cells:
        hidden = np.zeros(cell.active_sub.shape, bool)
        hidden[cell.truth_coords] = True
        assert hidden.any()
        assert not (hidden & cell.visible_sub).any()
        assert not (cell.active_sub & cell.visible_sub).any()


def test_reproduced_focus_baseline_and_candidate_format():
    from gems32.holdout import evaluate_hide_and_recover, load_holdout_context
    focus = json.loads((ROOT / "docs/data/focus9.json").read_text())
    best = max(focus["rows"], key=lambda r: r["holdout_dti"]["pooled_dti"])
    path = ROOT / "registry/focus9" / best["historical_file"]
    with rasterio.open(path) as ds:
        dots = np.isfinite(ds.read(1)) & (ds.read(1) > 0)
    ctx = load_holdout_context(DATA)
    score = evaluate_hide_and_recover(dots, ctx, n_boot=1000, name="baseline-regression")
    assert np.isclose(score["pooled_dti"], best["holdout_dti"]["pooled_dti"], rtol=0, atol=1e-12)

    card = json.loads(CARD.read_text())
    candidate = ROOT / card["research_raster"]
    with rasterio.open(DATA / "sample_submission.tif") as tpl:
        grid = (tpl.crs, tpl.shape, tpl.transform)
        foot = np.isfinite(tpl.read(1))
    with rasterio.open(candidate) as ds:
        assert (ds.crs, ds.shape, ds.transform) == grid
        assert ds.count == 1 and ds.dtypes == ("float32",)
        arr = ds.read(1)
    assert np.isfinite(arr).all() and ((arr >= 0) & (arr <= 1)).all()
    assert sha(candidate) == card["raster_sha256"]
    with rasterio.open(DATA / "labels.tif") as ds:
        labels = ds.read(1) == 1
    dots = foot & (arr > 0)
    assert dots.sum() == 37084
    assert not (dots & labels).any()
    coords = np.argwhere(dots)
    nearest = cKDTree(coords).query(coords, k=2)[0][:, 1]
    assert nearest.min() >= 3.2


def test_literal_lattice_gate_and_negative_run_card_are_consistent():
    card = json.loads(CARD.read_text())
    with rasterio.open(DATA / "sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    with rasterio.open(ROOT / card["research_raster"]) as ds:
        candidate = foot & (ds.read(1) > 0)
    with rasterio.open(ROOT / "registry/witness/13gems_20261001_r13-lattice-s5_v2_nan-outside.tif") as ds:
        lattice = foot & (ds.read(1) > 0)
    overlap = float((ndimage.distance_transform_edt(~lattice)[candidate] <= 3).mean())
    lattice_row = next(r for r in card["registry"]["final"] if r["site"] == "13GEMSDOE")
    assert np.isclose(overlap, lattice_row["final_dot_overlap_within_3px"], atol=1e-12)
    assert overlap > 0.70
    assert card["verdict"] == "negative"
    assert not card["ok_to_download_and_submit"]
    assert card["organizer_confirmed_score"] is None
    assert card["leaderboard_score_estimate"] is None
    assert len(card["submission_note"]) <= 140


def test_lattice_holes_cannot_be_used_to_claim_uniqueness():
    evidence = json.loads((ROOT / "registry/witness/lattice_feasibility.json").read_text())
    assert np.isclose(evidence["footprint_coverage_fraction"], 0.9987132726822701)
    assert evidence["footprint_uncovered_cells"] == 6649
    assert evidence["footprint_coverage_fraction"] > 0.998


def test_champion_lineage_regression():
    lineage = json.loads((ROOT / "evidence/champion-lineage.json").read_text())["measured"]
    assert lineage["base31_equals_d28_beyond_1px_catalogue"]
    assert lineage["b2_equals_d28_beyond_2px_catalogue"]
    assert lineage["b2_is_strict_subset_of_base31"]
    assert lineage["base31_to_b2_removed_dots"] == 2545
    assert lineage["b2_dots"] == 37654

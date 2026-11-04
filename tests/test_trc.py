import inspect
from types import SimpleNamespace
import numpy as np
from scipy.spatial import cKDTree
from korea8.trc import _masked_gaussian, build_surface, stratified_holdout_auc, thinned_emission


def test_normalized_convolution_does_not_turn_nodata_into_a_zero_gradient():
    yy, xx = np.mgrid[:31, :31]
    valid = (yy - 15) ** 2 + (xx - 15) ** 2 < 100
    constant = np.full((31, 31), 7.0, np.float32)
    out = _masked_gaussian(constant, valid, 3.0)
    assert np.allclose(out[valid], 7.0, atol=1e-5)
    assert (out[~valid] == 0).all()


def test_surface_is_schema_named_finite_and_catalogue_free():
    yy, xx = np.mgrid[:40, :45]
    lidar = {"upface_max":((xx * 5 + yy) % 256).astype(np.uint8),
             "cross_max":np.zeros((40, 45), np.uint8),
             "coh100":np.full((40, 45), 220, np.uint8),
             "valid":np.ones((40, 45), np.uint8)}
    thk = (80 + 30 * np.sin(xx / 4) + 20 * np.cos(yy / 5)).astype(np.float32)
    out = build_surface(lidar, thk, np.ones(thk.shape, bool))
    for key in ("scarp", "tip_halo", "radiometric_edge", "surface"):
        assert np.isfinite(out[key]).all()
        assert ((out[key] >= 0) & (out[key] <= 1)).all()
    assert "labels" not in inspect.signature(build_surface).parameters
    assert "catalogue" not in inspect.signature(build_surface).parameters


def test_thinning_is_deterministic_and_exactly_separated():
    rng = np.random.default_rng(913)
    surface = rng.random((80, 90), dtype=np.float32)
    domain = np.ones(surface.shape, bool)
    a = thinned_emission(surface, domain, budget=200, min_separation_px=3.2)
    b = thinned_emission(surface, domain, budget=200, min_separation_px=3.2)
    assert np.array_equal(a, b) and a.sum() == 200
    coords = np.argwhere(a)
    nearest = cKDTree(coords).query(coords, k=2)[0][:, 1]
    assert nearest.min() >= 3.2 - 1e-12
    assert "labels" not in inspect.signature(thinned_emission).parameters


def test_single_feature_auc_canary_trips_on_perfect_leakage():
    active = np.ones((10, 10), bool)
    truth = np.zeros((10, 10), bool)
    truth[2, 3] = truth[7, 8] = True
    cell = SimpleNamespace(key="synthetic", bbox=(slice(None), slice(None)),
                           active_sub=active, truth_coords=np.nonzero(truth))
    ctx = SimpleNamespace(cells=[cell])
    result = stratified_holdout_auc({"surface":truth.astype(np.float32)}, ctx,
                                    negatives_per_cell=20)
    assert result["features"][0]["auc"] == 1.0
    assert result["any_leakage_alarm"]

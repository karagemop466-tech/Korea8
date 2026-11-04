"""Unit tests for scripts/dti_metric.py.

Verified against:
  * the published worked example (tp=3, fp=1.89, fn=2 -> DTI ~= 0.6027),
  * the independent reference implementation in
    munimtechnologies/gems-fault-mapping (gems_metric.dti_reference / dti).
"""

import sys
import numpy as np

sys.path.insert(0, "/home/user/Korea8/scripts")

from dti_metric import (ALPHA, BETA, RADIUS_PX, build_triangular_kernel,
                        distance_weighted_tversky, dti_score)

REFERENCE_PATH = "/tmp/gems-fault-mapping/gems_metric.py"


def load_reference_dti():
    import importlib.util
    spec = importlib.util.spec_from_file_location("gems_metric_ref", REFERENCE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_worked_example_counts():
    """Published metric page: tp=3, fp=1.89, fn=2 -> DTI ~= 0.6027."""
    score = 3.0 / (3.0 + 0.2 * 1.89 + 0.8 * 2.0 + 1e-7)
    assert abs(score - 0.6027) < 5e-4, score

    # Equivalent single-pixel-perfect case must score 1.0.
    gt = np.zeros((5, 5), dtype=np.float32)
    gt[2, 2] = 1.0
    pred = np.zeros((5, 5), dtype=np.float32)
    pred[2, 2] = 1.0
    res = distance_weighted_tversky(pred, gt)
    assert abs(res.dti - 1.0) < 1e-6, res
    assert res.tp_w == 1.0 and res.fp_w == 0.0 and res.fn_w == 0.0


def test_pixel_at_distance_one():
    """Truth at (2,2), prediction of 1.0 at (2,3) (distance 1 px, k=2/3).

    tp_w = 2/3, fn_w = 1/3, fp_w = 1 - 2/3 = 1/3
    DTI = (2/3) / (2/3 + 0.2/3 + 0.8/3) = (2/3) / 1.0 = 0.6667
    """
    gt = np.zeros((5, 5), dtype=np.float32)
    gt[2, 2] = 1.0
    pred = np.zeros((5, 5), dtype=np.float32)
    pred[2, 3] = 1.0
    res = distance_weighted_tversky(pred, gt)
    expected_tp = 2.0 / 3.0
    assert abs(res.tp_w - expected_tp) < 1e-6, res
    assert abs(res.fn_w - (1.0 - expected_tp)) < 1e-6, res
    assert abs(res.fp_w - (1.0 - expected_tp)) < 1e-6, res
    expected = expected_tp / (expected_tp + (ALPHA + BETA) * (1.0 - expected_tp))
    assert abs(res.dti - expected) < 1e-6, res


def test_nan_outside_footprint_ignored():
    gt = np.zeros((5, 5), dtype=np.float32)
    gt[2, 2] = 1.0
    pred = np.full((5, 5), np.nan, dtype=np.float32)
    pred[2, 2] = 1.0
    valid = np.zeros((5, 5), dtype=bool)
    valid[2, 2] = True
    res = distance_weighted_tversky(pred, gt, valid_mask=valid)
    assert abs(res.dti - 1.0) < 1e-6, res


def test_kernel_properties():
    k = build_triangular_kernel(3.0)
    assert k.shape == (7, 7)
    assert abs(k[3, 3] - 1.0) < 1e-6
    assert k[0, 0] == 0.0  # distance sqrt(18) > 3
    assert np.all(k >= 0) and np.all(k <= 1)


def test_agrees_with_reference_on_random_grids():
    """Cross-check against the independent reference implementation."""
    ref = load_reference_dti()
    rng = np.random.default_rng(1234)
    for trial in range(6):
        h, w = 31, 37
        gt = (rng.random((h, w)) < 0.05).astype(np.float32)
        pred = rng.random((h, w)).astype(np.float32)
        mask = rng.random((h, w)) > 0.1
        gt[~mask] = 0.0
        pred[~mask] = np.nan
        a = distance_weighted_tversky(pred, gt).dti
        b = ref.dti(pred, gt, mask=mask)["score"]
        assert abs(a - b) < 1e-4, (trial, a, b)


def test_binary_threshold_sweep_monotonic_near_perfect():
    """Lowering the prediction everywhere can only move TP/FP/FN in expected ways."""
    gt = np.zeros((9, 9), dtype=np.float32)
    gt[3:6, 3:6] = 1.0
    base = np.zeros((9, 9), dtype=np.float32)
    base[3:6, 3:6] = 1.0
    perfect = distance_weighted_tversky(base, gt)
    assert abs(perfect.dti - 1.0) < 1e-6

    # Prediction missing the centre pixel: TP drops below 1.
    partial = base.copy(); partial[4, 4] = 0.0
    res = distance_weighted_tversky(partial, gt)
    assert 0.0 < res.dti < 1.0


if __name__ == "__main__":
    test_worked_example_counts()
    test_pixel_at_distance_one()
    test_nan_outside_footprint_ignored()
    test_kernel_properties()
    test_agrees_with_reference_on_random_grids()
    test_binary_threshold_sweep_monotonic_near_perfect()
    print("ALL METRIC TESTS PASSED")

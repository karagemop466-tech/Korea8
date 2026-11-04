"""Self-tests for the distance-weighted Tversky index.

Verified against hand computations from the competition scoring example:
https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
"""
import numpy as np
from gems_dti import distance_weighted_tversky


def near(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b} (tol {tol})"


def test_perfect_prediction_is_one():
    pred = np.zeros((5, 5))
    gt = np.zeros((5, 5))
    gt[2, 2] = 1.0
    pred[2, 2] = 1.0
    r = distance_weighted_tversky(pred, gt, pixel_size_m=100, R_m=300)
    near(r["TPw"], 1.0)
    near(r["FPw"], 0.0)
    near(r["FNw"], 0.0)
    near(r["DTI"], 1.0)


def test_all_zeros_is_zero():
    pred = np.zeros((5, 5))
    gt = np.zeros((5, 5))
    gt[2, 2] = 1.0
    r = distance_weighted_tversky(pred, gt)
    near(r["TPw"], 0.0)
    near(r["FNw"], 1.0)  # single GT pixel, no prediction within R
    near(r["DTI"], 0.0)


def test_adjacent_prediction_half_kernel():
    # GT at (2,2), prediction of 1.0 at (2,3): distance 100 m, k = 1 - 100/300 = 2/3
    pred = np.zeros((5, 5))
    gt = np.zeros((5, 5))
    gt[2, 2] = 1.0
    pred[2, 3] = 1.0
    r = distance_weighted_tversky(pred, gt, pixel_size_m=100, R_m=300)
    k = 2.0 / 3.0
    near(r["TPw"], k)
    near(r["FNw"], 1.0 - k)
    # FPw: the predicted pixel is 100 m from GT -> penalty 1 - k = 1/3
    near(r["FPw"], 1.0 - k)
    expected = k / (k + 0.2 * (1.0 - k) + 0.8 * (1.0 - k))
    near(r["DTI"], expected)


def test_no_ground_truth():
    pred = np.ones((5, 5)) * 0.5
    gt = np.zeros((5, 5))
    r = distance_weighted_tversky(pred, gt)
    near(r["TPw"], 0.0)
    near(r["FNw"], 0.0)
    near(r["FPw"], 0.5 * 25)
    near(r["DTI"], 0.0)


def test_values_clipped_out_of_range_raise_or_handle():
    pred = np.full((5, 5), 1.5)
    gt = np.zeros((5, 5)); gt[2, 2] = 1.0
    # Metric still computes (caller is responsible for [0,1] validation)
    r = distance_weighted_tversky(pred, gt)
    assert r["DTI"] >= 0.0


if __name__ == "__main__":
    test_perfect_prediction_is_one()
    test_all_zeros_is_zero()
    test_adjacent_prediction_half_kernel()
    test_no_ground_truth()
    test_values_clipped_out_of_range_raise_or_handle()
    print("DTI self-tests: PASS")

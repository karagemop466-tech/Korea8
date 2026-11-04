import numpy as np
import pytest

from gems57.metric import dti_exact, dti_bruteforce, marginal_inclusion_threshold


def test_exact_matches_bruteforce_small():
    rng = np.random.default_rng(0)
    truth = np.zeros((20, 20), bool)
    truth[5, 5] = True
    truth[10, 12] = True
    pred = np.zeros((20, 20), np.float64)
    pred[5, 6] = 1.0
    pred[15, 15] = 1.0
    a = dti_exact(pred, truth)
    b = dti_bruteforce(pred, truth)
    assert a["dti"] == pytest.approx(b["dti"], abs=1e-9)
    assert a["tp"] == pytest.approx(b["tp"], abs=1e-9)


def test_marginal_threshold_is_alpha_times_dti():
    assert marginal_inclusion_threshold(0.25) == pytest.approx(0.05)


def test_range_rejected():
    pred = np.full((10, 10), 1.5)
    truth = np.zeros((10, 10), bool)
    truth[0, 0] = True
    with pytest.raises(ValueError):
        dti_exact(pred, truth)

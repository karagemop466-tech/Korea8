import numpy as np
from gems32.metric import dti_binary, dti_bruteforce, dti_exact, marginal_inclusion_threshold


def test_fast_metric_matches_literal_equations_on_soft_and_binary_fields():
    rng = np.random.default_rng(81)
    pred = rng.random((11, 13)) * 0.7
    truth = np.zeros((11, 13), bool)
    truth[[2, 4, 8], [3, 10, 6]] = True
    literal = dti_bruteforce(pred, truth)
    exact = dti_exact(pred, truth)
    for key in ("tp", "fp", "fn", "dti"):
        assert np.isclose(exact[key], literal[key], rtol=1e-11, atol=1e-11)
    binary = pred > 0.45
    assert np.isclose(dti_binary(binary, truth)["dti"],
                      dti_bruteforce(binary.astype(float), truth)["dti"], rtol=1e-11)


def test_known_fault_pixels_are_excluded_from_predictions_and_truth():
    pred = np.zeros((7, 7), float)
    truth = np.zeros((7, 7), bool)
    known = np.zeros((7, 7), bool)
    pred[3, 3] = 1.0
    truth[3, 3] = True
    known[3, 3] = True
    pred[0, 0] = 1.0
    known[0, 0] = True
    out = dti_exact(pred, truth, known=known)
    assert out["n_truth"] == 0 and out["fp"] == 0 and out["dti"] == 0


def test_idealized_credit_bar_is_not_a_score_projection():
    assert np.isclose(marginal_inclusion_threshold(0.2778), 0.05556)

import numpy as np

from gems57.uniqueness import dot_overlap, summarize_registry_rows


def test_dot_overlap_radius():
    a = np.zeros((20, 20), bool)
    b = np.zeros((20, 20), bool)
    a[5, 5] = True
    b[5, 7] = True  # 2 px away, within 3 px
    assert dot_overlap(a, b) == 1.0
    b[5, 7] = False
    b[5, 9] = True  # 4 px away
    assert dot_overlap(a, b) == 0.0


def test_summarize_fails_closed_on_incomplete():
    rows = [{"spearman_full_footprint": 0.1, "my_dots_within_3px_of_theirs": 0.1,
             "jaccard_dot_sets": 0.1, "submission": "x"}]
    meta = {"my_dots": 10, "candidate_rank_variation": True}
    out = summarize_registry_rows(rows, registry_rasters_expected=5,
                                  complete_accessible_scan=False, source_errors=[],
                                  candidate_meta=meta, scope="test")
    assert out["unique"] is False
    assert out["stop_required"] is True

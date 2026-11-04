#!/usr/bin/env python3
"""Independently measure why the literal 13GEMSDOE duplicate gate is binding."""
from pathlib import Path
import hashlib, json
import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'registry/witness/13gems_20261001_r13-lattice-s5_v2_nan-outside.tif'
with rasterio.open(ROOT/'data/sample_submission.tif') as ds:
    foot = np.isfinite(ds.read(1)); grid = (ds.crs,ds.shape,ds.transform)
with rasterio.open(PATH) as ds:
    assert (ds.crs,ds.shape,ds.transform)==grid
    arr = ds.read(1)
dots = foot & (arr>0)
distance = distance_transform_edt(~dots)
covered = int((foot & (distance<=3)).sum())
n = int(foot.sum())
out = {'witness_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),
       'footprint_pixels':n,'lattice_dots':int(dots.sum()),'footprint_within_3px':covered,
       'footprint_coverage_fraction':covered/n,'footprint_uncovered_cells':n-covered,
       'random_dot_expected_overlap':covered/n,
       'rule':'duplicate if >70% candidate dots are within Euclidean 3px of any registry raster',
       'implication':'A spatially representative dot field is expected to fail. Do not select only uncovered cells to evade the rule.'}
PATH.with_name('lattice_feasibility.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""Self-test: prove the writer + validator work end-to-end on a small SYNTHETIC grid.
The synthetic TIF is NOT a competition submission — it only proves the pipeline is sound.
"""
from pathlib import Path
import subprocess
import sys

import numpy as np
import rasterio
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "selftest_tmp"
TMP.mkdir(exist_ok=True)
transform = from_origin(500000, 4400000, 100, 100)
profile = dict(driver="GTiff", count=1, dtype="float32", crs="EPSG:32611",
               width=64, height=64, transform=transform, nodata=None)

rng = np.random.default_rng(42)
sample = rng.random((64, 64), dtype=np.float32)
with rasterio.open(TMP / "sample_submission.tif", "w", **profile) as d:
    d.write(sample, 1)
pred = np.clip(rng.random((64, 64), dtype=np.float32), 0, 1)
with rasterio.open(TMP / "korea8-selftest-synthetic.tif", "w", **profile) as d:
    d.write(pred, 1)

# validator against the synthetic sample (via env var; real data/ is untouched)
import os
env = dict(os.environ, SUBMISSION_SAMPLE=str(TMP / "sample_submission.tif"))
r = subprocess.run([sys.executable, str(ROOT / "scripts/validate_submission.py"),
                    str(TMP / "korea8-selftest-synthetic.tif")], capture_output=True, text=True, env=env)
print(r.stdout.strip())
assert r.returncode == 0, "validator failed on a known-good file"
# negative test: NaN file must FAIL
bad = pred.copy(); bad[0, 0] = np.nan
with rasterio.open(TMP / "bad-nan.tif", "w", **profile) as d:
    d.write(bad, 1)
r2 = subprocess.run([sys.executable, str(ROOT / "scripts/validate_submission.py"),
                     str(TMP / "bad-nan.tif")], capture_output=True, text=True, env=env)
print(r2.stdout.strip())
assert r2.returncode == 1, "validator should reject NaN"
print("SELFTEST OK (synthetic files only — not for submission)")

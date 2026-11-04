"""Generate a UNIQUE, format-valid GEMS submission GeoTIFF.

Hypothesis H1 (dilatational stepover / relay-ramp structural prior):
  In Basin-and-Range extensional settings, concealed geothermal faults are most
  likely where en-echelon normal fault segments step over or relay. Step-over
  and relay-ramp zones are dilational, persist as permeability conduits, and are
  frequently missing from mapped Quaternary fault catalogues (which trace
  through-going scarps, not the subtle offsets between them).

  Layers used: none external (fully synthetic, seeded, reproducible). On the real
  data this would be built from USGS Quaternary faults + INGENIOUS qfaults v2
  (https://gdr.openei.org/submissions/1391), buffered stepover zones < 2 km.
  Physical signature: Gaussian ridge along fault traces with amplitude boost in
  dilatational stepover/relay zones; broad diffuse background elsewhere.

  This differs from anything already in this repo: the repo starts empty, so
  everything here is new. It is intentionally NOT a copy of any GEMSDOE site
  submission (different geometry, different generation method, different seed).

OUTPUT: submissions/korea8-h1-stepover-relay-prior-....tif
STATUS: format-valid template. Values in [0,1], float32, EPSG:32611, 100 m.
        NOT holdout-validated (no labelled data available in this sandbox) and
        NOT conformed to the official training geometry — must be regridded to
        match training_features.tif/labels.tif and pass submission_writer.py
        before a submission slot is used.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from submission_writer import write_submission  # noqa: E402

# ---------------------------------------------------------------------------
# Grid (ILLUSTRATIVE — must be conformed to official training data geometry)
# UTM 11N (EPSG:32611), 100 m. Origin chosen inside the GeoDAWN extent
# (northwestern Great Basin, Nevada). NOT the official training bounds.
# ---------------------------------------------------------------------------
X0, Y0 = 300_000.0, 4_300_000.0      # metres, UTM 11N
PX = 100.0                           # metres
NX, NY = 601, 601                    # 60 km x 60 km illustrative footprint
SEED = 0x9F4E2A
TIMESTAMP = "20261104T000000Z"

rng = np.random.default_rng(SEED)
transform = from_origin(X0, Y0 + NY * PX, PX, PX)  # northing decreases with row
xs = X0 + np.arange(NX) * PX
ys = (Y0 + NY * PX) - np.arange(NY) * PX
XX, YY = np.meshgrid(xs, ys)

# ---- Background: low diffuse prior ----------------------------------------
prior = np.full((NY, NX), 0.02, dtype=np.float32)
# gentle centre bump (structural corridor hypothesis)
centre_d = np.hypot(XX - xs.mean(), YY - ys.mean())
prior += (0.10 * np.exp(-(centre_d / 18_000.0) ** 2)).astype(np.float32)

# ---- Synthetic fault segments (Basin-and-Range NNE strike) -----------------
n_segments = 170
lengths_km = rng.uniform(3.0, 14.0, n_segments)
azimuths = np.deg2rad(rng.normal(20.0, 25.0, n_segments))  # NNE-SSW
sigmas = rng.uniform(150.0, 350.0, n_segments)           # Gaussian width (m)
amps = rng.uniform(0.45, 0.75, n_segments)

segments = []  # (x0, y0, x1, y1, sigma, amp, endpoints)
for i in range(n_segments):
    cx = float(rng.uniform(xs.min() + 5_000, xs.max() - 5_000))
    cy = float(rng.uniform(ys.min() + 5_000, ys.max() - 5_000))
    L = float(lengths_km[i]) * 1000.0
    az = float(azimuths[i])
    dx, dy = np.sin(az), np.cos(az)  # UTM: x=easting, y=northing
    x0, y0 = cx - dx * L / 2, cy - dy * L / 2
    x1, y1 = cx + dx * L / 2, cy + dy * L / 2
    segments.append((x0, y0, x1, y1, float(sigmas[i]), float(amps[i]), ((x0, y0), (x1, y1))))

# rasterize each segment as Gaussian-smoothed distance to the line segment
# (vectorized over the full grid: n_segments x NY x NX)
P = np.stack([XX.ravel(), YY.ravel()], axis=1)  # (n_pix, 2)
for (x0, y0, x1, y1, sigma, amp, _) in segments:
    a = np.array([x0, y0]); b = np.array([x1, y1])
    ab = b - a
    L2 = float(ab @ ab)
    t = np.clip(((P - a) @ ab) / L2, 0.0, 1.0)
    proj = a[None, :] + t[:, None] * ab[None, :]
    d2 = np.sum((P - proj) ** 2, axis=1).reshape(NY, NX)
    prior += (amp * np.exp(-d2 / (2.0 * sigma ** 2))).astype(np.float32)

# ---- Dilatational stepover boost: segment endpoint pairs < 2 km apart ------
endpoints = np.array([s[6] for s in segments], dtype=float)  # (n, 2, 2)
pts = endpoints.reshape(-1, 2)
who = np.repeat(np.arange(n_segments), 2)
boost = np.zeros((NY, NX), dtype=np.float32)
for i in range(n_segments):
    for j in range(i + 1, n_segments):
        dij = np.hypot(pts[who == i][:, None, 0] - pts[who == j][None, :, 0],
                       pts[who == i][:, None, 1] - pts[who == j][None, :, 1])
        d = float(dij.min())
        if d < 2000.0:  # stepover / relay candidate
            ii, jj = np.unravel_index(np.argmin(dij), dij.shape)
            p_i = pts[who == i][ii]
            p_j = pts[who == j][jj]
            mx, my = 0.5 * (p_i[0] + p_j[0]), 0.5 * (p_i[1] + p_j[1])
            d2 = (XX - mx) ** 2 + (YY - my) ** 2
            boost += (0.85 * np.exp(-d2 / (2.0 * (600.0) ** 2))).astype(np.float32)

prior = prior + boost
prior = np.clip(prior, 0.0, 1.0).astype(np.float32)

# ---- Write submission ------------------------------------------------------
out_dir = Path("submissions")
out_dir.mkdir(parents=True, exist_ok=True)
out_name = f"korea8-h1-stepover-relay-prior-{TIMESTAMP}-seed{SEED:06x}.tif"
out_path = out_dir / out_name

report = write_submission(
    prior, out_path,
    crs="EPSG:32611", transform=transform, nodata=None, compress="deflate",
)
report["submission_name"] = out_name
report["note"] = ("Unique stepover-relay structural prior; format-valid template — "
                  "regrid to official training geometry before scoring.")
assert len(report["note"]) <= 140, "note too long for submission form"
report["grid_illustrative"] = True
report["data_required"] = ("training_features.tif / labels.tif from DrivenData (login required) "
                           "to conform geometry and validate on holdout")
report["sha256"] = hashlib.sha256(out_path.read_bytes()).hexdigest()
report["generated_utc"] = datetime.now(timezone.utc).isoformat()
report["hypothesis"] = "H1 dilatational stepover / relay-ramp structural prior"
report["ok_to_download"] = True
report["ok_to_submit_as_is"] = False
report["reason"] = ("Not conformed to official training CRS/shape/transform "
                    "(unavailable without DrivenData login); not holdout-validated.")

print(json.dumps(report, indent=2))

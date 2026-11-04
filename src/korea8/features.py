"""Candidate-specific geophysical feature planes (Korea8 lane).

These are static raster transforms of the 19-band competition stack plus
catalogue-derived context that is rebuilt from *visible* faults only inside a
holdout fold.  Nothing here reads the hidden truth mask.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

# Band indices are 1-based in the TIFF; cache is 0-based.
BANDS = {
    "mag_anom": 1, "rtp": 2, "tmi_hg": 3, "geod_2ndinv": 4,
    "iso_grav_anom_slope": 5, "tc": 6, "geod_shearrate": 7, "geod_dilaterate": 8,
    "tmi_vg": 9, "deq_n100a15": 10, "iso_grav_anom_vg": 11, "det_elev": 12,
    "iso_grav_anom": 13, "tmi": 14, "depth_to_base_surf": 15, "ieq_n100a15": 16,
    "cond_surf": 17, "iso_grav_anom_hg": 18, "det_elev_slope": 19,
}

# Accommodation-transfer / buried-lineament lane: range-front relief, gravity
# saddle, basement-depth curvature, and strain-to-seismicity decoupling.
STATIC_BANDS = (12, 13, 15, 17, 2, 14, 4, 7, 10, 16)


def _z(a: np.ndarray, valid: np.ndarray) -> np.ndarray:
    v = a[valid]
    if v.size == 0:
        return np.zeros_like(a)
    mu, sd = float(v.mean()), float(v.std())
    sd = sd if sd > 1e-12 else 1.0
    return ((a - mu) / sd).astype(np.float32)


def gradient_mag(a: np.ndarray, sigma: float) -> np.ndarray:
    gx = ndi.gaussian_filter(a, sigma, order=(0, 1))
    gy = ndi.gaussian_filter(a, sigma, order=(1, 0))
    return np.hypot(gx, gy).astype(np.float32)


def ridge(a: np.ndarray, sigma: float) -> np.ndarray:
    """Maximum Hessian eigenvalue: lineament/ridge response."""
    gy = ndi.gaussian_filter(a, sigma, order=(1, 0))
    gx = ndi.gaussian_filter(a, sigma, order=(0, 1))
    gyy = ndi.gaussian_filter(a, sigma, order=(2, 0))
    gxx = ndi.gaussian_filter(a, sigma, order=(0, 2))
    gxy = ndi.gaussian_filter(a, sigma, order=(1, 1))
    tr = gxx + gyy
    det = gxx * gyy - gxy * gxy
    disc = np.sqrt(np.maximum(tr * tr - 4 * det, 0.0))
    lam1 = 0.5 * (tr + disc)
    return lam1.astype(np.float32)


def local_relief(a: np.ndarray, size: int = 5) -> np.ndarray:
    return (ndi.maximum_filter(a, size=size) - ndi.minimum_filter(a, size=size)).astype(np.float32)


def build_static(stack: np.ndarray, footprint: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """Return (H,W,F) float32 planes and names. stack is (H,W,19)."""
    planes, names = [], []

    def add(name: str, arr: np.ndarray) -> None:
        planes.append(np.where(footprint, arr, 0.0).astype(np.float32))
        names.append(name)

    for b in STATIC_BANDS:
        a = stack[:, :, b - 1].astype(np.float32)
        z = _z(a, footprint)
        add(f"b{b:02d}_z", z)
        add(f"b{b:02d}_grad1", _z(gradient_mag(a, 1.0), footprint))
        add(f"b{b:02d}_grad2", _z(gradient_mag(a, 2.0), footprint))
        if b in (12, 13, 15):
            add(f"b{b:02d}_ridge2", _z(ridge(a, 2.0), footprint))
    elev = stack[:, :, 11].astype(np.float32)
    add("elev_relief5", _z(local_relief(elev, 5), footprint))
    grav = stack[:, :, 12].astype(np.float32)
    depth = stack[:, :, 14].astype(np.float32)
    cond = stack[:, :, 16].astype(np.float32)
    strain = stack[:, :, 3].astype(np.float32)
    deq = stack[:, :, 9].astype(np.float32)
    add("conductance", _z(cond * depth, footprint))
    add("strain_quake_ratio", _z(strain / (deq + 1.0), footprint))
    return np.stack(planes, axis=-1), names


def catalogue_context(visible: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """Per-fold context derived ONLY from visible catalogue pixels."""
    dist = ndi.distance_transform_edt(~visible).astype(np.float32)
    yy, xx = np.mgrid[-5:6, -5:6]
    k = ((yy * yy + xx * xx) <= 25).astype(np.float32)
    dens = ndi.convolve(visible.astype(np.float32), k, mode="constant")
    planes = np.stack([
        dist,
        np.log1p(dist),
        dens,
        ((dist > 3) & (dist <= 10)).astype(np.float32),
        ((dist > 10) & (dist <= 30)).astype(np.float32),
    ], axis=-1)
    names = ["dist_visible", "log_dist_visible", "vis_density5", "annulus3_10", "annulus10_30"]
    return planes, names

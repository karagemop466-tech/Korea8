#!/usr/bin/env python3
"""Recompute nine-site format, holdout, lineage and directed-overlap evidence."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import numpy as np
import rasterio
from scipy import ndimage
from scipy.stats import spearmanr
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from gems32 import holdout  # noqa: E402

DATA = ROOT/'data'
FILES = ROOT/'registry/focus9'
SCORES = {'GEMSDOE24':0.2477,'GEMSDOE25':0.2600,'GEMSDOE27':0.2449,
          'GEMSDOE28':0.2710,'GEMSDOE30':0.2600,'GEMSDOE31':0.2708,
          'GEMSDOE32':0.2778,'GEMSDOE33':0.2632,'GEMSDOE36':0.2750}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path: Path):
    with rasterio.open(path) as ds:
        a = ds.read(1)
        grid = (ds.crs, ds.shape, ds.transform)
    return a, grid

def main() -> int:
    paths = {p.name.split('-')[0]:p for p in FILES.glob('*.tif')}
    if set(paths) != set(SCORES):
        raise ValueError(f'focus site mismatch: {set(paths)}')
    sample, grid = read(DATA/'sample_submission.tif')
    foot = np.isfinite(sample)
    labels, label_grid = read(DATA/'labels.tif')
    if label_grid != grid:
        raise ValueError('labels grid mismatch')
    catalogue = (labels == 1) & foot
    arrays, grids, dots, profiles = {}, {}, {}, {}
    for site, path in paths.items():
        arrays[site], grids[site] = read(path)
        with rasterio.open(path) as src:
            profiles[site] = {'count':src.count, 'dtype':src.dtypes[0]}
        if grids[site] != grid:
            raise ValueError(f'{site}: grid mismatch')
        if not np.isfinite(arrays[site][foot]).all():
            raise ValueError(f'{site}: nonfinite inside footprint')
        dots[site] = foot & (arrays[site] > 0)
    sites = sorted(SCORES)
    matrix = {s:{} for s in sites}
    for target in sites:
        distance = ndimage.distance_transform_edt(~dots[target])
        for source in sites:
            matrix[source][target] = float((distance[dots[source]] <= 3.0).mean())
    ctx = holdout.load_holdout_context(DATA)
    rows = []
    for site in sites:
        arr = arrays[site]
        hide = holdout.evaluate_hide_and_recover(dots[site], ctx, name=site)
        hide = {k:v for k,v in hide.items() if not k.startswith('_')}
        sg = holdout.evaluate_sgmc_with_ci(dots[site], ctx, name=site)
        sg = {k:v for k,v in sg.items() if not k.startswith('_')}
        other = {k:v for k,v in matrix[site].items() if k != site}
        worst = max(other, key=other.get)
        full_finite = bool(np.isfinite(arr).all())
        rows.append({
            'site':site, 'historical_file':paths[site].name, 'sha256':sha(paths[site]),
            'user_reported_score':SCORES[site],
            'score_evidence':'USER-REPORTED; no submission-page receipt inspected',
            'leaderboard_score_estimate':None,
            'emitted_dots':int(dots[site].sum()),
            'on_catalogue_dots':int((dots[site]&catalogue).sum()),
            'format':{'single_band_float32':profiles[site]['count']==1 and profiles[site]['dtype']=='float32','grid_match':True,
                      'inside_footprint_finite_range_0_1':bool(((arr[foot]>=0)&(arr[foot]<=1)).all()),
                      'full_grid_finite_range_0_1':bool(full_finite and ((arr>=0)&(arr<=1)).all()),
                      'outside_convention':'NaN outside is officially allowed; full-grid finite is a separate conservative portal-range preflight'},
            'holdout_dti':{'score_label':'HOLDOUT-DTI','evaluator_version':hide['evaluator_version'],
                           'pooled_dti':hide['pooled_dti'],'ci95':hide['ci95_cluster_bootstrap'],
                           'withheld_positives':hide['n_withheld_positives'],
                           'spatial_clusters':hide['n_spatial_clusters'],'bootstrap_reps':hide['n_bootstrap_reps']},
            'sgmc_off_catalogue':sg,
            'max_directed_overlap_3px':{'other_site':worst,'fraction':other[worst]},
            'unique_vs_other_focus':other[worst] <= 0.70,
            'ok_to_download_and_submit':False,
            'reason':'Historical near-duplicate and no new-lane/selector clearance; never resubmit as a new discovery'
        })
        print(site, f"holdout={hide['pooled_dti']:.9f}", f"worst={worst}:{other[worst]:.4f}", flush=True)
    baseline = max(r['holdout_dti']['pooled_dti'] for r in rows)
    score_values = [r['user_reported_score'] for r in rows]
    holdout_values = [r['holdout_dti']['pooled_dti'] for r in rows]
    rho = spearmanr(score_values, holdout_values)
    out = {'schema':'korea8.focus9-audit.v1','scope':'Nine highest user-supplied focus-site submissions only',
           'no_organizer_receipt':True,'current_leaderboard_verified':False,
           'holdout_baseline_max':baseline,
           'score_vs_holdout_spearman':{'rho':float(rho.statistic),'p_value':float(rho.pvalue),'n':9,
                                        'caveat':'Descriptive only; not a leaderboard calibration'},
           'directed_overlap_3px':matrix,'rows':rows}
    (ROOT/'docs/data').mkdir(parents=True,exist_ok=True)
    (ROOT/'docs/data/focus9.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/focus9-holdout-recomputed.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')

    # Pixel-exact lineage of the reported GEMSDOE32 leader; no causal hidden-label claim.
    d28 = dots['GEMSDOE25']
    base = dots['GEMSDOE31']
    b2 = dots['GEMSDOE32']
    distance = ndimage.distance_transform_edt(~catalogue)
    expected_base = d28 & (distance > 1.0)
    expected_b2 = d28 & (distance > 2.0)
    lineage = {
        'schema':'korea8.gemsdoe32-lineage.v1',
        'evidence_boundary':'Measured set algebra from public mirror bytes. User-reported scores are not receipts; private test labels are unavailable, so causation is unproven.',
        'official_known_fault_mask':'https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516',
        'measured':{
            'd28_dots':int(d28.sum()),'base31_dots':int(base.sum()),'b2_dots':int(b2.sum()),
            'd28_on_catalogue_dots':int((d28&catalogue).sum()),
            'base31_on_catalogue_dots':int((base&catalogue).sum()),
            'b2_on_catalogue_dots':int((b2&catalogue).sum()),
            'base31_is_strict_subset_of_d28':bool((base&~d28).sum()==0 and (d28&~base).sum()>0),
            'base31_equals_d28_beyond_1px_catalogue':bool(np.array_equal(base,expected_base)),
            'd28_to_base31_removed_dots':int((d28&~base).sum()),
            'b2_equals_d28_beyond_2px_catalogue':bool(np.array_equal(b2,expected_b2)),
            'b2_is_strict_subset_of_base31':bool((b2&~base).sum()==0 and (base&~b2).sum()>0),
            'd28_to_b2_removed_dots':int((d28&~b2).sum()),
            'base31_to_b2_removed_dots':int((base&~b2).sum()),
            'removed_equals_base31_within_2px':bool(np.array_equal(base&~b2,base&(distance<=2.0))),
            'b2_min_distance_to_catalogue_px':float(distance[b2].min()),
            'b2_fraction_within_3px_of_d28':float((ndimage.distance_transform_edt(~d28)[b2]<=3).mean())},
        'user_reported':{'GEMSDOE25':0.2600,'GEMSDOE31':0.2708,'GEMSDOE32':0.2778,
                         'd28_to_base31_delta':0.0108,'base31_to_b2_delta':0.0070},
        'interpretation':'No dots are added along this lineage. D2.8 already has zero on-catalogue dots; GEMSDOE31 exactly removes D2.8 pixels at catalogue distance <=100 m, and B2 exactly removes D2.8 pixels at distance <=200 m. Under distance-weighted Tversky DTI this can reduce low-credit false-positive mass while preserving off-catalogue coverage. The private-label effect is not observable here.',
        'marginal_credit_identity':{'alpha':0.2,'reported_dti':0.2778,'alpha_times_reported_dti':0.2*0.2778,
                                    'warning':'Idealized isolated-pixel intuition only; not a score estimate or general update rule'},
        'can_we_beat_02778':'UNKNOWN without a new organizer receipt. E1 did not clear the holdout or literal uniqueness gates.'
    }
    (ROOT/'evidence/champion-lineage.json').write_text(json.dumps(lineage,indent=2,allow_nan=False)+'\n')
    print(json.dumps(lineage['measured'],indent=2),flush=True)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

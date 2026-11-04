#!/usr/bin/env python3
"""Independent line-by-line delivery verification, including deliberate bad inputs."""
from __future__ import annotations
import hashlib, json, math, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import rasterio
from scipy import ndimage
from scipy.spatial import cKDTree
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from gems32.submission import audit_geotiff  # noqa: E402
DATA=ROOT/'data'
checks=[]

def record(name, passed, detail):
    checks.append({'check':name,'passed':bool(passed),'detail':detail})
    print(('PASS' if passed else 'FAIL'),name,'—',detail,flush=True)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def finite_json(x):
    if isinstance(x,float): return math.isfinite(x)
    if isinstance(x,dict): return all(finite_json(v) for v in x.values())
    if isinstance(x,list): return all(finite_json(v) for v in x)
    return True

def main():
    card=json.loads((ROOT/'run-card.json').read_text())
    focus=json.loads((ROOT/'docs/data/focus9.json').read_text())
    lineage=json.loads((ROOT/'evidence/champion-lineage.json').read_text())
    lattice_evidence=json.loads((ROOT/'registry/witness/lattice_feasibility.json').read_text())
    record('JSON values finite',all(finite_json(x) for x in (card,focus,lineage)),'No NaN/Infinity in machine-readable claims')

    manifest=json.loads((ROOT/'registry/inputs.json').read_text())
    bad=[]
    for entry in manifest['files']:
        p=ROOT/entry['dest']
        if not p.exists() or sha(p)!=entry['sha256']: bad.append(entry['dest'])
    record('Pinned input hashes',not bad,f"{len(manifest['files'])-len(bad)}/{len(manifest['files'])} verified; bad={bad}")
    bad=[]
    for line in (ROOT/'registry/shared_tools.sha256').read_text().splitlines():
        digest,path=line.split('  ',1)
        if sha(ROOT/path)!=digest: bad.append(path)
    record('Shared tools unchanged',not bad,f'Hash mismatches: {bad}')

    candidate=ROOT/card['research_raster']
    with rasterio.open(DATA/'sample_submission.tif') as ds:
        grid=(ds.crs,ds.shape,ds.transform); foot=np.isfinite(ds.read(1))
    with rasterio.open(DATA/'labels.tif') as ds:
        labels=(ds.read(1)==1)&foot
    with rasterio.open(candidate) as ds:
        candidate_grid=(ds.crs,ds.shape,ds.transform)
        arr=ds.read(1); profile=ds.profile.copy(); count=ds.count; dtypes=ds.dtypes
    dots=foot&(arr>0)
    record('Candidate SHA-256 identity',sha(candidate)==card['raster_sha256'],card['raster_sha256'])
    record('Exact grid/band/dtype',candidate_grid==grid and count==1 and dtypes==('float32',),f'{candidate_grid[0]} {candidate_grid[1]} {count} {dtypes}')
    record('Full-grid finite range',bool(np.isfinite(arr).all() and ((arr>=0)&(arr<=1)).all()),f'{np.isfinite(arr).sum():,}/{arr.size:,} finite; min={arr.min()} max={arr.max()}')
    record('Known-fault leakage',not (dots&labels).any(),f'{int((dots&labels).sum())} on-catalogue dots')
    coords=np.argwhere(dots)
    minsep=float(cKDTree(coords).query(coords,k=2)[0][:,1].min())
    record('Final dot count and separation',len(coords)==37084 and minsep>=3.2,f'{len(coords):,} dots; minimum {minsep:.9f} px')
    audit=audit_geotiff(candidate,foot,labels,mode='zeros',template_tif=DATA/'sample_submission.tif')
    record('Independent shared-writer audit',audit['all_checks_passed'],f"{len(audit['checks'])} checks passed")

    lattice_path=ROOT/'registry/witness/13gems_20261001_r13-lattice-s5_v2_nan-outside.tif'
    with rasterio.open(lattice_path) as ds:
        lattice=foot&(ds.read(1)>0)
    distance=ndimage.distance_transform_edt(~lattice)
    overlap=float((distance[dots]<=3).mean())
    row=next(r for r in card['registry']['final'] if r['site']=='13GEMSDOE')
    record('Literal lattice duplicate gate',overlap>0.70 and np.isclose(overlap,row['final_dot_overlap_within_3px'],atol=1e-12),f'{overlap:.12%} > 70%; verdict must be negative')
    coverage=float((foot&(distance<=3)).sum()/foot.sum())
    record('Lattice coverage feasibility',np.isclose(coverage,lattice_evidence['footprint_coverage_fraction'],atol=1e-12) and lattice_evidence['footprint_uncovered_cells']==6649,f'{coverage:.12%}; only 6,649 uncovered cells; no hole targeting')
    self_overlap=float((distance[lattice]<=3).mean())
    record('Duplicate negative control',self_overlap==1.0,'Submitting the lattice itself would produce 100% overlap and stop')

    h=card['holdout_dti']
    record('HOLDOUT provenance tuple',h['score_label']=='HOLDOUT-DTI' and h['evaluator_version']=='GEMSDOE32-HIDE-RECOVER-v3.0' and h['withheld_positives']==22232 and len(h['ci95'])==2 and h['bootstrap_reps']==1000,f"{h['pooled_dti']:.12f} CI {h['ci95']}")
    record('Baseline not beaten',not h['beats_baseline'] and h['pooled_dti']<focus['holdout_baseline_max'],f"{h['pooled_dti']:.12f} < {focus['holdout_baseline_max']:.12f}")
    record('No fabricated organizer score',card['organizer_confirmed_score'] is None and card['leaderboard_score_estimate'] is None,'Both organizer-confirmed score and leaderboard estimate are null')
    record('Fail-closed verdict',card['verdict']=='negative' and not card['ok_to_download_and_submit'] and not card['weekly_slot_used'],'negative; research only; slot unused')
    record('Scoped uniqueness disclosed',not card['registry']['registry_complete'] and not card['registry']['unique_submission_unlike_all_previous'],'Ten-raster scope is not global uniqueness')
    record('Lane and selector not invented','not supplied' in card['lane'] and not card['separate_selector_approved'],card['lane'])
    record('Provenance limitation gated',not card['provenance']['organizer_authenticated_inputs'] and not card['provenance']['external_derivative_license_verified'],'Mirror authentication/derivative license not claimed')
    record('Submission note',len(card['submission_note'])<=140 and 'RESEARCH ONLY' in card['submission_note'],f"{len(card['submission_note'])} characters: {card['submission_note']}")
    record('Leakage canary below alarm',not card['leakage_canary']['any_leakage_alarm'] and max(r['orientation_free_auc'] for r in card['leakage_canary']['features'])<0.9,'All features <0.90; not a validity proof')
    premax=max(r['surface_spearman_rho'] for r in card['registry']['preplacement'])
    record('Pre-placement rank gate',premax<0.9 and not any(r['preplacement_duplicate'] for r in card['registry']['preplacement']),f'maximum rho={premax:.9f}')
    focus_rows=card['registry']['final'][:-1]
    record('Focus-only overlap is not global uniqueness',all(r['final_dot_overlap_within_3px']<=0.7 for r in focus_rows) and overlap>0.7,'Nine focus rasters pass, literal lattice fails')

    record('Nine-site count and labels',len(focus['rows'])==9 and all(r['score_evidence'].startswith('USER-REPORTED') and r['holdout_dti']['score_label']=='HOLDOUT-DTI' and not r['ok_to_download_and_submit'] for r in focus['rows']),'9 user-reported rows; all ineligible')
    record('Nine-site near duplicates',all(r['max_directed_overlap_3px']['fraction']>0.7 for r in focus['rows']),'Every focus row exceeds 70% with another focus raster')
    measured=lineage['measured']
    lineage_ok=(measured['base31_equals_d28_beyond_1px_catalogue'] and measured['b2_equals_d28_beyond_2px_catalogue'] and measured['b2_is_strict_subset_of_base31'] and measured['base31_to_b2_removed_dots']==2545 and measured['b2_dots']==37654)
    record('Champion lineage exact',lineage_ok,'D2.8 >100 m = 40,199; D2.8 >200 m = 37,654; 2,545 second-stage removals')
    record('Champion score not a receipt',lineage['user_reported']['GEMSDOE32']==0.2778 and card['organizer_confirmed_score'] is None,'0.2778 remains user-reported; private-label causation unproven')

    readme=(ROOT/'README.md').read_text(); site=(ROOT/'docs/index.html').read_text(); sources=(ROOT/'docs/sources.md').read_text()
    for name,text in [('README',readme),('Pages site',site)]:
        required=['NEGATIVE',card['raster_sha256'],f'{100*overlap:.4f}%','0.041593697','0.096743304','No leaderboard estimate' if name=='Pages site' else 'Leaderboard score estimate']
        record(f'{name} decision consistency',all(x in text for x in required) and FILENAME_OK(text,card),f'Negative verdict, score, lattice overlap, hash and research filename present')
    record('Official sources and license limits',all(x in sources for x in ['drivendata.org','sciencebase.gov','usgs.gov/3d-elevation-program','gdr.openei.org','did not expose a recognized license file']),'Competition/USGS/DOE links plus mirror limitation')
    import re
    local_links=[x for x in re.findall(r'href="([^"]+)"',site) if not x.startswith(('http://','https://','#','mailto:'))]
    broken=[x for x in local_links if not (ROOT/'docs'/x).exists()]
    record('Static assets and browser independence',not broken and 'localhost' not in site and '127.0.0.1' not in site,f'{len(local_links)} relative links resolve; broken={broken}; no localhost dependency')

    # Deliberately corrupt saved bytes and prove the unchanged shared validator rejects them.
    with tempfile.TemporaryDirectory(prefix='korea8-verify-') as td:
        zero_locations=np.argwhere(foot&(arr==0))
        y,x=zero_locations[0]
        mutated=arr.copy(); mutated[y,x]=1.5
        path=Path(td)/'range-failure.tif'
        with rasterio.open(path,'w',**profile) as dst: dst.write(mutated,1)
        try:
            audit_geotiff(path,foot,labels,mode='zeros',template_tif=DATA/'sample_submission.tif')
            range_rejected=False; message='validator accepted out-of-range value'
        except ValueError as exc:
            message=str(exc); range_rejected='in_footprint_range_0_1' in message and 'validator_range_0_1_guaranteed' in message
        record('Range mutation negative control',range_rejected,message)
        y,x=np.argwhere(labels)[0]
        mutated=arr.copy(); mutated[y,x]=1.0
        path=Path(td)/'catalogue-failure.tif'
        with rasterio.open(path,'w',**profile) as dst: dst.write(mutated,1)
        try:
            audit_geotiff(path,foot,labels,mode='zeros',template_tif=DATA/'sample_submission.tif')
            catalogue_rejected=False; message='validator accepted catalogue leakage'
        except ValueError as exc:
            message=str(exc); catalogue_rejected='zero_on_catalogue_leakage' in message
        record('Catalogue mutation negative control',catalogue_rejected,message)

    out={'schema':'korea8.delivery-verification.v1','generated_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
         'all_passed':all(c['passed'] for c in checks),'n_checks':len(checks),'checks':checks}
    (ROOT/'evidence/delivery-verification.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    (ROOT/'docs/data/verification.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(f"VERIFICATION {'PASS' if out['all_passed'] else 'FAIL'}: {sum(c['passed'] for c in checks)}/{len(checks)}",flush=True)
    return 0 if out['all_passed'] else 1

def FILENAME_OK(text,card):
    return Path(card['research_raster']).name in text

if __name__=='__main__':
    raise SystemExit(main())

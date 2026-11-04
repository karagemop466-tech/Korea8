# Executive summary — Korea8 session (2026-11-04)

## Verdict: NEGATIVE / DO-NOT-SUBMIT

A new single-band GeoTIFF was generated (`docs/downloads/korea8_candidate.tif`,
SHA-256 `328804…` → see run card for the current hash, 8,316 dots, 852 KB). It is
**not** a copy of any prior submission. It passes the format gate and is unique
versus the nine focus sites, but it fails the literal uniqueness gate against the
`r13-lattice-s5` covering witness and underperforms the distance-only control on
spatially blocked holdout. No submission slot was spent.

## Requested sites (USER-REPORTED scores; no organizer receipts)

| Site | Score | Dots | Mechanism | Uniqueness |
|---|---|---|---|---|
| GEMSDOE24 | 0.2477 | 60,069 | nan-outside dot family | near-duplicate |
| GEMSDOE25 | 0.2600 | 44,090 | d28 dot family | near-duplicate |
| GEMSDOE27 | 0.2449 | 61,328 | nan-outside dot family | near-duplicate |
| GEMSDOE28 | 0.2710 | 37,660 | rung30 blind | near-duplicate |
| GEMSDOE30 | 0.2600 | 44,090 | poisson300m off-cat d28 | near-duplicate |
| GEMSDOE31 | 0.2708 | 40,199 | solo-d28 | near-duplicate |
| GEMSDOE32 | 0.2778 | 37,654 | h33-h33-2-b2 zeros (subset of 25) | near-duplicate |
| GEMSDOE33 | 0.2632 | 41,865 | analog-tip-stepover-r30 | near-duplicate |
| GEMSDOE36 | 0.2750 | 38,854 | anderson-geothermal-pinn | near-duplicate |
| **Korea8** | **0.0219 HOLDOUT-DTI** | **8,316** | H1 accommodation-transfer lineaments | unique vs focus9; fails lattice |

## Why GEMSDOE32 reported 0.2778

Strict subset of GEMSDOE25's 44,090 dots minus 6,436 zero-credit dots 1–2 px from
the catalogue. For a binary map `DTI = TP/(0.2·D + 0.8·N)`; deleting zero-credit
mass strictly raises the score. Dot-pruning arithmetic, not hidden-fault skill.

## Is a higher-scoring distinct strategy supported?

**Not by this session.** The pre-registered H1 candidate scored HOLDOUT-DTI 0.0219
(CI 0.0177–0.0261), below the distance-only control (0.0460) and random (0.0344).
Catalogue-fit holdout is not a leaderboard proxy (staff mask known faults; sibling
measured HIDE-RECOVER ↔ leaderboard ρ≈+0.143), so even a holdout win would not
establish a leaderboard win. The literal uniqueness gate is unsatisfiable for any
dense candidate because of the covering witness.

## What was fixed

- Portal range error `"Predicted values must be in range [0, 1]"`: finite [0,1]
  data band + GDAL internal mask band declaring outside-footprint cells null.
- Data acquisition: hash-verified public Dropbox mirrors restored on GitHub
  Actions (sandbox cannot reach Dropbox; original GitHub mirrors deleted).
- Shared-tool reuse: exact `vendor/gems57` bytes; no private forks.

## Remaining work

See `knowledge/limitations.md`. Key items: authenticated leaderboard scrape,
owner-scope decision on the covering witness, block-inversion overlap projection
for a calibrated leaderboard estimate, and H2–H5 with external GeoDAWN K/Th/U.

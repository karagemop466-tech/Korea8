# Why did GEMSDOE32 reportedly lead, and can 0.2778 be beaten?

## What is actually measured

`0.2778` is **USER-REPORTED**, not `ORGANIZER-CONFIRMED`: no DrivenData submission receipt was available. The current overall leader is also unverified; the two supplied claims, 0.4413 and 0.3195, conflict and are not repeated as fact.

The public mirror bytes nevertheless permit an exact set-algebra audit. Let `d` be Euclidean distance in pixels to the known-fault catalogue (1 px = 100 m):

| Historical stage | Dots | Exact measured relation to GEMSDOE25 D2.8 | User-reported score |
|---|---:|---|---:|
| GEMSDOE25 / 30, D2.8 | 44,090 | Base set; zero on-catalogue dots | 0.2600 |
| GEMSDOE31, H27.4 | 40,199 | Exactly D2.8 pixels with `d > 1`; removes 3,891 dots | 0.2708 |
| GEMSDOE32, B2 | 37,654 | Exactly D2.8 pixels with `d > 2`; removes another 2,545 dots from GEMSDOE31 | 0.2778 |

B2 adds no dots. Its minimum distance to the catalogue is √5 = 2.236 px. All B2 dots are within 3 px of D2.8 because B2 is its strict subset. An older broad description of GEMSDOE31 as merely “off catalogue” was imprecise: D2.8 was already off catalogue; the exact extra operation is the 100 m collar exclusion. This is now regression-tested.

## Plausible metric mechanism, not hidden-truth causation

DrivenData staff states that known USGS/INGENIOUS fault pixels are masked/excluded during initial scoring and final reevaluation. DTI also gives reduced credit with distance from a target. Removing catalogue-adjacent predictions can therefore reduce low-credit false-positive mass while retaining predictions farther away that cover new targets. This is consistent with pruning improving a score without adding any geological discovery.

It does **not** prove that the private labels caused the reported increases. The private test labels and receipts are unavailable. For an idealized isolated pixel, the inclusion credit bar at DTI `s` is `alpha*s = 0.2*0.2778 = 0.05556`; that identity is not a prediction of the score change and is not a general rule for partially covered fields.

## Why the holdout tells a different story

On the shared whole-fault-segment holdout, GEMSDOE32 has HOLDOUT-DTI **0.0045153787** (95% CI `[0.0038164176, 0.0052615983]`, 22,232 withheld positives, evaluator `GEMSDOE32-HIDE-RECOVER-v3.0`). GEMSDOE25/30 instead lead the nine-site holdout at **0.0967433040**.

Across these nine selected, user-reported rows, score versus HOLDOUT-DTI has descriptive Spearman ρ **−0.848739**, p=0.00381. This is not a leaderboard calibration and does not establish causality. It is a warning that optimizing catalogue-collar pruning under known-fault masking can diverge sharply from recovering hidden whole fault segments.

E1 scored HOLDOUT-DTI **0.0415936971** (95% CI `[0.0338515507, 0.0493925969]`): above GEMSDOE32 on this diagnostic, but below the focus baseline and without any leaderboard interpretation. Its secondary SGMC prevalence-calibrated diagnostic is 0.0941027873 (95% CI `[0.0784531981, 0.1092398165]`, 62,703 positives), which is interesting but cannot override the primary gate.

## Can it be beaten?

**Unknown; E1 did not establish that it can.** A genuine future candidate would need a unique lane, holdout improvement, full-registry clearance and a new organizer receipt. E1 fails the literal 13GEMSDOE duplicate gate at 99.1964% and the holdout baseline. No score projection or submission is offered. Scientifically, moving away from catalogue-distance pruning toward independently supported off-catalogue targets remains the relevant direction, but this run is not evidence of a leaderboard win.

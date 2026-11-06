# DATA_DICTIONARY.md — `data/tub/*.json`

Every page on the site is generated from these eight files by `scripts/build_tub_site.py`.
No value reaches the site any other way, and `scripts/verify_tub_site.py` fails the build if a
referenced source ID does not exist, if a table row has no source cell, or if a data count does not
match the rendered row count.

Common conventions

| Field | Meaning |
|---|---|
| `source_ids` | Array of IDs from `sources.json`. Never empty unless the row is explicitly unverified. |
| `evidence_label` | `OFFICIAL` (government/statute/regulator) · `USER-REPORTED` (owner-supplied, no document) · `MIXED` · `INFERENCE` |
| blank / `null` | Not stated by any source. Renders as an amber "Not stated" cell. Never guessed. |

---

## `sources.json` → `sources[]`

| Field | Type | Notes |
|---|---|---|
| `id` | `"S01"…"S45"` | Referenced by every other file |
| `official` | bool | `true` only for government, statute, or the licensing regulator |
| `self_published` | bool | The business's own site; used for scope claims only, never licence status |
| `third_party` | bool | Directory/aggregator; used for discovery only, never as verification |
| `publisher` | string | Issuing body |
| `title` | string | Document title |
| `url` | https string | The exact URL fetched |
| `used_for` | string | What claim this source is allowed to support |

## `requirements.json` → `requirements[]`

| Field | Type | Notes |
|---|---|---|
| `id` | `R1…R16` | |
| `category` | string | Scope / Access / Licensing / One-stop / Permit / Tenancy / Habitability / Cost / Vendor / Contract / Lead / Insurance / Timing / Documentation |
| `requirement` | string | The need as stated |
| `why` | string | Why it matters |
| `how_addressed` | string | How the shortlist or scope meets it |
| `verification_state` | enum | `verified` · `partial` · `unverified` |
| `note` | string | Caveat, or a pointer to the flagged item |
| `source_ids` | array | |

## `vendors.json` → `vendors[]`

Licence fields are transcribed from the CSLB `LicenseDetail` page. Nothing here is from marketing.

| Field | Type | Notes |
|---|---|---|
| `id` | `V01…V13` | |
| `licence` | string | CSLB licence number, digits only, as printed |
| `entity` | string | Sole Ownership / Corporation / Ltd Liability |
| `address`, `phone` | string | As printed by CSLB (including the "POTRAL" typo on #1024971 — see flagged I-02) |
| `status` | string | CSLB's own status sentence |
| `classifications` | array | Copied verbatim, e.g. `C36 - PLUMBING` |
| `issue_date`, `expire_date` | `MM/DD/YYYY` | |
| `bond`, `workers_comp`, `liability_insurance` | string | Insurer, policy/number, amount, effective dates |
| `gates_met`, `gates_missed` | array | Subset/complement of `G1…G6` in `fit_rubric` |
| `rank` | int | 1 = best fit. `0` = excluded, reason in `why` |
| `why` | string | The reason for the rank in one paragraph |
| `open_question` | string? | What to ask by phone. Absent if nothing |
| `source_ids` | array | Always includes the official CSLB record |

`rating` and `review_count` do **not** exist as fields. They were deliberately not modelled because
Yelp returned HTTP 403 and no verified value could be obtained.

## `estimates.json`

| Field | Type | Notes |
|---|---|---|
| `estimates[].amount_usd` | number | Exactly as written in the brief |
| `estimates[].amount_as_written` | string | `"$614"` etc., preserved |
| `estimates[].stated_scope_as_written` | string | Quoted from the brief |
| `estimates[].includes_labour_and_materials`, `open_wall_work_included`, `drywall_repair_included`, `permit_included` | string or null | `null` where the brief is silent → renders blank |
| `estimates[].licence_verified` | string | Pairs each quote with its CSLB check |
| `estimates[].evidence_label` | string | Always `USER-REPORTED` |
| `official_cost_reference` | object | DBI Cat. 1P fee, so quotes can be compared to a permit-inclusive path |
| `spread` | object | min / max / difference / ratio, computed from the three amounts |

## `rules.json` → `rules[]`

| Field | Type | Notes |
|---|---|---|
| `id` | `RULE-01…RULE-13` | |
| `topic` | string | |
| `statement` | string | Quotes or closely paraphrases the official text |
| `exact_limit`, `effective` | string? | Present only where the source states a number or date |
| `effect_on_this_job` | string | Applied to this specific job |
| `evidence_label` | string | `OFFICIAL` |
| `source_ids` | array | |

## `scope.json`

| Field | Type | Notes |
|---|---|---|
| `options[]` | object | Three access routes (A above, B below, C access panel) |
| `options[].prerequisites_unverified` | array | Explicitly marked unverified |
| `options[].opens_drywall` | bool | |
| `options[].estimated_time_on_site` | string | Marked "inference - not verified" in the string itself |
| `recommended_sequence[]` | object | Six steps, each with the rule it rests on |
| `why_plumbers_may_have_declined` | object | `label: HYPOTHESIS`, with an explicit `status` caveat |

## `flagged.json`

| Field | Notes |
|---|---|
| `unverified_items[]` | `U-01…U-07` — value, what is missing, effect, how to close it |
| `irregularities[]` | `I-01…I-09` — finding, detail, action taken, review question, severity |
| `questions_to_ask[]` | Ten questions with the source behind each |
| `redaction_policy` | One paragraph describing what is and is not reproduced |

`irregularities` in this file cover the **domain** findings. Repository-structure findings
(I-10 onwards) live in `REPO_REVIEW.md`, because they are about the repo rather than the job.

## `executive.json`

| Field | Notes |
|---|---|
| `key_numbers[]` | The KPI strip; every entry carries `basis` and `source_ids` |
| `bottom_line[]` | Ordered recommendations |
| `recommendation` | primary / why / condition / runner_up / cheapest_first_move |
| `evidence_policy[]` | The four rules the site is held to |

---

## Verification artefacts

| File | Produced by | Meaning |
|---|---|---|
| `tub-verification.json` | `scripts/verify_tub_site.py` | 19 checks; `ok: true` only when all pass |

Rebuild and re-verify:

```bash
python3 scripts/build_tub_site.py
python3 scripts/verify_tub_site.py   # exits 1 on any failure
```

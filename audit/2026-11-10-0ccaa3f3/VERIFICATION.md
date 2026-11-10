# Live-network official-source re-verification — 2026-11-10

Session `arena/0ccaa3f3-korea8`. Task `0cc-03`.

## Why this pass exists

Every 2026-11-10 session that preceded this one recorded a network limitation. Session
`arena/660ab2dd-korea8` wrote on the shared board that it claimed **no** fresh official-provider
checks "because those external domains are outside this session's allowed network". Session
`arena/be9ec407-korea8` recorded that "`yelp.com`, `bbb.org` and direct `github.io` are unreachable
from this sandbox".

This session confirmed the same limitation for in-sandbox `curl` (TLS handshake fails to
`www.cslb.ca.gov`, `www.sf.gov`, `sfplanning.org`) but has a **working page-retrieval tool** that
reaches those hosts. That difference is the entire purpose of this pass: to obtain primary records
directly, rather than carrying forward another session's retrieval.

Nothing below is inferred. Where a value could not be confirmed it is recorded as unconfirmed.

## Retrieval log

| # | Official source | Retrieved | Result |
|---|---|---|---|
| 1 | CSLB licence detail #829071 (Ace Plumbing & Rooter) | direct, live | matches canonical row |
| 2 | CSLB licence detail #1089561 (Taro Group Inc dba Heises Plumbing) | direct, live | matches |
| 3 | CSLB licence detail #1115649 (Rapid Flow Plumbing & Rooter Inc) | direct, live | matches |
| 4 | CSLB licence detail #1027286 (Kenneth Asire Plumbing) | direct, live | matches; **new detail** |
| 5 | CSLB licence detail #977638 (Expert Plumbing Solutions) | direct, live | matches |
| 6 | CSLB licence detail #757796 (Bay Area Plumbing) | direct, live | matches |
| 7 | CSLB licence detail #1024971 (Joseph Tinsley dba Fast Response) | direct, live | matches; **new detail** |
| 8 | CSLB licence detail #1009195 (Advanced Plumbing and Drain Inc) | direct, live | matches; Additional Status verbatim confirmed |
| 9 | CSLB licence detail #297604 (D G Construction Co) | direct, live | matches; **material correction** |
| 10 | CSLB licence detail #995163 (Bernal Hill Drywall Inc) | direct, live | matches |
| 11 | CSLB complaint disclosure #297604 | direct, live | citation confirmed |
| 12 | CSLB **citation-violation** disclosure #297604 | direct, live | **conduct published — see 0cc-IR-01** |
| 13 | Cal. Bus. & Prof. Code §7114 | direct, live (leginfo) | verbatim captured |
| 14 | Cal. Bus. & Prof. Code §7124.6 | direct, live (leginfo) | verbatim captured |
| 15 | sf.gov — Apply for a plumbing and mechanical permit | direct, live | confirmed; **new time-sensitive detail** |
| 16 | Heise's Plumbing — Paint, Patch & Drywall Repair | direct, live | independently corroborates `HEISE-PATCH` |
| 17 | Heise's Plumbing — Ingleside tub waste & overflow case | direct, live | confirmed; embedded 404 block still present |
| 18 | Heise's Plumbing — Panhandle tub waste & overflow case | direct, live | **new source, not in register** |
| 19 | GitHub Pages API — site settings and build history | direct, live (api.github.com) | **config irregularity, see 0cc-IR-04** |
| 20 | Live published site (`github.io`) | direct, live | current; root URL CDN-cached |

All ten CSLB licence pages carried the banner **"Data current as of 11/9/2026 4:49 PM"**
(timestamps ranged 4:49:12 PM – 4:49:37 PM; the page does not state a timezone).

Field-by-field receipts are in [`receipts/`](receipts/).

## Result: the stored licensure data is correct

All ten licence records retrieved directly in this session matched the canonical rows on legal name,
dba, entity type, classifications, status, expiry, registered city, business phone and
workers-compensation entry. **No licensure correction was required.** This independently corroborates
the 24/24 result reported by sessions `arena/d6196195-korea8` and `arena/be9ec407-korea8` for the
ten records in common.

## Four findings that are new to the repository

### 0cc-IR-01 — MATERIAL CORRECTION: CSLB *does* publish the conduct behind the D G Construction citation

The canonical flag for licence #297604 reads, in `overflow-integration/data/flags.json`:

> "#297604 is active B + C-36; the disclosure lists citation 2 2022 002099 dated 03/23/2023, for
> disclosure only per B&P 7124.6."

Session `arena/b0d7ecf7-korea8` recorded on the shared board that the disclosure "does not publish
the conduct". **That is not correct.** The conduct is published on a third-level CSLB page reached by
following the citation link:

| Field | Value as CSLB publishes it |
|---|---|
| Citation # | 2 2022 2099 |
| Date | 03/23/2023 |
| Status | FOR DISCLOSURE ONLY PER B&P CODE 7124.6 |
| Code | Business & Professions Code |
| Violation | **7114.A** |
| Description | **"Aided and abetted non-licensee"** |

Official page:
<https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CitationViolationDisclosure.aspx?LicType=LIC&LicNum=297604&LmfPre=&Class=2&FiscalYear=2022&SeqNbr=2099&ActionCde=K&Status=FOR+DISCLOSURE+ONLY+PER+B%26P+CODE+7124.6&LicName=D+G+CONSTRUCTION+CO&StatusDt=03/23/2023>

**Why this matters to this specific job.** The owner's controlling requirement is one all-in-one
contract covering plumbing *and* the ceiling/drywall restoration. BPC §7114(a) provides, verbatim:

> "Aiding or abetting an unlicensed person to evade the provisions of this chapter or combining or
> conspiring with an unlicensed person, or allowing one's license to be used by an unlicensed person,
> or acting as agent or partner or associate, or otherwise, of an unlicensed person with the intent to
> evade the provisions of this chapter constitutes a cause for disciplinary action."

A citation whose CSLB-published description is "aided and abetted non-licensee" therefore goes
directly to the one risk the all-in-one requirement exists to control: whether unlicensed parties end
up performing part of the scope. #297604 is also one of only six B + C-36 identities in the register
and the longest-tenured (issued 08/23/1974), so it would otherwise be a strong combined-scope lead.

**Neutrality control.** This is a CSLB *citation* disclosed under B&P §7124.6, not an adjudicated
finding of wrongdoing. §7124.6(b) requires the board to accompany a disclosed complaint with a
disclaimer stating that the complaint is an allegation. §7124.6(e)(1)(A) sets the disclosure window at
five years after the date of compliance, so the record is expected to remain visible and is not a
transient artefact. No conclusion on merit is drawn here. The existing "held back" classification
remains correct — but it should now rest on a **named** violation and a **linked** primary page rather
than on an assertion that the conduct is unavailable.

### 0cc-IR-02 — NEW time-sensitive city detail: Permit Center closed 2026-11-11

The sf.gov permit page carried a live banner on 2026-11-10:

> "City offices will be closed on Wednesday, November 11 for Veterans Day."

Consequence: the Permit Center help desk (628-652-4900) and the 49 South Van Ness counter are closed
on 2026-11-11. The next business day for a permit determination is **Thursday 2026-11-12**. Because
sf.gov commits to "We will contact you within 2 business days" for help-desk voicemail, a question
left on 2026-11-10 should be answered by 2026-11-13. This is a scheduling fact the owner needs and it
is not currently in the register.

### 0cc-IR-03 — NEW source: a third company-published San Francisco tub waste-and-overflow replacement

The register carries three Heise's case pages (`HEISE-INGLESIDE`, `HEISE-MISSION`, `HEISE-MARINA`).
Retrieval of the company's drywall service page exposed a fourth, not in the register:

<https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-171358/>

Verbatim: "Heises Plumbing in San Francisco, CA replaced the tub waste and overflow assembly in a
residence. They removed the old overflow, installed a new assembly, and tested the bathtub for
leaks." Area: Panhandle, San Francisco, CA.

Limitation, stated plainly: this case does **not** mention ceiling access or drywall restoration, so
it does not strengthen the all-in-one evidence. It does add a third independent San Francisco
waste-and-overflow replacement by the same company. Its page carries the same embedded "Page Not
Found (404)" template block already flagged for the other case pages — confirmed still present on
2026-11-10.

For completeness, the strongest existing case was re-confirmed verbatim this session
(`HEISE-INGLESIDE`, Ingleside, San Francisco): "Accessed the exterior ceiling to remove the old
overflow, installed a new brass P-trap and trap adapter, and replaced the tub waste and overflow
assembly." The canonical caveat that "exterior ceiling" is not confirmed to mean the storage-unit
ceiling below this particular tub is correct and is retained.

### 0cc-IR-04 — DEPLOYMENT: Pages `build_type` is `legacy` while the published artefact is the workflow's

| Observation | Evidence |
|---|---|
| Pages API reports `"build_type": "legacy"`, source branch `main`, path `/`, `"public": true` | <https://api.github.com/repos/karagemop466-tech/Korea8/pages> |
| Yet non-staged repository files are **not** served: `COORDINATION.md` and `pyproject.toml` both return GitHub Pages 404 | live retrieval, 2026-11-10 |
| The staged closure is 21 files (was 20 before `audit/2026-11-10-47d993da/REPORT.md` was linked) | `python scripts/stage_overflow_pages.py` |
| Legacy Pages builds **errored** for three commits on 2026-11-10 (`caab44e`, `a510682`, `b30f89d`) while the Actions runs for those same commits reported **success** | <https://api.github.com/repos/karagemop466-tech/Korea8/pages/builds> |
| `PUT /repos/.../pages` with `build_type=workflow` returns **HTTP 403 "Resource not accessible by integration"** — the same result session `660ab2dd` recorded | attempted live, 2026-11-10 |

Two consequences, stated without embellishment:

1. **The publication boundary is currently holding, but not because of the configured build type.**
   The observed 404s show the workflow artefact is what is live. The API still declares `legacy`,
   which would publish the *entire* repository root — including `COORDINATION.md` and every internal
   audit record — if a legacy build ever succeeded instead of erroring. The three legacy build
   failures on 2026-11-10 are the only thing between the current state and full-root publication.
2. **"The workflow succeeded" is not by itself proof the site deployed.** For `b30f89d` the Actions
   conclusion was `success` and the Pages build record was `errored`. Any deployment claim must be
   backed by a live route fetch, which is what session `d6196195` correctly did.

The available token cannot change the setting. This is recorded as an owner action, not silently
worked around: **set Pages → Build and deployment → Source to "GitHub Actions" in the repository UI.**

### Confirmed live and current

- The published dashboard is live at <https://karagemop466-tech.github.io/Korea8/> and serves the
  bathtub project, not the archived geothermal project.
- Cache-busted `sources.html` returned **87 source records** and "reviewed 2026-11-10", matching
  `main`. The bare root URL returned a stale "reviewed 2026-11-08" / "85 source records" page —
  CDN caching of the root route, the same pattern sessions `f4bb970c`, `d120270b` and `b0d7ecf7`
  logged. Not a deploy failure; recorded so nobody mistakes the cached root for the deployed state.
- The privacy boundary holds. A `git ls-files` sweep for the internal-instruction phrasings returns
  only verifier banned-pattern lists and statements that the content was *not* recorded. No private
  circumstance, and no reason for one, appears in any tracked file. `COORDINATION.md` is not publicly
  served (404).

## Sources not re-fetched this session (carried forward, labelled)

Recorded honestly rather than claimed as today's verification:

- San Francisco Plumbing Code §104.2 full text (American Legal Publishing chunk retrieval) and the
  city-hosted 2025 SF Plumbing Code PDF — retrieved directly by `be9ec407` on 2026-11-10.
- July 2026 DBI Table 1A-C fee PDF (1P $290; 11P/M $320; $519/hr; $555/hr; $259 half-hour) —
  retrieved directly by `d6196195` and `be9ec407` on 2026-11-10.
- BPC §7048, §7057, §7057.5 and Civil Code §1954 — retrieved directly by `d6196195`/`be9ec407`.
- Watco 500/501/600-TL trip-lever instructions; EPA lead-RRP and asbestos pages.
- CSLB classification pages C-9, C-36, B; CSLB contracts and finding-a-contractor guidance.
- The fourteen remaining licence records not listed in the retrieval log above. Those identities are
  all outside the hiring order (held back or unresolved), so the ten decision-critical records were
  prioritised. Their canonical rows rest on the 24/24 re-reads reported by `d6196195` and `be9ec407`
  on 2026-11-10 and are **not** re-claimed here.
- Yelp, BBB, Angi and Google review data: **still unobtainable**, consistent with every prior
  session. Ratings and review counts remain blank and must stay blank.

## What was NOT done

No provider was contacted, called, emailed, quoted, booked or paid. No permit position was asserted
for this address. No price was inferred. No ranking position was changed on the basis of this pass —
the corrections above are evidentiary and sourcing corrections, and the one that bears on hiring
(#297604) reinforces an existing exclusion rather than creating a new recommendation.

---

## Outcome — what happened to each finding (recorded after integration)

This pass ran while five other sessions were committing to `main`. Two of the four findings were
independently discovered and merged by session `arena/87e121e1-korea8` (PR #65) **before** this session
applied any edit. That is recorded here rather than claimed as this session's correction, and no
duplicate edit was made.

| Finding | Disposition on `main` |
|---|---|
| 0cc-IR-01 — CSLB publishes the D G Construction conduct (BPC §7114.A, "Aided and abetted non-licensee") | **Independently corroborated.** Merged by `87e121e1` into `flags.json`, `providers.json`, `ranking.json`, `sources.json` (`DG-CITATION`) and `EXECUTIVE_SUMMARY.md` before this session edited. Two sessions retrieving separately reached the same violation code, description and citation number. No duplicate edit made by this session. |
| 0cc-IR-02 — Permit Center closed 2026-11-11 (Veterans Day) | **New to the repository.** Applied by this session as compliance row `C-14` and flag `F-49`. Not present anywhere on `main` at `98b3d09`. |
| 0cc-IR-03 — Heise's Panhandle tub waste-and-overflow case #171358 | **Independently corroborated.** Merged by `87e121e1` (`sources.json`, `flags.json`, `providers.json`, `ranking.json`) before this session edited. No duplicate edit made. |
| 0cc-IR-04 — Pages `build_type: legacy` vs the workflow artefact; legacy builds erroring while Actions report success; `PUT` 403 | **Partly pre-existing, extended.** `F-34` already noted the legacy/workflow mismatch. This session added the three errored legacy build commits, the HTTP 403 on `PUT build_type=workflow`, the 21-file staged closure, the live 404 evidence for `COORDINATION.md` and `pyproject.toml`, and the whole-root exposure risk; severity raised to High with an explicit owner action. |

Two further repository findings were new and are applied here:

| Finding | Disposition |
|---|---|
| `.github/workflows/gems-pipeline.yml` line 59 pushes to the hardcoded branch `arena/d7026453-korea8` | **New.** Applied as flag `F-50`. Not previously flagged. |
| 14,052,602 bytes of `.tif` committed against `AGENTS.md` line 39 ("never committed") | **New.** Applied as flag `F-51`. Not previously flagged. |
| Four run cards with four different schemas | **Pre-existing flag corrected.** `F-40` said "two run-card files"; this session corrected it to four, with byte sizes and distinguishing top-level keys. |

## Privacy verification (final)

- The canonical verifier's own banned-pattern gate — `['private reason','must stay private','without a
  permit for this week','cannot pull a permit','cannot obtain a permit', conflict markers, 'TODO',
  'TBD','Lorem ipsum']` — returns **PASS with zero hits** over all generated pages.
- A broader sweep of every changed and new file returned exactly one phrase hit, `do not publish`, in
  the pre-existing flag **F-31** ("A third-party directory misattributes license #297604"), whose
  action reads "Use CSLB as the license authority; do not publish the directory attribution." That
  concerns a third-party directory's misattribution of licence #297604 and is unrelated to permits. No new wording added by this session refers to the owner's internal
  constraint or to any reason for it.
- `COORDINATION.md` returns GitHub Pages 404 live, so the internal board is not publicly served.

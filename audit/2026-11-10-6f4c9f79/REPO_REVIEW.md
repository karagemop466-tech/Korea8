# Line-by-Line Repository Review — 2026-11-10 (`arena/6f4c9f79-korea8`)

**Baseline audited:** `origin/main` at `67b9e98c8364396315ce067aca07938cfc95f369` (Merge PR #70).
**Scope:** Canonical data (`overflow-integration/data/*.json`), site generator (`scripts/build_overflow_site.py`), verifier (`scripts/verify_overflow_site.py`), publication staging (`scripts/stage_overflow_pages.py`), wording guard (`scripts/wording_guard.py`), unit tests (`tests/test_overflow*.py`), independent audit (`audit/independent_audit.py`), recent session audits (`audit/2026-11-10-*`), open PRs (`#63`, `#64`, `#66`, and earlier), and live GitHub Pages deployment behavior.

---

## 1. Cross-Session Requests & Open Defects Resolved

| Ref | Origin | Finding on `main` (`67b9e98`) | Resolution Applied |
|---|---|---|---|
| `B5-05` | `arena/b5ed3a43-korea8` (`COORDINATION.md`) | `audit/2026-11-10-b5ed3a43/REPORT.md` (and companion JSONs) committed to `main` but unlinked from `verification.html`, causing 404 under the staged public closure. | Linked `audit/2026-11-10-b5ed3a43/REPORT.md` (`live-route-check.json`, `source-verification.json`, `traceability.json`) and `audit/2026-11-10-6f4c9f79/` artifacts on `verification.html` (and referenced in `flagged-for-review.html`). |
| `I-4` (`F-08`) | `arena/b5ed3a43-korea8` | `F-08` summary could be misread as asserting a categorical SF.gov permit bar against B-2 rather than SF.gov's scope-and-approval wording plus BPC §7057.5 limits. | Refined `F-08` to pair SF.gov's `"B license, after approval based on the scope of work"` text directly with BPC §7057.5's statutory `>=3`-trade and plumbing-system restrictions. |
| `I-5` (`estimates.json`) | `arena/b5ed3a43-korea8` | `estimates.html` lacked a canonical cost-driver breakdown explaining why scopes differ ($135 vs $550 vs $614 + restoration + DBI fees). | Added a 6-row source-linked `cost_drivers` table to `estimates.json` and rendered it on `estimates.html` without fabricating prices. |
| `7FF-E-1` (`BPC §7059(a)`) | `arena/7ff689a1-korea8` (open PR #66) | Canonical data omitted `BPC §7059(a)` and `16 CCR §831` ("incidental and supplemental") allowance/limits for C-36 specialty contractors. | Verified `BPC §7059(a)` & `16 CCR §831` directly on official sources; added `BPC-7059`, `CSLB-831`, compliance row `C-15`, and updated `R-15`, `T-06`, `F-06`, `F-18`. |
| `BE-01` (`SF-CODE-104-PDF`) | `arena/be9ec407-korea8` (open PR #63) | §104.2 cited only American Legal Publishing (which carries a non-definitive publisher disclaimer) rather than SF.gov's own hosted code PDF. | Verified `https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf` & `2025_SFBC_Amendments.pdf` live; added `SF-CODE-104-PDF` & `SF-CODE-106-PDF` as primary citations on `C-02` / `C-13` / `R-22` / `R-23` / `R-12`. |
| `7FF-C` (`#954813`, `#888630`, `HEISE-FIXTURES`, unverified ads) | `arena/7ff689a1-korea8` (open PR #66) | Additional verified SF/Peninsula leads (`24/7 Rooter #954813`, `George Salet #888630`), Heise's `/plumbing-fixtures/`, and two unverified leads (`C J's Plumbing`, `Golden Gate Plumbing`) sat outside canonical data. | Re-verified `#954813`, `#888630`, `#1089561`, `24-7rooter.com`, `plumbingpro.com`, `heisesplumbing.com/plumbing-fixtures/`, and `cjplumbing.net` directly on `2026-11-10`; added to `providers.json`, `ranking.json` (`not_recommended`), `sources.json`, and `F-52` (with unverified identities strictly blank!). Rejected PR #66's erroneous `#1089561` dates (`09/04/2014`, `09/30/2028`) in favor of live CSLB (`04/06/2022`, `04/30/2028`). |

---

## 2. Newly Caught Discrepancies Fixed in Canonical Data

1. **Broken `HEISE-PANHANDLE` URL (`sources.json`):** Stored URL `/projects/plumbing-repair-and-replacement/171358/` returned pure 404. Fixed to live `/recent-jobs/projects/the-tub-waste-and-overflow-assembly-171358/`.
2. **Invalid-parameter `DG-CITATION` URL (`sources.json`):** Abbreviated query parameters displayed `"Invalid Parameters passed"` on CSLB; replaced with exact query URL linked by `ComplaintDisclosure.aspx`.
3. **Updated `BBB-EXPERT` expiry (`reviews.json` `RV-16`, `sources.json`):** BBB now displays `10/31/2028` matching CSLB `#977638` (no longer stale `10/31/2026`).
4. **Stale `2026-11-08` text in `ranking.json`, `requirements.json`, `sources.json`:** Updated `method_note`, `final_verification_note`, `requirements` status dates, and CSLB `limitations` to `2026-11-10` after direct re-checks; deduplicated `"ACE"` in `ranking.json` `C4.source_ids`; fixed `"restoration.; SFBC"` typo in `R-12`.
5. **Contradictory `F-39`, stale `F-34` / `F-40` / `F-45` & `deployment.json`:**
   - `F-39` title said `"Three"` while detail said `"Nine"` and actual GitHub open PRs = `11` (`#7, #35, #38, #39, #44, #49, #51, #53, #63, #64, #66`). Fixed both title and detail.
   - `F-34` updated to reflect live `2026-11-10` proof that legacy Pages builds resumed succeeding (`1e7f03f`, `9f1e76d`, `67b9e98`), overwriting the workflow artifact and exposing `/` (`COORDINATION.md`, `project/EXECUTIVE_SUMMARY.md`). Updated exact staged file count.
   - `F-40` updated remote `arena/*` branch count (`41` prior branches + current).
   - `F-45` resolved by updating `BATHTUB_EXECUTIVE_SUMMARY.md` and `EXECUTIVE_SUMMARY_bathtub.md` to point to `executive-summary.html` and `OVERFLOW_EXECUTIVE_SUMMARY.md`, plus prepending a non-destructive `Superseded 2026-11-07` notice on `project/EXECUTIVE_SUMMARY.md` (`I-1`).
   - `deployment.json` refreshed from stale PR #56 metadata ahead of our PR/deploy receipt.

---

## 3. Historical Audit Note (Preserved Read-Only)

- **`audit/2026-11-10-87e121e1/REPORT.md` line 52 weight typo:** That report wrote `Weighted sum C1*0.30 + C2*0.25 + C3*0.20 + C4*0.15 + C5*0.10`, whereas `overflow-integration/data/ranking.json` actually uses **`C1 0.30 + C2 0.20 + C3 0.20 + C4 0.15 + C5 0.15 = 1.00`** (which produces the exact published scores: Ace `3.85`, Heise's `3.45`, Rapid Flow `3.15`, Ayoob & Peery `3.15`, We Do `2.95`, Expert `2.90`, Save-On-Interior `2.60`, Bay Area `2.55`, Discount `2.30`, Fast Response `2.20`; Bernal Hill `2.15`). Documented as `F-53` without altering `87e121e1`'s archived report.
- **Unrelated DOE GEMS preservation & `site-data/`:** `docs/` (excluding retired `docs/bathtub-*` stubs), `src/`, `vendor/`, `registry/`, `evidence/`, `downloads/`, `submissions/`, and `gems-pipeline.yml` remain completely untouched. `site-data/README.md` already identifies `site-data/` as a superseded mirror except current `build-report.json` and `verification.json` outputs.

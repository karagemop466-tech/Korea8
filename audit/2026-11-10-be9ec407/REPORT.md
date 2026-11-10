# Independent line-by-line verification and repository audit — 2026-11-10

**Session:** `arena/be9ec407-korea8` (task BE-01)
**Scope:** audit of the canonical dashboard, its data files and build, plus independent
re-verification of every official source reachable on 10 November 2026.
**Not claimed:** no provider was contacted, quoted, scheduled or booked; no permit position is
asserted for this specific job; no value was filled in to close a gap. Where a field could not be
confirmed from an official source it stays blank and is flagged.

---

## 1. Sources re-read directly on 2026-11-10

Every source below was fetched in this session and compared field by field with
`overflow-integration/data/`. CSLB pages carried the banner *"Data current as of 11/9/2026 4:49 PM"*.

| Source class | Count | Result |
|---|---|---|
| CSLB licence-detail pages (`cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=…`) | 24 | **24/24 matched** the register exactly — legal name/dba, classification list, entity type, current-vs-suspended status, expiry, business phone, registered city |
| SF DBI fee schedule Table 1A-C (July 2026 PDF) | 1 | All six published fee rows matched: 1P $290, 11P/M $320, regular inspection $519/hour, off-hour $555/hour, reinspection $259/half-hour, effective for permits issued on/after 2026-07-12 |
| SF.gov permit pages (`apply-plumbing-and-mechanical-permit`, `apply-kitchen-or-bath-remodel-permit`) | 2 | Permit trigger ("before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground"), the C-4/C-16/C-20/C-36/C-54/B/A applicant classes and the inspect-before-covering step all matched |
| 2025 San Francisco Plumbing Code (city-hosted PDF) | 1 | **New primary source** — §104.2 reproduces the nine-item exempt list, each item conditioned on not cutting into or removing piping |
| Cal. Bus. & Prof. Code §§7048, 7057, 7057.5; Civ. Code §1954 (leginfo) | 4 | All four matched the site's wording, including the §7048 $1,000 aggregate threshold and its 2026-01-01 amendment, and the §1954 24-hour / six-day notice presumptions |
| CSLB C-9 classification page; CSLB contracts guidance | 2 | C-9 scope ("gypsum wall board … taping and texturing") and the over-$500 written-contract plus 10%-or-$1,000 down-payment rules matched |
| Company pages: Rapid Flow, Ace, Expert Plumbing, Bay Area Plumbing, Fast Response, We Do Construction, Heise's, Bernal Hill Drywall | 8 | Every service claim printed on the site is supported by text on the company's own page; Ace still publishes HOA/property-manager work and all six classifications |
| Watco 500/501/600-TL manufacturer instructions | 1 | Steps 6–7, the SLIP LOCK / QUICK ADJUST / TURNSTYLE variants and the "linkage must not be kinked" warning matched |
| Heise's Ingleside case study | 1 | "Accessed the exterior ceiling to remove the old overflow, installed a new brass P-trap and trap adapter, and replaced the tub waste and overflow assembly" — matched; the page's embedded 404 block is still present (already published) |

**Unreachable from this environment (recorded, not papered over):** `yelp.com`, `bbb.org` and the
other review platforms still block automated retrieval, and direct `github.io` fetches are blocked
here. Yelp ratings and review counts therefore stay **blank** — that is the correct state, not a
missing measurement. Live-route confirmation is performed from the GitHub Actions runner.

---

## 2. Arithmetic and internal consistency (recomputed from the data, not trusted)

- Ranking weights C1 0.30, C2 0.20, C3 0.20, C4 0.15, C5 0.15 sum to **1.000**.
- Weighted totals recomputed for all ten ranked rows: Ace **3.85**, Heise's **3.45**, Rapid Flow **3.15**,
  Ayoob & Peery **3.15**, We Do **2.95**, Expert **2.90**, Save-On-Interior **2.60**, Bay Area **2.55**,
  Discount **2.30**, Fast Response **2.20** — the published order is exactly the descending total, and the
  3.15 tie is resolved in the stated editorial order rather than by an undisclosed numeric difference.
- Every provider in the hiring order is `Current and active`. Kenneth Asire (#1027286) still shows
  **"License is under Contractors Bond Suspension"** with bond cancellation 08/16/2026, and Portola is
  still unresolved with blank fields; both appear only in the held-back list.
- Bernal Hill Drywall (#995163, C-9 + B) is placed as restoration partner, not as a plumber — consistent
  with the C-9 scope text and with the absence of a plumbing classification on that record.
- Counts: 25 identities = 24 CSLB records + 1 unresolved; every canonical table row carries a registered
  official-primary source link.

## 3. Blank-vs-unverified discipline

- `amount_verified` is `null` for all three owner-supplied estimates; the $614 / $550 / $135 figures are
  labelled owner-reported with the 2026-08-30 date only, and the page states the scopes are not like-for-like.
- All review `rating` and `review_count` fields are `null`.
- Portola's licence, phone, expiry, status and city are blank, with the identity flagged unresolved.
- No source, date, phone or price is inferred from a directory or aggregator; where a third-party
  directory disagreed with CSLB (licence #297604) the CSLB mapping is the one used.

## 4. Irregularities found

One, now published on the **Flagged for review** page.

1. **F-47 (new, resolved).** The §104.2 exemption row previously cited only the American Legal Publishing
   code-library copy. The City and County of San Francisco hosts its own PDF of the 2025 Plumbing Code,
   which reproduces the exact nine-item exempt list and the no-cutting clause. `C-02` now cites the
   city-hosted PDF first (`SF-CODE-104-PDF`), keeps the library copy as a secondary reference, and the row
   text was tightened to the exempt-list wording instead of a paraphrase.
2. **Still open, re-confirmed:** no provider confirms this exact stuck-lever job, an all-in price,
   availability or ceiling restoration (F-01, F-04, F-46); the job-level permit determination is open
   (F-21); access-panel dimensions are unverified (F-23); Heise's case study is self-published and contains
   a 404 template block (F-17); B + C-36 does not prove drywall self-performance (F-06); D G Construction's
   row links CSLB complaint-disclosure information (F-11); Advanced Plumbing and Drain carries a
   future-suspension warning (F-10).
3. **No defect found** in the provider register, ranking arithmetic, fee table, statute citations or company
   service claims. No provider value was corrected.
4. **Repository/topic mismatch (F-32) persists by design:** this repository also hosts the unrelated DOE
   GEMS geothermal research, which was not modified in this session.

## 5. Build, verification and publication checks

- `python3 scripts/build_overflow_site.py` → 11 pages, 25 identities, 42 requirements, 88 sources,
  47 flags, 10 ranked + 14 held.
- `python3 scripts/verify_overflow_site.py` → **27/27 checks passed** (300 source-covered rows, 0 broken
  internal links across tracked HTML).
- `python3 -m unittest discover -s tests -p 'test_overflow*.py'` → all tests passed.
- `git diff --check` → clean.

## 6. Limits this audit does not remove

Checking official sources line by line establishes what those sources say today. It does **not** establish
that a provider will accept the job, will price it as the owner hopes, is available this week, or will
self-perform a lawful ceiling restoration. Those remain open inquiries (F-01, F-46).

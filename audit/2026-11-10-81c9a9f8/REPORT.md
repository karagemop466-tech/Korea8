# Independent line-by-line re-verification — 2026-11-10

Session `arena/81c9a9f8-korea8`. This report records what was actually retrieved, what was
compared, what matched, and what remains unverified. It is a **source re-read**, not a new
ranking: no weight, score, scope, price or provider claim was changed.

## 1. Method

Every row of the published register was checked against the primary source it cites. Where a
value could not be reproduced from an official source it was left blank and is flagged. No value
was inferred, averaged or completed from a secondary source.

Field-level CSLB snapshots are stored machine-readably in
`audit/2026-11-10-81c9a9f8/observed_cslb_2026-11-10.py` so the comparison can be re-run.

## 2. CSLB licence records — 24 of 24 reproduced

All 24 licence-detail pages were retrieved directly from `cslb.ca.gov` on 2026-11-10. The CSLB
page banner read **"Data current as of 11/9/2026 4:49:… PM"** for every one of them (timezone not
stated on the page).

| Field compared | Result |
|---|---|
| Legal name (including `dba` trade name where the official page shows one) | 24/24 match |
| Classifications (set comparison) | 24/24 match |
| Business phone | 24/24 match |
| Registered city | 24/24 match |
| Licence expiry date | 24/24 match |
| Suspension status (only #1027286 suspended) | 24/24 match |
| Workers'-compensation *exemption* status | 24/24 match |

Newly identical details re-confirmed this session:

- **#1089561** TARO GROUP INC dba HEISES PLUMBING — C36, C10, A, C20; current and active; expires 04/30/2028.
- **#829071** ACE PLUMBING & ROOTER — C36, A, C-4, C16, B, C10; current and active; expires 06/30/2027.
- **#1115649** RAPID FLOW PLUMBING & ROOTER INC — B, C36; current and active; expires 01/31/2028; workers-comp **exempt**.
- **#1027286** KENNETH ASIRE PLUMBING — **under contractors-bond suspension**; bond 04CF616317 cancelled 08/16/2026.
- **#1009195** ADVANCED PLUMBING AND DRAIN INC — additional status: may be suspended at a future date for an outstanding final liability.
- **#297604** D G CONSTRUCTION CO — complaint-disclosure information published for this licence.
- **#1140843** DISCOUNT PLUMBING ROOTER SERVICES LLC — $2,000,000 liability insurance and a $100,000 LLC employee/worker bond recorded.
- **#954385** CW PLUMBING INC dba CITYWIDE PLUMBING — reissued to another entity 07/06/2026.
- **#749536** SAVE - ON - INTERIOR — 2015/2016 cash-deposit miscellaneous entries still present.
- **#868994** ATLAS PLUMBING & ROOTER — employee service group holds the workers-comp policy.

Official records:
<https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx> (search entry point) and
`https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=<number>` for each
licence above. #1027286 is at
<https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1027286>.

**Portola Plumbing Services** remains an unresolved identity: no licence number is published and
no licence number could be matched, so all of its licence fields stay blank (flag F-13).

## 3. Statutes and regulations re-read at source

| Rule relied on by the site | Official source retrieved 2026-11-10 | Result |
|---|---|---|
| BPC §7057 — when a B licensee may take a prime contract covering other trades | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057.> | Verified verbatim: two unrelated trades, **or** holds the classification, **or** subcontracts with an appropriately licensed contractor |
| BPC §7057.5 — B-2 residential remodelling limits | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057.5.> | Verified: three or more unrelated trades; no structural work; plumbing-system replacement needs the appropriate classification |
| BPC §7048 — small-work exemption | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048.> | Verified: under $1,000 **and** work that does not require a building permit; does not apply to advertisers or employers |
| Civil Code §1954 — landlord entry | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.> | Verified: necessary/agreed repairs, normal business hours, reasonable written notice, 24 h presumed / 6 days if mailed |
| SF Plumbing Code §104.2 — exempt work | <https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830> | Verified in the 2026 S-96 text: leak repair, unstopping and faucet/angle-stop/hose-bibb work are exempt **only** where cutting into or removing piping is not required |
| SF DBI permit trigger and licence classes | <https://www.sf.gov/apply-plumbing-and-mechanical-permit> | Verified: permit needed before cutting into or replacing pipes, particularly pipes covered by a wall; C4, C16, C20, C36, C54, B or A may apply |
| DBI fee schedule, July 2026 | <https://media.api.sf.gov/documents/Table_1A-C_-_Plumbing_Mechanical_2026.pdf> | Verified: Category 1P $290; 11P/M $320; inspections $519/h, off-hour $555/h, re-inspection $259 per half hour |
| CSLB C-9 drywall scope | <https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9> | Verified: gypsum board installation, taping and texturing |
| CSLB C-36 plumbing scope | <https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36> | Verified |
| CSLB written-contract and down-payment rules | <https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx> | Verified: written contract over $500; down payment no more than 10% or $1,000, whichever is less |
| PermitSF authorised-agent (AUTH) registration | <https://www.sf.gov/licensed-contractors-register-yourself-or-authorized-agents-on-permitsf> | Verified: AUTH record streamlines permit issue for eligible plumbing/mechanical applications |

Two source-quality observations were re-confirmed and remain published as flags:

- **F-44** — the CSLB B-classification page reproduces an older statutory version of BPC §7057
  ("*Amended by Stats. 1997*") while the Legislature page shows the current 2013 amendment. The
  Legislature text controls.
- **F-23** — no free official text of the 12-inch access-panel rule could be retrieved (IAPMO
  chapter 4 redirects to a members-only login), so no access-panel dimension is published.

The superseded brief at `project/EXECUTIVE_SUMMARY.md` still asserts "UPC §402.10 requires a
12-inch access panel" and "satisfies UPC §402.10". That file is **not** linked from the canonical
site, contradicts the published flags, and is now recorded as a repository flag (F-47).

## 4. Manufacturer and company sources re-read

| Source | What it supports | Result |
|---|---|---|
| [Watco 500/501/600TL trip-lever instructions](https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf) | Overflow plate, drop cylinder and linkage service path; SLIP LOCK insertion through the overflow; step 7 readjustment; linkage must not be kinked | Verified verbatim. The instructions describe a **drain stop** function; they do not state a complete tub fill/leak test, matching the published limitation |
| [Heise's Ingleside waste-and-overflow case](https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-san-francisco-163802/) | Below-ceiling fallback in San Francisco: "Accessed the exterior ceiling to remove the old overflow…" | Verified verbatim; the page also renders an embedded "Page Not Found (404)" template block (F-17) |
| [Heise's paint, patch and drywall repair](https://www.heisesplumbing.com/property-maintenance/paint-patch-and-drywall-repair/) | Advertised "plumbing access hole repair", ceiling patching and paint touch-up | Verified (self-published service claim) |
| [Ace Plumbing & Rooter](https://www.aceplumbingandrooter.com/) | Contractors Licence #829071 and the A/B/C4/C10/C16/C36 list; HOA and property-manager work | Verified; the site's own licence list matches the CSLB record |
| [Rapid Flow](https://www.rapidflowbayarea.com/) | "simple repair all the way to a complete renovation"; B + C-36; 844-BAY-FLOW phone | Verified; the website phone differs from the CSLB business phone (F-43) |
| [Atlas contact page](https://www.atlasplumbingandrooter.com/contact/) and [BBB profile](https://www.bbb.org/us/ca/san-francisco/profile/plumber/atlas-plumbing-rooter-1116-116593) | Address and phone discrepancies; BBB licence record 868994 expiring 3/31/2028 | Verified: three different contact numbers exist across official primary sources (F-42) |

Yelp business pages returned **HTTP 403** again on 2026-11-10. No rating, review count or review
text is published anywhere on the site.

BBB is directly retrievable and publishes an accreditation and rating for one candidate (Atlas).
Those fields are left unpublished here: accreditation is not a job-fit or quality measurement for
this repair, and adding them would change the published ranking basis. The observation is logged
in the audit only. This is a deliberate limitation, not a verified ranking input.

## 5. Repository irregularities found in this session

| # | Finding | Handling |
|---|---|---|
| 1 | `project/EXECUTIVE_SUMMARY.md` and `project/README.md` state a 12-inch UPC §402.10 access-panel rule as verified, contradicting F-23/F-45 | Published as **F-47**; the canonical site publishes no dimension |
| 2 | Live GitHub Pages mode is **legacy, source `main` / path `/`**, so every tracked file at the repository root is publicly served, including `COORDINATION.md` and `PROJECT_PROMPT.md`, and a validator test enforces that `docs/index.html` keeps redirecting to the dashboard | Published as **F-48**; no privacy finding in the served text (see §6), but the exposure exists |
| 3 | ~25 open pull requests from earlier sessions remain unmerged on this project | Published as **F-49**; not touched by this session |
| 4 | Root still carries several competing executive-summary files (`EXECUTIVE_SUMMARY.md` = DOE GEMS, `OVERFLOW_EXECUTIVE_SUMMARY.md` = current, two retired stubs) | Documented in this report; the canonical entry point remains `index.html` and `OVERFLOW_EXECUTIVE_SUMMARY.md` |

## 6. Publication-boundary and neutral-wording check

- Retrieved from the live site: `index.html`, `decision-analysis.html`, `docs/index.html`,
  `docs/limitations.html`. The dashboard renders; `docs/` is a redirect stub as designed.
- The public site, the data files, the owner record and the generated pages contain **no**
  internal-only owner constraint and **no** private reason for it. Handling is by omission; the
  decision is recorded on the board without content.
- The only "without a permit" string in published data is the code-neutral quotation of the CSLB
  rule inside a superseded draft (`bathtub-overflow/data/findings.json`), which is a redirect-stub
  subtree and states the law, not an intention.
- A neutral-wording sweep over the canonical pages, the data files and this report found no
  instruction to work outside permit requirements, no evasion wording, and no placeholder text.

## 7. What this audit does **not** establish

- It does not confirm that any provider will accept this exact job, its scope, a schedule, a
  price, or availability. No provider has been contacted.
- It does not make the owner-supplied amounts ($614 / $550 / $135) verified prices; they remain
  owner-reported with verified amounts blank.
- It does not resolve the job-specific permit determination, the storage-unit authority, the
  assembly brand/model, the building age, or the presence of lead/asbestos-containing materials.
- It does not verify Yelp ratings or review counts (HTTP 403).
- Link coverage and structural checks prove that every published row carries an official source
  link; they do not by themselves prove that each source entails each claim.

## 8. Machine-checked results for the rebuilt site

- `python scripts/build_overflow_site.py` — 11 canonical pages, 25 identities (24 CSLB records + 1 unresolved), 49 published flags.
- `python scripts/verify_overflow_site.py` — all structural checks pass, every canonical table row source-covered, no broken internal links.
- `python -m unittest discover -s tests -p 'test_overflow*.py'` — all tests pass.
- CSLB reproduction harness in `observed_cslb_2026-11-10.py` — 24/24 records reproduce every published licensure field.

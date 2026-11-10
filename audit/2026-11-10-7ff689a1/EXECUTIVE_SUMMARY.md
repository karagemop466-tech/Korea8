# 7FF · Executive summary of the 2026-11-10 audit

**Session:** `arena/7ff689a1-korea8` · **Everything below read on 2026-11-10; CSLB banner on all licence pages: "Data current as of 11/9/2026".**

A bathtub trip-lever overflow that five plumbers cannot free from above, in a rented San Francisco unit, with a drywall ceiling over somebody else's storage underneath. The shared site already carries the 42-row requirements register, 24 CSLB-checked providers, 46 flags and 87 sources. This audit did three things: **checked the table against the regulator row by row, found the legal provision that makes an all-in-one plumber-plus-drywall contract work, and established what the review platforms can and cannot support.**

## What is now known with certainty

| # | Finding | Source |
| --- | --- | --- |
| 1 | **Every published provider row is right.** All 24 licence numbers in the register were re-read from the board's own detail pages and compared field by field with a normalising script: legal name, phone, registered city, expiry, classification set, status. Result: 0 mismatches. 1 row remains unverified (Portola Plumbing, which has no licence number to check). | [compare_providers.py](compare_providers.py) → [row-diff.md](row-diff.md) |
| 2 | **The from-above vs from-below question has a documented answer.** The manufacturer's own instruction sheet reaches the plate, drop cylinder and linkage from inside the tub; the drain elbow, **overflow elbow, tee and trap connections sit under and behind the tub**. So "try it from above" and "you must open the ceiling" are both correct — about different repairs. | [Watco 500/501/600-TL instructions](https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf) |
| 3 | **One plumber can lawfully do both halves.** A specialty contractor may "take and execute a contract involving the use of two or more crafts or trades, if the performance of the work in the crafts or trades, other than in which they are licensed, is **incidental and supplemental**" to the licensed craft. The patch of an access hole made to do the plumbing is the textbook case; a separately priced ceiling restoration is not. This provision is **not yet in the register** and is the audit's main handoff item. | [BPC 7059(a)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059) |
| 4 | **Which firms are licensed for both trades in one name today:** B + C-36 → Ace Plumbing & Rooter (829071), Rapid Flow (1115649), Ayoob & Peery (392967), We Do (1096552), Save-On Plumbing Interior (749536), D G Construction (297604, with a complaint disclosure). C-9 + B → Bernal Hill Drywall (995163). | [CSLB Check a License](https://www.cslb.ca.gov/OnlineServices/CheckLicense.aspx) |
| 5 | **Only one firm publishes the exact method the owner's plumbers recommend.** "Accessed the exterior ceiling to remove the old overflow … replaced the tub waste and overflow assembly" — with two more waste-and-overflow replacements and an overflow-gasket job in unit 302 of a multi-family building, plus an advertised **Paint, Patch & Drywall Repair** line covering plumbing access-hole repair and ceiling water stains. It holds C-36 + A + C-10 + C-20 and **no B, no C-9**, which rows 3 and 5 resolve rather than disqualify. | [Ingleside job](https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-san-francisco-163802/) · [patch service](https://www.heisesplumbing.com/property-maintenance/paint-patch-and-drywall-repair/) · [licence](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1089561) |
| 6 | **Ratings cannot be verified at all — and that is now evidenced, not assumed.** Yelp business pages still return HTTP 403 to direct retrieval; a guessed BBB profile path for Expert Plumbing Solutions returned "Page not found". Search-index snapshots of the *same* business disagree with each other (Ace: 4.5/685, 4.7/1.4k, 4.7/1.5k), and what firms print on their own sites (4.9★, "2,000+ reviews", "5★ Customer Rated") is self-published. The published tables therefore keep rating cells **blank with flags**, which is the correct handling, not a gap. | [review-platform-evidence.json](review-platform-evidence.json) |
| 7 | **Third-party directories are not safe for licence facts.** A BBB profile states licence 954813 "expiration date … 11/30/2026"; the board record says **11/30/2028** — two renewal cycles stale. Every licence value on the site comes from the board, never from a directory. | [24/7 Rooter record](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=954813) |
| 8 | **Where a firm's own site and the board's record diverge, the divergence is a vetting question, not a disqualification.** Rapid Flow advertises toll-free 844-BAY-FLOW vs the registered local number; 24/7 Rooter is reachable on three different published numbers; Heise's registers on Evans Ave and fronts on Ocean Ave; tenure claims ("Over 25 Years", "since 1995", "47 years") are not corroborated by issue dates (03/20/2017, 01/07/1999, 12/21/2006). Company sites do correctly print matching licence numbers for Ace, Expert, Bay Area, Rapid Flow and Fast Response. | [candidates](cslb-candidate-verification-2026-11-10.json) |

## Money and risk, in one place

| Item | Value | Status |
| --- | --- | --- |
| Expert Plumbing Solutions — "Replacing waste and overflow" | **$614** | owner-supplied, dated 08/30/2026; quotes expire, so re-quote |
| Bay Area Plumbing — "Replace lever … plug and spout with diverter, labor + materials" | **$550** | owner-supplied; entity linkage with Save-On #749536 unresolved (same address/phone, consecutive bonds) |
| Fast Response — "repair or adjust bath tub wastewater plunger handle" | **$135** | owner-supplied; the only quote matching the from-above path |
| Cost of a wrong sequence | one ceiling, then the patch, then texture and paint, then the neighbour's storage claim | why the tub-side attempt is worth buying first even if it fails |
| Insurance on record | all shortlist firms show a contractors bond; workers' comp noted per row | two dates matter **now**: Fast Response 1024971 coverage **ends 12/18/2026**; Expert 977638 policy to 07/19/2027 |
| Licence hygiene | Advanced 1009195 has a future-suspension Additional Status; Clever 1160613 issued 09/04/2026; Citywide 954385 reissued to another entity 07/06/2026; Asire 1027286 **under suspension** (bond cancelled 08/16/2026) | stay off the shortlist |

## What the owner should do next

1. **Re-quote the same scope to three firms** — Ace (B + C-36), Heise's (published method + patch line), Rapid Flow (B + C-36) — and ask each to price the tub-side attempt separately from a full waste-and-overflow replacement.
2. **Ask who closes the ceiling and under which licence**, and accept "my B/C-9 licence" or "incidental to the plumbing contract" as the two good answers.
3. **Confirm the number that dispatches a crew**, and confirm the entity on the contract matches the licence on the wall (matters most for the $550 Bay Area quote).
4. **Give the contractor the photos and the ceiling situation** before booking, so access is planned rather than discovered; the storage unit underneath needs protection and written entry notice to the tenant.
5. **Treat the 08/30/2026 prices as expired.** Nothing on the site presents them as current offers.

## Method, so the numbers can be checked

Two tools were used and nothing else: direct retrieval of official pages (`cslb.ca.gov`, `leginfo.legislature.ca.gov`, the City's `sf.gov`, the AmLegal San Francisco code library, manufacturer PDFs, company sites) and a search engine used only to *find* such pages. The sandbox has no general network access, so review platforms that block robots could not be read at all. Every licence assertion above links to a board detail page; every legal assertion links to the statute or regulation text; every capability assertion links to the company's own page and is labelled as advertising, not performance. Values that no official source could support — star ratings, review counts, price averages, an access-panel dimension — are recorded as blank with a reason rather than estimated. See [row-diff.md](row-diff.md) for the field-by-field table comparison and [regulatory-findings.json](regulatory-findings.json) for the ten verbatim provisions with the chunks they were read from.

## Notable negative results

- No San Francisco provider in any source found advertises "trip-lever removal from above" as a service outcome. The preference is an interview question, not a search result.
- The concealed-joint access-opening dimension claimed in some registers could not be verified from any free official copy, and no panel size is asserted anywhere in this audit.
- `cslb.ca.gov` business-name search is an interactive POST form with no static URL, so a provider known only by name (Portola) cannot be resolved by retrieval. Its row stays unverified.
- No provider publishes a price for this repair, so the site's price column stays blank; the only numbers on the site are the owner's own three quotes, labelled owner-supplied.

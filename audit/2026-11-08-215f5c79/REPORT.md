# Final integration freshness audit — 2026-11-08

Session: `arena/215f5c79-korea8`. This is an independent review of the existing canonical dashboard,
not a contractor booking, performance endorsement, legal opinion or new quote. The detailed field
snapshots are in [freshness-check.json](freshness-check.json).

## Result

**PASS for publication, with the existing 40 flagged items retained.** All 22 canonical verifier
checks and 10 unit tests passed after integrating PR #45. The verifier checked 274 table rows for row-level source links and
235 internal links across tracked HTML. No provider was contacted; exact-job acceptance, current
availability, all-in-one restoration and current pricing remain unconfirmed.

## Fresh official-source checks

| Provider / subject | Freshly confirmed official fact | Canonical comparison | Source |
|---|---|---|---|
| Rapid Flow #1115649 | Current/active; B + C-36; (415) 866-8401; expires 2028-01-31 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649) |
| Ace #829071 | Current/active; C-36, A, C-4, C-16, B, C-10; (415) 824-6444; expires 2027-06-30 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071) |
| Heise’s #1089561 | Current/active; C-36, C-10, A, C-20; (415) 333-0704; expires 2028-04-30 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1089561) |
| Expert #977638 | Current/active; C-36; (415) 531-5340; expires 2028-10-31 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638) |
| Bay Area #757796 | Current/active; C-36; (415) 668-8000; expires 2027-01-31 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796) |
| Fast Response #1024971 | Current/active; C-36; (415) 596-6115; expires 2027-03-31 | Match | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971) |
| Kenneth Asire #1027286 | Contractors Bond Suspension remains shown | Match; still excluded from priority leads | [CSLB detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1027286) |
| Rapid Flow service claim | Company advertises Bay Area plumbing/general contracting from simple repair to renovation and displays B/C-36 #1115649 | Match; self-description only | [Company site](https://www.rapidflowbayarea.com/) |
| Ace service claim | Company advertises San Francisco residential plumbing and HOA/property-manager work and displays #829071/classifications | Match; self-description only | [Company site](https://www.aceplumbingandrooter.com/) |
| Heise’s Marina case | Self-published case describes bathtub overflow assembly/gasket service | Match; adjacent case, not exact-job proof | [Company case study](https://www.heisesplumbing.com/recent-jobs/projects/an-overflow-gasket-on-a-bathtub-san-francisco-176011/) |

CSLB source timestamps and every compared field are preserved in the machine-readable snapshot.
The fresh evidence supports **no change to PR #45’s published evidence-based ranking**. Rapid Flow and Ace remain combined-classification
inquiry leads; Heise’s remains the adjacent technical-case lead. This does not establish workmanship,
drywall self-performance, tenant-specific protocols or job acceptance.

## Automated verification reproduced

Commands run from the repository root:

```sh
python scripts/build_overflow_site.py
python scripts/verify_overflow_site.py
python -m unittest discover -s tests -p 'test_overflow*.py'
git diff --check
```

Results: 22/22 checks PASS; 10/10 tests PASS; no whitespace errors. Counts after combining PR #45: 11 canonical pages, 24 provider identities
(23 CSLB records plus one unresolved identity), 22 active licenses, one suspended license, six B+C-36
leads, 42 requirements, 73 sources, 40 flags and 10 ranked candidates. The independent parser checked
245 rows on its 10-page scope and 161 internal links with zero problems. Owner-reported estimate amounts remain explicitly
labelled; independently verified amounts, unresolved identity fields and numeric review metrics stay blank.

## Parallel-audit findings resolved at integration

PR #43 added another independent audit, PR #45 added a full 2026-11-08 license recheck plus ranked decision analysis, and PR #47/#48 added deployment and repository-review updates while this branch was being integrated. All were retained; the final change set was reapplied cleanly onto PR #48 and the combined site was regenerated and re-verified. Its four parser-level
blank/source exceptions were manually reviewed: the §104.2 requirement row, Ayoob & Peery source row,
Bernal Hill Drywall source row and SF-CODE-104 source row each contain a direct primary-source link.
The older independent parser merely omitted American Legal Publishing, Ayoob & Peery and Bernal Hill
from its hostname allowlist; these are not missing-source rows. The canonical strict verifier separately
requires an HTTPS source link on all 274 rows and passes. Heise’s embedded 404 template block was already
recorded in the canonical source limitations and remains disclosed above and in the source register.

Rebase conflicts in `COORDINATION.md`, the generator and generated reports were resolved by retaining PR #43, PR #45 and this session’s audit link/log, then rebuilding from the combined canonical data; no parallel work was discarded.

## Review-platform limitation

A fresh [Yelp plumber search](https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA)
returned changing snippets with ratings/counts. Those search-index values were **not** promoted into
the canonical table because the corresponding business pages were not directly verified. The site
continues to link review leads while leaving ratings/counts blank, which is more conservative than
publishing ephemeral snippets as established facts.

## Irregularities and open items retained

1. No source confirms this exact stuck-lever extraction plus storage-unit ceiling restoration.
2. The three owner-supplied estimates have unlike scopes and no independently verified current amounts.
3. B+C-36 classification does not prove drywall self-performance; the restoration party must be named.
4. Kenneth Asire remains suspended and excluded from the active shortlist.
5. Portola identity and contact fields remain unresolved/blank.
6. Review ratings/counts remain blank; search snippets are not stable verification.
7. The exact permit determination, access-panel dimensions and building-material hazards remain open.
8. Older overlapping coordination claims are stale; the latest completed canonical handoff and independent audit are preserved. This session claimed only final integration and did not discard earlier work.

The public [Flagged for Review page](../../flagged-for-review.html) remains the authoritative complete
list. These items do not block deployment because they are explicitly disclosed rather than filled in.

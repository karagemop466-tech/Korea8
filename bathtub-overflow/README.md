# Bathtub wastewater overflow trip lever — requirements, vendor and code dossier

A self-contained dossier for a San Francisco job: a bathtub waste-and-overflow trip lever stuck inside concealed
plumbing behind the wall, in an occupied rental unit, where the owner needs **one licensed contractor** who can cover
both the plumbing and the drywall.

The dossier answers three questions: what the job must satisfy, who can legally do it, and what it costs.

**Live site:** <https://karagemop466-tech.github.io/Korea8/bathtub-overflow/>
**Executive summary:** [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) · **Sources list:** [`SOURCES.md`](SOURCES.md)

---

## Layout

```
bathtub-overflow/
├── data/                     # the single source of truth (JSON)
│   ├── sources.json          #   46 sources: official (24) + review platforms (22)
│   ├── requirements.json     #   34 requirements in 7 categories
│   ├── vendors.json          #   14 contractors with their official CSLB record
│   ├── costs.json            #   owner estimates, official DBI fees, cost drivers
│   ├── code_facts.json       #   CF-01…CF-18, code / permit / tenant-entry facts
│   ├── findings.json         #   F-01…F-14, what the evidence shows
│   └── flagged.json          #   FL-01…FL-22, unverified values and contradictions
├── scripts/
│   ├── build_site.py         # renders data/*.json into the HTML pages
│   └── verify_site.py        # 61 mechanical checks; exits non-zero on any failure
├── evidence/
│   └── verification.json     # the last verification run (checks + results)
├── index.html                # dashboard landing page (Executive summary + next actions)
├── scope.html                # requirements by category
├── vendors.html              # vendor shortlist, one CSLB record link per row
├── costs.html                # estimates, official DBI fees, cost drivers
├── code.html                 # code, permit, licensing and tenant-entry rules
├── findings.html             # findings with evidence and implications
├── flagged.html              # Flagged for Review
├── sources.html              # every source, with publisher, date and what it verifies
├── style.css
├── README.md
├── EXECUTIVE_SUMMARY.md
└── SOURCES.md
```

## Rebuild and verify

```bash
python3 bathtub-overflow/scripts/build_site.py    # data/*.json -> the HTML pages
python3 bathtub-overflow/scripts/verify_site.py   # 61 checks, exit 1 on any failure
```

`verify_site.py` fails closed and writes `evidence/verification.json`. It checks that:

* every rendered table row carries at least one source link;
* every source reference resolves to a real entry in `sources.json` or to an https URL;
* every vendor row points at an official CSLB licence page, and every flag id exists in `flagged.json`;
* a vendor with no established licence is flagged, and a suspended licence is marked do-not-hire;
* rendered row counts equal the JSON row counts;
* no internal link is broken;
* no placeholder text survives;
* no internal project information appears in any published file.

## Rules the data follows

1. **Every table row has a source link.** If a row has no official source, it carries a flagged item instead.
2. **Blank means unverified.** A value that could not be confirmed from an official source is left empty in the data and
   explained on the Flagged for Review page. Nothing is inferred or filled in.
3. **Official is not the same as non-official.** `sources.json` marks each source; review-platform figures (Yelp, BBB,
   HomeAdvisor) are supporting evidence only, always dated, always flagged. They were captured from search-index
   snapshots because those sites block automated retrieval.
4. **Licences are read, not assumed.** Vendor licence status, classifications, bond, workers-compensation status and
   complaint disclosure come from the CSLB licence-detail page linked in that row ("Data current as of 11/6/2026").
5. **Public verification only.** Sensitive personal owner details are excluded from the repository; only verifiable code, fee, and licensing facts are published. See FL-21.

## Deployment

The repository's GitHub Pages site is published from the `main` branch, path `/`, so this subtree is served at
`https://karagemop466-tech.github.io/Korea8/bathtub-overflow/`. The geothermal pages that live at the repository root
are untouched by anything in this directory.

## Known limitations

Everything that could not be confirmed, every contradiction found between sources, and the handling decisions taken
during the research are listed on the Flagged for Review page (`flagged.html`, FL-01 … FL-22). The DBI FAQ wording
used here comes from an archived copy of the City's FAQ and must be reconfirmed with DBI — that is FL-02, and it is the
first call to make.

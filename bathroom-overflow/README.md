# San Francisco bathtub overflow research brief

Standalone static GitHub Pages subsite for a reported stuck bathtub trip-lever / waste-and-overflow repair. The repo's existing root project is a separate DOE GEMS research project; this work is isolated in this directory rather than overwriting the existing homepage or navigation.

## Pages

- `index.html` — executive summary and shortlist
- `providers.html` — provider comparison
- `scope.html` — service scope and questions
- `quotes.html` — quote log (unverified amount fields intentionally blank)
- `flagged.html` — unresolved and unverified items
- `sources.html` — official source register and verification method

## Local preview / checks

From the repository root:

```sh
python -m http.server 8000
# open http://localhost:8000/bathroom-overflow/
```

The subsite uses only local HTML/CSS and outbound source links. It has no build step, JavaScript dependency, analytics, or form that sends user data. Run the repository's existing tests separately; they validate the unrelated Korea8 research project, not this site.

## Publishing path

This repository's existing GitHub Pages source is the `main` branch root. Once this directory is merged into `main`, its expected URL is:

`https://karagemop466-tech.github.io/Korea8/bathroom-overflow/`

## Evidence rules

- CSLB official license-detail pages were opened and recorded on 6 November 2026; statuses/classifications are time-specific snapshots. Verify live records again before engagement.
- A provider's own website supports only its stated identity, services, contact details, and claimed service area. It does not establish willingness, availability, estimate, exact trip-lever competence, or a full restoration scope.
- Yelp links point to third-party listings/customer accounts, not official contractor evidence. A review is anecdotal and not independently inspected.
- The requester-supplied estimate amounts are not shown: no original quote was supplied and no official published amount was located. Their verified-value cells are intentionally blank.
- No provider was contacted; no appointment or site inspection was arranged.
- No private property address, occupant identity, or confidential administrative context is published.

# 2026-11-11 reproducibility and publication audit

## Executive conclusion

The existing canonical dashboard builds successfully from its checked-in data. The decision remains a **conditional contact shortlist**, not a finding that anyone has accepted this particular job. No provider has been contacted, booked or paid by this session.

- First inquiry: Ace Plumbing & Rooter; second: Heise’s Plumbing; third: Rapid Flow.
- Heise’s published ceiling-access waste/overflow case is the closest documented technical example in the existing dossier. Company-published work is not an independent customer review.
- A written combined plumbing/access/finish scope is still needed. License classifications alone do not confirm that a provider offers a complete small-job service.
- Owner reports of $614, $550 and $135 describe different scopes and are not independently verified quotations. Verified price fields remain blank.

These conclusions summarize the existing dated dossier. They are not fresh external verification. Review the linked official sources and the preserved 10 November receipts on the site's Verification page.

## What was actually checked in this session

1. Read the coordination board and latest completed integration receipts; inspected root pages, source datasets, canonical build/verifier, tests, publication staging and workflow. Unrelated DOE GEMS scientific evidence was not revalidated or changed.
2. Rebuilt all 11 canonical pages using `python scripts/build_overflow_site.py`.
3. Ran `python scripts/verify_overflow_site.py`: all 28 structural checks pass, including official-primary link coverage of 405 table rows, blank unverified values, internal links/anchors and HTML balance.
4. Ran `python -m unittest discover -s tests -p 'test_overflow*.py'`: 40 tests pass.
5. Ran `python audit/independent_audit.py`: 11 pages, 405 source-linked rows, no reported problems.
6. Ran `python scripts/stage_overflow_pages.py`: the linked public-file closure stages successfully. This is not proof that every file in the public Git repository is suitable for publication.
7. GitHub API confirms the baseline Pages build for `b4912259465a85efaa6d49f370c7ab276c16e324` is `built` without an error. The matching Actions run [42766836882](https://github.com/karagemop466-tech/Korea8/actions/runs/42766836882) completed successfully. API snapshots are retained alongside this report as `pages-before.json` and `build-before.json`.

## Verification limits and irregularities for review

- **External-source freshness:** this session's outbound network is restricted to GitHub and package registries. Contractor, CSLB, City, statute, manufacturer and Yelp pages cannot be directly re-read here. A direct GitHub Pages retrieval also failed. Existing provider/source check dates remain 2026-11-10; no current license-standing claim was newly verified in this session. Structural source-link coverage does not prove factual support or current external-link reachability.
- **Publication mode:** the GitHub Pages API still reports legacy root publication from `main`, alongside a successful Actions deployment. The staging allowlist alone therefore cannot establish that unlinked repository paths are unavailable. This existing issue remains documented in the Flagged for Review page; no repository privacy or access-control guarantee is made.
- **Open alternatives:** existing open PRs were not merged or closed. Their findings are not automatically verified by this audit.
- **Decision gaps:** assembly model/photos, exact access route, storage authority, ceiling assembly/materials, combined restoration responsibility, tenant-access arrangements, current availability and an itemized total price are not supplied or confirmed. No estimate is treated as including ceiling work merely because that work was not mentioned.
- **Ranking:** editorial decision support, not an independently validated performance score. No numeric Yelp rating/count was added.

## How to close the decision gaps

Send the site's prepared two-path scope request to the shortlisted licensed entities. Request exact-job references and written confirmation of tub-side stop conditions, below-ceiling access fallback, trade responsibility, protection of occupied spaces, applicable approvals, testing and full finish restoration. Require itemized costs, exclusions and written change-order limits. Verify legal entity, license and insurance on signing day. The site contains the question register and official lookup links; none of these unanswered items is silently converted to a fact.

## Publication receipt

The session's PR, merge and exact-commit workflow outcome are recorded in the repository's `COORDINATION.md`. Deployment verification relies on GitHub's workflow and Pages API receipts because direct Pages HTTPS access is unavailable in this sandbox.

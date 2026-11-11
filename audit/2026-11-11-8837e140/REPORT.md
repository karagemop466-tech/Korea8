# Line-by-line review and decision-question register — 2026-11-11

Session `arena/8837e140-korea8`. Branch fixed by the session; the `session-<id>/<task>` convention in the brief cannot be
used, so the claim was made in `COORDINATION.md` on this branch and pushed before any file was edited.

## 1. What this session added

`overflow-integration/data/questions.json` — a decision-blocker register of **27 questions**, published as a twelfth
canonical page at `questions.html`. Each row separates four things that the rest of the dossier keeps apart but never
lined up in one place:

| Field | Meaning |
|---|---|
| Question to settle | The decision-relevant question, stated as a question |
| What is already established | What the dossier already holds, with the source link for that row |
| What is still missing | The specific gap, not a general disclaimer |
| Answer | The answer if one exists; **blank and marked unverified if not** |
| How to obtain the missing answer | The cheapest concrete route to the missing information |
| Blocking / linked flags | High, medium or low, plus the existing flag identifiers that cover the same gap |

Answer status: **9 answered, 4 partially answered, 18 unanswered (published blank)**. Blocking: **13 high, 11 medium, 3 low**.
Every row's anchor URL is itself a registered official-kind source cited on that row, so the verifier's
"every table row has a registered official-primary source link" rule holds without exception.

## 2. Baseline before any edit

Rebased onto current `origin/main` (`b6d9b92`, PR #79) first, because `main` had advanced thirteen commits while this
session was reviewing. On the untouched rebased tree: build ok, `verify_overflow_site.py` **28/28**, tests **40/40**,
independent audit **0 problems**, wording guard clean. Every check below was re-run after the edits, so a green result
is attributable to this session's changes.

## 3. Checks run after the edits

| Check | Result |
|---|---|
| `build_overflow_site.py` | ok — 12 pages, 27 questions, 65 flags |
| `verify_overflow_site.py` | **35/35 PASS** (was 28/28; 7 new checks for the register) |
| `unittest discover -p 'test_overflow*.py'` | **45/45 OK** (5 new tests) |
| `audit/independent_audit.py` | 12 pages, **432/432 rows source-linked**, 246 internal links, **0 problems** |
| `stage_overflow_pages.py` | 48 linked public files, no repository internals staged |
| `wording_guard.py` | clean |
| `git diff --check` | clean |

## 4. Line-by-line verification performed

I re-derived every published claim from the raw data files rather than trusting the existing verifiers, and recomputed
the ranking from its own published weights and components.

1. **Source integrity.** 135 source records, 135 unique identifiers, no duplicate identifiers. Every identifier cited by
   any of the ten data registers resolves. No row cites an unregistered source.
2. **Flag integrity.** All 65 flag identifiers are unique and every flag identifier referenced by a provider,
   requirement, estimate, ranking, technical, compliance or question row exists.
3. **Ranking arithmetic.** Recomputed `A*0.30 + B*0.20 + C*0.20 + D*0.15 + E*0.15` for all ten ranked rows and the
   partner. The rendered order matches the recomputed order exactly: Ace 3.85, Heise's 3.45, Rapid Flow 3.15,
   Ayoob & Peery 3.15, We Do 2.95, Expert 2.90, Save-On 2.60, Bay Area 2.55, Fast Response 2.20, Discount 1.70.
   The one exact tie, Rapid Flow and Ayoob & Peery at 3.15, breaks on the published C2 component and is deterministic.
4. **Contact parity.** For all eleven ranked and partner identities the phone number in the ranking equals the phone
   number on the provider register. No identity in the hiring order is suspended or of unresolved identity.
5. **Blank discipline.** All three owner-supplied amounts appear as owner-reported with the verified-amount column
   blank. No numeric rating or review count appears anywhere. The three unresolved identities still hold blank licence,
   phone, expiry and status fields.
6. **The register itself.** Every question row is anchored to a registered official-kind source; no unanswered row
   carries an answer; no answered row carries an empty answer; no row cites a private or confidential matter.

## 5. Irregularities found and flagged

Five new flags, none of them introduced by this session's edits, all published on the Flagged for Review page:

| Flag | Severity | Finding |
|---|---|---|
| **F-70** | Medium | Source record `SF-CODE-104` is titled *San Francisco Plumbing Code §104.0 — Permits* and its retrieval note describes Plumbing Code §104.2, but its stored URL carries the **`sf_building`** library segment. Thirteen rows cite it. The §104.2 text itself is separately sourced from the city-hosted 2025 Plumbing Code PDF, so the content is sourced and only the deep-link path is questionable. |
| **F-71** | Low | Sixty flags are published and the highest identifier is F-69, but **F-56 through F-64 are absent**. The board records two renumbering passes during concurrent merges. No canonical file, generated page, audit file or linked document cites the missing range. |
| **F-72** | Low | **Four registered sources are cited by no row**: BPC §7114, BPC §7124.6 and two earlier audit reports. Nothing was deleted, because deleting a source would erase a citation trail. |
| **F-73** | Low | Two Yelp source records share one search URL under different titles while supporting different observations. |
| **F-74** | Medium | **This session could not re-read any external source.** All findings here are structural, traceability and consistency checks against receipts recorded by earlier sessions. |

Pre-existing and unchanged: **F-52/F-35**, the Pages root publisher serving repository files beyond the staged
dashboard closure.

## 6. Retrieval limitation, stated plainly

This sandbox resolved outbound traffic only to `github.com`, `api.github.com`, `codeload.github.com`,
`registry.npmjs.org`, `pypi.org` and `files.pythonhosted.org`. Every other host — `cslb.ca.gov`, `sf.gov`,
`leginfo.legislature.ca.gov`, `amlegal.com`, company sites, Yelp, BBB — returned a connection failure. **No agency,
company or review page was re-read by this session, and no claim of fresh external verification is made anywhere in
this report or in the register.** The per-row check dates already published on the site remain the record of when each
value was actually read. The register's question Q-27 states this in the same words to the owner.

## 7. What was not touched

No provider, estimate, compliance, requirement, ranking, review or technical row was altered. No provider, agency or
review platform was contacted. No open pull request was merged, closed or modified. No unrelated GEMS file was edited.

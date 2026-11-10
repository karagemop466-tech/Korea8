# Independent External Verification & Audit Report — 2026-11-10 (`6f4c9f79`)

- **Audit date:** 2026-11-10 (UTC)
- **Session branch:** `arena/6f4c9f79-korea8`
- **Baseline:** `origin/main` at `67b9e98` (PR #70)
- **Tasks:** `6F4-01`, `6F4-02`, `6F4-03`, `6F4-04` (`COORDINATION.md`)
- **No outreach / no booking / no inferred prices:** No contractor was contacted, quoted, scheduled, or paid. Owner-supplied estimates dated 2026-08-30 remain labelled owner-reported with `amount_verified: null`. Unverified fields (Yelp ratings/counts, unresolved contractor identities, concealed access-panel dimensions) remain blank and flagged.

---

## 1. Live Official & Primary Source Re-Verification Summary (`2026-11-10`)

Every record below was directly fetched live by this session via `fetch_page` on `2026-11-10`:

### 1.1 CSLB Official Licensing Records (`cslb.ca.gov`)
All **24 canonical CSLB records** plus **3 supplementary CSLB records** (`#787733` dissolved prior Heise's entity, `#954813` 24/7 Rooter & Plumbing Services Inc, and `#888630` George Salet Plumbing Inc) and **2 disclosure pages** (`#297604` `ComplaintDisclosure.aspx` and `CitationViolationDisclosure.aspx`) were retrieved directly from CSLB's updated **`11/9/2026 9:49–9:52 PM`** database snapshot:

- **23/24 prior active/suspended canonical records matched exactly** (`#1115649` Rapid Flow, `#829071` Ace, `#1089561` Heise's / Taro Group Inc, `#977638` Expert, `#757796` Bay Area, `#1024971` Fast Response, `#749536` Save-On-Interior, `#1096552` We Do, `#392967` Ayoob & Peery, `#995163` Bernal Hill, `#1106131` SF Building Group, `#1105133` HARP/24-7 SF Handyman, `#1009195` Advanced Plumbing future-suspension warning, `#379364` Caccia, `#966337` Flow Masters, `#1140843` Discount, `#1086935` FDL, `#961218` Precision, `#954385` Citywide, `#300647` Cahill, `#297604` D G Construction, `#1027286` Kenneth Asire bond-suspended since `08/16/2026`, `#1160613` Clever, `#868994` Atlas).
- **Correction to prior unmerged PR #66 note on Heise's (`#1089561`):** Unmerged PR #66 (`cslb-candidate-verification-2026-11-10.json`) incorrectly noted `#1089561` as issued `09/04/2014` expiring `09/30/2028`. Live CSLB `#1089561` (`11/9/2026 9:50:02 PM`) confirms **`Issue Date: 04/06/2022`**, **`Expire Date: 04/30/2028`** — matching the canonical register on `main`.
- **Supplementary CSLB records verified live (`11/9/2026 9:52:21 PM`):**
  - `#787733` (`HEISE'S PLUMBING INC`): Expired `03/31/2023`, canceled and Secretary of State dissolved `02/12/2025`.
  - `#954813` (`24 / 7 ROOTER AND PLUMBING SERVICES INC dba A & R PLUMBING`): Current and active (`C-36`, `A`, `C-61/D-56`), SF (`1070 Quesada Ave`), `(415) 586-6851`, issued `11/18/2010`, expires `11/30/2028`, WC current to `07/01/2027`.
  - `#888630` (`GEORGE SALET PLUMBING INC`): Current and active (`C-36`, `C-16`), Brisbane CA, `(415) 334-0733`, issued `12/21/2006`, **expires `12/31/2026`** (inside near-term hiring window), WC current to `01/28/2027`.
- **Unverified discovery identities kept strictly blank (`F-52`):**
  - `C J's Plumbing & Rooter Service`: `https://cjplumbing.net/` served a GoDaddy "Launching Soon" placeholder with no CSLB license published; regulated fields left blank.
  - `Golden Gate Plumbing & Rooter Inc`: `http://www.goldengateplumbing.net/` failed to load; regulated fields left blank.
- **Clean `#297604` citation URL (`DG-CITATION`):** Replaced the abbreviated query string (which caused CSLB to render `"Invalid Parameters passed"` with blank metadata) with CSLB's exact `ComplaintDisclosure.aspx` link (`LicType=LIC&LicNum=297604&LmfPre=&Class=2&FiscalYear=2022&SeqNbr=2099&ActionCde=K&Status=FOR+DISCLOSURE+ONLY+PER+B%26P+CODE+7124.6&LicName=D+G+CONSTRUCTION+CO&StatusDt=03/23/2023`), confirming **`B&P Code 7114.A — Aided and abetted non-licensee`** cleanly.

### 1.2 Statutes, Municipal Codes, Agency & Manufacturer Docs
- **`BPC §7059(a)` & `16 CCR §831` (`BPC-7059`, `CSLB-831`):** Directly retrieved from `leginfo.legislature.ca.gov` and CSLB rulemaking notice (`CSLB_-_BESS_-_Notice_-__OAL.pdf`). Confirms specialty contractors (`C-36`) may perform another craft/trade only when **"incidental and supplemental"** — defined by `16 CCR §831` as **"essential to accomplish the work in which the contractor is classified."** Added as `C-15` in `compliance.json` and integrated into `requirements.json`, `technical.json`, and `flags.json`.
- **City-hosted `2025 San Francisco Plumbing Code PDF` (`SF-CODE-104-PDF`) & `2025 SFBC Amendments PDF` (`SF-CODE-106-PDF`):** Directly retrieved from `media.api.sf.gov`. Confirms §104.2 nine-item exempt list (conditioned on not cutting into or removing piping), §104.1 1-day emergency permit filing, §104.1.1 owner-occupied single-family homeowner permit limit, and §104.5 fixture-replacement fee condition.
- **`SFBC §106A.2(8)&(10)` (`AmLegal 0-0-0-92027`, chunk 39):** Directly verified verbatim: `(10) Minor repairs to existing interior plaster or wallboard, except when part of a fire-resistive assembly.`
- **`SF.gov` permit pages & DBI Table 1A-C (July 2026 PDF):** Directly retrieved. Confirmed `2026-11-11` Veterans Day office closure banner (`"CLOSED Veterans Day 11 NOV. Permit Services and inspections will resume operations on Thursday, November 12, 2026."`), PermitSF AUTH rules, remodel permit rules (including R-2 apartment owner plumbing prohibition), and all five Table 1A-C fee rates (`1P $290`, `11P/M $320`, `$519/hr`, `$555/hr`, `$259/half-hr`).
- **`BPC §§7048, 7057, 7057.5, 7114, 7124.6` & `CIV §1954`:** Directly retrieved verbatim on `leginfo.legislature.ca.gov`.
- **`CSLB B / C-9 / C-36 / FastFacts-GeneralB.pdf / Contracts / Finding`:** Directly retrieved on `cslb.ca.gov`.
- **`Watco 500/501/600TL` PDF & `EPA RRP / Asbestos`:** Directly retrieved; `aa.iapmo.org` re-tested (still behind members-only login wall; access-panel dimensions remain unverified/blank).

### 1.3 Company Websites, Third-Party Directories & Live GitHub Pages
- **Broken `HEISE-PANHANDLE` URL fixed:** `sources.json` previously linked `https://www.heisesplumbing.com/projects/plumbing-repair-and-replacement/171358/` which returned **Page Not Found (404)**. Replaced with the working live URL `https://www.heisesplumbing.com/recent-jobs/projects/the-tub-waste-and-overflow-assembly-171358/`, which verifies the Panhandle tub waste-and-overflow replacement (while still carrying Heise's embedded footer 404 block).
- **New `HEISE-FIXTURES` page verified:** `https://www.heisesplumbing.com/plumbing-fixtures/` directly retrieved; explicitly advertises *"Tub spouts, overflow plates, drain assemblies, and faucet sets replaced cleanly without unnecessary damage to surrounding tile"* and `(415) 333-0704`.
- **BBB & Angi re-checked (`2026-11-10`):**
  - **BBB Expert (`BBB-EXPERT`):** Now displays **`10/31/2028`** license expiration matching CSLB `#977638` (earlier sessions observed a stale `10/31/2026` date on BBB; `RV-16` and `BBB-EXPERT` updated accordingly).
  - **BBB Ace, Heise's (including misfiled Instagram/Meta complaint `#25014268` and canceled `#787733`), Fast Response, We Do, Ayoob & Peery, Bernal Hill, Atlas (including answered `$295` flush/warranty complaint):** All directly confirmed. `24/7 Rooter` BBB URL returned 404.
  - **Angi (`ANGI-SF`, `ANGI-ACE`, `ANGI-FAST`, `ANGI-BERNAL`, `ANGI-ATLAS`):** Directly confirmed; `ANGI-SF` notably lists `Kenneth Asire Plumbing` with positive reviews while official CSLB `#1027286` is bond-suspended — reinforcing strict CSLB-first verification.
  - **Yelp (`YELP-ACE`, etc.):** Returned **HTTP 403** again on `2026-11-10`. Numeric ratings/counts remain strictly blank (`null`).
- **Live GitHub Pages check (`https://karagemop466-tech.github.io/Korea8/`):**
  - Prior to this update, `index.html` served `24 CSLB / 112 sources / 51 flags` (`reviewed 2026-11-10`), **and** because legacy Pages builds resumed succeeding (`1e7f03f`, `9f1e76d`, `67b9e98`), `COORDINATION.md` and `project/EXECUTIVE_SUMMARY.md` were both publicly served from `/`! Updated `F-34` and mitigated `/project/EXECUTIVE_SUMMARY.md` with a clear non-destructive `Superseded` top notice.

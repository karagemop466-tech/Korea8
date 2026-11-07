import json, html, pathlib, sys
ROOT=pathlib.Path(__file__).parent
def L(name): return json.loads((ROOT/"data"/name).read_text())
prov, est, rules, req, flags = L("providers.json"), L("estimates.json"), L("rules.json"), L("requirements.json"), L("flags.json")
# enforcement: every row has a source URL
for p in prov["providers"]:
    assert p["cslb"].startswith("https://www.cslb.ca.gov/"), p["id"]
for r in rules["rules"]+req["requirements"]+flags["flags"]:
    assert r["source"].startswith("http"), r["id"]
for e in est["estimates"]:
    assert e["amount"]=="" , "estimate amounts must stay blank (unverified)"
CSS="style.css"
def esc(x): return html.escape(str(x or ""))
def page(title, body):
    nav=''.join(f'<a href="{h}">{t}</a>' for h,t in [("index.html","Dashboard"),("requirements.html","Requirements"),("estimates.html","Estimates"),("providers.html","Providers"),("rules.html","Rules & Technical"),("flagged.html","Flagged for Review"),("sources.html","Sources")])
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><link rel="stylesheet" href="{CSS}"></head><body><header><h1>Bathtub Overflow Trip Lever — San Francisco</h1><p>Consolidated brief · All licence data checked on official CSLB records 2026-11-07 · Unverified values are blank, never inferred</p><nav>{nav}</nav></header><main>{body}</main><footer><p>Sources are linked in every table row. Review-platform material is anecdotal only. Related parallel-session briefs in this repo: <a href="../index.html">root dashboard</a>, <a href="../bathtub/index.html">bathtub/</a>, <a href="../bathtub-overflow/index.html">bathtub-overflow/</a>, <a href="../bathroom-overflow/index.html">bathroom-overflow/</a>, <a href="../trip-lever/executive-summary.html">trip-lever/</a> — canonical-URL choice is flagged (F-10).</p></footer></body></html>'
def tbl(headers, rows):
    return '<table><thead><tr>'+''.join(f'<th>{esc(h)}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table>'
def src(url,label="CSLB record ↗"): return f'<a href="{esc(url)}">{esc(label)}</a>'
# index
cards=f'''<section class="cards">
<div class="card"><b>8</b><span>CSLB licence records checked 2026-11-07</span></div>
<div class="card"><b>{len(req["requirements"])}</b><span>requirements (RQ-01…)</span></div>
<div class="card"><b>3</b><span>owner estimates — amounts blank, unverified</span></div>
<div class="card"><b>{len(flags["flags"])}</b><span>flagged items for review</span></div></section>
<section><h2>Executive summary</h2>
<p><strong>Problem.</strong> A bath-tub waste-and-overflow trip lever (the lever on the overflow plate that raises/lowers a drop cylinder — the “plunger” — inside the hidden overflow tee) is stuck in plumbing concealed behind the tub wall. The unit is tenant-occupied; the space below is a storage unit, so below-access would mean opening its drywall ceiling.</p>
<p><strong>What is verified.</strong> Watco’s manufacturer instructions show the overflow plate, linkage and drop cylinder are serviced <em>through the overflow opening from inside the tub</em> (steps 5–7) — so a from-above attempt is the documented first move for those parts, without forcing anything that could damage the hidden tee/elbow (RULE-07). If the hidden tee/overflow elbow itself must be replaced, SF.gov states a permit is needed before cutting into or replacing pipes that will be covered by a wall, and a City-registered licensed contractor can obtain it online (Express Permit where eligible) (RULE-01/02).</p>
<p><strong>Who can do it all-in-one.</strong> California law lets a B (General Building) contractor prime a plumbing + drywall job when it involves two unrelated trades, when it also holds C-36, or when it subcontracts to a licensed C-36 (BPC §7057(b)). On CSLB records checked 2026-11-07, <strong>Save-On-Interior #749536 (B+C-36, same address/phone as Bay Area Plumbing #757796)</strong>, <strong>Rapid Flow #1115649 (B+C-36)</strong>, <strong>Ace Plumbing &amp; Rooter #829071 (B+C-36 + others)</strong> and <strong>Ayoob &amp; Peery #392967 (B+C-36, licensed since 1980)</strong> structurally fit the all-in-one requirement. None has been contacted; none has confirmed this exact job — those cells stay blank (F-03).</p>
<p><strong>Costs.</strong> The three owner-supplied estimates (dated as written 8/30/26) could not be confirmed from any official or provider-issued source, so their amounts are published blank and flagged unverified (F-01). Their scopes also differ, so they are not comparable (F-02). The next step is written, itemised re-quotes separating: from-above attempt, below-access work, ceiling patch/finish, parts, and permit/inspection fees (RQ-09).</p>
<p><strong>Tenant protection.</strong> Civil Code §1954: reasonable written notice (24 hours presumed reasonable) stating date, approximate time and purpose; normal business hours unless the tenant consents otherwise (RQ-08).</p>
<p><strong>Recommended order of contact.</strong> (1) The B+C-36 firms above — starting with the operator already associated with an owner estimate (P-02/P-02B) — asking first for a from-above attempt with a no-force limit; (2) the C-36 estimate firms (P-01, P-03) only with a named B/C-9 partner for any ceiling work. Ask every WC-exempt firm who will physically do the work (F-04). Do not start with P-07 until its CSLB Additional Status is resolved (F-05).</p></section>'''
(ROOT/"index.html").write_text(page("Dashboard", cards))
# requirements
rows=[[esc(r["id"]),esc(r["cat"]),esc(r["req"]),esc(r["status"]),src(r["source"],"Official source ↗")] for r in req["requirements"]]
(ROOT/"requirements.html").write_text(page("Requirements", "<h2>Full requirements list</h2><p>Every row links its governing official source. Owner-supplied requirements are labelled as such in Status.</p>"+tbl(["ID","Category","Requirement","Status / basis","Source"],rows)))
# estimates
prow={p["id"]:p for p in prov["providers"]}
rows=[]
for e in est["estimates"]:
    pid=e["provider"].split("(")[-1].rstrip(")")
    rows.append([esc(e["id"]),esc(e["provider"]),esc(e["scope_as_supplied"]),'<span class="blank">— blank —</span>',f'<span class="badge">{esc(e["status"])}</span>',esc(e["includes"]),src(prow[pid]["cslb"])])
(ROOT/"estimates.html").write_text(page("Estimates", f"<h2>Owner-supplied estimates (as written {esc(est['supplied_date_as_written'])})</h2><p>{esc(est['note'])}</p>"+tbl(["ID","Provider","Scope as supplied","Amount (USD)","Verification","Includes","Identity source"],rows)))
# providers
rows=[[esc(p["id"]),esc(p["name"]),esc(p["lic"]),esc(p["class"]),esc(p["status"]),esc(p["expires"]),esc(p["address"]),esc(p["phone"]),esc(p["wc"]),esc(p["all_in_one"]),("yes — amount unverified" if p["estimate_provider"] else "no"),src(p["cslb"])+(f'<br><a href="{esc(p["site"])}">Official site ↗</a>' if p["site"] else '<br><span class="blank">site not listed</span>')] for p in prov["providers"]]
(ROOT/"providers.html").write_text(page("Providers","<h2>Providers — CSLB-verified 2026-11-07</h2><p>All licence fields are from the official CSLB record linked in each row. Availability, job-specific experience and current pricing were not confirmed for any firm and are therefore blank/not claimed. Read current reviews manually via the <a href='https://www.yelp.com/search?cflt=plumbing&find_loc=San+Francisco%2C+CA'>Yelp San Francisco plumbing search</a> (anecdotal only, F-07).</p>"+tbl(["ID","Business","CSLB #","Classifications","Status","Expires","Address (CSLB)","Phone (CSLB)","Workers' comp","All-in-one (plumbing+drywall) assessment","Gave owner estimate?","Sources"],rows)))
# rules
rows=[[esc(r["id"]),esc(r["topic"]),esc(r["finding"]),src(r["source"],"Official source ↗")] for r in rules["rules"]]
(ROOT/"rules.html").write_text(page("Rules & Technical","<h2>Rules &amp; technical basis</h2>"+tbl(["ID","Topic","Finding (verified)","Source"],rows)))
# flagged
rows=[[esc(f["id"]),esc(f["item"]),esc(f["detail"]),src(f["source"],"Source ↗")] for f in flags["flags"]]
(ROOT/"flagged.html").write_text(page("Flagged for Review","<h2>Flagged for Review — irregularities &amp; unverified items</h2><p>These do not block publication. Each links a source for manual review.</p>"+tbl(["ID","Item","Detail","Source"],rows)))
# sources
seen=[]
for c in [prov["providers"],rules["rules"],req["requirements"]]:
    for r in c:
        u=r.get("cslb") or r.get("source")
        if u not in seen: seen.append(u)
rows=[[esc(u),'<a href="'+esc(u)+'">'+esc(u)+' ↗</a>'] for u in seen]
(ROOT/"sources.html").write_text(page("Sources","<h2>All sources used (official first)</h2><p>CSLB (cslb.ca.gov), SF.gov/DBI, California Legislative Information (leginfo), Watco Manufacturing. Checked 2026-11-07.</p>"+tbl(["URL","Link"],rows)))
print("built", 7, "pages,", len(prov["providers"]), "providers")

import json, pathlib, re, sys
R=pathlib.Path(__file__).parent; fails=[]
def chk(ok,msg):
    if not ok: fails.append(msg)
pages=list(R.glob("*.html")); chk(len(pages)==7,f"want 7 pages got {len(pages)}")
alltxt=""
for p in pages:
    t=p.read_text(); alltxt+=t
    for h in re.findall(r'href="([^"]+)"',t):
        if h.startswith("http") or h.startswith("#"): continue
        target=(p.parent/h.split("#")[0]).resolve()
        if h.startswith("../"): target=(p.parent/h).resolve()
        chk(target.exists(), f"{p.name}: broken internal {h}")
data={}
for n in ["providers","estimates","rules","requirements","flags"]:
    data[n]=json.loads((R/"data"/(n+".json")).read_text())
for p in data["providers"]["providers"]: chk(p["cslb"].startswith("https://www.cslb.ca.gov/"),"provider w/o CSLB "+p["id"])
for e in data["estimates"]["estimates"]: chk(e["amount"]=="","amount not blank "+e["id"])
chk("— blank —" in (R/"estimates.html").read_text(),"blank badge missing")
# wording check (shared guard: scripts/wording_guard.py)
sys.path.insert(0,str(R.parent/"scripts")); import wording_guard
chk(not wording_guard.scan_bytes(alltxt.encode("utf-8")), "wording outside the neutral repair-scope rule")
for name,n in [("providers",len(data["providers"]["providers"]))]:
    chk(f">{n}<" in (R/"index.html").read_text(), "count mismatch")
print(f"checks done, failures={len(fails)}")
for f in fails: print("FAIL",f)
sys.exit(1 if fails else 0)

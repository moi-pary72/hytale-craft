#!/usr/bin/env python3
"""Discover actual recipe catalog links and inspect schemas without guessing IDs."""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE="https://openhytale.org"
ROOT=Path("data")
ROOT.mkdir(exist_ok=True)
def fetch(path):
    url=urljoin(BASE,path)
    if urlparse(url).netloc!="openhytale.org": raise ValueError("untrusted host")
    req=urllib.request.Request(url,headers={"User-Agent":"HytaleCraftImporter/0.1","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read(15_000_001)
        if len(raw)>15_000_000: raise ValueError("oversized response")
        return json.loads(raw)
def paths_from_index(index):
    found=set()
    def walk(obj,depth=0):
        if depth>6:return
        if isinstance(obj,dict):
            for k,v in obj.items():
                if isinstance(v,str) and ("/api/" in v or v.endswith(".json")) and ("recipe" in v.lower() or "craft" in v.lower()):
                    found.add(v)
                if "recipe" in k.lower() and isinstance(v,str) and (v.startswith("/") or v.endswith(".json")):
                    found.add(v)
                walk(v,depth+1)
        elif isinstance(obj,list):
            for v in obj[:2000]:walk(v,depth+1)
    walk(index)
    return sorted(found)[:40]
def main():
    report={"checked_at":datetime.now(timezone.utc).isoformat(),"sources":{},"candidates":[]}
    for path in ["/api/meta.json","/api/catalogs.json","/api/search.json"]:
        try:
            data=fetch(path)
            info={"type":type(data).__name__}
            if isinstance(data,dict):info["keys"]=list(data)[:60]
            if isinstance(data,list):info["length"]=len(data)
            report["sources"][path]=info
            if path.endswith("catalogs.json"):
                (ROOT/"openhytale-catalog-index.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
                report["candidates"]+=paths_from_index(data)
            if path.endswith("meta.json"):report["meta"]=data
            if path.endswith("search.json"):
                report["search_index_recipe_examples"]=[x for x in (data if isinstance(data,list) else data.get("entries",[])) if isinstance(x,dict) and "recipe" in json.dumps(x,ensure_ascii=False).lower()][:3]
        except Exception as e:report["sources"][path]={"error":str(e)[:300]}
    report["candidates"]=sorted(set(report["candidates"]))
    report["candidate_results"]=[]
    for path in report["candidates"]:
        try:
            data=fetch(path)
            report["candidate_results"].append({"path":path,"type":type(data).__name__,"count":len(data) if isinstance(data,(list,dict)) else None,"keys":list(data)[:20] if isinstance(data,dict) else None,"sample":(data[:1] if isinstance(data,list) else {k:data[k] for k in list(data)[:1]})})
        except Exception as e:report["candidate_results"].append({"path":path,"error":str(e)[:180]})
    (ROOT/"recipe-discovery.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Catalog discovery:",json.dumps({"sources":report["sources"],"candidates":report["candidates"],"results":[{"path":r["path"],"count":r.get("count"),"error":r.get("error")} for r in report["candidate_results"]]},ensure_ascii=False))
    if not report["candidates"]:raise SystemExit("No recipe catalog path found in verified index; report saved")
if __name__=="__main__":main()

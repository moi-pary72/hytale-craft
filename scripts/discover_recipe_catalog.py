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
    raise PermissionError('Third-party collection disabled pending explicit rights and owner approval')
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
    raise SystemExit('Disabled: no third-party download or public snapshot write. Use import_catalog.py with authorized local JSON; review only.')

if __name__=="__main__":main()

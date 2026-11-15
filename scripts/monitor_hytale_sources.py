#!/usr/bin/env python3
"""Safe, scheduled Hytale source discovery and snapshot validation.

Never promotes a candidate to the live site without an explicit schema match.
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT=Path("data")
ROOT.mkdir(exist_ok=True)
SOURCES={
 "openhytale": ["https://openhytale.org/api/meta.json","https://openhytale.org/api/catalogs.json"],
 "hytale_source": ["https://hytale.source.gs/"],
 "hytaledb": ["https://hytaledb.net/"],
}
MAX_BYTES=8_000_000
def fetch(url):
    raise PermissionError('Third-party collection disabled pending explicit rights and owner approval')
    req=urllib.request.Request(url,headers={"User-Agent":"HytaleCraftSourceMonitor/1.0","Accept":"application/json,text/html;q=0.5"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            data=r.read(MAX_BYTES+1)
            if len(data)>MAX_BYTES: raise ValueError("response too large")
            typ=r.headers.get("Content-Type","")
            result={"url":url,"status":r.status,"bytes":len(data),"content_type":typ}
            if "json" in typ or data.lstrip()[:1] in (b"{",b"["):
                parsed=json.loads(data)
                result["json_type"]=type(parsed).__name__
                if isinstance(parsed,dict):
                    result["keys"]=list(parsed)[:50]
                    result["metadata"]={k:v for k,v in parsed.items() if k.lower() in ("version","build","updated","updatedat","generatedat","timestamp","count") and isinstance(v,(str,int,float))}
                    if url.endswith("/catalogs.json"):
                        (ROOT/"openhytale-catalog-index.json").write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+"\n")
                elif isinstance(parsed,list):
                    result["count"]=len(parsed)
                    if url.endswith("/catalogs.json"):
                        (ROOT/"openhytale-catalog-index.json").write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+"\n")
            return result
    except (urllib.error.URLError,TimeoutError,ValueError) as e:
        return {"url":url,"error":str(e)[:250]}
def main():
    raise SystemExit('Disabled: no third-party download or public snapshot write. Use import_catalog.py with authorized local JSON; review only.')

if __name__=="__main__":
    main()

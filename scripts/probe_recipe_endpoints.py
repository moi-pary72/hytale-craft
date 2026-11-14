#!/usr/bin/env python3
"""Inspect candidate OpenHytale recipe endpoints; never publish unvalidated data."""
import json
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = "https://openhytale.org/api/"
PATHS = ["catalogs/recipes.json", "recipes.json", "catalogs/recipes", "recipes", "catalog/recipes.json", "catalog/recipes"]
HEADERS = {"User-Agent": "HytaleCraftDataSync/0.2"}
OUT = Path("data/recipe-probe.json")

def inspect(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as res:
            raw = res.read(12_000_001)
            if len(raw) > 12_000_000:
                return {"path": path, "error": "Response exceeds 12 MB"}
            data = json.loads(raw)
            info = {"path": path, "http": res.status, "bytes": len(raw),
                    "type": type(data).__name__}
            if isinstance(data, list):
                info["count"] = len(data)
                info["sample"] = data[:2]
            elif isinstance(data, dict):
                info["keys"] = list(data)[:30]
                info["sample"] = {k: data[k] for k in list(data)[:2]}
            return info
    except (urllib.error.URLError, ValueError, TimeoutError) as exc:
        return {"path": path, "error": str(exc)[:350]}

def main():
    results = [inspect(p) for p in PATHS]
    report = {"checked_at": datetime.now(timezone.utc).isoformat(),
              "source": BASE, "results": results}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for r in results:
        print(r["path"], r.get("http", r.get("error")), r.get("count", ""), r.get("keys", ""))
    if not any(r.get("http") == 200 for r in results):
        raise SystemExit("No candidate recipe endpoint worked; inspect report")

if __name__ == "__main__":
    main()

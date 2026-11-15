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
    raise PermissionError('Third-party collection disabled pending explicit rights and owner approval')
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
    raise SystemExit('Disabled: no third-party download or public snapshot write. Use import_catalog.py with authorized local JSON; review only.')

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Probe OpenHytale's public catalog API without publishing unverified recipes."""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://openhytale.org/api/"
OUT = Path("data/source-status.json")
HEADERS = {"User-Agent": "HytaleCraftDataSync/0.1 (+https://github.com/moi-pary72/hytale-craft)"}

def fetch(name):
    req = urllib.request.Request(BASE + name, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
        body = response.read(8_000_001)
        if len(body) > 8_000_000:
            raise ValueError("Response too large")
        return json.loads(body)

def main():
    status = {"checked_at": datetime.now(timezone.utc).isoformat(),
              "source": BASE, "status": "unavailable", "catalogs": [],
              "recipe_catalog_candidates": [], "note": ""}
    try:
        catalogs = fetch("catalogs.json")
        meta = fetch("meta.json")
        if not isinstance(catalogs, (dict, list)):
            raise ValueError("Unexpected catalogs JSON type")
        status["status"] = "reachable"
        status["meta"] = meta
        entries = catalogs if isinstance(catalogs, list) else (
            catalogs.get("catalogs", catalogs))
        if isinstance(entries, dict):
            entries = [{"id": k, "details": v} for k, v in entries.items()]
        if not isinstance(entries, list):
            entries = []
        status["catalogs"] = entries[:150]
        status["recipe_catalog_candidates"] = [
            entry for entry in entries
            if "recip" in json.dumps(entry, ensure_ascii=False).lower()
        ][:20]
        status["note"] = ("Source metadata verified. Recipe records are NOT yet "
                          "imported or exposed to the calculator.")
    except Exception as exc:
        status["note"] = f"{type(exc).__name__}: {exc}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps({"status": status["status"],
                      "recipe_candidates": len(status["recipe_catalog_candidates"]),
                      "note": status["note"]}, ensure_ascii=False))
    if status["status"] != "reachable":
        raise SystemExit(1)

if __name__ == "__main__":
    main()

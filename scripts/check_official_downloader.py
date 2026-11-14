#!/usr/bin/env python3
"""Check official Hytale downloader availability without credentials or game download."""
import io
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

URL = "https://downloader.hytale.com/hytale-downloader.zip"
OUT = Path("data/official-downloader-status.json")
status = {"checked_at": datetime.now(timezone.utc).isoformat(), "source": URL,
          "downloadable": False, "contains_linux_binary": False,
          "authentication_required_for_game_assets": True,
          "game_assets_downloaded": False}
try:
    request = urllib.request.Request(URL, headers={"User-Agent": "HytaleCraftSourceCheck/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        content = response.read(25_000_001)
        if len(content) > 25_000_000:
            raise ValueError("Downloader archive exceeds 25 MB limit")
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = archive.namelist()
        status["downloadable"] = True
        status["archive_entries"] = names[:40]
        status["contains_linux_binary"] = any("linux" in name.lower() for name in names)
        status["note"] = "Official downloader archive verified. Game assets require separate OAuth authorization."
except Exception as exc:
    status["error"] = f"{type(exc).__name__}: {exc}"[:350]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(status, ensure_ascii=False))

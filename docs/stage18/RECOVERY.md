# Real Data Lab preservation and recovery

## What survives

On2026-11-16 the prior private source exports and `research-build/research-data.json` were present. All three raw hashes match the pinned [manifest](RESTORE_MANIFEST.json). The old build is preserved, not replaced. A fresh Stage18 build re-created the exact same normalized payload SHA-256 `65f5f3774f1e1afa470f03640fe249a8959960c884d978fe5b9e15c62adc314b` with pinned normalization date2026-11-16. UI assets/code are separate and may change without changing game records.

**This is not a durable full-data backup.** Raw/normalized real data live only in the restricted workspace. A code ZIP on Drive cannot recover source bytes if both the workspace and export URLs disappear. Full HySphere data is deliberately not uploaded to Drive or public archives while storage/redistribution conditions remain unresolved. The manifest has only source URLs, counts and hashes, no recipe content. No real CI artifact is created.

## Resume in this workspace

```sh
python3 scripts/verify_real_data_lab.py .private/real-data-lab
python3 scripts/verify_real_data_lab.py .private/real-data-lab --rebuild .private/stage18/restored-new
python3 scripts/serve_real_data_lab.py .private/stage18/restored-new --port 8765
```

Output directory must not already exist; builder preserves old versions. Only127.0.0.1 is served. Never tunnel or upload this directory. A browser openinglocalhost on Android refers to the phone, not the workspace. There is no public research preview.

## Recover in a clean checkout

1. Check out the Stage18 Draft branch (dependency PR17→PR16), with original assets intact. Python3.12 and standard library suffice to assemble/serve. Node22 is used for arithmetic tests. Mobile QA additionally needs Playwright1.56/Chromium; Pillow is only for contact sheets and source WebP conversion, not runtime. No app packages/build framework are required.
2. Re-read the source terms and robots policy before fetching. The known documented endpoints are in RESTORE_MANIFEST.json. Fetch only these explicitly offered files if access and intended private use remain permitted. No automatic downloader/collector was enabled by this stage. Do not use game archives, leaked mirrors or /api endpoints as a workaround.
3. Put each authorized original file under `.private/real-data-lab`, named manifest.json/items.json/recipes.json. Do not add them to Git or Drive. Their exact raw SHA-256 must match. If the endpoint now serves a different revision, STOP: preserve the existing manifest/snapshot, investigate the new source and create a separate reviewed version; do not merge builds or disable integrity checks.
4. Run the two verify commands above. The pinned date makes normalization deterministic across calendar dates. A mismatch fails without replacing an existing build. Private source files are bounded and duplicate JSON keys rejected.
5. Run synthetic public tests first, then opt-in real local QA. `node scripts/check_research_math.js` also needs the preserved historical private623snapshot for its independent legacy comparison; that historical snapshot is NOT included in the code backup. If absent, clearly report that comparison as unavailable rather than claiming a complete reproduction. Normalization/UI do not depend on that snapshot.
6. `python3 scripts/check_real_data_lab.py BUILD MATH_REPORT --output .private/stage18/screens` is local real-data QA only. Its output must stay private. Existing public CI uses invented fixtures only.

## Integrity scope

The verifier checks exact raw source hashes, normalization date, source revision, normalized hash and aggregate record metrics. The app verifies normalized SHA before parsing/rendering. Public builder checks original atlas SHA and other artwork manifests. No hash proves legal permission, current-game accuracy or source independence. Exact game build remains unknown. Source-backed638methods are not638officially game-verified/cleared recipes.

## Source replacement and user recovery

The source adapter, image resolver and user storage keys are independent. Disconnect hides research catalogue/calculations, retains original inventory/plan strings and can reconnect locally. Orphan/retired item IDs remain opaque; they are not automatically deleted or renamed. `withoutSource` returns a new dependency-filtered catalogue, never mutating the original input or user stock. An empty active catalogue is handled as a UI empty state rather than sent to the engine. The optional view preference has its own key `hytale-craft-item-view-v1`; no storage migration runs.

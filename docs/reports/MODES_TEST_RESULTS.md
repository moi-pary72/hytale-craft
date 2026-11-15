# Seeker / Maker release checks — 2026-11-15

PR11 completed before mode work: main `bba201f55bb15a2b619d8d6188cdc61b88e29c17`; validation43680781606 and Pages43680781504 successful. Both production hosts actually verified by HTTPS, manifest/content SHA and Chromium flows; no active queued/running collector jobs at merge. Rollback tag `backup/pre-modes-20261115` retained remotely.

## Local checks

- **38Python unit tests passed** (all available suites).
- **24JavaScript tests passed**: planner11, preview4, beta2, workspace7. New tests cover opaque IDs/limits, station metadata, projects and damaged stores, yield-aware dependency trees/cycles and all four mode dictionaries.
- **29Chromium integration tests passed**: existing25 plus4mode scenarios. Exact user-only dist under CSP; EN/RU/ES/PT-BR,320/360/393/430px, all10goals/all8Maker tools, mode persistence, shared recipes/inventory, projects/save/load, resource deficits, tree, user stations/editor, full/legacy backup restore, invalid import non-destruction and corrupt project raw recovery. Existing suite covers animated first/repeat action, Android-like Back, native sheet/keyboard/swipe/focus, storage errors, offline HTML, unavailable examples and corrupt translations. No page errors or horizontal overflow in checked flows.
- Real browser screenshot review corrected duplicate tile labels and lower frame padding in Maker. Approved ten Seeker illustrations/pose assets remain byte-identical (`git diff -- assets` empty).
- Slow mobile simulation:4×CPU,150ms latency,150000bytes/s download; Seeker decoded home ready4.293s, below15s gate. This is a controlled local run, not field/physical Android data. New Maker uses cached original art and no permanent animation.
- Root Cloudflare and GitHub `/hytale-craft/` builds pass exact publication audit: **41files,40content SHA checks**, fouroriginal educational examples, zero community snapshots/internal documents/archives/trackers. Repeated root builds produce identical manifests. New helper is explicitly allowlisted and included in standalone export.
- Repository data guard and scoped credential-signature scan pass. Five collectors stay manual read-only notices and blocked network entry points. Historical datasets in old refs remain a separate license/remediation issue; no history/backup/tag deletion or external letters.

## Publication gates and limitations

Both validation and Pages workflows run the new workspace and mode tests. Production uses only `python3 scripts/build_pages.py --data-policy user-only`, `dist`; existing Cloudflare main integration and GitHub Actions Pages. Exact PR/CI/main merge/live verification links are appended to the native project passport and PR. A local pass alone is not proof of publication.

No physical Android, IME or real screen reader was available. The structural tree expands branches separately; final shared stock/surplus is computed by the existing calculator. Stations are optional user-provided metadata; no invented game benches. Projects reference current user recipes and do not freeze recipe versions. Browser data stays per origin; use full export/import between hosts. No commercial real-data rights acquired, no real Hytale recipes published, no ads/analytics/paid features. Temporary noindex remains.

# Stage5 test results — 2026-11-14

Base PR4 `7744a5af2971a9eb2e3f515def15ea7da396c4f7`. New branch codex/approved-art-pair. No snapshot changed or source data published.

| Check | Actual local result |
|---|---|
| Python unittest | 20 passed:17 prior +3 art packaging/manifest/hash cases |
| JS planner and locale checks | 15 passed |
| Existing preview Chromium | 9 passed |
| Existing Pages output/CSP Chromium | 2 passed |
| Legacy mobile smoke | 1 passed |
| New art Chromium | 4 passed |
| JS syntax, JSON, git diff --check | passed |

New art scenarios cover four locales, widths320/360/393/430, two-column pair, eight pending-art goals, keyboard skip/focus, readable HTML labels, no horizontal scrolling or JS/console errors, no community fetch, no rejected SVG requests, no atlas request before interaction. Character frames change on interaction; only one action runs; stops after900ms, no looping. Navigation remains immediate. Reduced-motion and simulated Save-Data suppress playback; reduced-motion prevents atlas requests; disabling the toggle cancels a keyboard-started action; missing atlas keeps poster. User recipe editor/calculation survives reload. Offline HTML works with one document and zero subresource requests over local HTTP. Replay session recorded to WebM for owner demonstration, not loaded by site.

Startup resource budget ~115–119KB decoded (four locales differ),12requests, zero game-data requests. Two posters ~61KB combined, each atlas ~98–109KB fetched only on interaction. CPU4×/150ms/150000B/s: two posters decoded in **1.653s** locally. Offline review HTML≈461KB. Exact bytes/hashes and metrics: STAGE5_PERFORMANCE.json and assets/art-pair/manifest.json. First on-demand action waits for atlas download/decode; on slow networks this is not guaranteed immediate. Click navigation is not delayed.

Four poses are a deliberately limited flipbook motion sample, not a smooth rigged animation. Generated background/pose continuity needs art review. No final art approval, physical Android, full accessibility audit or native-language QA. file:// cannot be exercised in managed browser policy; Android file-viewer behavior remains owner's check. Full reference comparison is private Drive-only; raw reference images were not committed or deployed. Cloudflare builder excludes this new art review until approval.

## Remote CI / artifacts

Code checkpoint `1a978c9929d330052780ea1839945869c43b7509`: [GitHub Actions43588499509](https://github.com/moi-pary72/hytale-craft/actions/runs/43588499509) test job and all steps succeeded, including all mobile scenarios and video dependency installation. [Draft PR5](https://github.com/moi-pary72/hytale-craft/pull/5) targets PR4 branch. Drive uploads were metadata-readback verified; exact links/bytes/localSHA256 in STAGE5_DRIVE_BACKUPS.json. No Cloudflare or production publication.

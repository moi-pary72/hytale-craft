# Stage 3 tests — 2026-11-14

- Python unit tests: 14 existing tests, pass.
- Existing JS engine/source regression tests: 11, pass. 623 recipe snapshot/manifest and ID catalog are unchanged.
- New JS locale/SEO/scene tests: 4, pass (identical nonempty keys across EN/RU/ES/PT-BR, browser/manual locale matching, literal UI key coverage, strict missing-key detection, noindex/single sitemap URL and original local scenes).
- New mobile preview integration: 6 tests, pass locally. Four locales, 10 goals/two columns, keyboard skip/focus, widths320/393, complete real shortbow flow in all languages, inventory/clipboard/batch/reload, existing user data unchanged, editor/export/invalid import, delayed snapshot plan preserved, corrupt user JSON preserved, invalid/missing recipe snapshot fallback, self-contained export with one document request and zero subresources, CPU×4/150ms reduced motion.
- Existing mobile regression runs separately against index.html to detect regressions from metadata changes.
- Performance report: STAGE3_PERFORMANCE.json. Home decoded bytes ≈57–61KB, no game JSON before goal, no video/audio/iframe/continuous animation. Throttled local timings are not physical Android/Core Web Vitals certification.
- Layout/keyboard tested in Chromium; native screen-reader and physical Android QA not available. Dictionaries cover preview UI completely; native editorial sign-off is outstanding. Legacy interface retains partial EN/RU.
- Managed Chromium blocks file:// access; no bypass attempted. Export checked through local HTTP, no external subresources, real recipe works. Android local HTML viewer compatibility remains unverified.
- Full SHA/JSON/backup validation, git diff --check, GitHub CI results and verified Drive receipts are recorded after execution. No commercial/production launch is implied by tests.

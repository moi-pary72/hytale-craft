# Stage 4 test results — 2026-11-14

Baseline: PR2 d90e0105 + PR3 7267f289; work branch codex/cloudflare-testing-ready. No source snapshot changed.

| Check | Actual local result |
|---|---|
| Python unittest discover | 17 passed (14 existing + 3 Pages packaging cases) |
| JS planner/source-backed regression | 11 passed |
| JS four-language/SEO checks | 4 passed |
| Preview Chromium integration | 9 passed |
| Actual Pages output Chromium + CSP | 2 passed |
| Legacy mobile browser smoke | 1 passed |
| git diff --check / JS syntax / JSON | passed |

Widths **320, 360, 393, 430**: two goal columns, no horizontal scroll. Four dictionaries have 119 matching nonempty keys; manual locale preference persists and browser regional detection falls back correctly. Keyboard skip link/focus and semantic native buttons/select/forms are tested. No unfinished FR/DE/Chinese selector choices. Native-speaker review remains pending.

Preview scenarios cover all ten goals, stale-card regression, Crude Shortbow direct card, quantities, inventory/missing resources, nested real smelting, surplus/batches/cycles (engine tests), saved inventory/recipes/plans after reload, editor/export/invalid import, corrupt user storage preservation, external editor updates, missing/bad snapshot and malformed ID metadata, slow JSON, request timeout and retry. SHA-256/schema checks preserve source isolation and incomplete-recipe warnings. Self-contained review HTML runs through local HTTP with one document request and no subresource requests.

Pages tests exercise the actual allowlisted output with an applied test CSP: four locales, all goals, user-only no community fetch, editor persistence/calculation, widths, 404 and inaccessible internal docs/database. Unit tests verify output hashes, data mode, explicit noncommercial snapshot inclusion and invalid origin rejection. CI runs these tests but has **no deployment job**.

Performance receipt: `STAGE4_PERFORMANCE.json`; first-screen decoded resources about 61–65KB, zero database requests before a goal. CPU4×/150ms/150000B/s readiness measured locally at 1.171 seconds, zero continuous animations. Separate real JSON test uses 200ms/400000B/s. These are emulations, not guarantees for every weak phone.

## Limits

No physical Android, real Cloudflare account/deploy/TLS/header test, native-language QA or complete WCAG audit. File:// is unavailable under managed browser policy; offline HTML is validated via local HTTP, Android downloaded-file behavior needs owner testing. No public preview URL was created: owner review is an autonomous HTML on Drive, not a hosted deployment. Full-data artifact retains the snapshot licence restrictions. All data/build SHA and upload receipts are in Stage4 Drive manifest; remote connector metadata confirms name/size/parent but exposes no remote checksum.

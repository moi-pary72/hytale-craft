# Stage 4 independent audit — 2026-11-14

## Baseline actually inspected

- main `1c9c1e035207b954894fdba225ceca2dc4742f38`.
- draft PR2, `codex/verified-catalog-planner`, `d90e0105ec9c9a4283e0f142fdc4092df471c77b`.
- draft PR3, `codex/international-ux-preview`, `7267f2891b0edd9d91d3616ea4c21e5353a420c3`, base PR2 branch.
- Stage4 is a separate branch `codex/cloudflare-testing-ready` based on PR3. No branch below it was modified. Actual HTML, engines, workflows, source metadata and tests were read, not only previous reports. Existing Drive folder/passport and Stage3 history were inspected.

## Confirmed defects fixed

1. Switching goals after selecting an item left the previous item card open under a different goal/category. Goal selection now clears selection/results before rendering. Regression exercises all ten goals.
2. The ID catalog was only partially shape-checked; malformed source dates or names could crash metadata rendering. Validation occurs inside each settled source promise, and malformed data fall back safely. Recipe schema validation additionally checks names, extraction date type, station rows, material rows and incomplete-record shape.
3. New preview kept an in-memory recipe database and could overwrite recipes saved by the legacy interface/another tab. It now rereads storage before save/delete/import/calculation, listens for cross-tab storage events, preserves external edits and asks the user to review before retrying a save. Inventory updates clear stale result displays. The existing storage keys are unchanged. This is best-effort browser concurrency, not a transactional multi-tab database.
4. Add-to-plan could replace a storage failure warning with a success notice. Success is now reported only after saving succeeds.
5. Data requests had no upper wait bound. Fetch/body reads now have abort timeout and response size guard; failure does not erase the pinned repository snapshot or user data. Retry clears the old card/index before reloading.
6. Directly publishing repository root would serve the old interface and internal documents. New explicit builder emits only runtime files, writes the new preview as `dist/index.html`, excludes legacy/internal sources, and provides a real 404, CSP, noindex and build hashes.

## What remains deliberately unchanged

623 source-backed HySphere recipes, 3219 items, 1486 incomplete/unsupported records, original IDs and SHA-256 snapshot remain unchanged. This is community-extracted dated data, not an independently verified official Assets.zip database; exact game build is unknown. Separate OpenHytale catalog remains 3641 item IDs and 403 recipe IDs without ingredients. Do not sum overlapping item counts or mix dated sources in one recipe plan.

Crude Shortbow opens directly from Fight → weapons (category selected automatically), displays real source inputs, permits quantity/inventory/plan. Unsupported items show missing recipe and own-recipe action. Explore/enemy/skills goals are navigable with explicit planned guidance; no boss/progression walkthrough was fabricated. Full community owner preview remains available; the default future Pages artifact is user-recipes-only pending publication rights.

## Verification scope and limits

See `STAGE4_TEST_RESULTS.md` and machine-readable performance receipts. Local Chromium emulates touch/mobile widths; no physical Android. Browser tests cover bad/missing JSON, fallback, user data after reload, keyboard skip/focus, source-backed calculations, cycles/yields/surplus, all four language dictionaries, source isolation and actual deploy output. No automated test proves native translation quality, legal permission, actual Cloudflare configuration or on-device file handling. No production deploy, merge, ads, analytics, outreach or paid service was performed.

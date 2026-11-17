# Stage 23 — bounded public crafting paths

Progress: implementation and local validation complete; CI and deployed-version verification pending.
Baseline/rollback: b1dea8a3f704c699060be586446faf696a4918bd. Main artwork, ten tiles and storage keys preserved.

## Public selection

7 real item identities, 4 source-reported ingredient compositions, **0 fully game-verified recipes**. Four populated themes: fight, defend, gather, workshop. Original category art is identified as illustrative, not official item imagery. No Survival availability is inferred.

The existing sword and iron helmet citations are supplemented by two intermediate compositions:
- https://hytale.source.gs/items/iron-ingot/ — Iron Ore ×1; Furnace.
- https://hytale.source.gs/items/light-leather/ — Light Hide ×1; Tanning Rack.
- https://hytale.source.gs/items/iron-ore/ — Ore_Iron identity.
- https://hytale.source.gs/items/light-hide/ — Ingredient_Hide_Light identity.
- https://hytale.source.gs/items/iron-sword/ and https://hytale.source.gs/items/iron-helm/ — existing bounded numerical references, item level20, durability120/100 respectively.

All citations identify Source build0.6.4-b27; current-game verification absent. Output quantities are not stated and remain null. An ingredient edge is a **local batch composition**, never a computed total raw-material requirement. No ore drops, spawn locations or unlocks are invented.

https://hytale.source.gs/terms/ allows linked numerical citations but restricts high-volume scraping/wholesale republishing. This narrowly reviewed selection is not permission to scrape100records. No source text, icons or bulk export is copied. Existing content approval is scoped by exact SHA-256 and counts. Any further data release needs review. Future monetization needs its own scope review.

## Paths and catalogue

Read-only indexed multilingual/ID search; result cap48, themed pagination; declared category art bindings; A/B/C/D badges. Collapsible vertical steps, ingredient navigation, source links, alternative method selection, unknown acquisition/output, version boundaries, depth/node budgets and cycle guards. No new calculator, user-storage migration or dependency library. Public paths do not write inventory/projects. Missing sources preserve user records.

## Private batch readiness

Existing restored research snapshot reused:3219items,2109source rows,638supported methods,1471quarantined source rows. Item-level classifications: A0/B637/C1480/D1102 (not recipe-row counts). Two self-input methods remain blocked: craft-Plant_Moss_Green, craft-Plant_Petals_Yellow. Exact game build unknown; do not mix it with the public Source build.

`scripts/prepare_catalog_batch.py SOURCE --output .private/NEW-BATCH` uses existing canonical-v2 validation, duplicate/reference checks and private-path enforcement. A requires independent observation in the trusted SHA-scoped review registry; provider licence declarations do not authorize publication. Existing outputs cannot be overwritten. Data backup remains the separately verified Stage22 recovery set; code is not a substitute for those data archives.

## Next authorized source

https://hytl.dev/developers and https://hytl.dev/developers/docs describe free authenticated metadata access, including commercial uses within rights the provider can grant. This is not blanket permission for game assets or third-party rights. No key is configured; zero HYTL records downloaded. `scripts/fetch_hytl_batch.py` prepares one documented100-record metadata page to private staging, refuses redirects and overwrites, stops on access/rate failures, and keeps credentials outside browser/Git. Raw provider response still needs a reviewed schema adapter and publication review. A key alone never auto-publishes.

Alternative checks: hytalewiki.info returns401 (no bypass); current official/community wiki content has noncommercial conditions. An open-source mod dataset is not a vanilla recipe catalogue. No new studio letter sent. The100-item target remains unmet; extending a restricted database is not used as a shortcut. Fastest next step: approved free HYTL metadata access or an explicitly authorized export, then a reviewed first100-record batch.

## Verification

See Stage23 release evidence and CI. Synthetic5000-item tests check bounded search/path cost, not physical Android performance. Browser checks use mobile Chromium emulation; no physical Samsung claim. Restricted research data and screenshots are excluded from public CI artifacts and release files.

Local results (2026-11-17):79 Python tests passed; all existing JavaScript suites and3new reference-index tests passed; reference mobile3tests, thematic mobile3tests and path mobile3tests passed. Four languages × four widths checked. Synthetic5000-record browser load+search1.426s under4×CPU slowdown, themed DOM capped48; this is emulation, not network/device benchmarking. Public build audit passed. Existing user-ID collision/source-failure regression retained. First sandbox-only Python attempt could not bind sockets; authorized rerun passed.

# Hytale Craft — product benchmark & verified-data policy
Updated: 2026-11-14

## What the competition already offers
- OrbisHytale (https://orbishytale.com/en/tools/): crafting calculator with workbenches and material locations, gear/build planners, "what can I do with this?" reverse lookup, mob and item comparisons.
- Almanauts (https://almanauts.com/hytale/crafting/): full crafting dependency tree, bench list, timing, inventory/surplus logic; examples checked against the game. Its data has explicit game-version stamps.
- Hytale Guide Wiki (https://hytaleguide.net/wiki): searchable database with thousands of item pages and per-patch updates.
- Hytale Source (https://hytale.source.gs/): extracted game-file item/recipe database, but its displayed release version may lag current game.
- Hytale Companion (https://hytalecompanion.com/calculator): add multiple items to a crafting queue.

## Our product differentiation
1. Searchable ready-to-use recipe catalog. The current user-only recipe editor is insufficient for launch.
2. Multi-item build queue and global deduplication of shared ingredients (round crafts only once across the queue).
3. Inventory-aware ingredient totals and leftovers, with clear crafting steps and bench requirements.
4. Reverse lookup: what can be crafted from a resource / current inventory.
5. Deep-linkable item/build plans, copyable checklist, local saves and JSON backup.
6. Fast mobile UX, English default with complete Russian translation; later pt-BR and es.
7. Version badge, source and verification status on every recipe, and patch-diff workflow.

## Data ingestion policy
- Do not scrape or bulk republish third-party copyrighted databases or icons without checking permission/license.
- Prefer official game files and explicit reuse licenses, or independently verified gameplay entries.
- Each recipe needs game_version, verified_at, source_url, output quantity, inputs, bench and optional duration.
- Never silently import older game-version data as current. Flag it as unverified/stale.
- No invented recipe values, drop rates, bench names or crafting times.
- Data and UI should be stored separately. Add automated validation and smoke tests before deployment.

## Immediate priorities
A. Fix i18n leftovers and test EN/RU including dynamic notifications, title, placeholder and copy/export.
B. Add catalog schema and first small verified dataset with per-record provenance.
C. Implement search, multi-target queue, merged calculation, bench list and version badges.
D. Build automated source/license/version validation, browser smoke tests, and accessibility checks.
E. Publish item-specific SEO pages only for records with verified data.

This document is an implementation benchmark, not evidence of competitor traffic or revenue.
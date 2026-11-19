# Stage 32 — Multi-target historical crafting list

## User problem and exact delivered scope
A player choosing three Iron Shields and two Iron Maces should see **one** combined shopping list rather than separately calculating each recipe and subtracting owned iron ingots twice.

The guide's **My crafting list** entry is visible directly on the homepage. For each of the eight carefully reviewed historical Hytale Update 2 (January 2026) recipes with documented output counts, a source-labelled item page now has **Add to crafting list**. The player chooses quantity, optionally a documented station method (Iron Mace Forge or Anvil), adds a target, and opens the persistent basket. The basket supports up to eight distinct targets, quantity editing, target removal, explicit list clear, owned stock editing (pre-filled from the existing saved inventory), combined totals and a copyable gathering checklist.

The basket is saved under a **new** localStorage key `hytale-craft-historical-basket-v1`, unrelated to recipes/inventory/saved projects. Its contents are optionally included in the existing full backup and restored only when schema/build/item/method checks pass; old backups are still accepted without the field. Neither the calculation nor copy action changes saved inventory or the player's separate personal-recipe plans.

## Arithmetic and safeguards
- All targets must have independently source-documented **positive output** and belong to **the exact same historical build label**. No Unknown-yield, unreviewed, other-version or future game-data records are promoted.
- Each recipe's input quantities are multiplied by integer craft batches, honoring output yield. The merged ingredients are summed across all selected targets **before** deducting the once-applied owned inventory. Total and stock bounds are checked; never turn unknown into zero.
- Example from published Update2 source figures: 3 Iron Shields + 2 Iron Maces need **32 Iron Ingots, 17 Light Leather, 15 Linen Scraps** directly. With stock of 5 ingots and 1 leather the shortage is **27, 16, 15** respectively.
- The historical basket **never** recursively expands to ore/hides/material extraction through old `0.6.4-b27` recipes. That would be a cross-version calculation. All source links, provenance badges, status information and existing item art are reused rather than copied.
- Warning in all EN/RU/ES/PT-BR variants: old Update2 figures do **not** prove availability or correct quantities in the current game; none has an independently current-build verified record.
- Invalid stored data is left untouched and explicitly flagged. A reset requires user confirmation. No scraping, paid service, unauthorized data import, external requests, or altered asset permissions.

## Test gates
- `tests/reference_catalog.test.js`: two-target merged total, once-only stock subtraction, method choice, missing/unknown output, wrong build and invalid quantity refusal.
- `tests/reference_browser.py`: actual mobile Chromium test across EN/RU/ES/PT-BR and 320/360/393/430 widths. Open two real historical cards, add 3+2 items, open basket, check direct totals and shortage, verify saved inventory unchanged, reload, change target quantity.
- Existing full CI, audited user-only production manifest, original Seeker/Maker navigation, saved recipes/inventory, local personal JSON reader and 100-item reference index must remain intact. Art PR #35 remains separate and owns `web/item-visuals.css`/image tests.
- No player-currency/creator-code/payment integration.

## Unfinished project-wide blockers
Issue #31 remains open: **zero** independently verified current-game recipes, no licensed full current-build 3219-item export cleared for public commercial use. This implementation adds a meaningful UX capability to the small previously reviewed subset, **not** a full game database or legal clearance. Source still requires permissioned current-game data acquisition and owner visual acceptance.

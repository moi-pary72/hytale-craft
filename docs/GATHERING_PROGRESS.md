# Stage 33 — Remembered gathering progress for the historical craft list

## Why this is useful for a player
After choosing several source-described crafting targets, the player now has an actual **offline gathering checklist** instead of a result that disappears on reload. For each material in My crafting list, the player can tap `+1`, `+5`, `−1`, or enter the exact amount collected. The basket immediately shows needed, owned and still missing, plus a native progress bar. Counts persist locally after closing and reopening the site. "Reset tracked amounts to saved inventory" discards the basket-only overrides and explicitly resamples current saved inventory.

## Safety and compatibility
- **Not** synced back into the player's global saved inventory. Progress is only an override stored inside the existing versioned `hytale-craft-historical-basket-v1` record. The separate `hytale-craft-inventory-v1` store, recipes, plans, projects and all other user state remain untouched.
- On first use, existing saved inventory counts are prefilled; after the player adjusts them, the basket's override becomes the source of truth for that material. This prevents unexpected resets when the user reloads.
- Older Stage32 baskets **without** a `stock` field still work. A new `stock` field is optional. Only nonnegative integers 0–999999 for ingredient IDs actually supported by the basket's reviewed source methods are accepted. Malformed stored records are preserved unmodified and flagged, never silently overwritten.
- Removing a target prunes progress records for no-longer-needed ingredient IDs; clearing the list resets all. Existing export/full backup already includes the whole basket object and restoration checks it via the same schema verifier, so no backup-version migration is needed.
- The plan can contain at most eight historically source-documented January 2026 Update2 recipes with known yields. **Zero** current-game independently verified recipes, no inferred ore/hide/drop chain, no unlicensed new data, no fake names or imagery. The warning remains visible in the basket in all four languages.
- No new network calls or developer dependencies, no external accounts, no writing to clipboard except existing explicit Copy button. No graphical image file changes; ART Issue #33 remains owned by second chat.

## QA
- Chromium regression in `tests/reference_browser.py`: EN/RU/ES/PT-BR, 320/360/393/430px viewports, +5/−1/typed, progress bar capped to target, persistence after reload, reset-to-inventory, main inventory localStorage unchanged.
- Browser check covers legacy Stage32 basket lacking stock, malformed item/stock data refusal with no automatic mutation.
- Follow exact-head PR CI and merged-main Pages deploy green; the owner still should visually inspect the mobile version, not accept a theoretical UX PASS.

Related: PR #34 single calculator; PR #36 multi-target basket; Issue #31 full verified legal game data remains OPEN.

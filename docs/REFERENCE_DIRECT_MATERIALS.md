# Direct historical recipe estimate — Stage 31a (owner-useful slice)

## What the player can do
On the ordinary Hytale Craft guide homepage, pick any of the eight individually sourced **Hytale Update 2 / January 2026** items with output quantity 1 (e.g. Iron Shield, Iron Daggers, Iron Mace, Iron Longsword, Iron Cuirass, Iron Greaves, Iron Hatchet, Iron Shovel). The item page shows a **direct material estimate**. Enter number of items to make and how much Iron Ingot / Light Leather / Linen Scraps is on hand. Previously saved inventory counts are prefilled for matching IDs. Click Calculate; see batches, output, each direct amount needed, owned and missing. Mace also supports its documented Forge versus Blacksmith's Anvil source choice.

No upload is required. No inventory or saved recipe is changed by this calculator. It's functional in all four languages, including 320px mobile widths. Its logic uses the reviewed *existing* public subset; neither a full 3219-item HySphere dataset nor unlicensed data is incorporated.

## Historical and legal limits — prominent in UI
- **Zero** current game-version independently verified recipes; all eight are January 2026 historical, source-documented only. Calculations are arithmetically valid **for the input source record**, not a guarantee about the installed game.
- Only first-order ingredients are counted. **No** recursive expansion to Iron Ore, hide, drops, forge time, stations required for intermediates, quantities across incompatible builds, or stock-saving side effects. If output count is unknown (e.g. previous Hytale Source 0.6.4-b27 Iron Sword), the estimator is deliberately hidden rather than guessing.
- Review source links on each item before using in a newer game build. User-verified recipes can continue through existing user recipe editor/canonical planner, separate from these historical reference numbers.
- Current private 3219-item research pack remains isolated and public-data source licensing still BLOCKED under Issue #31. This change is not a claim that the overall data completeness problem has been solved.

## Code and acceptance
- `web/reference-catalog.js`: deterministic `directMaterials` with strict positive integer quantity/output, batch rounding, source status, method choice, stock subtraction, bounds/no cyclic version mixing.
- `web/beta/app.js`: visible inline calculator next to historical ingredient card; source labelled, no persistent data changes.
- `tests/reference_catalog.test.js`: Shield qty3 yields 12 ingots, 9 leather, 9 linen; with stock 5 ingots,1 leather => missing 7,8,9; forge alternative; unknown output refused; batch rounding and invalid inputs.
- `tests/reference_browser.py`: EN/RU/ES/PT-BR item page, prefilled existing inventory, no localStorage mutation, mobile 320/360/393/430, old incomplete recipe lacks calculator.
- **CI green is a code gate only**. Verify actual mobile layout on owner's phone before claiming final UX success. Retain old local catalogue reader from PR #30 and the visible catalogue from PR #32.

This is a deliberately small source-limited functional milestone. The next stage of Issue #31 is permissioned current-build data ingestion, not fake mass imports.

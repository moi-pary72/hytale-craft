# Canonical crafting engine — release candidate, 2026-11-15

Owner authorizes tested code/function releases and allowed original data, not restricted game databases. Studio enquiry already sent by owner; response pending, no duplicate enquiry. Preserve the approved Seeker/Maker home, artwork, CSS, mode preference and legacy storage.

## Relationship to PR13

Research PR13 is **not merged**. Reviewed its17-file diff against main24200b4 and transferred only `scripts/import_catalog_v2.py`, its17unit tests and original synthetic fixture from exact head `efd5ca24375b22789677e153de9f14d5b320ca15`. No third-party dataset or research cache is transferred. This independent release branch is based on approved main, not on the research commit. The source investigation/rights limitations remain available in PR13 and the Drive passport.

## Engine and adapter

`web/planner-v2.js` implements pure local `HytaleCanonicalPlanner.compile/compute`. It accepts the canonical-v2 model, returns `totals` (raw resources still to acquire), `stock` (remaining inventory and outputs), `steps` (recipe batches), `consumed` (material ledger), `waste` (unused resource contribution, not reusable items), requirement checks and bounded-search diagnostics. Original item/recipe IDs remain opaque.

- Alternative recipes and input options are selected transactionally; failed/cyclic trial branches do not mutate shared state. Explicit recipe/member choices are honored. Default choice minimizes raw-item count then batches then unit waste among explored branches, with stable tie ordering.
- Material groups require confirmed membership and explicit mixed/single policy. Per-item resource units remain distinct from item counts. Existing group stock is used first, then whole-item rounded demand; excess contribution is reported and never turned into fictitious reusable stock.
- All outputs are credited once after all inputs exist; primary output is a reference, not another yield. Co-producing target goals are processed first; shared stock/by-products can satisfy subsequent goals and chains.
- Station any/all requirements, type, minimum level, categories/augment tags and knowledge/memory requirements are preserved. Missing metadata stays unknown. Material planning can show missing requirements; strict mode permits only confirmed available/unlocked routes.
- Salvage is disabled by default. Explicit opt-in is required, and selected salvage methods consume real available/intermediate items. Dynamic cycle/quantity/overflow/depth/branch limits stop unsafe plans; no partially fabricated result is returned.
- Limits:500goals/inventory IDs,10000records/table,100terms,50options,5000group members,2000trial branches,20000walk calls,100depth,1e12per-item quantity. No unbounded combinatorial search. Canonical category/augment arrays use all-of matching; this synthetic contract is not an inferred claim about every native engine field. An authorized native adapter must mark unknown native semantics unresolved.

**This is a bounded stock-first planner, not a globally optimal weighted-cost solver.** Different input order/alternative routes can yield feasible but non-minimal raw requirements. Seeded productive cycles/SCC optimization are not supported; choose an acyclic route or plan separate steps. Unknown native metadata/output-group semantics still require an explicit adapter/schema extension. These limits are shown in the learning panel; real-build correctness is not claimed without authorized data.

`web/canonical-adapter.js` keeps technical validation separate from publication authorization. Its legacy entry delegates to the unchanged `web/planner.js`; existing calculations and projects therefore keep their IDs/formats and results. Canonical calculation has no network or writes.

## Original learning data

`data/educational-canonical-v2.json`:5original imagined materials/items,1resource group,1practice station,4methods (craft,processing,co-product assembly,salvage), explicitly not Hytale. Data authored for this project under CC0; source provenance identifies original learning data, not a game build. Names in four UI dictionaries are original educational labels, not official game localization.

Public scope is **4existing learning recipes +4advanced learning methods =8educational records,0real Hytale recipes**. No HySphere/OpenHytale/foreign assets/icons/descriptions are bundled. Genuine source permission remains pending.

`data/educational-publication-approval.json` is separately reviewed trusted build configuration: original-synthetic kind, no game data, exact SHA/provenance. `scripts/canonical_publication.py` checks this approval, technical schema, original tutorial statuses and version/channel before packaging. Input JSON licence/status flags cannot approve publication. It is not a studio permission document or a cryptographic guarantee of human authorship; changing the registry requires code/rights review.

The builder packages only this approved payload as `web/beta/advanced-data.json`. The browser fetches it lazily, bounds its size, checks SHA and binds the parsed object to the exact approved bytes. Invalid/missing/tampered data fails closed in the new panel; the ordinary calculator remains usable. No arbitrary remote canonical import/automatic collector is enabled. Existing personal v1 recipe import remains available.

## Access and storage

Maker → Calculator → Advanced learning workshop; also under More. Uses the existing bottom sheet, HTML controls, Back/Escape/focus trap and lower navigation. No home tiles, artwork, CSS or animation assets changed. EN/RU/ES/PT-BR complete. Plan IDs can be entered or selected by translated label. The shared inventory remains the original key and is never decremented automatically by planning.

New independent `hytale-craft-advanced-v1` stores the learning plan, selected methods/material, quantity and requirement settings. It does not migrate or rewrite existing recipes, inventory, mode or saved projects. Unfinished plan text persists; malformed settings remain recoverable through full export. Full v1 backups add optional `advanced` raw settings; old backups without it leave current settings intact. Restore validates optional settings before any writes. Existing project schema/scopes are unchanged; canonical plans are separate saved workshop drafts, not silently converted legacy projects.

## Hosting and rollback

Same existing main integrations, user-only builder and exact publication allowlist; no new Cloudflare project, fees, ads or trackers. New scripts plus one original JSON are included; internal schema tooling/docs/tests/approval file/archives remain outside dist. Offline HTML export embeds the same approved data/configuration. No raw game archives or real recipe snapshots.

Pre-release remote tag `backup/pre-canonical-engine-20261115` preserves main24200b4. [Pre-release Drive backup](https://drive.google.com/file/d/1ALRwf92oZFHVE1F2aMtmyk6pALyckiS1/view) contains227verified source+dist files from that exact baseline, no Git history/disputed data. It was actually downloaded and CRC/SHA/allfiles verified before merge. Rollback is a normal revert/release, never force push or backup deletion.

See [tests](reports/CANONICAL_ENGINE_TEST_RESULTS.md) and [practical sources](PRACTICAL_DATA_OPTIONS.md). Exact final PR/CI/merge/deployment evidence is appended to the release PR and existing passport after verification.

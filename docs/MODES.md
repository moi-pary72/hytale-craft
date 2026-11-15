# Seeker and Maker — 2026-11-15

The default **Seeker** keeps the approved ten illustrated goals, two columns on phones, original two pose actions and direct goal → item → recipe/calculation in the existing accessible bottom sheet. **Maker** is a separate framed fantasy workshop home with eight entries: calculator, inventory, saved projects, recipe tree, required resources, stations, editor and transfer. Both use the same planner, sheet, inventory and user recipes. Mode and language changes do not migrate or reset user data.

## Storage and compatibility

- Mode: `hytale-craft-mode-v1`, `seeker` by default or `maker`.
- Existing `hytale-craft-recipes-v1`, inventory, demo/user active plans and session quantities/results retain their formats and keys.
- Saved projects: `hytale-craft-projects-v1`, JSON array, maximum30. Each `{id,name,scope,plan,updatedAt}` stores an active-plan snapshot and explicit `demo`/`user` source. Opening replaces only that scope's active plan; it does not change inventory or recipes. Projects reference current recipes, not an immutable recipe-version snapshot.
- User recipes can optionally include `workstations: [string,...]`, maximum20 names of100characters. The editor preserves other recipe fields; station names are user metadata, not verified game facts.
- Full v1 beta backups add optional `projects` containing raw JSON text. Existing backups without this field leave projects intact. Invalid imported projects are rejected before any writes. Corrupt existing project storage is preserved for raw export, not silently erased. Full backup restore is bounded to8MB; recipe-only imports remain2MB.
- UI labels in EN/RU/ES/PT-BR are separate from opaque user IDs. No automatic translation of user names or game IDs.

## Calculation semantics

The existing planner handles recursive yields, inventory, shared intermediate stock/surplus and cycle detection. The tree is a bounded structural view (500nodes,100depth); branches are expanded separately. Its explicit notice sends final inventory/surplus totals to the calculator. Required resources use the active scoped plan, or a single chosen recipe if no plan exists. Stations lists only metadata actually present in user recipes. The four original learning examples intentionally provide no fictional Hytale station requirements.

## Navigation and accessibility

Mode buttons expose `aria-pressed`; choice persists across reloads. Same native modal history/Back, Escape, swipe and focus trap; close restores focus to the corresponding goal/tool. Maker reuses existing original scenes and frame, no new third-party artwork or permanent animation. Reduced-motion and existing animation control remain honored. The lower navigation works in either mode and inside the panel.

## Publication and rollback

Owner explicitly authorized tested ordinary PR merges and main auto-deployment. PR11 merged normally at `bba201f55bb15a2b619d8d6188cdc61b88e29c17`, successful Pages run43680781504 and validation43680781606; both actual sites checked before mode work. Annotated remote rollback tag `backup/pre-modes-20261115` preserves that safe baseline. Rollback is a normal reviewed revert/release, never force push. Historic disputed snapshots in old Git refs remain a separately authorized cleanup issue.

Build only `python3 scripts/build_pages.py --data-policy user-only`, output `dist`; GitHub project path adds `--base-path /hytale-craft/`. Exact publication allowlist adds only `web/beta/workspace.js`. Four educational examples, zero real game recipes, no source catalog, internal docs, archives, ads, trackers or paid features. `noindex` stays. Same existing Cloudflare project and GitHub Pages; storage is per origin, use export/import to move between sites.

Physical Android/IME/screen-reader testing remains a device check; mobile Chromium does not establish physical-device compatibility. Commercial real-data rights remain unresolved. See reports/MODES_TEST_RESULTS.md for test evidence and the PR for exact merge/deployment status.

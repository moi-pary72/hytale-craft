# Stage18 — item visuals, deep workshop and private lab preservation

Research/Draft only. Branch `codex/stage18-visual-items` starts from PR17 `71e0d5e`; PR17 still depends on PR16 `891904a`; main `e1395d9` and public sites are untouched. No merge, deployment, collectors, paid tools, game archive or external enquiry. `CF-Pages-Skip` is preserved on branch commits.

## Implemented visual system

- Shared `web/item-visuals.js/.css` resolver decoupled from catalogue, engine and user formats. A:7 exact original lesson illustrations. B:15 original generic families (14requested plus workbench) in a16tile136,822-byte WebP including neutral. C: neutral branded medallion and CSS fallback if the image is missing. No downloaded game art or third-party catalogue image mappings.
- Category images carry visible ≈ and accessible/category disclosure; unknown images carry ?. Only exact original lesson mappings are individual. Unknown ores, unusual materials, essence, arcade machines and cauldrons stay neutral rather than unrelated objects. Iron/steel tool category silhouettes are generic; unsupported wood/bronze/rare tool/armour appearances are not guessed. No real item's exact appearance has been independently established in this stage. See [art provenance](../../assets/item-system/PROVENANCE.md).
- Square metal slots96px(default),104–116px(detail),64–68px(compact),42px(material); dark navy, bronze edges, gold focus and restrained cyan lighting. Labels and quantities remain HTML. Availability/unknowns remain text, not only colour. No rarity tint inferred. Source quality badges are displayed only when source metadata supplies them.
- Beautiful Cards / Compact Inventory controls share a separate saved view preference.3columns on mobile in compact mode;2in beautiful catalogue/inventory;6compact columns on desktop. Search/render pagination stays24, never3,219DOM nodes. Legacy discovery retains its existing bounded selection. Original learning item labels are available in4languages; new visual/disclosure controls cover EN/RU/ES/PT-BR. Private lab remains English-only.

## Deep screens

Native branded mobile sheets remain, with keyboard focus, Back/Escape, source detail accordions, crafted item/ingredient slots, craft-path cards and shared plan results. Existing core engine and storage are reused unchanged. A bounded per-route scroll map restores internal position on Back; lab also retains background scroll and per-item input quantities. Reduced viewport tests approximate an open keyboard; no claim to have used a physical Android keyboard/screen reader.

The regular Inventory now offers a visual quick-adjust grid using the existing inventory string key and optimistic update checks. The original exact text editor remains available below it for compatibility/recovery. Plans include an illustrated goal preview; Projects have item miniatures and decorated panels; Advanced includes a selected-item panel, shared material styling and compact disclosure. It remains an advanced form, not a fictional game screen. Existing native confirmations for destructive import/delete actions remain browser confirmations; their semantics were deliberately preserved rather than risk data handling.

Long repeated tutorial banners were replaced with a short Demo badge and collapsed branded explanation. The full statement that these are original learning examples, not real Hytale recipes, is preserved inside the disclosure and source notes. User/learning/research are distinguished. No provenance is hidden or changed.

## Real data and preservation

The prior raw exports and private build are present. [Pinned manifest](RESTORE_MANIFEST.json), offline verifier and [recovery instructions](RECOVERY.md) now cover exact source and normalized SHA-256, versions/counts, dependencies, clean-checkout reproduction and the case where URLs change or disappear. The original build and raw exports are preserved. A fresh private build reproduced normalized SHA `65f5f3774f1e1afa470f03640fe249a8959960c884d978fe5b9e15c62adc314b`. A clean extracted code checkout with copied authorized local inputs reproduced that same hash, without network or installed game. This is a clean source checkout, not a fresh OS/container installation.

There is **no durable full-data cloud backup**. Workspace-only preservation can be lost if the environment is destroyed. Raw source/bundle/build/detailed formulas are not on Drive/GitHub/Cloudflare. Code-only backups plus instructions do not restore source bytes if both workspace and export endpoints disappear. Terms were not treated as permission to mirror the full dataset. Existing studio enquiry remains pending.

3,219items /2,109source rows /638supported material methods /1,471quarantined /17stationIDs. Extract2026-08-12, exact build unknown. Supported638=623single-output+15multi-output;4TODO-station records remain excluded. All403salvage rows remain quarantined; missing selectors and duplicate outputs are not repaired by invention. Different OpenHytale versions are not merged.

Source disconnect/reconnect disables catalogue/calculation UI while preserving original inventory/plan bytes. Retired/unknown item IDs remain stored, not silently deleted. An immutable source filter excludes dependent records and never mutates user storage. Empty source sets are UI empty states, not invalid engine calls. Image lookup has no dependency on source existence.

## Checks and measurement

Public tests run only original/synthetic data. The private opt-in real harness verifies100/1000/full catalogues,24DOM cards/slots,3,219-entry stock, real alternative-method selection, multiple results, complex chains, missing paths, cycles, station uncertainty, strict blocking, shared plan, independent craftability, source disconnect and storage.620 arithmetic comparisons with explicit external stops match; default354matches plus blocked/partial source paths remain honestly labelled.15multi-output/150station-level checks. Material availability is not guaranteed station/unlock eligibility. This is source-backed technical verification, not in-game verification.

Private Chromium320/360/393/430:0JS errors/overflow. Latest unthrottled readiness0.49–0.67s. At150ms latency,150KB/s and4xCPU, UI ready3.274s (previous comparable sample3.214s); first visible new miniature4.442s, measured separately. New atlas costs136.8KB total, one shared lazy resource. Full JSON remains2.10MB decoded/~113KB gzip. JS heap sample about9.5MB used; not a real imposed OS memory limit. This does not promise all devices will match those numbers.

Physical Android, actual mobile IME, screen reader and forced low-memory eviction are not available. No service worker/offline-install feature is introduced; already loaded data/calculations can be exercised offline, but offline reload and uncached artwork are not guaranteed. No heavy continuous animations were added.

Public user-only builder/audit/standalone includes only own visuals/code and original examples; restricted real-data viewer and bundles stay excluded. SHA checks cover the atlas. Public CI artifact paths explicitly include only safe `public-screens`, not real screenshots/reports.

## Delivery and next step

Stage18 stays a Draft above PR17, preserving16→17→18 dependency. Only own code, original artwork, synthetic fixtures, manifest metadata and aggregate QA are public. Existing Drive folders hold the safe source backup, technical/visual report, recovery instructions, test summary and safe contact sheet; bounded attributed real UI review stays owner-only. Private Drive file identifiers are retained only in the native passport/private journal, never added to this public report. Readbacks must match SHA before claiming uploaded.

Next: owner visual review of compact slots and deep panels, then remaining exact item illustrations only after verified silhouette/material evidence and approved rights. A current full source with selectors/build information and clarified reuse/storage rights is still necessary for real public catalogue release. No permissions are requested to publish the current restricted research data.

# Stage 3 design preview — review before adoption

`preview.html` is a parallel interface in the existing repository. It uses the existing `web/planner.js`, `web/game-recipes.js`, pinned JSON snapshots and original browser storage. It does not replace the approved `index.html` design and is not deployed. Stage 3 branch is based on PR #2 head d90e010; its draft PR targets the PR #2 branch to keep the review focused. Neither PR is merged.

## Review the concept

Run `python -m http.server 8000` in the repository and open `/preview.html`. A self-contained owner-review artifact can be generated with `python scripts/export_preview.py --output /tmp/hytale-craft-stage3-preview.html`. It includes restricted non-commercial snapshots: do not post it as commercial-ready software. It needs no external CSS/JS/fonts/images/JSON requests. A normal browser capable of opening local HTML should be used; Android file-viewer behavior is not verified. Managed Chromium here blocks file:// navigation; the self-contained HTML is tested over a permitted local HTTP route with zero subresource requests. No browser policy was bypassed. File-origin user storage is separate from the hosted site's storage: export/import existing recipes explicitly, do not assume automatic transfer.

## Visual prototype, not approved final art

Ten original SVG miniature scenes: sword, shield, pickaxe/rock, house, cooking pot, harvest, map, enemy, crystal/abilities and workbench. They share one friendly stylized block character, an isometric platform, soft earthy gradients, mint highlights and warm parchment accents. Everything was drawn by project code (`scripts/build_preview_scenes.py`); no Hytale/Minecraft image, game texture, icon or model was copied. These are **vector placeholders for a 3D art direction**, not final 3D renders or official Hytale assets. Social image is an original text/geometric card, not a game screenshot.

Next art brief if owner approves: commission ten cohesive stylized 3D scenes, transparent/clean silhouettes, readable at 140px, a distinctive original character silhouette/clothing, varied skin/character designs, sword/pickaxe/house/cooking/harvest/map/enemy/abilities/workbench poses. Require documented rights for all models/textures/fonts, source files, source license and commercial scope. Export responsive WebP/AVIF with SVG fallbacks; cap individual tiles near 20KB. Do not replace placeholders with random search images.

Mobile: two columns at 320/393px, minimum 48px controls, four-column/five-column responsive space on wider screens, no video/audio, no constant animation loops. Only brief hover/press transitions; prefers-reduced-motion disables them. Tools are collapsed beneath the ten goals. Deferred snapshot fetch keeps the first view small. Early performance checks measure decoded bytes and throttled local Chromium, not guaranteed real Android/Core Web Vitals.

## Functional scope

Fight → weapons → Crude Shortbow opens a direct card; no empty search redirect. Source/date/build caveat and non-commercial attribution remain visible. Existing 623 recipes and separate ID catalog remain unchanged. Quantity, recursive totals, inventory, leftovers, stations, copy, shared-stock multi-goal plan, custom recipe editor and JSON import/export are connected. Missing recipes offer custom input; incomplete intermediates warn; cycles require explicit acquisition choice. Unsupported explore/boss/skills guides say so and offer item browsing, without invented content.

User data keys remain compatible: `hytale-craft-recipes-v1`, `hytale-craft-inventory-v1`, `hytale-craft-language`, `hytale-craft-plan-<revision>`. A separate preview-user-plan key handles custom plans. Corrupt saved recipes are kept and can be exported, not silently overwritten. Manual language choice is saved before asynchronous dictionary loading; stale language responses cannot overwrite a newer choice.

## Language status

| Scope | Status |
|---|---|
| Preview English | Complete UI dictionary and functional coverage |
| Preview Russian | Complete UI dictionary and functional coverage |
| Preview Spanish | Complete UI dictionary and functional coverage; native-speaker editorial QA outstanding |
| Preview Portuguese (Brazil) | Complete UI dictionary and functional coverage; native-speaker editorial QA outstanding |
| French/German/Simplified Chinese | Draft dictionaries only, not selectable and not advertised as complete |
| Legacy `index.html` / standalone old asset importer | Existing partial EN/RU retained; not silently declared fully international |
| Game data names | Original English and IDs retained; no official Russian/Spanish/Portuguese game translation invented |

Interface translations are project-authored drafts, not official game localizations. “Complete” here means no missing dictionary keys or untranslated preview UI branches, not native-language certification. Browser locales map regional EN/RU/ES/PT to supported dictionaries; unsupported languages fall back to English. Manual supported choice wins. No false hreflang pages: languages are UI state on one canonical app URL. Preview is noindex and outside sitemap.

## Publication decision

Owner must review the visual concept and approve any replacement/merge/deployment. Commercial launch is blocked by data rights and exact-build uncertainty. No ads/analytics/messages/accounts/domain changes performed. Read COMMERCIAL_DATA_READINESS.md and GROWTH_PLAN.md before planning launch.


## Stage4 continuation

The reviewed style and SVG prototypes remain unchanged. `FINAL_ILLUSTRATIONS_BRIEF.md` is the production art brief; no final art is implied. `scripts/build_pages.py` stages this interface as `dist/index.html`; source `index.html` remains legacy and must not be deployed as the new design. Default build excludes community data pending rights; full owner-review HTML still preserves the pinned snapshot. See `CLOUDFLARE_PAGES.md` and Stage4 reports.


## Stage5 superseding art decision

The owner rejected the Stage3/4 SVG look. Those files are historical functional prototypes, NOT the approved art direction. Always consult `APPROVED_DESIGN_REFERENCES.md` and the saved primary design image first. `art-preview.html` now provides an isolated rendered Fight/Gather pair for approval; other eight remain pending. See `STAGE5_ART_PAIR.md`. Do not replace Pages entry or mass-integrate new art before owner acceptance.

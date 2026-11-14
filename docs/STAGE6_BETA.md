# Stage6 — mobile beta, ready for owner review, not deployed

Source base: PR5 `6e1e5da61be9398a7f20efeb8ed6af9a5dfdff70`. Branch `codex/mobile-beta`, draft PR6 targets PR5, preserving the existing stack. main `1c9c1e035207b954894fdba225ceca2dc4742f38` and production remain unchanged.

## Mobile interaction

`beta.html` is a new application shell around the existing `web/planner.js` and established recipe/inventory storage keys. Historical legacy/preview/art-review pages are retained in source and tested; they are not the publish entry point. No real data or working editor/planner was deleted.

Ten goals appear in two columns at320–430px. Two original PR5 scenes are preserved; eight other goals have functional symbols rather than pretend final art. No new illustration style was generated. Permanent references remain `APPROVED_DESIGN_REFERENCES.md` and the owner's Drive folder; eight final scenes still need approval/artwork.

First selection of an illustrated goal can play its character action, then open a native modal `<dialog>` bottom sheet. It does not scroll the home grid. Only one action runs, fetch/decode wait is capped120ms (otherwise use poster), playback820ms, repeated selections open immediately. New selections/navigation cancel pending work, preventing delayed duplicate panels. Four actual poses now use two layers with90ms crossfades; this reduces abrupt frame changes but **does not create eight independent poses or a smooth rigged animation**. Additional consistent frames/rig are still needed for that quality. Reduced motion/Save-Data/user toggle/hidden page suppress or stop playback; all cards work statically. No loop, video or3D runtime.

Panel starts at68dvh and can expand to94dvh with its handle. Internal category list → item → calculation, inventory, plans and editor all stay inside the sheet. Close button, handle swipe down, Escape and browser/Android-style Back are supported. Back returns item→category→home; close/Escape/swipe return all the way home. Own history entries use the same URL, no SEO duplicate routes. A close guard prevents repeated taps from stepping outside the beta history accidentally. Background stays fixed at its original scroll offset and inert; native modal semantics, labelled heading, explicit Tab wrapping, focus return and keyboard controls are tested. Touch drag is restricted to the handle/header rather than hijacking content scrolling. Real Android hardware/IME/screen-reader gestures remain untested.

Main navigation is Home / Inventory / Plan / More. No giant tools block or replay/test buttons on the home screen. More retains editor, import/export, privacy and motion preference. Compact limited-catalog notice stays visible because the beta is not a verified Hytale database.

## State and data

- Recipe key `hytale-craft-recipes-v1` and inventory key `hytale-craft-inventory-v1` retained. Saved/corrupt data are never replaced by lesson fixtures. Read-before-write guard detects legacy/other-tab recipe updates. Inventory syntax uses last colon, supporting `lesson:fibre: 3`.
- Four original educational examples are read-only and explicitly marked NOT Hytale. Separate lesson/user plans; no community catalog or recipe snapshot. Full details in `EDUCATIONAL_EXAMPLES.md`.
- Batch yields, recursive chains, inventory deficits, shared stock/surplus and cycles use the existing deterministic engine. Missing/invalid recipes show an error, no simulated game result. Lesson recipes assert no real stations/game mechanics.
- Panel/item/quantity/results survive closing/back; quantity/result caches survive same-tab reload via sessionStorage when available and are reused only when recipe/inventory/quantity signatures still match. Changed inputs invalidate derived results. This is a single-tab convenience cache, not a portable backup or transactional database.
- User recipe format `hytale-craft-v1` remains importable/exportable. Full beta backup includes raw recipe JSON, inventory and two plan texts (with legacy user-plan fallback), not all unrelated keys or session-derived caches. Restore validates first, asks before replacement and attempts rollback on storage failure; browser multi-key writes are not a transaction. Corrupt recipe data can be exported raw and are never silently overwritten.
- EN/RU/ES/PT-BR dictionaries separate original educational labels from real game names. Manual preference and browser language detection retained. FR/DE/Chinese remain hidden. No claim of native-speaker or official game localization review.

## Deployment and preview

`python3 scripts/build_pages.py --data-policy user-only` builds **beta** into `dist`; `scripts/audit_pages.py` validates the boundary/checksums. Restricted modes are rejected. PR5 posters/atlases are included, source masters/docs/tests/backups/game snapshots are not. Static404/noindex/CSP/robots remain; no ads/analytics/external fonts or CDN. Build is deterministic and does not fetch live sources.

Exact free Pages settings, intended `hytale-craft.pages.dev` address, rollback and PR2–6 integration instructions: `CLOUDFLARE_PAGES.md`. Name availability/account configuration/TLS were not tested, no Pages project or public URL was created. GitHub Pages may publish automatically on main merges: check settings before any separately approved integration.

`python3 scripts/export_beta.py` creates a standalone private owner-review HTML. It is tested via local HTTP with one document and no subresources, not claimed physically tested via Android file viewer. Downloading through Drive may show source or require a supported HTML viewer. Do not disable browser protections. Dist ZIP can be served locally with Python; no public tunnel or external Site was created to bypass the deployment boundary.

## Remaining gates

Owner reviews screenshots/HTML and decides whether to approve the free **educational UX beta**. This is not a real Hytale recipe beta or commercial launch. Physical Android, native-language QA, eight final illustrations and smoother authored frames remain pending. Real game catalog requires independent permission/version/provenance work. Merge and Deploy are explicitly separate owner decisions; neither happened in this stage.

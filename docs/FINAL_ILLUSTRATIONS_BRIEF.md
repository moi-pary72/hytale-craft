# Final goal illustrations: production brief (not finished art)

Keep the reviewed ten-card layout, two columns at 320–430px, dark blue/charcoal environment and friendly original block-shaped 3D characters. Existing `assets/preview/*.svg` are functional prototypes, not official Hytale art or final renders. Do not replace them until a contact sheet and mobile crop are approved. No screenshots, copied models, extracted textures, logos or third-party databases without written rights.

## Shared specification

Create ten original isometric miniature scenes with one readable action each, soft volumetric shapes, expressive friendly faces, modest cartoon proportions and consistent character scale/camera (about 35° elevated, 3/4 view). Distinguish them through silhouette and a single restrained accent colour, not ten bright backgrounds. Render over transparent background with soft contact shadows, compatible with #101f2b. Avoid Minecraft faces/textures and reproduce no recognisable protected character. No blood, graphic violence, tiny text, interface text or baked-in category label. Labels stay localized HTML.

Master each scene at 1260×996 (same 210:166 aspect as prototypes), with 10% safe edges and main subject inside central 80%; verify at about 130×103 display on 320px phones. Deliver layered editable scene/source, lighting/material setup, transparent PNG master, optimized WebP at 420×332 and 210×166 (AVIF optional with fallback), and a contact sheet. Target ≤35KB per 420px WebP, ten images ≤350KB; use explicit width/height to prevent layout shift. Do not commit heavy masters to deployed dist. Existing builder allowlist must be deliberately updated when replacing SVGs, with regression tests. No remote image CDN.

## Ten scene shots

| Key / purpose | Foreground action | Supporting scene / readability |
|---|---|---|
| fight / Fight | Friendly adventurer holding a simple sword in ready stance | Small practice target, no enemy injury; sword clear in silhouette |
| defend / Defend | Adventurer crouches behind broad shield | Two stylized deflected sparks, recognisable armour, no projectile toward viewer |
| gather / Gather resources | Miner swings pickaxe toward rock | Chunk of ore and two chips, tool head readable |
| build / Build & decorate | Builder sets a block into cottage wall | Partial roof and single plant; no dense town panorama |
| survive / Survive | Camper stirs pot over compact stove/fire | Bowl and tent corner; warm accent remains restrained |
| farm / Farm | Farmer lifts basket beside crop row | Two large crop silhouettes, no detailed field texture |
| explore / Explore | Explorer raises lantern and unfolds map | Small path/rock arch; map has no readable text |
| boss / Defeat an enemy | Small adventurer faces friendly-stylized large creature silhouette | Clear size difference, non-graphic anticipation, avoid actual unlicensed Hytale enemy model |
| skills / Develop abilities | Character practices a modest magical light or skill gesture | Three simple runic shapes, no invented promise of actual game progression |
| workshop / Improve workshop | Craftsperson works at compact bench | Hammer, tool rack and one improvement part; distinct from building scene |

Boss/skills/explore art indicates a user intention only. Their game guidance remains explicitly unavailable/planned where verified data do not exist. Do not fabricate mechanics to match artwork.

## Rights and acceptance

Artist contract must grant international web/commercial display, modification, compression, source/master backup, duration and attribution terms; record author, creation date, tool/model licences and provenance. AI-assisted work must disclose generation provenance and be checked for copied elements; do not call generated or commissioned illustrations official assets. No final illustrations commissioned or generated in this stage.

Approve a greybox contact sheet first, then one fully rendered fight+farm pair, then all ten. Acceptance: readable action at 130px; consistent perspective/light/character; no clipping with long ES/PT labels; keyboard outline and touch target unchanged; text contrast intact; no flashing/video; no perpetual animation. Keep existing lightweight press/hover transforms, disable with prefers-reduced-motion. Test slow network and image failure before accepting final files.


## Stage5 correction / mandatory reference precedence

The owner explicitly rejected the prior SVG look. Use `APPROVED_DESIGN_REFERENCES.md` and its primary dark mobile PNG as the permanent visual source. Stage5 rendered pair is a candidate for approval, not authority to create all eight remaining scenes. Its four-pose actions are limited motion samples; 8–12 consistent frames or a rig are needed for smooth final animation. Revised per-action delivery contract is in `STAGE5_ART_PAIR.md`.

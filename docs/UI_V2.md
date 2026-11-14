# Hytale Craft 2.0 — artwork and functional interface

2026-11-14. One branch `codex/ui-v2`, based on main `232b9c4f1da592e415245d0144c1d7acb1e7b845`. The owner explicitly authorized one PR and merge/publication after CI and visual QA. Rollback source: annotated tag `backup/pre-ui-v2-20261114` and a ZIP of that exact main.

## Reference and implementation

Primary reference is the 1170×1280 image attached to the owner's Hytale Craft 2.0 task: crystal-topped metallic wordmark, castle/waterfall setting, ten framed illustrated cards and a four-slot game navigation bar. It supersedes prior SVG previews. Historical reference folder is https://drive.google.com/drive/folders/1_IZebF8sttpwqA1B-rP4oH9HuX7xG1Ve . The exact latest attachment was visually available but no downloadable file was exposed by the workspace; the old Drive references must not be mislabeled as that attachment.

Eight new original mini-scenes plus the existing original fight/gather scenes give all ten goals full illustrations. Additional originals: fantasy landscape in two resolutions, transparent wordmark, metal/stone frame, four illustrated navigation icons. Generated with OpenAI image generation; no third-party game assets downloaded. See assets/ui-v2/PROVENANCE.md and both asset manifests. Original PNG masters remain private backups, not dist. This is unofficial artwork, not official Hytale art or a trademark license.

Logo is its own image, world is its own background, card scenes and frame are separate WebP files. Labels, Beta badge, navigation, controls, recipes and sheets are real localized HTML. Mobile: two columns. Desktop: four, four, then two centered. The main page is not a flattened mockup.

The reference's unsupported “complete guide” claim is deliberately replaced by the limited learning-beta notice. Own original illustrations are interpretive equivalents, not pixel-identical copies of the reference. The two existing fight/gather one-shot pose sequences remain unchanged; the other eight scenes are complete still artwork. Hover/focus lighting is an interface reaction, not claimed as character animation. Reduced motion, Save-Data safeguards and no permanent animation are retained.

## Functionality and storage

Planner, recipe/inventory keys, independent demo/user plans, editor, import/export, backup restore, quantities, recursive yields, inventory consumption and cycle guards are retained. No storage migration or key changes. The bottom sheet has a second instance of the same four navigation controls INSIDE the native modal, making navigation operable while background stays inert. Only one bar is visible at a time. Home closes history depth; Back, swipe, Escape, focus trap and scroll restoration remain native/explicit as before. All four launch UI languages remain available.

## Build and deployment

Existing Cloudflare project hytale-craft, production main, Framework None, Root blank, build `python3 scripts/build_pages.py --data-policy user-only`, output dist. GitHub Pages workflow also builds only dist and retains its project-path404. No new hosting project. Extend the exact public allowlist by 16 WebP assets; check source SHA-256 before staging and every output checksum afterward. No internal docs, masters, source catalogs, secrets, archives, ads or trackers. Noindex stays. Standalone export embeds all artwork without external requests.

## QA and comparison

See reports/UI_V2_TEST_RESULTS.md. Review actual browser screenshots at 393px and 1170px alongside the owner attachment. Matches: dimensional logo/crystal crest, illustrated fantasy setting, ten individualized scenes, dimensional frames and glow, real localized titles, game navigation. Corrected first-pass overcropped background, overly tight long-title padding and missing-art regression coverage. Physical Android, native keyboard and assistive-technology checks remain a manual follow-up; emulated Chromium is not a real device.

After merge verify both live manifests and actual HTTPS mobile flows. Do not equate CI success with deployment success. Store exact PR/head/merge/deployment evidence and Drive backup registry in the existing project history, preserving previous entries. Roll back through an ordinary reviewed revert and audited-dist workflow, never force main or publish the repository root. Browser data remains on its original hostname.

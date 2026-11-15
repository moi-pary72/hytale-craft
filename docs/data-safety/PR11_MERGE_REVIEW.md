# PR11 — pre-merge review, 2026-11-15

Review of main a972e4d664687211319b1b94cf87462de7022f1a against the data-safety draft. Merge is NOT authorized by this review; main, production sites, tags and history remain unchanged.

## Findings and correction

All40 original changed files reviewed: current-tree dataset removal/neutral markers, paused collectors, safe educational export, offline importer, synthetic fixtures/tests and documentation/evidence. No approved UI, CSS, artwork, localization, public builder or deployment workflow changed.

One importer issue reproduced: an existing candidate containing a JSON array/null or malformed snapshot metadata raised an uncaught AttributeError. Corrected to produce an explicit failed-import report while preserving the prior bytes and creating no replacement/backup. New regression covers five malformed existing states, including when version-change permission is set. This is offline tooling only, not a site change.

## Fresh verification

-38Python unit tests,17JavaScript tests and all25existing browser tests pass locally. Coverage includes calculator, inventory, surplus, batch plan, editor, import/export, reload/language persistence, navigation, Back/Escape/swipe and damaged/missing data.
-Four UI languages and320/360/393/430px tested. Main and PR publication builds freshly generated in isolated directories: all40files (including manifest) byte-identical. UI baseline copied from Git without copying game datasets. Real Chromium screenshot pairs also compared; minor antialiasing variation is recorded rather than called a design change. The byte comparison is exact.
-Tracked-tree data guard passes. Credential-signature scan of180tracked paths found no matching credentials/private keys; this is a scoped scan, not an absolute guarantee against every possible secret. Existing metadata/IDs/links are distinguished from copied recipe bodies.
-All five collector workflows have only manual notice jobs, contents:read, no schedule/network/update-PR steps. Their network/CLI entry points are blocked. Until merge, main and old refs still retain their original code/snapshots; check queued/running old jobs immediately before any separately authorized merge.
-Google Drive safe backup13TBZk16K6Twm9vwuIH6DpmVkIBFcZWKX downloaded through the connected account, SHA-256 verified as69742df2c1a51db6e7eb16f1154e28af31adb4bb7ac4c7c669e5c17183d56e19, ZIP CRC passed, every one of180files compared to original PR head cee5314. No disputed snapshot; bulk catalogue empty. A separate current-head backup is retained after this small correction. Private storage does not resolve licence rights.

## Decision

Technically suitable for owner-approved integration after final-head CI is green and main/head are rechecked. On the current public beta, appearance/data/functions stay unchanged:4original educational recipes,0real Hytale recipes. Repository cleanup and collector pausing take effect in the default branch only after merge. The old source-only preview/export is deliberately prevented from serving disputed catalogues; standalone export now uses the safe beta.

Remaining: no physical Android/IME/TalkBack test; full Cloudflare history/account settings not independently accessible; historical refs, backups, old artifacts/forks/caches retain prior copies; no commercial game-data permission. Importer supports the documented limited candidate schema, not all future game mechanisms. Review does not authorize new recipes, monetization, messages, history rewrite or deployment.

Separate owner permission is required for merge and its automatic-main-publication implications; historical cleanup/deletions; sending the prepared licensing letters; obtaining/integrating real game data. This task performs none of those actions. Draft branch commits retain CF-Pages-Skip to avoid preview deployment. Exact final CI, screenshot/backup checks and native-passport update are recorded in PR11 and Drive evidence.

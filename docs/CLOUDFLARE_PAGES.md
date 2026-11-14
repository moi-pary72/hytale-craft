# Cloudflare Pages: review build, not deployed — 2026-11-14

Stage 4 is stacked on draft PR3, itself stacked on PR2. No merge, production change, Cloudflare account connection or public deployment was performed. Existing GitHub Pages stays untouched. This preparation needs no paid feature; domain registration is outside scope.

## Exact settings for a future owner-approved connection

| Setting | Value |
|---|---|
| Git repository | `moi-pary72/hytale-craft` only |
| Framework preset | None |
| Root directory | repository root (leave blank) |
| Build command | `python3 scripts/build_pages.py --data-policy user-only` |
| Build output directory | `dist` |
| Python | Python 3, standard library only; tested 3.12 |
| Environment/secrets | none required |
| Functions / Workers / database | none |
| Initially reviewed branch | `codex/cloudflare-testing-ready`, only after owner approval |
| Automatic production/preview deployments | disable until an explicit publishing decision |

**Saving a Git integration with “Save and Deploy” can publish immediately. Do not click it merely to configure this task.** Even a preview deployment is publicly reachable unless access protection is configured. No real Pages URL exists for this stage; no guessed URL is provided.

The source `index.html` is the legacy interface. Never use repository root as the output directory or a blank build command. The builder reads `preview.html`, adds the testing configuration, and writes the NEW interface to `dist/index.html`. Explicit allowlisting copies only four complete dictionaries, runtime JS/CSS and ten original SVGs. No docs, tests, scripts, old index, licensed archives, backups or `.git` are copied. It makes a real `404.html`, so missing routes do not silently fall back to a SPA; `/preview.html` redirects to `/`. There is no service worker. Only generated `dist` may be uploaded. `dist` is ignored by Git, regenerated every build.

## Data modes and rights

Default `user-only` ships NO community catalogs or recipes and makes NO data requests. The editor, inventory, export/import and manual plans work. It is suitable for reviewing mechanics without bundled database redistribution; this is not a blanket legal clearance for commercial launch.

`python3 scripts/build_pages.py --data-policy noncommercial-review` includes exactly the pinned HySphere snapshot + separate ID catalog, validates SHA-256 and rejects empty data. It preserves 623 source-backed recipes for owner review. This is **not** permission to publish those datasets. Confirm the scope of public noncommercial mirroring with HySphere before choosing this mode for a public test; commercial use remains blocked. See `COMMERCIAL_DATA_READINESS.md`.

## Security, SEO and paths

All paths are relative and work at the Pages domain root. HTTPS is provided by Pages for its assigned `*.pages.dev` hostname; validate actual TLS, MIME types, `_headers`, redirects and 404 after any future approved deployment. Local tests simulate the CSP but do not prove Cloudflare applied it. CSP allows only same-origin scripts/styles/fetch and local/data images; no external trackers/fonts, ads or analytics. `_headers` adds noindex, nosniff, no-referrer, limited permissions and revalidation. File checksums are recorded in `build-manifest.json`; every build starts from the reviewed repository snapshot.

All Stage4 builds are intentionally noindex with host-root `robots.txt` disallowing crawling. For testing, no `SITE_URL` is needed. An optional `--site-url https://APPROVED-HOST` supplies canonical/OG URL and single-URL sitemap; it must be a valid HTTPS origin. Do not enter a placeholder in an actual deployment. Four UI languages use one URL and browser/manual preference, with no fake language pages or hreflang. Game English names remain separate from UI localization. Open Graph has a title/description; final share artwork and indexable SEO release need a later review. Remove testing/noindex only in a separately approved launch change; sitemap presence alone does not enable indexing.

## Updates and rollback

Existing source-update Actions check permitted endpoints, validate and propose versioned data via PR. They do not deploy or merge. Pages builds do not download game data. To update a hosted test later: review data/rights/hash/diff in Git, approve the dependency stack, merge only with permission, then build the selected approved branch. Enable branch build controls only as part of that publishing decision. Do not connect Pages to main assuming PR2/3/4 already landed.

Keep previous successful Pages deployments and reviewed Git commit/ZIP manifests. Cloudflare production rollback can restore a prior successful production deployment; a Git revert/rebuild also requires approval. Browser inventory and recipes are **not** rolled back with code. A hostname change creates a different localStorage origin: export recipes and record/copy inventory/plans before migration. Current export is recipe-only, not a full backup of all browser state.

## Later custom international domain

Owner chooses and controls the domain separately. Add it through Pages Custom domains, follow Cloudflare DNS/HTTPS verification, set the actual origin in the build, test links/canonical/sitemap and single-host redirects, then request indexing after legal/content approval. Do not add DNS or buy a domain now. Keep the old origin available long enough for manual browser-data export/import; cross-origin localStorage cannot be read automatically.

## References checked for configuration

- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
- https://developers.cloudflare.com/pages/configuration/branch-build-controls/
- https://developers.cloudflare.com/pages/configuration/preview-deployments/
- https://developers.cloudflare.com/pages/configuration/headers/
- https://developers.cloudflare.com/pages/configuration/serving-pages/
- https://developers.cloudflare.com/pages/configuration/rollbacks/
- https://developers.cloudflare.com/pages/configuration/custom-domains/
- https://developers.cloudflare.com/pages/platform/limits/

Cloudflare Free limits and current dashboard defaults should be rechecked at the actual owner-approved connection. This is a static Python build, no npm/framework subscription, Workers billing or bank-card feature is required by the implementation.

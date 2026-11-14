# Stage7: isolated HTTPS preview without merge

Current owner setup: [CLOUDFLARE_ANDROID_PREVIEW.md](CLOUDFLARE_ANDROID_PREVIEW.md), branch `codex/https-preview` based on PR6. Recommended new test project `hytale-craft-preview`, its Production branch set to that test branch (not main). No project or URL created; Save and Deploy still requires owner approval. Dashboard settings have not been changed by the reference JSON.

**GitHub Pages settings are now verified**, not hypothetical: legacy branch publishing from main:/, public/HTTPS, last build commit1c9c1e035207b954894fdba225ceca2dc4742f38. Do not merge to get a preview. All existing draft PR2–6 remain unmerged with successful CI.

The first deployment of a new isolated project is called Production in Cloudflare even though it is only the owner's beta test. A true non-production Cloudflare Preview is possible within an existing configured project, but existing Cloudflare account state is not accessible here. Avoid changing a current production project blindly. Preview URLs are public by default; noindex is not access protection. No publishing or paid feature was performed.

The Stage6 build/boundary remains unchanged. GitHub CI now saves an audited `dist` artifact only for the isolated preview branch; no deployment token/job exists. Source/root, datasets, docs/backups remain excluded. Artifact download is not a running HTTPS site.

---

# Stage6: Cloudflare Pages beta — prepared, not deployed

**The current entry point is `beta.html` → `dist/index.html`.** Never publish repository root, source `index.html`, `preview.html` or `art-preview.html`. They remain historical/source review interfaces. `scripts/build_pages.py` now includes PR5’s two posters/atlases and the beta shell. The old Stage4 build description is superseded by this document; history remains in development records.

## Exact settings after separate owner approval

| Setting | Value |
|---|---|
| Account plan | Cloudflare Pages Free; no paid function required |
| Repository | `moi-pary72/hytale-craft` only |
| Project name requested | `hytale-craft` |
| Intended address | `https://hytale-craft.pages.dev` — not created, ownership/availability not verified |
| Framework preset | None |
| Root directory | Repository root (leave blank) |
| Build command | `python3 scripts/build_pages.py --data-policy user-only` |
| Output directory | `dist` |
| Python | Python3, tested3.12, standard library only |
| Secrets/functions/database | None |
| First review branch | `codex/mobile-beta` only after an explicit deployment decision |
| Production/preview auto-builds | Keep disabled until the owner approves publication policy |

Connecting Git and clicking **Save and Deploy can publish immediately**. A Pages preview URL is still publicly reachable by default. No public deployment, tunnel, new Site, Cloudflare integration, paid service, account or analytics was created here. No live address is claimed. This task stops before merge/Deploy. Standalone HTML and ZIP provide private owner review without making a public site.

## Build, audit and local review

```
python3 scripts/build_pages.py --data-policy user-only
python3 scripts/audit_pages.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000/` on the developer machine. For another device, local networking/firewall setup is the owner's choice; do not expose a repository-root server publicly. `python3 scripts/export_beta.py` makes a standalone HTML, containing UI/art/original educational examples only. Downloaded-file behavior on physical Android is untested; do not disable browser security if scripts/storage are restricted.

The whitelist contains the beta entry, planner/i18n, beta CSS/JS, eight dictionaries, four optimized PR5 WebPs, static404, noindex robots, headers/redirects and checksum manifest. Source snapshots, ID catalog, old SPA, licensed archives, masters, reports, tests, docs, backups and credentials are excluded. Builder now **rejects `noncommercial-review`**. Restricted owner review remains separate (`export_preview.py`), never use that HTML as the public beta entry.

Builds fetch no remote data and require no npm install. Art checksums are verified against the checked-in manifest before copying. All public bytes except the self-referential manifest have SHA-256 entries. Two consecutive builds are compared by tests; audit rejects unlisted files. Files/HTML have deterministic content, no build clock or random ID. Updated art/source changes should be reviewed in PR and rebuild the pinned Git revision.

## HTTPS, CSP, SEO and domains

Relative same-origin paths work at the Pages root. Intended `pages.dev` HTTPS/TLS and actual `_headers`, redirects, MIME types and404 must be smoke-tested after an approved deploy; local CSP simulation is not proof of Cloudflare configuration. CSP permits same-origin scripts/styles/fetch plus self/data images, blocks inline script/eval, frames, objects and form posts. No third-party trackers, ads, external font/CDN or cookies are introduced. Native dialogs and CSSOM pose styles are tested under this policy.

Temporary noindex is present in HTML, headers and root robots. No fake item or language SEO URLs. A canonical/single-URL sitemap can optionally be generated with `--site-url https://hytale-craft.pages.dev` only once that origin is confirmed; the exact requested default command works without it. Keep noindex for this limited educational beta. A later domain requires owner-controlled DNS/Pages custom-domain verification and an approved canonical/redirect change. Domain purchase/DNS changes are outside this task.

## Updates, storage and rollback

Current beta has4 **original educational recipes, not Hytale data** and user-entered/imported recipes. Source-monitor/update workflows remain PR-only; no downloaded community database is included by the beta whitelist. Updating those snapshots does not enable them in beta. Do not enable a source without provenance and public-use rights review. No auto-merge/deployment job was added.

Keep successful Git/ZIP/build-manifest versions and Cloudflare production deployments. Cloudflare rollback targets prior successful production deployments; preview deployments themselves are not production rollback targets. Any rollback/rebuild is an owner action requiring deployment approval. Site rollback does not revert localStorage. Export beta recipes/inventory/both plans before changing hostnames; browser origins are isolated. Derived result/quantity session caches are not portable backups.

## Safe dependency integration: PR2 → PR3 → PR4 → PR5 → PR6

1. Before any merge, inspect GitHub Pages settings and Actions: **a main merge may automatically publish the existing GitHub Pages site**, even if no deploy workflow is checked in. Coordinate/disable production auto-publication only with owner permission. Do not use merging as a harmless test.
2. Obtain explicit approval for merge and separately for deployment; confirm current branch heads and PR diffs. Prefer ordinary merge commits preserving stack ancestry. Do not delete a base branch while a dependent PR still targets it.
3. Merge PR2 into main only after approval/checks. Retarget PR3 to main; resolve any conflicts and run CI, then obtain/perform approved merge3.
4. Retarget PR4 to main, inspect final diff/CI, then approved merge4. Repeat for PR5, then PR6. Each retarget is after its dependency is incorporated. Never merge PR6 alone against an unprepared main.
5. If using squash/rebase merges instead, explicitly rebase each dependent branch onto the new main and review the rewritten diff; do not assume old stack SHAs remain ancestors. Recheck parallel changes before every action.
6. Build/audit final approved revision. Owner verifies Android, intended slug and rights-limited catalog. Only then connect the approved Git branch and click Deploy. Do not accidentally enable Cloudflare main auto-builds before the complete stack is ready.

## Readiness

Prepared for **free UX/calculator testing with explicitly educational examples**, subject to owner acceptance and deployment authorization. It is not a verified Hytale recipe database or commercial launch. Two art scenes remain four-pose samples with short cross-fades; eight final scenes and physical Android/native-language QA remain pending.

Official references: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ ; https://developers.cloudflare.com/pages/configuration/headers/ ; https://developers.cloudflare.com/pages/configuration/branch-build-controls/ ; https://developers.cloudflare.com/pages/configuration/serving-pages/ ; https://developers.cloudflare.com/pages/configuration/rollbacks/ ; https://developers.cloudflare.com/pages/configuration/custom-domains/ ; https://developers.cloudflare.com/pages/platform/limits/ . No paid product is needed by this implementation; check actual dashboard defaults at the approved connection.

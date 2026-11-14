# Owner-authorized production launch — 2026-11-14

The owner explicitly authorized publishing the free educational beta and sequential normal merges of PR2–7. This supersedes earlier no-merge/no-deploy instructions, but not the ban on restricted datasets, third-party game assets, ads or paid services. Use one main branch and one Cloudflare project **hytale-craft**, not a separate preview project.

## Actual preflight / current blocker

Main backup: commit `1c9c1e035207b954894fdba225ceca2dc4742f38`, annotated remote tag `backup/main-before-beta-20261114`. ZIP CRC and SHA-256 verified: `1ee2283a3edbef3fd823076034f1ec12a809a5f1478b935f7c13ab8e482b1845`;43208bytes. Drive upload name/size/parent read back: https://drive.google.com/file/d/1bac-DFOkhG_y0PxAxSknrk6JDUb49jkB/view . Keep this source backup and all previous versions; no force/reset needed.

All PRs2–7 were mergeable. A red push check on PR6 was investigated before merging: language was saved after async dictionary fetch, and fast reload could reset selection. Fix commit `69e600081609c6a58c3822ef2bd20ac376f288f4` saves preference before fetch before starting asynchronous loading. Those initial CI runs passed, but launch push CI reproduced a second part of the race: cancelled dictionary fetches during reload could roll the preference back. The final fix preserves explicit preference even on cancelled/failed fetch, with a new delayed-network reload regression. No stale red check is bypassed; current heads must pass again.

GitHub Pages remains **legacy source main:/**. Attempt to change it to workflow through the connected integration returned **HTTP403 Resource not accessible by integration**. Readback confirmed no change. No main merge was performed because intermediate PRs would then publish their repository-root snapshots. This is an integration permission limitation, not a request for new merge/deployment permission and not an automatic-approval-review rejection.

Required owner action on Android: GitHub repo **Settings → Pages → Build and deployment → Source → GitHub Actions**. If needed use Chrome **⋮ → Desktop site**. No password/token needs to be shared. Tell the executor when switched; it must verify via GET before continuing. Until then merges/deployment remain stopped. No conflicts/admin checks are forced.

## Prepared GitHub Pages release configuration

`.github/workflows/deploy-pages.yml` triggers on main only (or manual dispatch on main), gates publication behind unit/calculator/mobile checks, then builds `dist` and audits it. Upload/deploy uses official Pages actions with minimal Pages/OIDC permissions. It never uploads repository root. Existing beta/art/editor/storage retained.

GitHub project path is `/hytale-craft/`; builder `--base-path /hytale-craft/` adjusts404 home link, while app resources remain relative. HTML CSP is injected into built index because GitHub Pages cannot apply Cloudflare `_headers`; header-only frame-ancestors is not claimed for meta. Offline owner export remains free of injected CSP and works independently. Temporary noindex stays on both hosts.

After owner switches source and checks pass: merge PR2 normally with expected head guard; retarget PR3 to main and incorporate new base without force, re-run CI, then normal merge; repeat4→5→6→7. The launch configuration PR follows the completed stack and must pass CI too. Do not publish an intermediate root or force a conflict. If a check fails, stop and investigate before any next merge. Preserve ancestry; no squash/branch deletion while dependencies remain.

## Cloudflare production — owner setup when final main is ready

No Cloudflare tools/account authorization are available here. No project/URL has been created or ownership verified. Publication is already authorized by this task; owner must perform the unavailable account steps, not re-approve the same deployment.

1. Chrome → dash.cloudflare.com → **Workers & Pages → Create application → Pages → Connect to Git → GitHub**. If project **hytale-craft** already exists, open/configure that project instead; do not create a preview project or duplicate.
2. Authorize only `moi-pary72/hytale-craft`, choose repository → **Begin setup**.
3. Project **hytale-craft**; Production branch **main**; Framework **None**; Build command `python3 scripts/build_pages.py --data-policy user-only`; Output **dist**; Root directory **blank**. No secrets, Functions, analytics, paid plan or card required by this implementation.
4. After the completed main release is verified, **Save and Deploy → Continue to project → Visit site**. Record the actual assigned HTTPS address; expected name is hytale-craft.pages.dev, not proof that it is live or belongs to this account.
5. **Settings → Builds & deployments → Configure Production deployments**: enable **Enable automatic production branch deployments**. Preview branch control **None**. Future changes to main then update this same production project. Do not deploy old draft branches or the whole repository.

Settings reference: `.cloudflare/production-settings.json` (documentation only; does not configure dashboard). Old Stage7 preview guide/settings are historical and superseded.

## Verification and rollback

Before publish:22Python+17JS plus beta mobile8 and project-path1 checks locally; full CI must pass. Audit whitelist excludes data/docs/tests/source archives/credentials; art SHA validated. Four examples are educational, NOT Hytale recipes; real HySphere/OpenHytale snapshots remain excluded.

After actual publish verify both hosts separately: index has new beta/nav/sheet,24public files/manifest hashes (Github404 base differs),4locales,320/360/393/430, Back/Escape/swipe, actions, quantity/inventory/plan/reload, missing paths404 and no forbidden source files. Real Android/IME/screen reader remains a hardware limitation. GitHub Pages ignores Cloudflare headers/redirect files; rely on HTML CSP/noindex there and validate actual HTTPS behavior.

Failed workflow checks must not deploy; prior served version stays in place. Keep old main tag/ZIP and last verified beta dist ZIP. For a code rollback, create an ordinary reviewed revert/restore commit/PR, never force-push main. Keep Pages in Actions mode; do not return to publishing repository root while restricted snapshots are present. Rebuild/audit the selected verified beta revision before republishing. Browser inventories/recipes are not reverted with site code; export full beta data before host migration. A hostname has separate localStorage.

## Final observed preparation checks

PR6 headc4accf4 passed runs43603568865/43603564361. Release PR8 head8ea6720 passed43603570551/43603566411 (22Python,17JS,24browser across the full suite). Local beta8 and GitHub project-path1 also pass. Permission403 remains, main and all existing PR merges unchanged. Existing GitHub URL responds200 but is still old interface, not new beta. No Cloudflare working address claimed. Machine receipt: reports/PRODUCTION_LAUNCH_STATUS.json.

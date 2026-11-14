# Main production setup — owner authorized

Current instruction: [PRODUCTION_LAUNCH.md](PRODUCTION_LAUNCH.md). The owner authorized free educational beta publication and merges. Use **one project hytale-craft**, production **main**, automatic updates from main. Earlier isolated-preview instructions are historical and superseded; do not create a preview project.

| Setting | Value |
|---|---|
| Repository | moi-pary72/hytale-craft |
| Project | hytale-craft |
| Production branch | main |
| Framework | None |
| Build command | python3 scripts/build_pages.py --data-policy user-only |
| Output | dist |
| Root | blank |
| Automatic production branch deployments | Enabled |
| Preview branches | None |
| Secrets / paid services | Not required |

No direct Cloudflare account access is available; actual project/HTTPS deployment must be confirmed by owner/dashboard and then tested. Do not claim hytale-craft.pages.dev is working until verified. Publish only after completed main contains builder/beta. No HySphere/OpenHytale datasets, source docs/tests/archives/secrets are in dist; noncommercial-review is rejected. Four original learning examples are explicitly not Hytale recipes. No ads/analytics or new third-party assets.

GitHub Pages needs a separate audited-dist workflow because existing main:/ root publishing is unsafe for the intermediate stack. The connected integration's attempt to switch Source to Actions returned403; owner must select Settings→Pages→Source→GitHub Actions before merges proceed. This does not revoke the existing publication authorization.

Noindex remains intentional. HTTPS/CSP/redirects and Android behavior must be validated on the real host after deployment. Cloudflare applies `_headers`; GitHub Pages uses generated meta CSP and its own host headers. For rollback/source backups/PR sequence see PRODUCTION_LAUNCH.md. Preserve old main tag and last audited dist; never reset/force main.

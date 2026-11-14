# Stage6 test results — 2026-11-14

Baseline PR5 `6e1e5da61be9398a7f20efeb8ed6af9a5dfdff70`; branch codex/mobile-beta. No source snapshots altered.

| Check | Local result |
|---|---|
| Python import/sync/build/packaging unit tests |21passed |
| Planner JS |11passed |
| Existing locale/SEO JS |4passed |
| New beta locale/educational arithmetic JS |2passed |
| Existing preview Chromium |9passed |
| Existing art pair Chromium |4passed |
| Legacy mobile smoke |1passed |
| New publish-boundary Chromium |1passed |
| Beta output under strict CSP |7passed |
| Two consecutive builds/checksums/audit |passed, byte-identical manifests |

Beta scenarios: four languages,320/360/393/430px,10goals/two columns, compact nav, no horizontal overflow; all categories open with learning item; grid scroll restored; native modal background lock/inert, Tab wrapping/focus restoration; browser Back item→list→home, Escape, actual pointer swipe;820ms first action, quick repeat, actual atlas backgrounds under CSP; quantity/recursive yields/deficits/inventory/plans, reload/result cache, editor, source isolation, import/export/full beta restore, cycles, damaged saved recipes preserved, invalid import, missing examples/art, damaged locale JSON, storage failure, slow network and standalone HTML with zero subresource requests.

The previous Pages interface-specific tests were updated to the new actual beta entry/boundary rather than retained against obsolete selectors. Legacy and previous preview/art source regression suites still run. CI includes new beta JS/browser cases. CSP was not relaxed to make tests pass; Playwright string predicates were changed to function predicates because CSP correctly rejected eval in the test harness. No unsafe-inline or unsafe-eval is enabled.

See `STAGE6_PERFORMANCE.json` for actual local measurements and `STAGE6_DIST_AUDIT.json` for every public file checksum. First-screen decoded resource bytes (not compressed transfer) approx100–105KB depending on locale; zero game-data requests or initial atlases. CPU4×/150ms/150000B/s home readiness approx1.56s; exact measured value is recorded. Four-pose crossfade is not a claim of eight authored frames. Offline HTML is larger because it embeds both atlases up front.

Limits: emulated touch Chromium only, no physical Android/IME/screen reader/native-speaker QA. Strict-CSP local HTTP tests do not prove real Cloudflare applied headers/HTTPS/redirect rules; no deployment was performed. No public online preview or verified pages.dev hostname. All4game-data/rights questions remain separate; only the original educational fixture set is included.

## Remote CI and owner artifacts

[CI43593544711](https://github.com/moi-pary72/hytale-craft/actions/runs/43593544711) test job/all steps succeeded for code7176b06ac767539f62c0eca7e9cfe688af53a39a, including public boundary build/audit and Chromium suites. [Draft PR6](https://github.com/moi-pary72/hytale-craft/pull/6) targets PR5 branch.12initial Drive uploads metadata-verified, CRC/localSHA receipts in STAGE6_DRIVE_BACKUPS.json. No public deployment or real HTTPS/Cloudflare validation claimed; later commits are docs/receipts only.

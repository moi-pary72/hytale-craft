# Commercial data readiness — 14 November 2026

**Commercial launch: blocked. No ads or monetization added.** This is an engineering readiness assessment, not a legal opinion or an assertion of rights. A free preview in a monetization project is not automatically a licensed commercial use.

## What the current permissions actually say

- [HySphere data license](https://hysphere.app/about#data-license) covers attribution for personal, educational and non-commercial citation/linking. The [public export](https://hysphere.app/data) is labelled non-commercial. It does not grant this project a commercial database-republication license. Even broad non-commercial mirroring rights should be clarified in writing: the site text speaks of citation/linking. Our snapshot is descriptive, dated, community-extracted; exact build unknown. Do not add ads, affiliate links, paid access, sponsorship or promote it as commercial-ready.
- [HySphere contact](https://hysphere.app/contact) offers a form for partnership/attribution requests; no public inbox is published. Permission **can be requested**, but no request has been sent and no approval exists. We did not submit the owner's identity or contact anyone automatically.
- [Hytale EULA](https://hytale.com/eula), version 2.3, effective 2026-01-13, permits some monetized mods subject to conditions and prohibits distributing original game files. Those mod permissions are not a blanket commercial license for an extracted recipe website. A game purchase grants access, not ownership of game content. Seek clarification on descriptive normalized recipes/names, rights of redistribution, update automation and trademark presentation.
- [Creator policy URL](https://hytale.com/creator-policy) currently resolves to Support-a-Creator affiliate program terms (v1.1, 2026-03-18). Membership would concern eligible content and affiliate commissions; it would not remove third-party database restrictions or automatically license this site's dataset. No account/application created.
- OpenHytale has a documented open descriptive API, but no explicit commercial database license was verified. It supplies IDs, not recipe bodies. It cannot replace the current recipes for commercial launch without additional evidence and permissions.
- HytaleDB and Hytale Source restrict bulk downloading/republication; their data is not a commercial fallback. No bulk scraping performed.

## Concrete paths to unblock

| Path | Required evidence | What it solves | Remaining issues |
|---|---|---|---|
| Written HySphere license | Explicit permission for storage, transformation, public display, commercial/advertising use, distribution via public Git, backups, automated updates, territories/languages, duration, attribution and termination | Rights to their compilation/tooling/export presentation | Underlying game IP, exact build/quality and retention terms still need verification |
| Independently normalized licensed assets | Authorized owner obtains Assets.zip with official OAuth; confirm game terms or written studio permission for publishing descriptive derived fields commercially; document independent pipeline and exact build | Avoids reliance on HySphere's compilation | Does not automatically remove game rights restrictions; do not publish original ZIP/JSON/binaries/icons or treat EULA mod rights as blanket permission |
| User-owned recipes only | Original UI/code/art, manual recipe input, clear user-data policy; rights assessment before monetization | Removes bundled third-party recipe dataset | Less useful onboarding; user submissions and game names still require thoughtful handling |

Do not “clean” HySphere data and call it independent. New dataset must be built independently from authorized inputs, with provenance and checksums. Keep it version-isolated; do not silently backfill with restricted data. Existing backups remain restricted too.

## Owner-ready request draft (not sent)

Subject: Commercial permission request — Hytale Craft recipe planner

Hello HySphere team,
We are building Hytale Craft, an independent mobile crafting planner. We would like written permission to use your sphere-data/v1 item names, IDs, recipe inputs/outputs and station requirements, cache normalized snapshots, publish them in our public source repository, keep private backups and periodically update them. We intend future advertising or other monetization, but have not added any.
Could you specify whether this use is permitted commercially, the required attribution, allowed redistribution/transformations, update access, license duration, territories/languages, revocation and deletion requirements, and any fees? Please also clarify the scope of underlying game-data rights covered by your permission. We can provide a preview and exact fields for review.
Thank you.

Owner must supply their real contact details and approve/send through the official form. No invented email address, no automated message sent. Record the actual response, scope and date in the project passport before changing readiness to approved.

## Launch gates

Design approval → language/native-speaker review → explicit data rights for intended use → licensed build verification → physical Android check → owner-approved merge/deployment. Domain purchase, ads/affiliate/analytics SDKs, outreach and account creation require separate explicit actions; none were done here.

## Stage 4 public-test distinction — 2026-11-14

A free test with no ads may fit noncommercial purposes, but the verified HySphere wording about citation/linking does not conclusively authorize full snapshot republication. No permission response was obtained. The new Pages builder defaults to **user-only** (no bundled HySphere or OpenHytale data), while an explicit `noncommercial-review` mode keeps the existing restricted snapshot for owner review. That switch is a packaging choice, not a licence. Public hosting of the full dataset and all commercial/advertising/affiliate use remain separate permission gates. Source terms were reviewed again; no scraping, account creation or contact submission was performed. Alternatives remain an independently normalized licensed archive with derived-data permission, or user-entered recipes without bundled third-party compilation. An Assets.zip purchase/access alone does not resolve publication rights.

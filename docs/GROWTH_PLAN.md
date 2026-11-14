# International growth plan — preparation only

Positioning: **Choose what you want to do in Hytale; find out what you need.** Lead with one practical task, not a large encyclopedia. No traffic/revenue promises. No accounts, social posts, analytics or outreach have been created automatically.

## Release sequence

1. Keep design preview noindex and out of sitemap. Approve art/navigation separately. EN/RU/ES/PT-BR UI dictionaries have explicit QA gates; source item names remain English and never masquerade as official localization.
2. Resolve commercial-data rights (COMMERCIAL_DATA_READINESS.md). Check exact-build reliability, mobile performance, keyboard use, readable errors and backup behavior.
3. Publish only after owner permission. One canonical application URL initially. Browser-selected languages are UI states, not separately indexable pages: do not invent hreflang URLs or mass-generate duplicate item pages. Preview/importer/data/docs are not SEO landing pages.
4. Submit the single canonical sitemap manually in owner-controlled Google Search Console and Bing Webmaster Tools after domain verification. Avoid fabricated schema ratings, unsupported Recipe structured data (that schema is for food) and pages claiming an official relationship.

## Free channels and useful content

| Channel | Material | First experiment | Measure without tracking users |
|---|---|---|---|
| Google / Bing | Concise original task explanation, source/date, fast interface | One useful indexed homepage; answer “materials for a crafting goal” honestly | Search Console/Bing aggregate queries and impressions after owner setup; no client tracker |
| Reddit | Transparent fan-tool demo and limitations | Ask moderators whether a short demo/helpful reply is welcome; respect self-promotion rules | Qualitative feedback and aggregate referrals if available under a privacy-reviewed hosting policy |
| Discord | A compact screenshot or support answer relevant to a real question | Owner requests moderator permission and posts manually in appropriate channel | Opt-in feedback; no DM automation, scraping or member collection |
| YouTube Shorts | 15–30s original recording: choose weapon → quantity → inventory → list | English captions, then native-reviewed RU/ES/PT-BR versions | Platform aggregate views/completion; no profiling on our site |
| TikTok | Same practical walkthrough, platform-appropriate captions | One clearly unofficial tutorial, no invented game facts | Platform aggregates; minors-aware settings and no retargeting |
| Game communities | Share a checklist and explain source/build limits | Small feedback session with volunteers | Anonymous written usability observations; no usernames stored unless necessary/consented |

Do not cross-post identical spam, create fake endorsements or target children with monetization. Publishing posts and contacting moderators are owner actions, not authorized background automation.

## Domain transition plan

No domain chosen or purchased. Owner chooses/owns the name and confirms trademark presentation. Configure GitHub Pages custom domain and DNS only after approval; enable HTTPS and verify certificate/DNS takeover protections. Add CNAME only when domain ownership is verified. Update canonical, og:url, og:image, robots Sitemap and sitemap loc in one reviewed PR. Pages redirects and old URL behavior must be checked on the actual hosting setup; do not promise a configurable 301 without testing.

Browser localStorage is origin-specific: a move from github.io to a custom domain will not carry recipes/inventory automatically. Before migration provide export/import instructions; never silently transfer personal data to a new origin. Keep the old origin accessible long enough for users to export. Later localized URLs require real translated static content, unique canonicals, reciprocal hreflang and x-default; first prepare actual content, not empty locale shells.

## Privacy and minors

Current preview sends no analytics/events, uses no third-party fonts/SDKs/cookies, asks for no identity/age/email. Recipes/plans/inventory/language remain browser storage. Hosting sees normal HTTP requests and may retain IP/access logs; do not call the site “zero data processing”. External source links navigate only when clicked. Minors may use the tool: avoid advertising IDs, fingerprinting, session replay and behavioral targeting. Before any analytics, define purpose/data retention/legal basis/regions/age implications, assess consent and privacy notice needs, minimize data, and obtain owner approval. “Cookieless” alone does not establish compliance.

## Initial success criteria

New player can choose a goal and reach a usable recipe without guidance; no false calculations; readable 320px layout; keyboard flow; tested missing/corrupt snapshots; preserved backups. Review aggregate search performance only after launch. Choose next content by real questions, not page volume.


## GitHub Project Pages robots limitation

This repository's robots.txt is served at `/hytale-craft/robots.txt`. Crawlers look for `/robots.txt` at the **host root**, so the project file alone does not control the current github.io host. We did not touch another repository to change that root. Preview and asset importer carry their own meta noindex and remain outside sitemap; do not block them before crawlers can read noindex. Data/docs Disallow rules are a reviewed template for a setup where host-root control exists, not a privacy boundary. On a future custom domain/root deployment, adjust every path and test the actual host-root response. sitemap.xml is explicitly available for owner submission; discovery is not claimed merely because a file exists.

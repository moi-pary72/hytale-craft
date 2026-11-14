# Owner-authorized production launch — in preparation, not yet published

Owner explicitly approved sequential PR2–7 merges and free educational beta deployment. Earlier no-merge/no-deploy and separate-preview instructions are superseded. Target one Cloudflare project hytale-craft, productionmain, user-only dist, automatic main updates; no restricted datasets/ads/paid services.

Resolved blocker: owner switched Pages Source to GitHub Actions; REST now confirms workflow mode. The earlier integration403 is historical. Authorized sequential merges have resumed. This is missing integration administration permission, not missing user authorization. Do not merge intermediate snapshots into a root-published site. No main merge/deploy performed yet.

Main backup remote tag backup/main-before-beta-20261114 →1c9c1e035207b954894fdba225ceca2dc4742f38; CRC/SHA-verified ZIP saved/read back on Drive. PR6 language-persistence race fixed by69e6000; initial CI passed, then an abort-on-reload rollback was removed and a delayed-network regression added; new heads must pass. Prepared codex/production-launch adds an audited-dist Pages workflow, Github project-path404 and meta CSP, one main Cloudflare configuration. PRODUCTION_LAUNCH.md records exact blocker, authorized continuation/merge sequence, Android setup and rollback.

Runtime changes only fix language-save race; art, examples, calculators and user storage retained. No verified game catalog is published. Cloudflare account access absent; expected domain is not a confirmed live site. Previous history below is preserved.

---

# Stage7 — isolated HTTPS preview preparation (2026-11-14)

Final documentation backup ad245718f3879fe5e8dfff7ccca1857047d8470b verified by Drive name/size/parent: https://drive.google.com/file/d/1xR-e_sGKnNLayijpk1aQsPOyA4y57MPm/view?usp=drivesdk . Total7 Stage7 files; native passport appended with guarded revision preserving history. No public deploy/merge/settings change; later commits are receipts only.

Branch `codex/https-preview` based on PR6 head79941caba61bf5fd73812e32e6f7f4b579771f67, stack2→3→4→5→6→[draftPR7](https://github.com/moi-pary72/hytale-craft/pull/7). No merge, main change or deployment. Runtime/art/data identical to Stage6; all24public file hashes match. Four educational examples remain explicitly NOT Hytale.

**GitHub Pages settings actually verified through REST**: legacy publishing from main:/, public+HTTPS, built commit1c9c1e035207b954894fdba225ceca2dc4742f38, build2026-11-14T08:19:28Z. Therefore main merges can really publish the existing site; do not merge for preview. All current PR2–6 heads are draft/unmerged and CI-success, exact snapshots in reports/STAGE7_GITHUB_STATE.json. No deployment workflow is checked in; source updates create automation PRs, not merges.

Cloudflare tools/account connection are unavailable here; no project/settings/slug checked or created. Official docs confirm a test branch can be deployed without main merge. Recommended new isolated Pages project hytale-craft-preview, Production branch codex/https-preview, FrameworkNone, exact user-only Python command, outputdist. Its first deploy is called production in that new project but is a public test requiring separate owner approval. Existing configured projects can use true non-production previews; do not reconfigure an unknown production project blindly. URLs are public by default/noindex is not access control.

Android owner steps and approval boundary: CLOUDFLARE_ANDROID_PREVIEW.md. `.cloudflare/preview-settings.json` is a reference, not auto-applied API configuration. CI saves an audited dist artifact only for this test branch, no deployment job/token. Cloudflare Git default auto-deploy must be restricted by owner after the first approved deploy; don't choose All non-Production branches or main. No paid service, DNS, analytics, old data or art change.

Local checks:21Python+17JS and7beta mobile scenarios passed; existing full suite runs in CI. Audit verifies24files/23content checksums, no game snapshots/private/docs/backups, no secret-like patterns; hashes identical to Stage6. Current limits remain physical Android, actual HTTPS/Cloudflare headers/Back behavior on hardware,8final scenes and smooth authored animation. Source code is ready for owner-approved connection, not an already live site. Owner must use the actual URL returned by Cloudflare, no guessed preview link.

Reports: STAGE7_DIST_AUDIT.json, STAGE7_GITHUB_STATE.json, STAGE7_TEST_RESULTS.md. Receipts/CI/artifact IDs and Drive verification will be recorded after actual completion. Previous history below is preserved.

---

# Stage6 — mobile beta candidate, awaiting merge/deployment approval (2026-11-14)

Final documentation checkpoint `6c009cffb091ff61382b91ec4d6556c09307bae3` additionally archived and metadata-readback verified: https://drive.google.com/file/d/1MKoM9EOlwnFNRNc2vr-bGbYCQiDAB0Qk/view?usp=drivesdk . Total13 Stage6 uploads, existing folders/sharing unchanged. Runtime checkpoint7176b06a remains unchanged; later commits contain documentation receipts only.

Branch `codex/mobile-beta`, based on PR5 head `6e1e5da61be9398a7f20efeb8ed6af9a5dfdff70`. Stack PR2→3→4→5→[draft PR6](https://github.com/moi-pary72/hytale-craft/pull/6); prior branches/main/production unchanged. This is a prepared **free educational UX beta**, not a verified Hytale recipe catalog. No public deployment or hostname created.

## Current entry/architecture

- `beta.html`, `web/beta/app.js`, `style.css`, `examples.js`:10goals,2mobile columns, two PR5 rendered scenes plus eight functional symbols (final art pending), compact Home/Inventory/Plan/More nav. Optional short actions then native modal bottom sheet, no goal scrollIntoView. Sheet68dvh/expand94dvh, internal item/recipe/calc routes, body lock, focus trap/return, Escape/swipe/browser Back; repeat goals do not wait. Native Android device/IME/reader QA remains pending.
- Existing `web/planner.js` is reused; old `index.html`, `preview.html`, `art-preview.html` and tests are preserved as source/history. No legacy/interface files are included accidentally in beta publication. User recipe/inventory keys retained; source-separated beta plans; user import/export/full beta backup, guarded saves, cycle/quantity/overflow checks and damaged-data preservation. Quantity/results cache survives panel navigation and same-tab reload when sessionStorage works, validated against current recipe/inventory signature.
- Two original four-pose PR5 atlases preserved, with90ms pose crossfades and820ms one-shot; max120ms network wait, poster fallback, one action, reduced motion/Save-Data and hidden-page cancellation. No full-card scaling substitute, no new8–12authored frames or rig. Additional art frames and eight remaining scenes still need owner approval/provision. Reference folder remains https://drive.google.com/drive/folders/1_IZebF8sttpwqA1B-rP4oH9HuX7xG1Ve ; primary https://drive.google.com/file/d/1r8teXmtwr_Ml9prg1z9Skb39P4jFaVEE/view . Never use the rejected Stage3/4 SVG look as final art.
- Four **original educational recipes**, prefixed lesson:, displayed as NOT Hytale. No source-backed game recipe published in beta. Existing623HySphere recipes/3219items and separate3641/403ID snapshot remain unchanged/excluded. No fake game stations, official localization or provenance asserted. See EDUCATIONAL_EXAMPLES.md.
- EN/RU/ES/PT-BR share existing base UI plus `locales/beta/` dictionaries, browser detection/manual preference. Native-speaker QA remains pending; FR/DE/Chinese not offered. No ads/trackers/external fonts.

## Publish boundary and review

`python3 scripts/build_pages.py --data-policy user-only` now emits beta into `dist`, including both PR5 posters/atlases and beta JS/CSS. Restricted modes **rejected**. `scripts/audit_pages.py` checks24-file whitelist/checksums, new entry, indexing gates, absent source snapshots/internal files and external script/CSS network references. Consecutive builds are byte-reproducible. Exact counts/bytes/hashes in `reports/STAGE6_DIST_AUDIT.json`.

`python3 scripts/export_beta.py` makes a standalone UI/art/lesson HTML; served locally in tests with one document/no subresources, actual Android file handling untested. No public online URL was created, because Deploy requires separate owner approval. Intended future host hytale-craft.pages.dev is unclaimed/unverified in this task. Exact Free settings/HTTPS/domain/rollback and **safe PR2–6 merge order**: `CLOUDFLARE_PAGES.md`. Main merges may trigger existing GitHub Pages publication; check settings before approval/action. Never publish source root/old index.

## Verification and next step

21Python+17JS tests;9existing preview+4art+1legacy+1publish boundary+7beta Chromium cases passed locally. Widths320/360/393/430,4locales, modal/history/focus/swipe, persistence/import/backup, damaged/missing data, strict CSP, slow network and offline preview covered. Exact scope/limits/performance: reports/STAGE6_TEST_RESULTS.md and STAGE6_PERFORMANCE.json. CI is updated; its actual final status is recorded separately when observed.

Next owner action: review home/panel/result screenshots and standalone beta; confirm whether to approve a **free educational public test**. Eight final illustrations, smooth authored motion, native-language/physical Android QA and verified game-data rights remain pending. Merge and Deploy are separate explicit approvals. No public Hytale recipe dataset can be enabled silently. Drive receipts/backups for this stage are recorded after upload verification; prior history below remains intact.

---

# Stage5 — reference-led rendered pair, awaiting owner approval (2026-11-14)

Final documentation checkpoint `8335fc5b99a68554abc5703053f7adbfa0c5f0c9` additionally backed up and metadata-readback verified: https://drive.google.com/file/d/1A24aqZUdV9BSdlQfAkTPkJDlZai91dXD/view?usp=drivesdk . Total12 Stage5 uploads. Runtime remains checkpoint1a978c99; later changes are receipts only.

**Permanent art reference folder:** https://drive.google.com/drive/folders/1_IZebF8sttpwqA1B-rP4oH9HuX7xG1Ve . **Primary:** https://drive.google.com/file/d/1r8teXmtwr_Ml9prg1z9Skb39P4jFaVEE/view . See `APPROVED_DESIGN_REFERENCES.md` for all four images and README. They were visually inspected before coding. Owner rejected Stage3/4 SVG look; do not use those as approved final art. Historical descriptions below are retained, not current art approval.

Current branch `codex/approved-art-pair`, based on PR4 head7744a5af2971a9eb2e3f515def15ea7da396c4f7. Stack PR2→3→4→[draft PR5](https://github.com/moi-pary72/hytale-craft/pull/5); no prior branch/main/deployment changed. Stage5 isolates only Fight + Gather resources for approval, not all ten new illustrations.

- `art-preview.html` generated from existing preview by `scripts/build_art_preview.py`, with `web/art-pair/` and original `assets/art-pair/` WebP scenes. Two adjacent rendered character cards with angular coloured frames; remaining eight are accessible text scaffolds marked pending art. Labels remain HTML and all four launch UI languages work. Default Pages output remains unchanged; art preview/assets are excluded from its allowlist pending approval.
- Original AI-generated atlas PNG masters: four real key poses per character (sword swing and pickaxe strike/sparks). WebP posters/atlases plus provenance/hashes and all-ten action contracts in `assets/art-pair`. No copied game assets, logo or raw references in Git. Masters and private comparison saved to existing Drive structure with metadata verification receipts in `reports/STAGE5_DRIVE_BACKUPS.json`.
- Runtime:900ms one-shot, single active action, pointer/focus/hover, replay controls; no loop/video/audio/3D runtime or card-scale substitute. Four key poses are a flipbook sample, not smooth final animation. Reduced motion/Save-Data/disabled toggle use full still cards. Lazy atlas decode, cancellation, hidden-page stop and failure fallback. Review uses user-only data: no HySphere/ID JSON bundled/fetched. Existing calc/tools and stored user recipes remain available.
- Standalone owner HTML via `python3 scripts/build_art_preview.py --offline` contains only UI/art, no game dataset. It is downloadable, not a public deployment; file:// on physical Android remains untested. Existing source/code/data retained. Optional hook in `web/preview/app.js` is inactive outside the art review.
- Current results:20Python+15JS,9preview+2Pages+1legacy+4art browser cases passed locally; widths320/360/393/430 and4locales. Performance/provenance/source limitations: `reports/STAGE5_TEST_RESULTS.md`, `STAGE5_PERFORMANCE.json`, `STAGE5_ART_PAIR.md`. Local CPU4×/150ms/150KB/s poster-ready1.653s; ~115–119KB startup, zero dataset/atlas requests initially.

Next step is owner approval of the **concrete pair**, available in review HTML, action video and reference comparison. User explicitly requires this before generating/integrating the remaining eight final illustrations. Their shot/frame specifications and integration steps are in `STAGE5_ART_PAIR.md`; do not automatically spread the candidate look. No merge/deploy permitted. Data rights, commercial readiness, physical Android and native-language QA remain unresolved as before.

---

# Stage 4 — Cloudflare/public test preparation (2026-11-14)

Current work: `codex/cloudflare-testing-ready`, based on PR3 head `7267f2891b0edd9d91d3616ea4c21e5353a420c3`. Dependency is **PR2 → PR3 → [draft PR4](https://github.com/moi-pary72/hytale-craft/pull/4)**; main and prior branches stay unchanged. No deployment or merge authorized/performed.

- Audit/fixes: `reports/STAGE4_AUDIT.md`. Goal changes clear stale cards; malformed metadata fails safely; preview detects legacy/other-tab recipe changes before save; add-plan preserves storage warnings; bounded data requests and safe retry. Shared recipe engine validates additional schema fields. Existing snapshots/IDs/calculation semantics retained.
- Packaging: `scripts/build_pages.py` is a standard-library staging build, **not** deploy code. It writes NEW interface from `preview.html` to `dist/index.html` and copies only allowlisted runtime files. Never publish source root/legacy index. `dist` is ignored. Default `user-only` excludes third-party catalogs; explicit `noncommercial-review` includes pinned snapshots for owner review with unchanged legal restrictions. Test/noindex remains enabled in every build.
- Exact future Pages settings, HTTPS/domain/rollback/data-update path: `CLOUDFLARE_PAGES.md`. No account connected, Pages project or URL created. Saving a Git integration can itself publish; requires owner's separate decision.
- Four complete preview dictionaries EN/RU/ES/PT-BR now include concurrency/timeout/testing messages. FR/DE/Chinese remain hidden drafts. Native-speaker QA still needed; original EN game data remain separate. Legacy source is retained but excluded from new deployment output.
- Art stays original SVG prototype. `FINAL_ILLUSTRATIONS_BRIEF.md` specifies all ten final shots, sizes/budgets, rights and acceptance. No final art created/commissioned, no copied game assets.
- Tests and Drive receipts: `reports/STAGE4_TEST_RESULTS.md`, `STAGE4_PERFORMANCE.json`, `STAGE4_DRIVE_BACKUPS.json` (12 uploads verified by metadata readback). Existing history below is preserved. Backups go into the same six existing Drive folders, no duplicate folder creation.
- Publication readiness: code is locally reviewable, full bundled data public/commercial clearance remains blocked. Public testing can instead use a user-only build after owner approves hosting; this alone does not approve commercial launch. No analytics/ads/paid service added.

Code checkpoint `d94523240252b87563cd12d7456ef7b86d371d66` passed GitHub CI [43585948449](https://github.com/moi-pary72/hytale-craft/actions/runs/43585948449). Passport was appended without replacing previous history. Owner HTML: https://drive.google.com/file/d/1NUbM7S9ZtijX29imQb7CzMuWyR5H1zEj/view . Upload hashes/links are in the Stage4 Drive manifest; sharing permissions unchanged.

Next: owner checks Android review artifact/screenshots, obtains native-language QA and decides whether a user-only public test should be published; separately request written HySphere scope for public mirroring/commercial use or independently derive permitted data. Merge/rebase the stack only with explicit permission and after checking concurrent changes. Physical Android, real Pages headers/HTTPS and final art remain unverified. Download/local HTTP steps and storage limits are in `ANDROID_REVIEW.md`.

---

# Stage 3 — International UX preview (2026-11-14)

Актуальное продолжение: ветка `codex/international-ux-preview`, основана на PR №2 head `d90e0105ec9c9a4283e0f142fdc4092df471c77b`. Main/production и ветка PR №2 не меняются. Отдельный draft [PR №3](https://github.com/moi-pary72/hytale-craft/pull/3) нацелен на ветку PR №2: сначала согласовать визуальный концепт, не выполнять merge автоматически.

## Что добавлено

- `preview.html` и `web/preview/`: работающий goal-first интерфейс поверх прежних planner/game-recipes engines, snapshots и ключей user storage. `index.html` сохраняет текущий дизайн; в нём добавлены только SEO metadata и helper. Старый asset importer получает noindex.
- Десять крупных целей по две в ряд на мобильном, оригинальные SVG miniature scenes (`assets/preview`, генератор `scripts/build_preview_scenes.py`). Это векторные прототипы 3D art direction, не официальные ассеты и не утверждённый финальный дизайн. Подробнее `UX_PREVIEW.md`.
- Preview подключает все 623 recipes/отдельный OpenHytale IDs, карточки, quantity/inventory/leftovers/stations, shared-stock batch plan, editor/JSON import-export, cycle/acquire/incomplete warnings и SHA-256. Снимки JSON и engines не изменены. Snapshot fetch отложен до цели/расчёта, на первом экране их нет.
- UI dictionaries `locales/en.json`, `ru.json`, `es.json`, `pt-BR.json` имеют одинаковое полное покрытие всех preview UI keys. Browser detection, manual override/persistence, regional fallback, защита async language race. Языки FR/DE/zh-Hans — draft, не selectable. Оригинальные EN game names/IDs отделены от UI. Официальные переводы игровых названий не придумываются.
- EN/RU/ES/PT-BR технически полностью покрывают **preview**, native-speaker QA ещё не проведена. Старый index/asset-importer остаётся с прежним частичным EN/RU, не объявлять весь production полностью локализованным. После утверждения концепта отдельно решить, переносить preview в основной entry point.
- SEO: one canonical URL, root title/description/OG locale/image, original social card, sitemap only homepage, preview/importer noindex. robots.txt в GitHub project subpath сам по себе не контролирует host-root robots; это ограничение задокументировано, другие репозитории не менялись. Нет фиктивных localized URLs/hreflang, нет дублирующих item SEO pages.
- `scripts/export_preview.py`: self-contained HTML с original CSS/JS/SVG + pinned snapshots/словари для owner review без deploy. Коммерческие ограничения данных остаются. file:// заблокирован политикой browser environment, не обходился; artifact проверен через разрешённый local HTTP без подресурсных запросов. Actual Android file viewer не проверен. local file и hosted origin имеют отдельный storage, нужен явный export/import.
- `COMMERCIAL_DATA_READINESS.md`: запрет коммерческого запуска с текущей лицензией, проверенные URL, конкретные пути разрешения, готовый unsent запрос HySphere. `GROWTH_PLAN.md`: бесплатные каналы, SEO, домен/localStorage migration, privacy/minors gates. Никаких ads/analytics/accounts/outreach/domain changes.

## Проверки и результаты этапа 3

14 прежних Python tests + 11 прежних JS regression tests; 4 новых JS localization/SEO tests; 6 новых browser scenarios (включают четыре языка, widths320/393, keyboard skip/focus, исходные данные без потерь, реальный shortbow/inventory/batch/editor/export/import, bad/missing snapshot, broken user storage, delayed catalog plan, self-contained export, throttled startup). Прежний mobile regression test тоже запускается. GitHub CI дополняется этими тестами.

Стартовый preview ≈57–61KB decoded resources; 0 data JSON requests до цели, 0 постоянных animations. Local CPU×4 + 150ms latency +150000bytes/s: точное измерение и ограничения в reports/STAGE3_PERFORMANCE.json. Это не physical Android или field performance guarantee.

Новые действия владельца: оценить screenshot/preview и оригинальный арт-концепт; дать native QA переводов; получить письменные коммерческие права/сменить источник; отдельно разрешить merge/deployment. Ни запуск рекламы, ни сам домен, ни публичный деплой сейчас не готовы автоматически. Подробный этап2 контекст и права/данные сохранены ниже.

---

# Hytale Craft — актуальное состояние

Обновлено 2026-11-14, второй этап ревью PR №2. Предыдущие события сохранены в `DEVELOPMENT_HISTORY.md` и Google Docs; старые утверждения «0 рецептов» относились к первому этапу.

Репозиторий: https://github.com/moi-pary72/hytale-craft . PR: https://github.com/moi-pary72/hytale-craft/pull/2 . Ветка `codex/verified-catalog-planner`. Main `1c9c1e035207b954894fdba225ceca2dc4742f38` не меняется. Сайт https://moi-pary72.github.io/hytale-craft/ в этом этапе не публикуется. `moi-pary72/moi-pary` — другой проект, не трогать.

## Назначение и архитектура

Мобильный помощник крафта, а не игровой портал. Static GitHub Pages; без сборки/сервера. Существующие тёмный дизайн, плитки целей, редактор/импорт/экспорт и browser storage сохранены.

- `index.html`: оригинальный интерфейс/CSS, пользовательский planner, локализация, редактор, ручные JSON-импорты и цели.
- `asset-importer.html`: отдельный ручной importer; Parent/группы/Metadata отклоняются, не выдаются за достоверный рецепт.
- `web/planner.js`: общий engine — инвентарь, партии/выход, leftovers, общий stock, циклы, лимиты.
- `web/game-recipes.js`: schema validation и отдельный adapter source-backed snapshot; версии и пользовательские рецепты не смешиваются; альтернативы/явное получение промежуточного предмета отдельно; stations и unexpanded warnings.
- `web/catalog.js`: версии источников, поиск name/ID, категории, карточки, количество, инвентарь, список, копирование, массовый план и сохранение по revision.
- `data/recipes/manifest.json`: pointer + SHA-256; `hysphere-2026-08-12.json`: активный recipe snapshot.
- `data/catalog.json`: старый ID-only OpenHytale snapshot, выбирается отдельно.
- `scripts/sync_recipes.py`: документированные JSON exports HySphere; схема/counts/license/revision/quantities/refs/stations; отдельно rejects; deterministic snapshots и backup; никакого HTML scraping.
- `scripts/import_game_assets.py`: локальный ZIP → `.private/` review candidate, Parent, CRC чтения ZIP/SHA-256, inputs/outputs/stations/groups; не публикует автоматически.
- `scripts/sync_catalog.py`: OpenHytale ID importer. Остальные check/discover/probe/monitor скрипты — диагностика, не доказательство игровой базы.
- `.github/workflows/validate.yml`: Python + JS + mobile Playwright Chromium. `sync-recipes.yml` и `sync-catalog.yml`: daily updates через PR, без auto-merge. Остальные пять workflows — source diagnostics.
- `tests/`: unit, source contract, реальные regression assertions и синтетические fixtures; browser_smoke. Тестовые рецепты в production data не входят.
- `docs/DATA_SCHEMA.md`, `ASSETS_IMPORT.md`, `DATA_SOURCES.md`: контракты, безопасный доступ к архиву, источники и лицензии.

## Реально полученные данные

**HySphere: 3219 предметов, 623 source-backed полных рецепта с явными ингредиентами и количествами; 1486 неполных/неподдерживаемых записей отдельно.** Исходный экспорт содержит 2109 записей: 1706 craft и 403 salvage. Причины отбраковки пересекаются: 1074 unresolved inputs, 47 unresolved station, 423 multiple/missing outputs, 403 salvage. Это не числа отдельных уникальных видов ошибок.

Происхождение — описательные данные из открытого экспорта https://hysphere.app/data , extraction 2026-08-12T11:09:57.625Z, gameVersion Early Access, **точная build неизвестна**. Source-backed означает проверку исходного открытого набора и структурной полноты, а не official verification. Никакой актуальности для текущего релиза не обещать. Использование: non-commercial attribution; ссылка HySphere показывается в карточке. Перед монетизацией нужно сменить источник или получить права. Иконки/игровые binaries не копируются.

**OpenHytale: 3641 ID предметов и 403 ID рецептов**, generated 2026-07-06, game build неизвестна, recipe bodies нет. Не складывать 3641 и 3219 как число уникальных предметов; наборы пересекаются и разных дат. Они не смешиваются в вычислениях.

Официальный Assets.zip не получен, официально сверенных на нашей копии игры рецептов **0**. Но исходные реальные рецепты независимого источника теперь доступны, их нельзя путать с синтетикой.

## Что работает

Цель→Сражаться→Оружие показывает карточки реальных предметов. Crude Shortbow приоритетно виден; поиск «Простой короткий лук» — пользовательский alias, официальное имя EN из источника. Клик сразу открывает карточку с источником/датой/ограничением версии, ингредиентами, количеством выхода и перечислением станций.

2 Crude Shortbow требуют 8 Ingredient_Stick + 12 Ingredient_Fibre; при наличии 3 sticks UI показывает 5 sticks и 12 fibre. Это проверка настоящей source-backed записи, а не восстановление старого sample. Есть recursive smelting example: copper ingots расходуются с инвентарём, остаток превращается в потребность Ore_Copper, station Furnace сохраняется.

Неизвестные/неполные recipes не рассчитываются как полноценные. Материалы без поддерживаемой цепочки обозначаются как «Нужно получить», а не гарантированные природные raw resources. Для известных неполных промежуточных recipes — warning. При cycle преобразований появляется остановка и явный выбор «получить отдельно». Несколько рецептов требуют выбора. Stations не выдумываются и не автокрафтятся как ингредиенты.

В карточке source-backed записи можно сохранить инвентарь, добавить цель в массовый план, рассчитать/скопировать список. Инвентарь не списывается постоянно. План привязан к revision источника и восстанавливается после reload. Отдельный пользовательский planner/редактор сохраняется и не может заменить публичный snapshot.

## Browser storage

`hytale-craft-recipes-v1` — старые пользовательские recipes. `hytale-craft-inventory-v1` — inventory lines. `hytale-craft-language` — язык. `hytale-craft-plan-<source revision>` — source-backed queue. Не переименовывать без миграции. Старые historical samples не удалены с устройств, помечаются неподтверждёнными; новые не внедряются.

## Проверки и границы

Второй этап: 14 Python unit tests, 11 JS tests, mobile Chromium integration, SHA-256/JSON validity, настоящие shortbow/smelting assertions. Browser test: goals/search/card/inventory/quantity/queue/reload/RU-EN/incomplete recipe/user editor/dataset isolation/cycle/acquire/checksum corruption fallback/no console errors/no horizontal overflow. Команды и фактический последний результат — `docs/reports/TEST_RESULTS.md`.

```
python -m unittest discover -s tests -v
node tests/planner.test.js
python tests/browser_smoke.py
python scripts/sync_recipes.py
```

Последняя команда обращается только к открытым export endpoints. Данные не меняются при повторном импорте. Browser smoke требует playwright + Chromium; `CHROMIUM_PATH` переопределяет `/usr/bin/chromium`. CI устанавливает зависимости. Физический Android недоступен. Нельзя утверждать, что новая версия проверена на production Pages.

## Нерешённые вопросы

- Нет точной build и русских игровых названий HySphere; 1486 записей неполны/неподдерживаемы. Нет официальной сверки всего snapshot.
- Не реализована оптимизация resource groups, salvage и multi-output. Из ZIP они сохраняются без подстановки. Field-specific inheritance merges требуют реального архива.
- Некоторые настоящие циклы требуют ручного выбора добычи; минимальная стоимость/автоматическое разрешение циклов не заявлены.
- Старый монолитный UI имеет частичный перевод; новые сценарии двуязычные. Служебные/template ID ещё могут присутствовать в каталоге.
- Non-commercial attribution — обязательное ограничение источника. Перед коммерческим запуском отдельная проверка прав.
- GitHub Actions permissions для PR могут зависеть от настроек организации; auto-merge отсутствует. Schedule новых workflows начнёт работать после их появления в default branch; merge сейчас не разрешён.

## Следующие действия

1. Просмотреть PR №2 и решить, принимать ли source-backed dated snapshot с указанными ограничениями. Merge/publication только после отдельного согласия пользователя.
2. Для полной актуальной базы владелец лицензии получает архив официальным OAuth и следует `ASSETS_IMPORT.md`. Пароль/credentials не передавать. Не отправлять игровой архив в публичный PR/Drive.
3. Проверить наследование и группы на реальной build, добавить русские локализации, права на нормализованный snapshot и сравнение с игрой; затем отдельный version-isolated источник.
4. Проверить опубликованную после разрешённого merge версию на физическом Android.

## Google Drive и история

Существующий Google Docs паспорт: https://docs.google.com/document/d/1-rruSanhYEEGBP9awFejT6CCiz9TIjE_kiypXfqsDSY . Не удалять предыдущий текст, добавлять этапы с commit/PR/CI.

После поиска Hytale и точного поиска в «Проекты с ChatGPT» папка проекта отсутствовала. В этом этапе создание разрешено и подтверждено: https://drive.google.com/drive/folders/1CyqdLmek-cig0dVSSH0y6hcfEPVRChkj . Созданы и прочитаны шесть разделов 01–06. Предыдущие отказы auto-review относятся к первому этапу и не означают текущую недоступность.

Ссылки на действительно загруженные архивы/JSON/отчёты и их checksums записываются в `docs/reports/DRIVE_BACKUPS.json` только после успешного upload+metadata readback. Наличие папки или обновление паспорта не равно резервной копии кода. GitHub Pages всегда читает данные из репозитория, не из Drive.

## Итог второго этапа: проверенные ссылки

Код/данные — `7802e0b57646708122b6b075d43cfae1c3449d7f` (включает source-backed snapshot и pin Ubuntu 24.04). Обе GitHub CI проверки этого кода успешны, включая мобильную integration: https://github.com/moi-pary72/hytale-craft/actions/runs/43578617436 . После этого менялись документы, не публичный сайт.

Десять backup-файлов действительно сохранены и metadata-readback подтверждены; манифест с URL, размерами и локальными SHA-256: `docs/reports/DRIVE_BACKUPS.json`. Remote checksum connector не возвращает. Два ZIP кода сохранены отдельно, последняя кодовая копия 7802e0b. Документы в этих ZIP относятся к моменту соответствующего commit; итоговая история и CI дополняются в Git и существующем Google Docs паспорте. Паспорт теперь в папке 01, прежняя ссылка остаётся действующей. Никаких авторизационных токенов/игровых binaries/Assets.zip в резервных копиях нет.


## Этап 3 — подтверждённый checkpoint

Код/preview: 02b0fe4d5cb74c0f005f824718aa5092a28932d4. Draft PR №3: https://github.com/moi-pary72/hytale-craft/pull/3 ; base codex/verified-catalog-planner (PR №2). Обе GitHub CI проверки success: https://github.com/moi-pary72/hytale-craft/actions/runs/43581924264 и https://github.com/moi-pary72/hytale-craft/actions/runs/43581914846 .

Шесть файлов этапа3 действительно сохранены в прежних разделах Drive, name/size/parent подтверждены metadata readback. Манифест с URL/local SHA: reports/STAGE3_DRIVE_BACKUPS.json. Автономный HTML: https://drive.google.com/file/d/1pS9eQle8hpIRp8iM5pI6S355ECFOhj2Z/view . EN screenshot: https://drive.google.com/file/d/1C3vhqJaXCj7iBTVDxhA0AFZmiTbrG8tb/view ; RU screenshot: https://drive.google.com/file/d/1ihmDO8-5wnvK_2jVLcmrf2p6PJVf-MwT/view . Remote checksum коннектор не вернул. Секретов/лицензионного Assets.zip нет. Production/main/PR2 branch не изменялись.

Final documentation ZIP (including Android guide and initial receipts), commit c7b0fc4e20f9c7945c6c652508fcd6f28c4808b9, was additionally uploaded/read back: https://drive.google.com/file/d/19xhUU9_zueOWRFOVyylw5MpOERxM3SkT/view . Runtime remains d945232 checkpoint.

Stage5 code checkpoint `1a978c9929d330052780ea1839945869c43b7509` passed remote CI [43588499509](https://github.com/moi-pary72/hytale-craft/actions/runs/43588499509). Eleven initial Drive uploads verified by name/size/parent, local hashes recorded; existing folders and sharing unchanged. Passport appended with guarded revision preserving history and permanent references. Owner HTML: https://drive.google.com/file/d/14-jkIFkTcEyVZ0TvMNDsvqpMvoAFDteX/view ; action demo: https://drive.google.com/file/d/1m2qMDRdEUMv1oyRM54oHeNbEF7OExTui/view ; reference comparison: https://drive.google.com/file/d/1XTQv7R3iD_0m9JZ66fKPoYYMQcZiiP6t/view . ZIPs represent that tested checkpoint; later commits are documentation/receipts only.

Stage6 checkpoint7176b06ac767539f62c0eca7e9cfe688af53a39a passed [CI43593544711](https://github.com/moi-pary72/hytale-craft/actions/runs/43593544711), including build/audit and all mobile tests.12initial uploads in existing Drive folders read back by name/size/parent; ZIP CRC and local SHA receipts in reports/STAGE6_DRIVE_BACKUPS.json. No new folders/sharing changes. Standalone HTML: https://drive.google.com/file/d/17HvVehf6Q6gMGCTWb4o1mA-F4dpdlK_L/view ; home393: https://drive.google.com/file/d/15Ve9XYq-1PBKlZrrKysLYIveCLgSIqzm/view ; sheet393: https://drive.google.com/file/d/1HF40OhfagVlesfZuRDzF5mRtoRJKw-DD/view ; result393: https://drive.google.com/file/d/1kQg4HUltmF0bus1w14KqHOlmaRleFRLE/view . Later receipt commits change documentation only.

Stage7 preparation0ae0edd6e2a4ebd51d49dbe3c0f43245f23507d9 passed CI43597302206, including full21Python/17JS/22browser suite and artifact upload. Artifact14114808254 was downloaded through GitHub connector, CRC/ZIP SHA256 matched GitHub digest,24runtime files/23hashes matched local/Stage6. Receipt: reports/STAGE7_CI_ARTIFACT_AUDIT.json. Six initial Drive files readback-verified; links/hashes in STAGE7_DRIVE_BACKUPS.json. Android guide: https://drive.google.com/file/d/1HxW6cB_wJUrBSZw3SLEBR7pxXa16MxLB/view . Artifact is a downloadable ZIP, not an HTTPS site; expiry2026-11-21. Later commits change docs/receipts only.

Authorized launch preflight: final PR6 c4accf4 and release PR8 8ea6720 both have green push+PR CI. Main remains unchanged because Pages administration403 is unresolved. Existing URL200 serves old version. Exact observed status/backup SHA in reports/PRODUCTION_LAUNCH_STATUS.json; no new publication claimed.

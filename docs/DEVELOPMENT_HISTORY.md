## 2026-11-16 — Deep workshop / inventory discovery draft

Independent branch from e1395d9. Audited current UI/engine/importers and selected public competitor UX without copying datasets. Reused existing calculation, storage and history; implemented branded slots/cards/detail/path/used-in and inventory feasibility with honest independent-vs-shared semantics. Added private content-addressed snapshot index over the existing canonical-v2 importer; rights gate unchanged. First browser review caught a shifted canonical-lab entrance and an offline generic-icon path; both corrected before review. No main change, merge, deploy, external messages or monetization. Links and final QA/backups recorded in docs/reports/deep-workshop.

# История разработки

## 2026-11-14 — аудит, ID-каталог и исправление карточек

База аудита: main `1c9c1e035207b954894fdba225ceca2dc4742f38`. Рабочая ветка `codex/verified-catalog-planner`.

Прочитан существующий паспорт на Google Drive. Найдены расхождения паспорта с кодом: девять исторических seeds без источника/версии; выбор предмета без обработчика карточки. Все исходные скрипты, workflow, HTML и документы просмотрены; другой репозиторий не изменялся.

Получен реальный открытый набор **3641 ID предметов / 403 ID рецептов**, но **0 полных подтверждённых рецептов**. Записаны источник и timestamp; актуальность для текущей игры не установлена. Официальный downloader ZIP проверен, игровые assets не загружены без OAuth. HytaleDB запрещает массовое скачивание; не использован для bulk import.

Решения: не выдумывать имена/ингредиенты, не смешивать community IDs с пользовательскими рецептами; убрать автоматическое создание неподтверждённых samples для новых пользователей, сохранив старые пользовательские данные. Карточки показывают статус. Одиночный и массовый калькуляторы используют один проверяемый движок; излишки больше не маскируют циклы. Добавлены лимиты и защита атомарного обновления каталога. Планировщик полностью работает с пользовательскими рецептами, игровая автоматическая рецептная база ещё не готова.

Проверки: 5 Python unit tests, 5 JS regression scenarios, мобильный Chromium 393×851 — успешно. Первый браузерный тест искал предполагаемый ID Rudimentary; исправлен на реальный `Weapon_Shortbow_Crude` из источника. Горизонтальной прокрутки и JS pageerrors нет. Проверка на физическом Android и опубликованной новой версии не выполнялась.

Добавлены CI validation и daily catalog PR workflow; не запускались на GitHub до публикации ветки. Автоматического merge нет. Сохранены отчёты проверки источников. Полное описание и оставшиеся задачи — `PROJECT_STATE.md`.

Google Drive подключён; существующий паспорт доступен. Создание структуры папок отклонено автоматической проверкой из-за риска дубликатов; запрошено уточнение. Статус фактических загрузок и ссылка PR будут добавлены после подтверждённых операций.


PR создан: https://github.com/moi-pary72/hytale-craft/pull/2 (draft, не merged). Код: https://github.com/moi-pary72/hytale-craft/commit/287b1dcb3a2a6991e0f8313a4a9943f51e334bf8 . GitHub CI validation прошёл: https://github.com/moi-pary72/hytale-craft/actions/runs/43576518362 .

Существующий Google Docs паспорт действительно обновлён через Docs API; добавлены результат, ограничения, источник и ссылка PR. Загрузка ZIP/JSON в Drive не выполнялась, структура папок остаётся заблокирована auto-review; ответ пользователя на вопрос ещё не получен. Не путать обновление документа с резервной копией исходников.

## 2026-11-14 — второй этап: ревью, реальные source-backed рецепты и Drive

Повторно fetched main и PR branch: main `1c9c1e0`, head до этапа `d16f043`, параллельных изменений не обнаружено. Изучены исходники/тесты/Actions и существующий Google Docs паспорт; прежние отчёты сверены с кодом. Review findings — `docs/reports/PR2_REVIEW.md`.

Найден новый разрешённый публичный export HySphere `sphere-data/v1`, extraction 2026-08-12. Получены реальные 3219 item / 2109 recipe records. 623 полных explicit single-output craft recipes нормализованы, 1486 неполных/неподдерживаемых (включая 403 salvage) выделены. Точная game build неизвестна; source-backed, не officially verified. English names из источника, RU не придуманы. Лицензия non-commercial attribution; ссылку на HySphere показываем. Файлы разных дат/источников не смешиваются.

В UI подключены source-backed карточки и калькулятор. Сражаться→Оружие→Crude Shortbow открывает ингредиенты/выход/станции; фраза пользователя «Простой короткий лук» — search alias. Инвентарь, партии/остатки, копирование и массовый план работают с настоящими записями; очередь сохраняется по source revision. Missing recipes предлагают свой рецепт. Старый editor/локальные записи сохраняются отдельно.

На реальном графе обнаружены cycles лепестков при изготовлении глины. Расчёт останавливается, пользователь явно выбирает получить промежуточный предмет отдельно. Автоматическая подстановка сырья/альтернатив не используется. Интеграционный тест расширен на этот случай.

Assets.zip importer разрешает документированное Parent override с циклами/неизвестными родителями, сохраняет groups/multiple/metadata/PrimaryOutput как review candidate и не публикует. Неподдерживаемые сложные данные не превращаются в конкретный ингредиент. Официальный архив по-прежнему не получен, локальный parser не проверен на полной актуальной game build.

Daily recipe workflow: HTTP allowlisted exports, schema/license/count/revision checks, local hashes, browser SHA-256, versioned snapshots, previous files, PR без merge. ID workflow больше не открывает PR из-за одного timestamp отчёта. CI дополнен Playwright mobile Chromium. Подробности — DATA_SCHEMA/ASSETS_IMPORT.

Google Drive: повторный поиск и точный parent query подтвердили отсутствие Hytale Craft; папка успешно создана в «Проекты с ChatGPT», затем шесть разделов 01–06, readback списка подтверждён. Это устраняет блокировку первого этапа. Фактические upload/checksum/readback backups будут записаны в DRIVE_BACKUPS.json после сохранения, без преждевременного заявления.

### Подтверждение второго этапа

Код/данные: `f4ca8eb` и `461b99b`; исправление воспроизводимости CI: `7802e0b57646708122b6b075d43cfae1c3449d7f`. В первом запуске Python/JS прошли, установка Playwright упала из-за ubuntu-latest (26.04); причина подтверждена логом. Validation закреплён на поддерживаемом Ubuntu 24.04. Новые **оба CI успешны**, включая браузер: https://github.com/moi-pary72/hytale-craft/actions/runs/43578617436 и https://github.com/moi-pary72/hytale-craft/actions/runs/43578613365 . Не приписывать успех старому упавшему запуску.

Существующий паспорт Docs перемещён в 01 с сохранением ID и истории; parent readback подтверждён. На Drive реально сохранены 10 файлов: два ZIP кода (461b99b/7802e0b), ZIP исходных публичных export JSON, normalized HySphere JSON, OpenHytale JSON, PROJECT_STATE.md, DEVELOPMENT_HISTORY.md, TEST_RESULTS.md, PR2_REVIEW.md, PNG mobile card. Имена/размеры/папки проверены отдельными metadata reads. Локальные SHA-256 и точные URL — docs/reports/DRIVE_BACKUPS.json. Коннектор не вернул remote checksum, поэтому проверка байтов на стороне Drive по SHA не заявлена. Игровой Assets.zip и секреты не загружались. Старые версии сохранены.

Дополнительно сохранён и metadata-readback проверен итоговый архив передачи контекста `hytale-craft-handoff-bd844ba.zip` (документы на commit bd844ba), ссылка и checksum в DRIVE_BACKUPS.json. Всего 11 файлов с этой итоговой копией; receipt самого handoff записан после создания ZIP, чтобы избежать циклического хеша. Google Docs паспорт дополнен итогами 623 recipes/CI/backups и повторно прочитан: запись подтверждена. Основная кодовая копия остаётся 7802e0b, код после неё не менялся.

## 2026-11-14 — этап 3: international UX и launch preparation

Сверены фактические main/PR2 head, прочитан Drive паспорт и документация/тесты. Параллельных изменений не было. Для reviewable визуального концепта создана отдельная зависимая ветка `codex/international-ux-preview` от d90e010, не перезаписан дизайн index. Draft PR target — ветка PR2, без merge/deploy.

Создан отдельный рабочий preview на существующих engines/data/storage: 10 goal tiles, оригинальные SVG мини-сцены, полноценные preview UI словари EN/RU/ES/PT-BR, browser/manual language choice, source isolation и все необходимые crafting/user-data tools. Данные и engines сохранены. Art остаётся prototype; FR/DE/zh-Hans остаются drafts; legacy partial EN/RU не выдаётся за полностью готовый международный production.

Проверки выявили race при reload сразу после выбора языка — предпочтение теперь сохраняется до fetch, устаревший ответ словаря не перезаписывает новый выбор. Исправлена потеря ещё не сохранённого batch textarea при первой lazy загрузке snapshot. Corrupt user JSON не удаляется и не заменяется без явного import.

Подготовлены robots/sitemap/OG и metadata; выявлено ограничение host-root robots для GitHub project Pages, не менялся чужой репозиторий. Preview/importer noindex, single canonical homepage. Домен не выбран/не куплен. Analytics/ads не добавлены.

Проверены HySphere license/contact, EULA и creator-policy URL; коммерческие права не подтверждены. Контактная форма поддерживает partnership requests, подготовлен unsent draft, ничего не отправлялось. Creator-policy URL — affiliate program, не blanket database license. Собственный normalized dataset из licensed archive тоже требует проверки прав, не автоматическая замена. Документы COMMERCIAL_DATA_READINESS.md/GROWTH_PLAN.md/UX_PREVIEW.md.

Preview metrics: home≈57–61KB decoded, no snapshots before action, no loops; widths320/393 и CPU×4/150ms network emulation. Self-contained artifact создан, file:// в managed browser blocked; policy не обходилась, альтернативный local HTTP test подтвердил отсутствие subresource requests и реальный расчёт. Физического Android нет. Новые CI/Drive backup receipts и SHA будут записаны после подтверждённых операций.


### Подтверждение этапа 3

Draft PR №3: https://github.com/moi-pary72/hytale-craft/pull/3 . Preview checkpoint 02b0fe4d5cb74c0f005f824718aa5092a28932d4. Оба CI success, включая existing mobile +6 preview tests: https://github.com/moi-pary72/hytale-craft/actions/runs/43581924264 и https://github.com/moi-pary72/hytale-craft/actions/runs/43581914846 .

Реально сохранены/metadata-readback проверены 6 stage3 файлов в существующих Drive folders: кодZIP, data+locales ZIP, docs ZIP, автономный HTML, EN PNG и RU PNG. Точные ссылки/размеры/local SHA в reports/STAGE3_DRIVE_BACKUPS.json. Архивы checkpoint02b0fe4 не включают собственный последующий receipt; новые изменения только документы. HySphere license остаётся ограничением, коммерческого approval нет. Никаких новых папок/secret/game archive/production deploy.


## 2026-11-14 — Stage4: isolated Pages test build, no publication

Independently inspected main/PR2/PR3 heads and code; continued in `codex/cloudflare-testing-ready` on PR3. Fixed stale goal cards, malformed source metadata, preview/legacy storage overwrite risk, false plan-save success and unbounded data waits. Added allowlisted `dist` builder defaulting to user-only data, new entry point, noindex, CSP/404/hash receipts; no Cloudflare connection or deploy. Expanded mobile widths320/360/393/430, all-goal/concurrency/JSON tests and actual output/CSP integration. Added final-art technical brief, exact Pages/rollback/domain instructions, public noncommercial-vs-commercial distinction. Preserved all data snapshots, prior source branches and history. See Stage4 audit/test/Drive reports for final receipts and limits.

Stage4 result: draft PR4 targets PR3, code checkpoint d94523240252b87563cd12d7456ef7b86d371d66; remote CI43585948449 success. Eleven files saved in existing Drive sections and verified by name/size/parent; local hashes in STAGE4_DRIVE_BACKUPS.json. Passport appended with guarded revision/readback preserving history. No merge/deploy.

Final documentation checkpoint c7b0fc4e was backed up separately and read back successfully (12 total Stage4 files); receipt added without altering runtime.


## 2026-11-14 — Stage5: restore approved art direction, two-card review

Owner rejected Stage3/4 SVG look. Authenticated Drive folder/README and all four design PNGs inspected first; permanent references recorded in APPROVED_DESIGN_REFERENCES.md and passport. Separate branch on PR4, no main/merge/deploy. Generated original rendered warrior/miner four-pose atlases, optimized WebP posters and900ms single-action runtime, with reduced-motion/Save-Data/failure handling and no full-card scaling substitute. Isolated art-preview.html/standalone UI-only HTML; other eight remain pending scaffolds. No game dataset bundled or published, old mechanics preserved. Added performance/tests, video and private reference comparison for owner's concrete approval before producing eight further scenes. Four poses are motion samples, final smooth animation still needs more frames/rig.

Stage5 review deliverables completed: draft PR5 on PR4, checkpoint1a978c9929d330052780ea1839945869c43b7509; CI43588499509 success.11initial Drive files verified by metadata; PNGmasters and code/data/docs ZIP CRC checked locally, SHA receipts in STAGE5_DRIVE_BACKUPS.json. Passport/history preserved and permanent reference links added. Other eight final art assets deliberately await owner's pair approval.


## 2026-11-14 — Stage6: mobile dialog beta and safe public packaging

Inspected PR2–5 heads, passport and saved art direction. Separate branch on PR5, no main/merge/deploy. Added beta shell reusing planner/storage;10goals/2columns, compact nav, native bottom sheet with selection/action/history/focus/swipe/background lock and cached quantity/results. Preserved PR5 scenes with short pose crossfades (not new authored frames);8final scenes remain pending. Added4original lesson recipes explicitly NOT Hytale, separate user scope/plans, import/export/full beta backup. Builder now publishes beta files/art and rejects restricted data mode; audit/byte reproducibility and strict CSP verified. Added beta locale/test/audit/offline artifacts and revised Cloudflare/stack-merge instructions including GitHub Pages auto-publication risk. No paid service/analytics/ads or game snapshot publication.

Stage6 result: draftPR6 targetsPR5; code7176b06ac767539f62c0eca7e9cfe688af53a39a passed CI43593544711.12initial Drive files saved/read back, ZIPCRC/localSHA in STAGE6_DRIVE_BACKUPS.json. Root passport and PROJECT_STATE now point to beta; existing art/data/history preserved. No merge/deployment.


## 2026-11-14 — Stage7: safe isolated Cloudflare connection preparation

Read actual PR2–6 heads/CI and native passport. GitHub Pages REST confirmed legacy main:/ publication, built1c9c1e0/HTTPS; no settings changed. Separate codex/https-preview on PR6, no merge/main/deploy. Added exact Android Pages setup/approval guide and non-automatic JSON settings reference; selected new isolated test project approach, explained first-deploy Cloudflare production vs real preview distinction/public-by-default. CI adds audited dist artifact only, no deployment credentials/job. Local21Python+17JS+7beta tests passed;24runtime hashes identical toStage6. No new art, game data, paid features or analytics.

Stage7 result: draftPR7 onPR6, CI43597302206 succeeded, actual CI artifact14114808254 downloaded/hash+CRC+public-boundary verified, six initial Drive files readback-verified. Main/Pages/Cloudflare unchanged. Android setup guide and exact approval boundary prepared; no live URL invented.


## 2026-11-14 — owner-authorized launch preflight, stopped before merge

Owner approved main merges2–7 and free educational production beta, one Cloudflare hytale-craft/main with automatic updates. Archived main1c9c1e0, remote annotated backup tag and CRC/SHA-verified Drive ZIP. Investigated red PR6 push check, fixed language-save/abort-on-reload rollback race and added delayed-network reload regression; final c4accf4 push/PR CI green. Prepared release PR8 with audited-dist Pages workflow, project-path404 and metaCSP, production-only Cloudflare instructions; push/PR CI green. Attempt to switch Pages Source to Actions failed403 integration permission; legacy main:/ readback unchanged. As required, no main merges/force/deploy. Owner asked to switch Source manually; prior merge/publication authorization persists. Existing GitHub HTTP200 is old interface, Cloudflare URL not confirmed.


## 2026-11-14 — authorized beta launched on GitHub Pages

Owner switched Source toActions, resolving403. Normal sequential merges2(55f55cfc)→3(ff9d7d79)→4(4cfaca7e)→5(d345cfec)→6(37d19e5d)→7(e6ba5dd0)→8(691fe87d), each after fresh successful CI, SHA/main concurrency checks, no force/conflicts. Workflow43605804630 built/audited/deployed onlydist. Actual HTTPS200 beta verified, public hashes match and forbidden paths404/403. Live mobile Chromium4widths/4locales/action/sheet/calculation/inventory/plan/Back/reload passed without JS errors/overflow/data requests. Source/root never published during integration. Old main tag/DriveZIP retained. Cloudflare remains unverified/unconnected; main-project Android steps prepared, no preview project or paid feature created.

## 2026-11-14 — Hytale Craft 2.0 artistic interface

Single branch codex/ui-v2 based on232b9c4; one PR, owner-authorized merge after visual QA/CI. Eight new original illustrated scenes complete all ten goals, plus original wordmark/world/frame/nav icons. Separate localized HTML captions and two-column mobile layout; four-plus-four-plus-two desktop layout. Preserve original fight/gather pose actions and existing storage/planner functions. Add usable navigation inside native modal while keeping background inert. Extend exact dist allowlist and source SHA checks, embed all art in standalone export, test all-art network failures without glyph substitutes. Correct background crop and long caption padding after actual screenshot review. Four educational examples remain clearly not Hytale. See UI_V2.md and reports/UI_V2_TEST_RESULTS.md. Existing Cloudflare HTTPS endpoint verified available; merge/publication proof belongs in the single PR and appended Drive passport. New rollback tag backup/pre-ui-v2-20261114 preserves previous main.

## 2026-11-15 — non-destructive data-safety draft

Branch codex/data-safety based on a972e4d. Audited11remote branches,2tags,10PR head refs/91commits and46accessible artifacts; no server copies deleted. Current-tree HySphere dataset withheld, neutral manifests/catalog, five collection workflows/network CLI paths paused in draft, offline legacy export delegates to original educational beta. Existing tests moved from third-party records to original synthetic fixtures. New offline import_catalog validates schema/references/quantities/duplicates/cycles/version/checksums, keeps candidates private and always publication-blocked.37Python/17JS/25Chromium tests passed; both builds retain39approved UI hashes. History cleanup plan prepared only; letters recipients/content rechecked, none sent. One Draft PR using Cloudflare CF-Pages-Skip commit prefix, no merge/deploy/force push. Exact PR/CI/Drive proof appended to native passport; main remains unchanged until owner review.

## 2026-11-15 — PR11 pre-merge re-review

Rechecked main a972e4d and all40draft changes, ran all available suites and compared approved UI assets/builds. Corrected importer handling of malformed existing candidate metadata; prior bytes remain intact, failed imports produce reports. Fresh38Python/17JS/25browser tests passed. Verified Drive safe backup by actual download, CRC/SHA and180file comparisons. Scoped credential scan clean; five collector workflows paused in draft. PR remains draft, no merge/deploy, histories/tags preserved. See data-safety/PR11_MERGE_REVIEW.md and native Drive passport for exact final-head CI/evidence.

## 2026-11-15 — PR11 published and Seeker/Maker modes

Owner authorized tested ordinary merges and publication. PR11 Ready→normal merge bba201f; fresh CI, no active old collector jobs, both actual HTTPS sites/hash/mobile flows verified. Remote annotated backup/pre-modes-20261115 retained. New single branch codex/seeker-maker-modes keeps approved Seeker art and adds Maker using the same planner/sheet/storage: eight tools, bounded saved projects, yield-aware structural tree, scoped resource list and optional user station metadata. Four locales; user-only four educational examples. New workspace helper and unit/browser regression tests included in CI/publication gates. Full backups preserve projects and old backups remain compatible. Exact final CI/merge/live proofs are recorded in the PR and native Drive passport; no disputed datasets/history rewrites/emails/paid features.

## 2026-11-15 — canonical calculation release

Studio enquiry already sent by owner; no duplicate communication. Review PR13 and transfer only original v2 importer/tests/fixture into independent code release. Add bounded canonical JS planner, material/stock ledger, alternatives/groups/weighted units/multi-output/co-products, explicit salvage and dynamic cycles, stations/levels/unlocks. Separate reviewed original-data approval+SHA gate, new lazy-loaded original learning panel in existing sheet, unchanged legacy calculator/storage/projects/home design.4existing+4advanced educational methods,0real recipes. Pre-release exact24200b4 backup uploaded/downloaded/CRC+SHA+227files verified, remote rollback tag retained.59Python/44JS/36browser tests passed; final CI/live/Drive evidence appended to release PR/passport. No research PR merge, disputed dataset, paid service or history/backup deletion.


## 2026-11-15 — expanded catalogue search and scale readiness

- Extended search to GitLab, Hugging Face, Kaggle, npm, multiple languages, new hosting/wiki/tool candidates; documented actual counts, missing rights and false positives. No third-party records downloaded or published.
- Added original private prepared canonical snapshot, bounded multilingual filtered/paginated search, up to10,000inventory keys; unchanged single-shot/legacy API and saved keys. Existing lab compiles once for repeat calculations.
- Generated5,000/9,999synthetic methods; verified existing offline importer with5,000records, publication remains blocked. Added Node and mobile Chromium scale regressions to CI.
- Approved artwork/CSS/home/navigation/locales unchanged. Publication evidence and Drive backup links are appended to the release PR/passport after checks, not presumed in advance.

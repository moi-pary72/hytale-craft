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

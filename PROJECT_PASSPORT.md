# Data safety — unmerged candidate, 2026-11-15

One branch codex/data-safety, no merge/deployment. [Audit](docs/data-safety/AUDIT.md), [history cleanup plan](docs/data-safety/HISTORY_CLEANUP_PLAN.md), [offline importer](docs/data-safety/IMPORTER.md), [tests](docs/data-safety/TEST_RESULTS.md). Dataset removed only from draft current tree; main/history/other refs still retain it. No irreversible deletion, force push, tag/artifact cleanup or new public disputed dataset. Public beta stays byte-identical. New private candidate importer tested with original synthetic records. Letters ready but not sent. Native Drive passport receives exact Draft PR and verified backups after creation; old history below preserved.

---

# Hytale Craft 2.0 — current release work (2026-11-14)

Current implementation: [UI_V2.md](docs/UI_V2.md). One branch `codex/ui-v2` based on main232b9c4; owner authorized one PR, merge after visual/CI checks and publication to the existing sites. All ten goals now have original illustrated scenes; original wordmark/background/frame/navigation artwork is separate from localized HTML. Existing two pose animations and all planner/storage mechanisms remain. Four languages EN/RU/ES/PT-BR; four explicitly educational recipes, **zero real Hytale recipes in dist**. Legal data plan: [LEGAL_RECIPE_PLAN.md](docs/LEGAL_RECIPE_PLAN.md).

Cloudflare https://hytale-craft.pages.dev/ now actually answers HTTPS200 (checked before changes); the earlier account-setup blocker below is historical. Existing project only, automatic main deployments; no new project. Public build remains user-only/noindex and exact allowlist. See [reports/UI_V2_TEST_RESULTS.md](docs/reports/UI_V2_TEST_RESULTS.md) for local QA and the PR for final CI/deployment evidence. A UI release is not a license to publish source datasets.

Rollback tag `backup/pre-ui-v2-20261114` points at232b9c4f1da592e415245d0144c1d7acb1e7b845. Existing Google Drive root: https://drive.google.com/drive/folders/1CyqdLmek-cig0dVSSH0y6hcfEPVRChkj ; source PNGs/changed-code ZIP/screenshots/checksum reports go to existing04/05/06 folders. Passport is updated in place, preserving history. Latest primary art reference: owner's attached Hytale Craft2.0 image; older reference archive https://drive.google.com/drive/folders/1_IZebF8sttpwqA1B-rP4oH9HuX7xG1Ve remains historical. Exact latest attachment bytes were not exposed for archival; no older file is falsely substituted.

---

# Учебная beta опубликована и проверена — 14.11.2026

Рабочий сайт: https://moi-pary72.github.io/hytale-craft/ . Разрешённые PR2–8 объединены последовательно с зелёным CI, без force/конфликтов. Release main691fe87db1b7d79f374fd8628ff7ad4a3f20c105, workflow43605804630success. SourceGitHubActions, публикуется только auditeddist. Старый403 снят владельцем, инструкции «остановиться доSource» ниже — история.

На живом HTTPS проверены320/360/393/430,4языка,10целей,панель,действиеперсонажа,расчёт/инвентарь/план/Back/Escape/reload; JSошибок/скролла/запросовигровойбазы нет. Manifest/hashes совпали, data/docs/архивы закрыты404/403.4учебных примера явно НЕ рецептыHytale; реальные базы не публикуются.8финальных иллюстраций/полная плавная анимация и физическийAndroid остаются ограничениями.

Cloudflare должен быть один: hytale-craft/main, None, python3 scripts/build_pages.py --data-policy user-only, outputdist, Rootпусто, auto productionON. Доступа к аккаунту у исполнителя нет, liveCloudflareURLне подтверждён. Пошаговая Androidинструкция docs/CLOUDFLARE_PAGES.md. Разрешение на публикацию уже получено, повторно его не спрашивать.

Oldmain1c9c1e0 сохранён remote tagbackup/main-before-beta-20261114 и провереннымDriveZIP. Полные текущие данные/ссылки: docs/PROJECT_STATE.md и reports/PRODUCTION_RELEASE_VERIFICATION.json. История ниже сохранена.

---

# Разрешённый запуск основной beta — подготовка, публикация ещё не выполнена

Владелец разрешил merge2–7 и бесплатную учебную beta. Использовать только основной Cloudflare hytale-craft/main, без preview-проекта; auto production updates включены. Актуальная инструкция docs/PRODUCTION_LAUNCH.md.

Сохранён main1c9c1e0: remote tag backup/main-before-beta-20261114 и проверенный ZIP Drive. До merge найден/исправлен PR6 race сохранения языка, commit69e6000, CI зелёный. GitHub API запретил смену PagesSource на workflow (403integrationpermissions). Владелец уже переключил Source на GitHub Actions; REST GET подтвердил workflow mode. Блокер403 снят, разрешённые последовательные merges возобновлены. Разрешение на merge/Deploy уже есть, повторно его запрашивать не нужно.

Готовится ветка codex/production-launch с workflow публикации только dist и правильным /hytale-craft/ путём. Main и сайты пока не менялись. Cloudflare аккаунт недоступен, живой URL не подтверждён. История ниже сохранена, старые инструкции preview устарели.

---

# Этап7 — изолированный HTTPS-preview, без публикации (2026-11-14)

Новая ветка codex/https-preview поверх PR6. Main/стек2–6 не объединять. GitHub Pages фактически публикуется из main:/ (legacy), build1c9c1e035207b954894fdba225ceca2dc4742f38; настройки прочитаны REST и не изменены. CI всех текущих PR2–6 успешен. Для онлайн-проверки merge не требуется.

Инструкция Android: docs/CLOUDFLARE_ANDROID_PREVIEW.md; точные поля .cloudflare/preview-settings.json. Рекомендуется отдельный новый Pages-проект hytale-craft-preview, Production branch codex/https-preview, None, Python user-only, outputdist. В Cloudflare первый deploy нового проекта называется production, но не затрагивает существующие main/GitHubPages. Всё равно публичен и требует отдельного разрешения. Аккаунт Cloudflare не подключён/не проверен; проект/URL не созданы. Noindex не защита доступа. Не нажимать Save and Deploy до решения владельца.

Runtime beta/две сцены/учебные примеры идентичны Stage6. Публичный dist исключает базы, документы, тесты, архивы/секреты; CI готовит скачиваемый artifact без deployment. История и постоянные художественные референсы сохранены ниже и в docs/PROJECT_STATE.md. Следующий шаг владельца: разрешить GitHub app только для этого repo, заполнить поля и отдельно подтвердить публичный Deploy; после публикации передать фактический HTTPS URL для проверки.

---

# Этап 6 — мобильная beta, подготовлена без публикации (2026-11-14)

Актуальный draft [PR №6](https://github.com/moi-pary72/hytale-craft/pull/6) поверх PR5, стек2→3→4→5→6. Runtime checkpoint7176b06ac767539f62c0eca7e9cfe688af53a39a, ветка codex/mobile-beta. Main/production/Cloudflare не изменены, merge/deploy не выполнялись. GitHub CI43593544711 прошёл полностью.

Новый вход: beta.html → dist/index.html. Десять целей/две колонки, нижняя панель без скролла сетки, Back/Escape/жест/фокус, компактная навигация. Сохранены движок, инвентарь, планы и редактор. Сборка только user-only:4оригинальных учебных примера, явно НЕ рецепты Hytale. HySphere/ID snapshots исключены,623реальных source-backed рецепта остаются только в прежнем исходном каталоге/резервных копиях. Noncommercial-review в публичном builder запрещён.

Постоянный художественный ориентир: https://drive.google.com/drive/folders/1_IZebF8sttpwqA1B-rP4oH9HuX7xG1Ve ; основной https://drive.google.com/file/d/1r8teXmtwr_Ml9prg1z9Skb39P4jFaVEE/view . Старые SVG отвергнуты владельцем. Две сцены PR5 сохранены,4позы смешиваются короткими crossfade;8финальных сцен и дополнительные художественные кадры ожидаются. Не объявлять их готовыми.

Начинай с docs/PROJECT_STATE.md, STAGE6_BETA.md, CLOUDFLARE_PAGES.md, EDUCATIONAL_EXAMPLES.md и reports/STAGE6_*. Точные Free настройки и безопасная последовательность merge2–6 описаны; перед merge проверить автопубликацию существующих GitHub Pages. Intended hytale-craft.pages.dev не создан/не проверен. Бесплатная учебная UX-beta готова к решению владельца, не к самостоятельному Deploy или коммерческому запуску.

PreviewHTML: https://drive.google.com/file/d/17HvVehf6Q6gMGCTWb4o1mA-F4dpdlK_L/view ; панель https://drive.google.com/file/d/1HF40OhfagVlesfZuRDzF5mRtoRJKw-DD/view . История ниже сохранена; её старые entry/data/art утверждения не являются текущим статусом.

---

# Этап 3 — международный UX preview, 2026-11-14

Отдельный draft PR №3: https://github.com/moi-pary72/hytale-craft/pull/3 (зависит от PR №2, target — его ветка). Preview: `preview.html`; архив/скриншоты на Drive перечислены в docs/reports/STAGE3_DRIVE_BACKUPS.json. 10 оригинальных векторных scenes, EN/RU/ES/PT-BR покрывают все 114 UI keys нового preview; legacy остаётся partial EN/RU. Данные/engines PR2 сохранены. Production/main/ветка PR2 не менялись. Commercial launch BLOCKED; ничего не deployed/merged. Начни с docs/PROJECT_STATE.md, UX_PREVIEW.md, COMMERCIAL_DATA_READINESS.md, GROWTH_PLAN.md.

---

# Текущее обновление — второй этап PR №2, 2026-11-14

Подробный актуальный паспорт: [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md). Получены и подключены 623 source-backed полных рецепта / 3219 предметов HySphere (2026-08-12, Early Access, exact build неизвестна), 1486 записей отделены. Это реальные данные независимого источника с non-commercial attribution, не официальная сверка. Старый каталог OpenHytale 3641/403 ID сохранён отдельно. Main/public Pages не изменяются. Инструкция для лицензированного Assets.zip — docs/ASSETS_IMPORT.md. История ниже отражает предыдущие этапы.

---

# Актуальное состояние — 2026-11-14

Основной документ продолжения: [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md). История: [docs/DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md).

Ветка codex/verified-catalog-planner: 3641 ID предметов, 403 ID рецептов, 0 полных подтверждённых рецептов. Карточки, поиск и исправленный калькулятор проверены локально. Main не обновлён. Официальный Assets.zip не получен; полный импорт заблокирован OAuth/отсутствием архива. Ниже сохранена предыдущая историческая версия паспорта; её утверждения о текущей базе и публикации могут быть устаревшими.

---

# Hytale Craft — паспорт проекта
Обновлено: 2026-11-14 (этап 3 — языки)
Статус: MVP создан в main; публикация GitHub Pages ещё не подтверждена.

## Ссылки
Репозиторий: https://github.com/moi-pary72/hytale-craft
Планируемый адрес Pages: https://moi-pary72.github.io/hytale-craft/ (будет работать после включения Pages)
Организация: moi-pary72; основной пользователь GitHub: cheloveck4-netizen.
Другой проект moi-pary72/moi-pary («Мои пары 72») НЕ ТРОГАТЬ.

## Цель
Создать полезный неофициальный Hytale Craft Planner для игроков. Первый функционал: цепочки крафта, список базовых ресурсов, редактор рецептов, перенос JSON, мобильный интерфейс. Позже — проверенная база игровых рецептов, поиск, фильтры, SEO и монетизация после появления аудитории. Никаких выдуманных рецептов.

## Что реализовано
index.html: автономное мобильное SPA без библиотек; создание/редактирование/удаление рецептов; проверка формата; localStorage; JSON импорт/экспорт; вычисление рекурсивных зависимостей с защитой от циклов; копирование списка; заметки об источнике. В расчёте не учитывается повторное использование излишков между ветвями, что прямо указано в UI. Игровая база не заполнена — это сознательное ограничение.
Коммит первой версии: 0d44294ff1c3c6ae8ef59946845a6e53986430e9.

## Важные правила
1. Не менять чужие проекты и другие репозитории.
2. Перед обновлением читать текущий main; не перезаписывать параллельные изменения.
3. Для спорных изменений использовать ветку и PR, если доступно.
4. Не заявлять о проверенных игровых рецептах без ссылок и проверки версии.
5. Не обещать доход. Продвижение и аналитика после запуска и реальных данных.
6. Хранить паспорт и журнал решений в GitHub и копию на Google Drive, чтобы новый чат мог продолжить работу.
7. Не публиковать секреты, токены и персональные данные.

## Этап 2 — добавлено
- Ввод и локальное сохранение инвентаря игрока.
- При расчёте расходуются доступные запасы и переиспользуются излишки от промежуточного крафта.
- Отображаются остатки после расчёта. Коммит: 513bbf97b19d9847ba966b7b1cf29882a9e02d01.
- Важно: автоматический браузерный smoke-test на опубликованном GitHub Pages ещё не выполнялся.

## Этап 3 — интернационализация
- Основной интерфейс English, переключатель English / Русский, язык сохраняется в localStorage.
- Добавлены английские title/description и canonical URL для международного SEO.
- Текущая локализация — первый проход: статические подписи и часть динамических сообщений; ошибки валидации и некоторые уведомления ещё могут остаться на русском. Не считать перевод полностью завершённым.
- Hytale официально поддерживает семь языков: zh-Hans, en, fr, pt-BR, ru, es, uk (https://hytale.com/accessibility). Достоверной разбивки игроков по странам/языкам нет. English-first — маркетинговая гипотеза, не измеренный лидер.
- Изменения: efaccbd63cc869605edafcbd5d08c4592eb502da, f48d612cbb0f74e6cae6cf7ce2c64aa608631d6e.

## Следующие задачи
1. Проверить, включён ли GitHub Pages, при необходимости включить Settings → Pages → Deploy from a branch → main / root.
2. Открыть публичный адрес, проверить мобильный интерфейс, создание рецепта, расчёт, циклы, экспорт/импорт.
3. Собрать проверенную актуальную базу Hytale рецептов с указанием источников и версий, не копируя чужие базы без разрешения.
4. Улучшить калькулятор: поиск, избранное, массовые цели, проверенные рецепты и тесты.
5. Сделать метаданные SEO, аналитические события и план продвижения; второй игровой сайт выбирать по спросу.

## Передача новому чату
Прочитай этот файл и актуальный index.html из GitHub, затем проверь состояние Pages. Продолжай разработку Hytale Craft, сохраняя существующий функционал. Пользователь предпочитает большие законченные этапы и самостоятельную работу, с отчётом о фактических изменениях.
Этап7: draftPR7 https://github.com/moi-pary72/hytale-craft/pull/7 ; CI43597302206 success, фактический CI ZIP14114808254 скачан, CRC/SHA256 GitHub digest и24runtime файла проверены. Инструкция Android сохранена: https://drive.google.com/file/d/1HxW6cB_wJUrBSZw3SLEBR7pxXa16MxLB/view . Реестр Drive: docs/reports/STAGE7_DRIVE_BACKUPS.json. Публикации нет.

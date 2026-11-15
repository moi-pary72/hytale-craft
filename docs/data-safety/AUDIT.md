# Аудит распространения данных — 15.11.2026

Baseline main a972e4d664687211319b1b94cf87462de7022f1a. Одна ветка codex/data-safety, Draft PR без merge/deploy. Этот отчёт не утверждает, что старые копии уже исчезли. Рабочий сайт, иллюстрации, анимации, языки и ключи пользовательского хранения не меняются.

## Объём и доказательства

Проверены все11удалённых веток,2опубликованных тега и10PR head refs:23ref,91достижимый commit на момент аудита. Рассмотрены исторические JSON blobs и старые HTML. GitHub releases отсутствуют. Через GitHub API перечислены и скачаны для локального чтения все46доступных Actions artifacts, включая ZIP и вложенные Pages tar; ничего не удалено и повторно не опубликовано. Манифесты архивации, SHA/размеры/пути и ref inventory сохранены в audit evidence, без копирования содержимого баз.

В46артефактах нет членов с полными item/recipe JSON-каталогами. Исторические Pages artifacts включают старые index.html и иногда документы источников; в старом baseline index находятся9образцов с generic источником Historical community guide. Это отдельные неподтверждённые исторические примеры, не доказательство коммерческого разрешения и не623-рецептная база. Технический маркер в renderer или URL HySphere сам по себе не означает наличия рецептов: текущий index по умолчанию пуст. Статистика и ссылки в диагностике/словарях отделены от dataset bodies.

Публичные сайты Cloudflare и GitHub Pages уже используют user-only сборку с4явно учебными примерами. Сборки этой ветки побайтово совпадают с прежней утверждённой UI2.0сборкой:39content hashes на каждом хосте,40файлов включая manifest. Никакой production deployment для этого не нужен.

Граница уверенности: GitHub API не перечисляет все Cloudflare dashboard deployments. Все исторические версии Cloudflare, CDN-кеши, форки, чужие clones и удалённые недоступные artifacts не объявляются полностью проверенными. Доступные Git refs и46артефактов проверены; для полного dashboard-аудита нужен владелец/разрешённое подключение. Внешние copies не удаляются этим PR.

## Классификация и точные текущие пути

| Путь / поверхность | Источник и основание | Категория | Подготовленное действие |
|---|---|---|---|
|data/recipes/hysphere-2026-08-12.json|HySphere;3219items/623полных recipes/1486исключённых; noncommercial attribution, commercial/mirroring grant не подтверждён|Подтверждённое ограничение commercial use; неясный scope полной перепубликации|Удалён только из current tree ветки PR; история/теги/локальная ignored-копия сохранены |
|data/recipes/manifest.json|Указатель на тот же snapshot, не самостоятельный чужой каталог|Технический канал повторного подключения|Нейтральный inactive manifest сnullpointer |
|data/catalog.json|OpenHytale;3641ID/403recipe IDs, без тел. MITкода не устанавливает лицензию компиляции|Неопределённый scope bulk reuse; **не утверждение нарушения каждым ID**|Ненужный bulk список заменён пустым явным маркером |
|tests/planner.test.js|Ранее использовал полный снимок и конкретные проверочные quantities|Зависимость от ограниченной базы / небольшие фактические фрагменты|Независимые Fixture_ regression recipes |
|tests/browser_smoke.py; tests/preview_browser.py|Ранее проверяли реальные quantities/ID на том же snapshot|Потенциальные ограниченные фрагменты и ненужная привязка к source|Искусственный HTTP fixture, без переноса игровых recipes |
|tests/test_recipe_sync.py|Ранее требовал наличие реального snapshot|Механизм давления на возврат данных|Тест нейтрального manifest и отключённого network вместо требования базы |
|scripts/export_preview.py|Раньше встраивал snapshot/IDкаталог в standalone HTML|Канал повторной раздачи|Совместимый entry point теперь экспортирует только существующую учебную beta |
|scripts/sync_recipes.py; .github/workflows/sync-recipes.yml|HySphere network + public snapshot update PR по расписанию|Риск автоматического возвращения копии|Network/CLIблокированы, schedule/write permission убраны вветке |
|scripts/sync_catalog.py; .github/workflows/sync-catalog.yml|OpenHytale bulk ID обновления|Неопределённый scope / повторная публикация|То же; pure synthetic helpers сохраняются |
|scripts/discover_recipe_catalog.py; .github/workflows/discover-recipe-catalog.yml|Поиск/сохранение index и sample ответа; первый key мог содержать большой массив|Потенциальная непреднамеренная перепубликация|Активные network/CLI entry points и расписание остановлены вветке |
|scripts/probe_recipe_endpoints.py; .github/workflows/probe-hytale-recipes.yml|Raw sample capture потенциально сохраняет nested payload|Потенциальный канал фрагментов/копий|То же |
|scripts/monitor_hytale_sources.py; .github/workflows/monitor-hytale-sources.yml|Записывал весь catalogs.json если upstream schema менялась|Потенциальный канал bulk snapshot|То же |
|data/recipe-discovery.json; data/source-health.json; data/openhytale-catalog-index.json; docs/reports/recipe-sync.json; docs/reports/catalog-sync.json|Небольшие ID/ссылки, counts, даты/хеши/статусы, без ingredient bodies|Описательные метаданные, не полная база; не blanket лицензия на всё|Сохранены как история аудита; новые raw dumps не добавлены |
|web/catalog.js; web/preview/app.js; locales/*.json; docs/DATA_SOURCES.md|Одиночные ID, атрибуция, URL и агрегаты / тексты проекта|Ограниченные описательные ссылки, не bulk copy|UI/словари не меняются, сами ID не объявляются нарушением |
|web/beta/examples.js; новые tests/fixtures/*.json|Оригинальные lesson:/Fixture_ арифметические данные CC0; не Hytale|Разрешённый для задачи оригинальный материал|Сохранены/созданы сявной маркировкой |
|assets/ui-v2; assets/art-pair|Оригинальная созданная для проекта графика, отдельная provenance|Не импортированная игровая база|Без изменений, никакой новой правовой гарантии на торговые обозначения не заявляется |
|Старые commits/branches/tags/PR refs; прежние index.html/Pages artifacts|Те же datasets/исторические9sample recipes, source provenance неполная|Сохраняющийся исторический риск|Ничего не удалено/не переписано; отдельный план HISTORY_CLEANUP_PLAN.md |

Лицензии/доказательства: https://hysphere.app/about#data-license ; https://hysphere.app/data ; https://openhytale.org/developers/#license ; https://hytaledb.net/terms ; https://hytale.com/eula ; https://hytale.com/terms-of-service . HytaleDB dataset в проекте не обнаружен. Ссылки на HytaleDB не считаются копией базы. Лицензия поставщика не заменяет решение об underlying game rights.

## Почему очистка не завершена на сервере

Draft PR меняет только собственную ветку. Main и его ежедневные collection workflows пока прежние. Даже после будущего обычного merge старые blobs доступны в истории, другихrefs и возможных кешах. PR не удаляет теги, backups, artifacts, forks или Cloudflare versions. История не переписывалась, force push не применялся. Приватная копия помогает не потерять данные при review, но не решает лицензию.

## Подготовленная защита

Новая audit_repository_data.py проверяет tracked tree вCI и не даёт незаметно вернуть known bulk snapshots, active pointers, review candidates или ZIP backups. Это эвристика, не автоматическая юридическая экспертиза и не гарантия против любого скрытого текста. В .gitignore добавлены snapshot/backup patterns. Публичный build whitelist и SHAпроверки сохранены.

Универсальный import_catalog.py работает только с локальным JSON и пишет только ignored.privateкандидат/отчёт. Положительный импорт означает структурную валидность, не право публикации. Применён только оригинальный тестовый набор3items/2recipes/1station. Полная архитектура и ограничения в ARCHITECTURE.md / IMPORTER.md. Новых игровых recipes не создано.

## Согласования

Нужны отдельные решения владельца: merge этого конкретного draft после review; возможная перепись Git history/обработка старых refs и artifacts; статус лицензированных backups; отправка3писем; дальнейший законный источник и интеграция. Ни одно из этих действий автоматически не выполняется. Разрешение на создание Draft PR не означает разрешение Deploy.

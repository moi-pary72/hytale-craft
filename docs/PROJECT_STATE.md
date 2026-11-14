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

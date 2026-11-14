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

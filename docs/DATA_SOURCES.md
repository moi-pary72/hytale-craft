# Проверенные источники Hytale — 2026-11-14

| Источник | Фактический результат | Версия / формат | Обновление и ограничения |
|---|---|---|---|
| [Официальное руководство](https://support.hytale.com/hc/en-us/articles/45326769420827-Hytale-Server-Manual), [downloader](https://downloader.hytale.com/hytale-downloader.zip) | ZIP загрузчика доступен, содержит Linux/Windows binary и QUICKSTART. Сам игровой Assets.zip **не получен** | В архиве загрузчика не обнаружена версия игровых данных; Assets.zip содержит игровые JSON | OAuth2 device flow владельца лицензии. Не обходить авторизацию, не хранить credentials в Git/артефактах. Условия игры и доступ по лицензии; не разрешение на перепубликацию игровых архивов |
| [OpenHytale](https://openhytale.org/llms.txt), [items API](https://openhytale.org/api/catalogs/items.json), [recipes API](https://openhytale.org/api/catalogs/recipes.json), [meta](https://openhytale.org/api/meta.json) | HTTP 200: 3641 строка-ID предметов и 403 строки-ID рецептов. Нет ингредиентов, количеств, станций и названий | `generated_at=2026-07-06T11:57:22.295504Z`; game build отсутствует. JSON arrays of strings | Публично документированный open data API, независимые descriptive metadata. Используем ID с атрибуцией; это не официальная база и не лицензия на игровые файлы. Ежедневная проверка готовит PR, нулевая/невалидная база отвергается |
| [Hytale Source](https://hytale.source.gs/) | HTML доступен; заявляет 3189 items / 2080 recipes, **не импортированы** | 0.6.4-b27, извлечено 2026-09-09; HTML | Использовать для ручного сравнения одинаковой версии. Разрешение на массовую перепубликацию/документированный полный API не установлены. Не смешивать с OpenHytale |
| [HytaleDB](https://hytaledb.net/data), [условия](https://hytaledb.net/terms) | HTML доступен; заявляет 3960 items / 410 recipes; **не импортированы** | snapshot 0.7.3-8e1d7ab9; статические страницы | Условия ограничивают массовую перепубликацию и automated bulk downloading. Compilation CC BY-NC 4.0; права на игру отдельные. Справочная ссылка и ручная проверка, не скрейпинг |
| [GitHub search](https://github.com/search?q=Hytale+assets+recipes&type=repositories) | Запрос repository search `Hytale assets recipes`: 0 результатов. Не доказательство отсутствия репозиториев | Набор с проверенной версией, происхождением и разрешением не найден в этом поиске | Не скачивать случайный дамп как официальный источник. Продолжить исследование, когда известна нужная game build |

## Правила

`data/catalog.json` — только ID. `recipes: []` означает отсутствие полных подтверждённых рецептов; `recipe_ids` нельзя подавать калькулятору. Русские и английские имена null, пока не получены настоящие локализации. Произвольные переводы/догадки не добавлять.

Старые Actions — diagnostics only. Успешный HTTP, workflow или наличие строк `Salvage_*` не доказывают получение рецептов. Отчёты текущего запуска находятся в `docs/reports/catalog-sync.json` и `data/*status.json`, `data/source-health.json`, `data/recipe-discovery.json`.

Публикация нового полного набора требует разрешённого источника, версии, ID, положительных количеств, выходов, станций, разрешения наследования, групп и тегов, ссылочной целостности, сравнения репрезентативных рецептов. Сбой сохраняет последнюю базу. Откат — previous JSON или Git, через PR. Никогда не смешивать разные game builds молча.

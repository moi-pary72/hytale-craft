# Проверки — второй этап PR №2, 2026-11-14

## Выполнено локально

- `python -m unittest discover -s tests -v`: **14 тестов**, проходят. Parent override/циклы/пропавшие parents; explicit/implicit outputs; группы сохраняются; multiple+PrimaryOutput; недопустимые количества; catalog duplicates/shrink; source license/revision/count; deterministic snapshots/backup; manifest SHA-256; CLI не затирает candidate при плохом checksum или ошибочных assets.
- `node tests/planner.test.js`: **11 тестов**, проходят. Партии, общий stock, остатки, инвентарь/недопустимые значения; прямой/косвенный cycle и overflow; безопасные opaque prototype-like ключи; hash/schema всего snapshot; реальный shortbow 2 штуки с inventory; вложенная copper smelting; incomplete copper shortbow не рассчитывается; синтетические альтернативы требуют выбора.
- `python tests/browser_smoke.py`: **1 расширенный mobile integration test**, Chromium **393×851**, проходит. Цель→Сражаться→Оружие; поиск «Простой короткий лук»→source-backed карточка; 2 лука / 3 sticks в inventory→5 sticks + 12 fibre; stations; source inventory save; массовый план/reload; RU/EN сохраняют quantity/inventory; реальный цикл глины→явное получение отдельно→Furnace; incomplete recipe→editor; old ID-only source isolated; пользовательская карточка/расчёт/inventory reload; route-injected corrupted snapshot отвергается по SHA-256 и остаётся ID fallback; no console error/pageerror; no horizontal overflow.
- Сетевой повторный `python scripts/sync_recipes.py`: **3219 items / 623 complete source-backed recipes / 1486 incomplete records**, `changed=false`, те же SHA-256.
- Сетевой `python scripts/sync_catalog.py`: **3641 item IDs / 403 recipe IDs / 0 recipe bodies**, `changed=false`.
- `git diff --check`: пройден. JSON читаются и хешируются Python/JS; integrity manifest проверен до browser import.

## Что выявили проверки

На реальном наборе обнаружился цикл преобразований лепестков в цепочке глины. Он не скрыт и не обходится автоматически: UI предлагает получить промежуточный предмет отдельно. Первый расширенный тест искал Alchemy_Cauldron при активной категории weapons; исправлен тестовый сценарий выбора категории all. Данные не менялись ради прохождения теста.

## GitHub Actions и границы

Предыдущий этап CI: success https://github.com/moi-pary72/hytale-craft/actions/runs/43576518362 . В этом этапе validation workflow расширен browser smoke и direct Node reporter; актуальные результаты новой ветки проверяются после push и фиксируются в истории/PR. Daily workflows сами не выполняют merge; расписания начнут работать только после отдельного разрешённого merge в default branch.

Физического Android нет; проверка — Chromium mobile emulation. Новая версия публичного Pages не публиковалась и не тестировалась как production. 623 source-backed записи **не означают официальную сверку** с лицензионным архивом. Точная game build не предоставлена источником. Синтетика существует только в тестах; реальные assertions ссылаются на source-backed snapshot.

## Подтверждённый CI второго этапа

Код `7802e0b57646708122b6b075d43cfae1c3449d7f`: **success**, включая Python, JS и mobile integration:

- https://github.com/moi-pary72/hytale-craft/actions/runs/43578617436 (pull_request).
- https://github.com/moi-pary72/hytale-craft/actions/runs/43578613365 (push).

Первоначальный запуск на `461b99b`: Python/JS success, установка browser dependency failure из-за ubuntu-latest=26.04, не поддерживаемой Playwright 1.56. Validation теперь закреплён на Ubuntu 24.04. Локально дополнительно проверена ширина **320 px**; горизонтальной прокрутки нет.

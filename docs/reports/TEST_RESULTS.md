# Проверки — 2026-11-14

- `python -m unittest discover -s tests -v`: 5 tests passed. Implicit output, сохранение станций и ID, отклонение Parent и испорченного явного выхода, количества, ID-only normalization, сохранение файла при сокращении базы.
- `node --test tests/planner.test.js`: 5 сценариев passed (runtime суммирует как 1 file suite): партии/общие излишки/инвентарь, готовая цель в инвентаре, прямой цикл при surplus, косвенный цикл/переполнение, prototype key.
- `python tests/browser_smoke.py`: 1 mobile integration test passed в локальном Chromium 393×851; реальный ID Weapon_Shortbow_Crude, честное отсутствие рецепта; сохранённый тестовый рецепт→карточка→расчёт→инвентарь после reload; RU/EN; no pageerrors; no horizontal overflow.
- `python scripts/check_official_downloader.py`: ZIP доступен, игровые assets не получены.
- `python scripts/monitor_hytale_sources.py`: четыре endpoint checks HTTP 200.
- `python scripts/sync_catalog.py`: 3641 ID items, 403 recipe IDs, 0 full recipes; повторная запись не нужна.
- `git diff --check`: passed.

Тесты не подтверждают полноту игровой базы. Физический Android, новая версия на опубликованном Pages не проверена. GitHub CI validation прошёл: https://github.com/moi-pary72/hytale-craft/actions/runs/43576518362 . Синтетические тестовые рецепты не публикуются как игровые данные.

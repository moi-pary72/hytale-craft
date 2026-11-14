# Второй этап PR №2 — результат

PR: https://github.com/moi-pary72/hytale-craft/pull/2 . Код `7802e0b57646708122b6b075d43cfae1c3449d7f`. Draft, без merge и без изменения production Pages.

- 623 полных source-backed рецепта с ингредиентами, 3219 items HySphere, 1486 записей отдельно. Snapshot 2026-08-12; Early Access; exact build неизвестна. Официально сверенных на нашей лицензии рецептов 0. Лицензия non-commercial attribution; источник в UI.
- OpenHytale 3641/403 ID-only snapshot сохранён отдельно. Даты и версии не смешиваются.
- Карточки/name+ID поиск/goal flow/пользовательский alias, реальный расчёт/инвентарь/остатки/станции/массовый план/копирование/browser persistence. Missing recipe предлагает свой editor, сложные cycles требуют явной добычи промежуточного материала.
- Assets importer: документированное Parent override, группы/multiple/metadata сохраняются без догадок, candidate в .private, CLI checksum/error не затирают рабочий candidate. Проверка на полном настоящем архиве ещё не выполнена.
- Раздельные versioned snapshots, source metadata/checksums, browser SHA validation/fallback, atomic writes и previous snapshots, PR updates без merge, CI включая mobile.
- Локально: 14 Python + 11 JS + mobile Chromium integration 393/320 px, no console/pageerror/overflow, cycle/acquire/incomplete/corrupt checksum/reload/RU-EN. CI: success https://github.com/moi-pary72/hytale-craft/actions/runs/43578617436 .
- Drive: структура 01–06 создана/прочитана; паспорт перемещён с сохранением ссылки/истории; 10 backup-files сохранены с metadata readback. Манифест DRIVE_BACKUPS.json. Remote checksum недоступен; local SHA сохранён. Официальные игровые ZIP/секреты не публиковались.

Следующий шаг владельца: просмотреть PR и ограничения non-commercial dated source; отдельно разрешить merge/publication при согласии. Для актуальной полной базы получить Assets.zip официальным OAuth и выполнить docs/ASSETS_IMPORT.md. Без пароля в чате и без публичной загрузки игровых архивов. Затем сверить build/наследование/группы/локализации и права на нормализованные данные. Физический Android недоступен, требуется проверка владельцем после разрешённого деплоя.

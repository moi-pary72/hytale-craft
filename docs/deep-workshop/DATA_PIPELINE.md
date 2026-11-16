# Подготовка большой базы: без обхода прав

Конвейер: разрешённый локальныйJSON → существующий import_catalog_v2.validate/run → version/channel/SHA256/duplicates/refs/cycle checks → private candidate → новый immutable content-addressed snapshot → added/changed/removed report → calculator tests → отдельная проверка прав/доверенного approval → будущий reviewed PR публикации.

`python3 scripts/catalog_snapshot.py INPUT.json` использует существующий импортёр, а не новую несовместимую схему. Все результаты строго внутри.private/catalog-snapshots. `index.json` хранитcurrent/previous/history, каждый snapshot — JSON поSHA256, без перезаписи содержимого. Повреждённый предыдущий snapshot блокирует update. Плохой import не меняетcurrent index. Для смены game_version/channel требуется явный --allow-version-change; это не разрешение публикации.

Источник не скачивается автоматически. Нет флага «я разрешаю» в недоверенномJSON, который включил бы публикацию. Вcandidate/index остаётся publication=blocked. Builder по-прежнему берёт только отдельно approved original educational canonical payload; этот этап не расширяет его лицензионный whitelist и не публикует.private.

Уже существующие prepared canonical snapshot/search,5k/9999 synthetic tests, change diff и fallback не дублируются. Новый маленький store добавляет долговременную историю версий и проверяемый last-good pointer. Канонические альтернативы/группы/единицы/outputs/salvage не сплющиваются до простого discovery.

Текущий discovery умеет bounded legacy-подмножество. Следующий этап: canonical inventory feasibility через тот же prepared planner с явными методами/материалами/требованиями; отдельный worker; paginated index/внешние reviewed data chunks; deterministic version selection. Отсутствующие сведения не восполняются выдумкой. Без согласованных коммерческих/публичных прав реальный snapshot остаётся private/blocked.

# Независимый конвейер и canonical-v2

## Граница текущего этапа

Новый `scripts/import_catalog_v2.py` — **локальный валидатор нормализованного JSON-кандидата**, без сети, загрузчика, Assets.zip adapter, UI integration и публикации. Он не выдаёт алгоритм выбора материалов/решатель by-products за готовый. Существующие `import_catalog.py`/`import_game_assets.py` и рабочий planner не меняются. Единственный новый вход — наш оригинальный CC0 synthetic fixture, не игровые сведения.

```mermaid
flowchart LR
    A[Разрешённый источник] --> B[Частное получение и SHA]
    B --> C[Источник, версия, права и разрешённые поля]
    C --> D[Адаптер формата]
    D --> E[Canonical candidate]
    E --> F[Схема, ссылки, циклы, diff]
    F --> G[Сверка одной build и тесты расчёта]
    G --> H[Проверка прав и решение владельца]
    H --> I[Отдельный разрешённый release PR]
    I --> J[Аудируемый публичный snapshot]
```

ДоH нет ребра в public builder. Флаг source.license.allowed не является доверенной подписью/разрешением. В public GitHub/Drive archive попадают только собственный код/синтетика/отчёт, не входные спорные данные, текстуры, raw game JSON или private-program материалы.

## Что подтверждено о Hytale JSON

[Официальная Recipes reference](https://docs.hytale.com/assets/item/recipes/) описывает `Server/Item/Recipes/*.json`: Input,Output,PrimaryOutput,OutputQuantity; MaterialQuantity имеет nullable ItemId/ResourceTypeId/ItemTag, Quantity с документированным default, Metadata. BenchRequirement содержит Type,Id,Categories,RequiredTierLevel,RequiredAugmentTags; TimeSeconds,KnowledgeRequired,RequiredMemoriesLevel. В[Items](https://docs.hytale.com/assets/item/items/) встроенное поле Recipe и ResourceTypes[{Id,Quantity}]; это единицы ресурса, не обязательно1предмет=1unit. `Parent` задаёт наследование с field-specific исключениями: простой deep merge не доказан для всех полей.

[Community manual](https://hytale-moddings.github.io/hytale-modding-docs/reference/crafting-system/recipes/) подтверждает embedded recipe и Salvage subfolder, но упрощает enum/selector schema относительно official0.7.7. [Official Groups](https://docs.hytale.com/assets/item/groups/) описывает BlockGroup/Blocks, не автоматически универсальный список взаимозаменяемых ингредиентов. Поэтому `ResourceTypeId`, `ItemTag` и block groups нельзя слить по сходству названий. Раздельные рецепты и item.Recipe нужно собирать вместе; подсчёт только файлов Recipes пропустит встроенные crafts. PrimaryOutput может описывать уже существующий Output и не должен прибавляться вторым продуктом.

Полный реальный архив не был доступен. Приоритет для будущего адаптера: читаемый codec текущей версии/точный разрешённый файл/игровая проверка → помеченный default этой версии → unresolved. Отсутствующие выходы/количества/bench logic не восстанавливать из названий или соседнего сайта. “Salvage” — семантический тип трансформации по подтверждённому источнику; это не BenchType, не автоматически арифметическая инверсия craft.

## Canonical-v2 (наш формат, не схема Hytale)

Это версия2семейства canonical; она не совпадает с legacy Assets.zip candidate schema3. Root строго: `schema_version:2`, `snapshot`, `sources`, `items`, `groups`, `stations`, `recipes`. Provenance/состояния items/stations/sources совместимы с[canonical-v1](../data-safety/IMPORTER.md). IDs остаются opaque и сохраняют namespace. Names: locale→text/null; interface dictionaries остаются отдельно, переводы не обозначаются official без доказательства.

| Поле | Значение |
|---|---|
|snapshot|game_version,channel,source_revision,updated_at timezoneISO; разные builds/channels не смешиваются |
|source|id,url,revision,license:{id,url,commercial_use,redistribution,automated_access,game_ip_use}; permissions allowed/prohibited/unknown — только заявления, не approval |
|item/station/group/recipe provenance|id,status,source_id,source_record; optional record game_version должен совпасть соsnapshot |
|status|verified/unverified/tutorial/incomplete/blocked — декларация отдельно от rights/publication и calculation compatibility |
|group|kind resource_type/item_tag/explicit, selection mixed/single/unknown, membership_complete boolean, members[{item_id,units}]. Unknown/неполное членство не дополняется догадками |
|recipe.kind|craft/processing/salvage/unknown; несколько рецептов одного output сохраняются отдельно поrecipeID |
|inputs|slots[{quantity,options:[{kind:item/group,id}]}]; внутри slot явное OR, slots суммируются. Альтернативы с разными дозировками — разные recipe records, пока не определён иной контракт |
|outputs|[{item_id,quantity}], допускается несколько продуктов; primary_output:null или ID уже существующего output, без повторного начисления |
|station_requirements|{mode:any/all/unknown,entries:[{station_id,type,min_level,categories,augment_tags}]}; Type допускает4official типа +unknown; уровеньnullable, не выводится из названия |
|requirements|knowledge_required:boolean/null,memories_level:positiveinteger/null; unknown сохраняется |
|time_seconds|nonnegative finite number/null; неизвестное время не превращается в0 |

Оригинальный пример: `tests/fixtures/catalog-v2-synthetic.json`,5вымышленныхitems,1group,1station,4transformations. fixture `synthetic-v2.1`, channeltest, example.invalid source, CC0; это **не ещё4учебных рецепта сайта и не настоящий Hytale snapshot**.

## Валидация и ограничения реализации

Stdlib Python; strict duplicate-key/nonfinite JSON parsing, input≤10MB,≤10000rows/table,≤100input/output terms,≤50options/slot,≤5000group members; bounded dependency expansion и iterative DFS depth256. Положительные целые количества; bool/fraction/string не принимаются. Дубликаты IDs/options/members/outputs, несуществующие ссылки, неправильные stations/unlocks/version rejected. Пустые incomplete group lists разрешены только с явным incomplete флагом и warning. Unknown metadata не получает выдуманную семантику.

Conservative craft+processing graph объединяет возможные альтернативы; цикл помечает arithmetic compatibility небезопасной, но может быть ложноположительным до выбора маршрута. Отдельный all-transformations graph включает salvage: ожидаемый обратный путь не объявляется невозможным обычным craft автоматически. Это диагностика, **не выбор оптимального плана/баланс энергии/эксплойтов**. Все candidates publication=blocked независимо от отсутствия циклов.

`legacy_arithmetic_shape` означает только простую форму (один fixed input choice per slot, один output, без salvage/unknown features и cycle candidates); это не automatic export/rights approval. В v2 вообще нет публичной projection. Групповые units, смешивание, выбор alternative recipes и совместный учёт by-products в действующем UI пока не реализованы.

## Запуск, отчёт, версии

```
python3 scripts/import_catalog_v2.py tests/fixtures/catalog-v2-synthetic.json
```

Default `.private/catalog-v2-candidate.json` и `.private/catalog-v2-report.json`; no public/symlink outputs, исходник не перезаписывается. `--expected-sha256` проверяет вход. Candidate содержит input SHA,original source/version/locator,per-record SHA и mandatory publication block. Report хранит counts/errors/warnings/diff added/removed/changed IDs, не bodies. Разные game versions/channels требуют `--allow-version-change`; старая рабочая копия сохраняется по SHA перед заменой, ошибочный вход сохраняет прежние bytes. Повторный одинаковый ввод детерминирован.

Смена версий/channel/source approval в будущем должна быть отдельным release decision; нельзя автоматически принять unknown game_version только потому, что это допустимая строка review schema. Raw/restricted inputs остаются частными и вне распространяемых backups. Никаких license/OAuth tokens в отчётах.

## План адаптера и расчётного слоя после прав

1. Private local extraction: archive checksum/version/channel; только разрешённые игровые JSON/language maps, без выноса binaries. Разрешение inheritance/metadata документируется per-field; неизвестные случаи quarantine.
2. Produce immutable canonical snapshot perbuild. Retain originalIDs/source paths, supported statuses and rights evidence; evidence approvals находятся в доверенном реестре вне входного JSON.
3. Dedicated calculation adapter после выбора recipe/group members: inventory constrained allocation, per-member units, multi-output stock ledger, rounding percraft, explicit salvage opt-in. Не уплощать OR в требование всех альтернатив. Не смешивать возврат при salvage со стоимостью craft.
4. Synthetic tests и затем permitted exact-version evaluation: стабильные IDs, patch diffs, stations/tiers/unlocks, cycles/alternative exits, shared inventory/surplus/by-products, version isolation. На UI повлияет только разрешённый data adapter; утверждённые карточки/режимы/localStorage keys сохраняются.
5. Fail-closed publication: licence scope/attribution/retention, no source asset leakage, counts/drop thresholds, approved schema, missing refs and review sample. Создать release PR, отдельное подтверждение владельца для любых новых real data, no automatic merge в этой задаче.

## Явные оставшиеся границы canonical-v2

Native MaterialQuantity.Metadata и выходы через ResourceTypeId/ItemTag не представлены как вычислимые outputs: v2 принимает только конкретные output item IDs. Будущий adapter обязан отправлять такие исходные записи в private quarantine и явно сообщать о неподдерживаемом поле; запрещено выбрасывать Metadata или угадывать output. Перед поддержкой этих случаев требуется версия контракта/разрешённая game-build проверка. Наличие расширенного review schema не означает полноту всех игровых механик.

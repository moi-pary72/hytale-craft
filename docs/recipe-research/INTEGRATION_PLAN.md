# Варианты, разрешения и безопасное внедрение

## Сравнение вариантов A–E

| Вариант | Законность / неопределённости | Полнота / актуальность | Сложность и стоимость | Обновления / монетизация |
|---|---|---|---|---|
|A. Чужой dataset по permissive licence|Проверенного разрешения именно на полный vanilla recipe index среди исследованных источников нет. MIT инструмента/CC BY статьи недостаточно; underlying game rights отдельно |Зависит от версии/coverage; zero authorized records сейчас |Низкая интеграция при наличии экспорта; licence fee неизвестна, ничего не оплачено |Возможны по explicit update/redistribution/commercial scope; сейчас blocked |
|B. Письменная лицензия агрегатора|Нужны разрешённые поля, commercial/display/cache/transformation/redistribution/public Git/browser downloads/backups/automatic access. Агрегатор может не владеть game IP |HYTL выглядит свежее, но count/export неизвестны; HySphere имеет2109dated rows и готовый формат |Запрос можно подготовить бесплатно; цена/лимиты/отзыв прав неизвестны, не придумывать |Хороший быстрый bridge при явных правах и studio clarification; смена Terms не должна незаметно открывать публикацию |
|C. Собственный extractor законных files|Технически возможен; EULA/ToS/shared-source не дают доказанного blanket commercial database grant. Сначала письменная студийная оценка конкретного сценария |Потенциально все embedded/standalone recipes точной game build; реальный count появится только после разрешённого scan |Нужны законный доступ/игра, ПК или разрешённый сервер и доработка адаптера. Покупка/расходы только после решения владельца; платный cloud не обязателен |Лучший долгосрочный контроль: patchline/build/hash/diff. Монетизация только в разрешённом объёме |
|D. Официальный open-data источник|Public schema/API docs есть, разрешённый bulk vanilla-recipe dataset/API не найден. Shared-source private repos не являются open-data |Схема актуальна0.7.7, но0recipe records из документации для нашего каталога |Изучение бесплатно; доступ к программе требует собственной лицензии/аккаунта/принятия условий |Следить за официальными форматами можно; автоматически извлекать commercial dataset без прав нельзя |
|E. Собственные разрешённые наблюдения/проверка|Самостоятельный текст/проверка не снимают договорные/underlying права на массив. Не «отмывать» ограниченный export переформатированием |Ручной ввод медленный; community submissions требуют provenance и rights review. Для sampleQA подходит |Низкие прямые расходы, высокая трудоёмкость/риск устаревания |Полезное дополнение C/B, не быстрый путь к тысячам без автоматики |

**Основной практический путь: C после studio permission; резервный: B с ModLabs/HYTL и явным export agreement**, затем HySphere при согласовании коммерции/актуальной build. До ответа остаётся нынешняя approved educational beta. Можно вести несколько разрешённых adapters, но не объединять builds молча и не использовать restricted fallback.

## Что можно сделать сейчас

- Независимый offline normalizer/validator и полностью оригинальные synthetic tests; immutable schema/provenance/checksum/diff design.
- Справочные ссылки, ограниченное сравнение наблюдений и original report; подготовка писем без отправки.
- Сохранить4учебных примера, оба режима и existing art/translation/storage/build точно как опубликованы.
- Записать approval matrix per-source/per-field с тремя исходами allowed/prohibited/unknown. Оставить publicationblocked для любого unknown/отсутствующего доказательства.

## Чего сейчас делать нельзя в рамках этой задачи

Ни одного нового real recipe в dist/preview/public fixture/backups; никакого восстановления old HySphere/OpenHytale snapshot. Не массово собирать HTML/ограниченныеAPI, не получать чужой Assets.zip, не входить в аккаунт владельца/покупать игру/принимать Program terms за него. Не отправлять письма, не включать рекламу, не делать merge/deploy, не менять утверждённый UI/Cloudflare/config/storage/history/старые backups.

## Что требуется от владельца

1. Указать имя/организацию и reply address, проверить3проекта писем; отдельно разрешить отправку либо отправить самостоятельно. **Первый адресат — официальная поддержка Hytale с маршрутизацией к licensing/legal**, вопрос о ToS7.2(g)/(i), Shared Source3.2/6.1/7.5 и точном field list.
2. При положительном ответе решить, приобретать ли собственную лицензию/использовать разрешённый авторизованный доступ, и где запускать локальный extractor. Пока архив не запрашивается и не нужен для чтения отчёта.
3. Отдельно утвердить источник, бюджет если понадобится, attribution/retention/update licence. Только потом оценочный authorized export/archive и точная build.
4. Утвердить PR с real data после sampleQA/rights evidence. Не считать разрешение на обычные UI merges разрешением на спорную базу.

## Будущая автоматика после разрешения

Авторизованный локальный/private runner получает конкретную версию → фиксирует archive/input SHA и source/version/terms approval → canonical candidate → schema/references/cycles/capabilities → semantic tests/diff/sampleQA → separate release PR. OAuth credentials остаются локально/private secret storage, не Git/artifact/Drive/report. Unknown license/обрыв/пустая/аномально уменьшившаяся база останавливает update, предыдущий published snapshot остаётся. В public GitHub Actions нет лицензированного rawarchive/credentials; только разрешённый normalized release и tests. Обратимость — предыдущая immutable snapshot и обычный revert, без force/history rewrite.

Новый разрешённый snapshot подключается data adapter к существующим каталогам/карточкам/панели/calculator, без редизайна. Отдельный calculation layer для групп/альтернатив/by-products внедряется тестами и feature capability gates, а не потерей данных при проекции в старый single-output формат.

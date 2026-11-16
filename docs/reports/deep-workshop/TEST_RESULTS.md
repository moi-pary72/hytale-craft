# Deep workshop — проверенный Draft

16.11.2026. Main/prod не изменены. Проверки на реальном allowlisted user-only dist.

- Python:63успешно, включая3новых snapshot-store сценария (immutable history/diff, corrupted prior, version switch).
- JavaScript:54успешно, включая6новых discovery-сценариев (direct/nested/batch/stock, independent-vs-shared, already-owned target, cycle/invalid/empty, bounds/reverse links,5000synthetic).
- Chromium:43успешно:1legacy,9preview,1pages,4art,9beta,4modes,8canonical,1GitHub-path,6deep-workshop. Четыре языка,320/360/393/430,Back/Escape/focus,persistence,import/export/projects,damaged data,offline/no-subrequests,long user IDs/stations.
- Главная сравнена со сборкой origin/main на всех4ширинах: финальные снимки совпали попиксельно. Стили главной/10сцен/режимов/навигации не менялись. Одиночные пиксели сглаживания fixed-nav в одном первоначальном запуске исчезли после повторного стабильного захвата.
- UI слотов/detail/craft paths/результатов просмотрен по настоящим скриншотам. Иностранные сайты не копировались в ассеты/датасеты; competitor audit содержит ссылки и наблюдения, не их каталоги.
-5000synthetic recipes,4×CPU throttle: index22.6ms,24capacity queries11.2ms в этой среде. Это измерение эмуляции desktop Chromium, не гарантия на физическом Android.
- Build payload983393→1110893bytes; новые учебные itemWebP94954bytes. Точные hashes/allowlist в dist-audit.json. Никаких спорных баз, приватных документов, архивов, рекламы/аналитики вdist.
- Воспроизводимость сборки проверяется по повторному manifest; SHA-256 artwork и approved canonical data проходят builder gate. Новая snapshot история остаётсяprivate/blocked и не включена вdist.

Draft PR16: https://github.com/moi-pary72/hytale-craft/pull/16 . CI исходного checkpoint1f95a05 успешно: https://github.com/moi-pary72/hytale-craft/actions/runs/43815053546 . Резервный sourceZIP1f95a05 скачан обратно и сверён поSHA256: https://drive.google.com/file/d/1ztRHUuCb4kUREnJS2MgxP8awQtfE8deH/view . Архив1395988bytes, SHA256bd38113dcc29760d418447ab1cefc4516102f660c03c42e429c4ba8be23b9522. Контактный лист и standalone preview: DELIVERY.json; HTML—автономный файл, не опубликованный онлайн-сайт. Физический Android/IME, скринридер, нативная редактура переводов и канонический discovery с группами/альтернативами остаются ограничениями. Все8учебных методов остаются оригинальными примерами,0настоящих игровых рецептов.

CI follow-up: повторный прогон55f5e6d выявил прежний10s navigation timeout в slow-network тесте при15s readiness бюджете. Навигация теперь ждёт DOMContentLoaded сdeadline15s; прежние decode/готовность и assert elapsed<15 сохранены. Это исправление тестовой синхронизации, не ослабление бюджета и не изменение production.

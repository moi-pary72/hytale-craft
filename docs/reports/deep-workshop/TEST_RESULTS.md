# Deep workshop — проверенный Draft

16.11.2026. Main/prod не изменены. Проверки на реальном allowlisted user-only dist.

- Python:63успешно, включая3новых snapshot-store сценария (immutable history/diff, corrupted prior, version switch).
- JavaScript:54успешно, включая6новых discovery-сценариев (direct/nested/batch/stock, independent-vs-shared, already-owned target, cycle/invalid/empty, bounds/reverse links,5000synthetic).
- Chromium:43успешно:1legacy,9preview,4pages,1art,9beta,4modes,8canonical,1GitHub-path,6deep-workshop. Четыре языка,320/360/393/430,Back/Escape/focus,persistence,import/export/projects,damaged data,offline/no-subrequests,long user IDs/stations.
- Главная сравнена со сборкой origin/main на всех4ширинах: финальные снимки совпали попиксельно. Стили главной/10сцен/режимов/навигации не менялись. Одиночные пиксели сглаживания fixed-nav в одном первоначальном запуске исчезли после повторного стабильного захвата.
- UI слотов/detail/craft paths/результатов просмотрен по настоящим скриншотам. Иностранные сайты не копировались в ассеты/датасеты; competitor audit содержит ссылки и наблюдения, не их каталоги.
-5000synthetic recipes,4×CPU throttle: index22.6ms,24capacity queries11.2ms в этой среде. Это измерение эмуляции desktop Chromium, не гарантия на физическом Android.
- Build payload983393→1110893bytes; новые учебные itemWebP94954bytes. Точные hashes/allowlist в dist-audit.json. Никаких спорных баз, приватных документов, архивов, рекламы/аналитики вdist.
- Воспроизводимость сборки проверяется по повторному manifest; SHA-256 artwork и approved canonical data проходят builder gate. Новая snapshot история остаётсяprivate/blocked и не включена вdist.

CI-проверки и конкретный Draft PR/backup receipt фиксируются после их фактического завершения; локальный успех не выдаётся за CI. Физический Android/IME, скринридер, нативная редактура переводов и канонический discovery с группами/альтернативами остаются ограничениями. Все8учебных методов остаются оригинальными примерами,0настоящих игровых рецептов.

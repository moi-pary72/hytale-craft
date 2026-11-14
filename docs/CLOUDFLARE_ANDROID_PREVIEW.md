> **Superseded by the owner-authorized main production launch. Do not create a preview project. Follow [PRODUCTION_LAUNCH.md](PRODUCTION_LAUNCH.md): project hytale-craft, branch main, automatic production updates.**

# Этап7: HTTPS-preview с Android, без merge

Готова ветка `codex/https-preview` поверх PR6. Это инструкция для будущего разрешённого размещения; Cloudflare не подключён и Deploy не выполнялся. Нет доступного Cloudflare-коннектора, поэтому состояние проектов/прав в аккаунте владельца не проверено. Пароли/токены не нужны в чате или репозитории.

## Что подтверждено

GitHub REST API: Pages включён, `build_type=legacy`, source=`main` + `/`, HTTPS enforced, public, status=built. Последний опубликованный commit `1c9c1e035207b954894fdba225ceca2dc4742f38`, build2026-11-14T08:19:28Z. Настройки не изменялись. PR2–6 draft/не merged, CI на всех их текущих heads success. Поэтому **не объединять стек ради preview**: merge действительно способен обновить существующий сайт.

## Выбранный безопасный путь

Создать отдельный **Pages**-проект `hytale-craft-preview` (если имя свободно) из тестовой ветки. В Cloudflare его Production branch будет `codex/https-preview`, а НЕ GitHub main. Его первый deploy технически называется production deployment **нового тестового проекта**; это не изменение основного сайта, но это всё равно публичная публикация и требует отдельного решения владельца.

Настоящий Cloudflare Preview deployment возможен в уже существующем Git-проекте из не-production ветки и не меняет его production URL. Однако без доступа к аккаунту нельзя проверить его наличие/настройки. Не менять существующий проект вслепую, не выбирать main для первоначального deploy и не публиковать старую ветку. Отдельный тестовый проект проще изолировать. Вариант `hytale-craft` оставлен на будущее; этот этап не создаёт и не заявляет владение никаким pages.dev адресом.

## Кнопки и поля на Android

Открыть Chrome → `dash.cloudflare.com`. Если форма слишком узкая, меню Chrome `⋮` → **Версия для ПК / Desktop site**.

1. **Workers & Pages → Create application → Pages → Connect to Git → GitHub**. Если новый экран предлагает Workers, найти **Pages / Looking to deploy Pages?** и перейти в Pages, не создавать Worker.
2. При запросе GitHub доступа выбрать **Only select repositories → moi-pary72/hytale-craft → Install & Authorize**. Это действие владелец подтверждает сам; не давать доступ другому проекту `moi-pary` и не передавать секреты в чат.
3. Выбрать **hytale-craft → Begin setup**. Проверить, что это новый тестовый Pages-проект, а не редактирование существующего production.
4. Заполнить:

| Поле | Значение |
|---|---|
| Project name | `hytale-craft-preview`, только если свободно |
| Production branch | `codex/https-preview` — **не main** |
| Framework preset | `None` |
| Build command | `python3 scripts/build_pages.py --data-policy user-only` |
| Build output directory | `dist` |
| Root directory (advanced) | оставить пустым — корень репозитория |
| Environment variables / secrets | не требуются |

5. **Остановиться перед Save and Deploy**, если отдельного решения о публикации ещё нет. Форма, GitHub-авторизация и эта инструкция сами по себе не означают разрешение на публичное размещение.
6. После явного разрешения владельца нажать **Save and Deploy**, дождаться Success, затем **Continue to project → Visit site**. Копировать только URL, реально выданный Cloudflare; пример/ожидаемое имя не является действующей ссылкой.
7. Сразу ограничить будущую автоматизацию: проект → **Settings → Builds & deployments → Configure Production deployments** → снять **Enable automatic production branch deployments** → Save. В **Preview branch control** выбрать **None** → Save. До этого Git integration обычно автоматически публикует новые pushes. Не отправлять новые коммиты в подключённую ветку до отключения либо нового разрешения. Оформление Settings может отличаться — искать названия этих параметров; их отсутствие не повод включать main.
8. Не добавлять домен/DNS, Workers, платные функции, Web Analytics или рекламу. Если предлагается обязательная оплата/карта — остановиться и проверить, что выбран Pages Free.

В дальнейшем выборочное автоматическое preview возможно через Custom branches, include ровно нужной тестовой ветки, только после отдельного решения. Не выбирать All non-Production branches: старые ветки стека не готовы к новой сборке.

## Что проверить на полученном HTTPS URL

Главная: Beta,10целей/2колонки, нет replay/технических панелей. Fight → учебный клинок → количество2 → расчёт; пример НЕ рецепт Hytale. Inventory: `lesson:fibre: 3`, повторить расчёт; добавить в Plan и перезагрузить. Открыть/закрыть sheet кнопкой, жестом за ручку, Back Android (предмет→список→главная). Проверить EN/RU/ES/PT-BR и сохранение языка. Reduced motion/экономия трафика могут законно отключить действие персонажа.

Перед переносом данных с GitHub Pages/HTML экспортировать рецепты/инвентарь/планы: другой origin имеет отдельное хранилище. При смене preview hash URL также может измениться origin; для повторных тестов использовать один проверенный URL/branch alias. Данные автоматически между ними не переносятся.

После публикации передать фактический URL для HTTPS/CSP/noindex/404 проверки. Локальные тесты не доказывают, что Cloudflare применил заголовки. Noindex не является ограничением доступа: без Access preview публичен. Access не настраивался, платных обещаний или включений нет. На новом тестовом проекте его корневой URL считается production, поэтому обычная настройка Access только для preview не защищает его автоматически.

## Разрешения

Уже сделаны: чтение GitHub/Pages, локальная сборка/тесты, рабочая ветка/draft PR, GitHub Actions artifact `dist` без deployment, документы/резервные копии.

Владелец отдельно разрешает/выполняет: GitHub app authorization, создание/подключение Cloudflare-проекта и первый публичный **Save and Deploy**, новые автоматические deployments, любые изменения существующего сайта/Pages settings, merge, DNS/домен, аналитику/платные услуги. Ничего из этого не выполнено исполнителем.

Тестовая сборка содержит4оригинальных учебных примера, не базу Hytale. Нет HySphere/OpenHytale snapshots, чужих игровых ассетов, секретов, отчётов или архивов. Две оригинальные ИИ-сцены PR5 сохранены,8финальных иллюстраций и плавная полноценная анимация всё ещё не завершены.

## Проверенные официальные инструкции (14.11.2026)

- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/configuration/branch-build-controls/
- https://developers.cloudflare.com/pages/configuration/preview-deployments/

JSON `.cloudflare/preview-settings.json` — точная памятка полей, **не автоматически применяемая конфигурация Cloudflare**. Коммит не создаёт проект и не меняет dashboard.

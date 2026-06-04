# URL Shortener

Сервис для сокращения URL с аналитикой переходов.

## Стек технологий

**Бэкенд:**
- Python 3.12
- FastAPI — веб-фреймворк для сервисов
- Uvicorn — ASGI сервер
- AsyncPG — асинхронная работа с PostgreSQL
- Redis — кэширование и синхронизация slug'ов
- RabbitMQ — обмен сообщениями между сервисами
- aio-pika / FastStream — работа с RabbitMQ

**Фронтенд:**
- React 19
- TypeScript
- Vite — сборщик
- Ant Design — UI библиотека
- React Router — маршрутизация
- @ant-design/charts — графики аналитики

**Инфраструктура:**
- Docker & Docker Compose
- PostgreSQL (2 БД: shortener_db, analytics_db)
- Redis (кэш)
- RabbitMQ (очереди событий)

## Сервисы

| Сервис | Описание |
|--------|----------|
| `users_service` | Аутентификация и управление пользователями (JWT) |
| `shortener_service` | Создание, удаление и перенаправление по коротким ссылкам |
| `analytics_service` | API для получения статистики по ссылкам |
| `analytics_worker` | Обработчик событий из RabbitMQ для сбора аналитики |

## Модель данных

**shortener_db:**
- `users`: id, email, password, created_at
- `short_urls`: slug (PK), origin, created_at, author_id (FK)

**analytics_db:**
- `clicks`: slug (PK), clicks_count, author_id
- `users_agents`: slug (FK), browser, clicks_count, raw_stat
- `users_os`: slug (FK), os, clicks_count, raw_stat
- `users_devices`: slug (FK), device_type, clicks_count, raw_stat

## Принцип работы

1. Пользователь создает короткую ссылку через `shortener_service`
2. Ссылка сохраняется в PostgreSQL и кэшируется в Redis
3. При переходе по короткой ссылке:
   - `shortener_service` перенаправляет и публикует событие в RabbitMQ
   - `analytics_worker` подписывается на событие и обновляет аналитику в PostgreSQL
4. Пользователь может просмотреть статистику через `analytics_service`

## Очереди RabbitMQ

- `sh_redirect` — информация о переходах (ip, slug, agent)
- `links_actions` — операции над ссылками (удаление, создание)

## Запуск

```bash
docker-compose up --build
```

Фронтенд доступен по адресу: `http://localhost:8080`

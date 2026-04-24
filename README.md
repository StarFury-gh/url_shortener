# Документация проекта

## Сервис: Postgresql DB для Пользователей (users_db контейнер)

### Таблица users

- id
- email
- password (hashed)
- created_at

---

## Сервис: Postgresql DB для Аналитики перехода по ссылкам (analytics_db контейнер)

#### Таблица clicks:

- slug PK
- clicked_times

### Таблица users_agents

- slug REFERENCES clicks(slug)
- raw_agent UNIQUE
- browser
- os
- device_type
- clicked_times

---

## Сервис: Postgresql DB для Сокращённых ссылок (shortener_db контейнер)

- slug PK
- origin
- created_at

## Сервис: RabbitMQ

### Очередь: sh_redirect

При сообщении, сохраняет информацию о переходе по сокращённой ссылке.
Формат сообщения:

- agent
- slug
- ip

### Очередь: links_actions

Отслеживает сообщения на изменение состояния ссылок (создание, удаление)
Формат сообщения:

- operation: created, deleted
- slug

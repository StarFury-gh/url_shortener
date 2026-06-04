# URL Shortener - API Documentation

Документация по API для микросервисной архитектуры URL-shortener сервиса.

## Содержание

- [Shortener Service](#shortener-service)
- [Analytics Service](#analytics-service)
- [Users Service](#users-service)
- [Analytics Worker](#analytics-worker)

---

## Shortener Service

**Порт:** По умолчанию 8001  
**Префикс API:** `/sh`

### Endpoints

#### 1. Получение всех ссылок пользователя

- **Метод:** `GET`
- **Эндпоинт:** `/sh/`
- **Описание:** Возвращает список всех ссылок, созданных авторизованным пользователем
- **Аутентификация:** Обязательна (через заголовок Authorization)

**Параметры запроса (Query Parameters):**

- `limit` (int, по умолчанию 100) - количество записей для возврата
- `offset` (int, по умолчанию 0) - смещение для пагинации

**Пример запроса:**

```bash
curl -X GET "http://localhost:8001/sh/?limit=10&offset=0" \
  -H "Authorization: <jwt>"
```

**Ответ (200 OK):**

```json
{
  "links": [
    {
      "slug": "abc123",
      "original_url": "https://example.com"
    }
  ],
  "total": 1
}
```

---

#### 2. Получение и редирект по короткой ссылке

- **Метод:** `GET`
- **Эндпоинт:** `/sh/{slug}`
- **Описание:** Возвращает редирект на оригинальную ссылку по короткому slug. Также отправляет информацию о клике в Analytics Worker через RabbitMQ

**Параметры пути:**

- `slug` (string) - короткий идентификатор ссылки

**Пример запроса:**

```bash
curl -X GET "http://localhost:8001/sh/abc123"
```

**Ответ:**

- `307 Temporary Redirect` - редирект на оригинальный URL
- `404 Not Found` - если ссылка не найдена

---

#### 3. Создание короткой ссылки

- **Метод:** `POST`
- **Эндпоинт:** `/sh/create`
- **Описание:** Создает новую короткую ссылку и отправляет уведомление в Analytics Worker

**Аутентификация:** Обязательна (через заголовок Authorization)

**Тело запроса (JSON):**

```json
{
  "original_url": "https://example.com/very-long-url"
}
```

**Пример запроса:**

```bash
curl -X POST "http://localhost:8001/sh/create" \
  -H "Authorization: <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very-long-url"}'
```

**Ответ (200 OK):**

```json
{
  "slug": "abc123"
}
```

**Возможные ошибки:**

- `400 Bad Request` - если URL недействителен
- `403 Forbidden` - если пользователь не авторизован
- `409 Conflict` - если slug уже существует

---

#### 4. Удаление короткой ссылки

- **Метод:** `DELETE`
- **Эндпоинт:** `/sh/delete/{slug}`
- **Описание:** Удаляет короткую ссылку и отправляет уведомление в Analytics Worker

**Параметры пути:**

- `slug` (string) - короткий идентификатор ссылки

**Пример запроса:**

```bash
curl -X DELETE "http://localhost:8001/sh/delete/abc123"
```

**Ответ (200 OK):**

```json
{
  "deleted": "abc123",
  "origin": "https://example.com"
}
```

**Возможные ошибки:**

- `404 Not Found` - если ссылка не найдена

---

## Analytics Service

**Порт:** По умолчанию 8002  
**Префикс API:** `/analytics`

### Endpoints

#### 1. Получение статистики по конкретной ссылке

- **Метод:** `GET`
- **Эндпоинт:** `/analytics/{slug}`
- **Описание:** Возвращает полную статистику по короткой ссылке (только для владельца)

**Аутентификация:** Обязательна (через заголовок Authorization)

**Параметры пути:**

- `slug` (string) - короткий идентификатор ссылки

**Пример запроса:**

```bash
curl -X GET "http://localhost:8002/analytics/abc123" \
  -H "Authorization: <jwt>"
```

**Ответ (200 OK):**

```json
{
  "slug": "abc123",
  "clicks_count": 42,
  "agents": [
    {
      "browser": "Chrome 120.0",
      "clicks_count": 35
    }
  ],
  "os": [
    {
      "os": "Windows 10",
      "clicks_count": 25
    }
  ],
  "devices": [
    {
      "device_type": "Desktop",
      "clicks_count": 30
    }
  ]
}
```

**Возможные ошибки:**

- `403 Forbidden` - если пользователь не является владельцем ссылки или не авторизован
- `404 Not Found` - если ссылка не найдена

---

#### 2. Получение популярных браузеров

- **Метод:** `GET`
- **Эндпоинт:** `/analytics/agents`
- **Описание:** Возвращает топ популярных браузеров по всем ссылкам

**Аутентификация:** Не требуется

**Пример запроса:**

```bash
curl -X GET "http://localhost:8002/analytics/agents"
```

**Ответ (200 OK):**

```json
[
  {
    "browser": "Chrome 120.0",
    "clicks_count": 150
  },
  {
    "browser": "Firefox 115.0",
    "clicks_count": 85
  }
]
```

---

## Users Service

**Порт:** По умолчанию 8003  
**Префикс API:** `/users`

### Endpoints

#### 1. Аутентификация пользователя (проверка токена)

- **Метод:** `GET`
- **Эндпоинт:** `/users/auth`
- **Описание:** Проверяет валидность JWT токена и возвращает информацию о пользователе

**Параметры заголовка:**

- `Authorization` (string, обязательный) - JWT токен в формате `<jwt>`

**Пример запроса:**

```bash
curl -X GET "http://localhost:8003/users/auth" \
  -H "Authorization: <jwt>"
```

**Ответ (200 OK):**

```json
{
  "status": true,
  "id": 1,
  "email": "user@example.com"
}
```

**Возможные ошибки:**

- `401 Unauthorized` - если токен отсутствует или недействителен
- `400 Bad Request` - если токен имеет неверную подпись

---

#### 2. Получение пользователя по ID

- **Метод:** `GET`
- **Эндпоинт:** `/users/{id}`
- **Описание:** Возвращает информацию о конкретном пользователе по его ID

**Аутентификация:** Обязательна (через заголовок Authorization)

**Параметры пути:**

- `id` (int) - идентификатор пользователя

**Пример запроса:**

```bash
curl -X GET "http://localhost:8003/users/1" \
  -H "Authorization: <jwt>"
```

**Ответ (200 OK):**

```json
{
  "user": {
    "id": 1,
    "email": "user1@example.com",
    "created_at": "2026-01-01T10:00:00"
  }
}
```

**Возможные ошибки:**

- `404 Not Found` - если пользователь не найден

---

#### 4. Вход пользователя (логин)

- **Метод:** `POST`
- **Эндпоинт:** `/users/login`
- **Описание:** Аутентифицирует пользователя и возвращает JWT токен

**Тело запроса (JSON):**

```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```

**Пример запроса:**

```bash
curl -X POST "http://localhost:8003/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "user_password"}'
```

**Ответ (200 OK):**

```json
{
  "status": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Возможные ошибки:**

- `401 Unauthorized` - если пароль неверный
- `404 Not Found` - если пользователь не найден

---

#### 5. Регистрация пользователя

- **Метод:** `POST`
- **Эндпоинт:** `/users/register`
- **Описание:** Регистрирует нового пользователя, автоматически логинит и возвращает токен

**Тело запроса (JSON):**

```json
{
  "email": "newuser@example.com",
  "password": "new_user_password"
}
```

**Пример запроса:**

```bash
curl -X POST "http://localhost:8003/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "newuser@example.com", "password": "new_user_password"}'
```

**Ответ (200 OK):**

```json
{
  "status": true,
  "user_id": 3,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Возможные ошибки:**

- `409 Conflict` - если пользователь с таким email уже существует

---

## Analytics Worker

**Описание:** Микросервис-обработчик сообщений из очереди RabbitMQ. Не имеет HTTP API endpoints. Получает сообщения и обновляет статистику.

### RabbitMQ Очереди

#### 1. `sh_redirect` - обработка кликов по коротким ссылкам

**Тип:** Subscriber (подписка на очередь)

**Сообщение (JSON):**

```json
{
  "ip": "192.168.1.1",
  "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "slug": "abc123"
}
```

**Обработка:**

- Парсит User-Agent для получения информации о браузере, ОС и устройстве
- Обновляет статистику по кликам в базе данных
- Увеличивает счетчик кликов для ссылки

**Лог:** `Redirected by short link with slug: abc123`

---

#### 2. `links_actions` - обработка операций со ссылками

**Тип:** Subscriber (подписка на очередь)

**Сообщение (JSON):**

```json
{
  "operation": "created|deleted",
  "slug": "abc123",
  "author": 1
}
```

**Поля:**

- `operation` (string) - тип операции: "created" или "deleted"
- `slug` (string) - короткий идентификатор ссылки
- `author` (int, опционально) - ID автора ссылки (для операции "created")

**Обработка:**

- При `created`: создает запись статистики для новой ссылки
- При `deleted`: удаляет запись статистики для удаленной ссылки

**Лог:** `Handled operation 'created' with slug: 'abc123' and author_id: 1`

---

## Модели данных (Schemas)

### CreateLinkDTO

```json
{
  "original_url": "https://example.com"
}
```

### Link

```json
{
  "slug": "abc123",
  "original_url": "https://example.com"
}
```

### UserLogin

```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```

### RegisterUser

```json
{
  "email": "newuser@example.com",
  "password": "new_user_password"
}
```

### BrowserAgent

```json
{
  "browser": "Chrome 120.0",
  "clicks_count": 35
}
```

### AgentOs

```json
{
  "os": "Windows 10",
  "clicks_count": 25
}
```

### AgentDevice

```json
{
  "device_type": "Desktop",
  "clicks_count": 30
}
```

### FullSlugInfo

```json
{
  "slug": "abc123",
  "clicks_count": 42,
  "agents": [...],
  "os": [...],
  "devices": [...]
}
```

---

## Схема взаимодействия сервисов

```
[Shortener Service] ↔ [RabbitMQ] ↔ [Analytics Worker]
     |                           |
     |                           └──► Обрабатывает клики и операции
     │
     └──► Создает/удаляет ссылки и отправляет сообщения в RabbitMQ

[Users Service] ──► Аутентификация и управление пользователями
                     ↑
                     └──► Используется Shortener Service для проверки авторизации
```

---

## Требования для вызова API

1. **JWT Token** - для защищенных endpoints используйте заголовок `Authorization: <jwt>`
2. **Content-Type** - для POST/PUT request используйте `application/json`
3. **Валидация URL** - оригинальные URL должны быть валидными HTTP/HTTPS ссылками

---

## Возможные HTTP статусы

| Код | Описание                  |
| --- | ------------------------- |
| 200 | Успех                     |
| 201 | Ресурс создан             |
| 307 | Временный редирект        |
| 400 | Неверный запрос           |
| 401 | Не авторизован            |
| 403 | Доступ запрещен           |
| 404 | Ресурс не найден          |
| 409 | Конфликт (дубликат)       |
| 500 | Внутренняя ошибка сервера |

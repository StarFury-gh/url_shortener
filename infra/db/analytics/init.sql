-- Интернет агенты пользователей
CREATE TABLE users_agents (
    id SERIAL PRIMARY KEY,
    raw_str TEXT UNIQUE,
    browser VARCHAR(32),
    os VARCHAR(32),
    device_type VARCHAR(32)
);

-- Переходы по ссылкам
CREATE TABLE clicks (
    slug VARCHAR(12),
    clicked_times INT
);
-- Интернет агенты пользователей
CREATE TABLE users_agents (
    slug VARCHAR(12),
    raw_str TEXT UNIQUE,
    browser VARCHAR(32),
    os VARCHAR(32),
    device_type VARCHAR(32),
    clicks_count INT
);

-- Переходы по ссылкам
CREATE TABLE clicks (
    slug VARCHAR(12),
    clicked_times INT
);
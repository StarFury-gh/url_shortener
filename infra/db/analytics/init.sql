-- Переходы по ссылкам
CREATE TABLE clicks (
    slug VARCHAR(12) PRIMARY KEY,
    clicked_times INT
);

-- Интернет агенты пользователей
CREATE TABLE users_agents (
    slug VARCHAR(12) REFERENCES clicks(slug),
    raw_agent VARCHAR(255) UNIQUE,
    browser VARCHAR(32),
    os VARCHAR(32),
    device_type VARCHAR(32),
    clicks_count INT
);

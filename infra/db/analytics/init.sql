-- Переходы по ссылкам
CREATE TABLE clicks (
    slug VARCHAR(12) PRIMARY KEY,
    clicks_count INT
);

-- Интернет браузеры пользователей
CREATE TABLE users_agents (
    slug VARCHAR(12) REFERENCES clicks(slug) UNIQUE,
    browser VARCHAR(32),
    clicks_count INT
);

-- ОС пользователей
CREATE TABLE users_os (
    slug VARCHAR(12) REFERENCES clicks(slug) UNIQUE,
    os VARCHAR(32),
    clicks_count INT
);

-- Типы устройства пользователей
CREATE TABLE users_devices (
    slug VARCHAR(12) REFERENCES clicks(slug) UNIQUE,
    device_type VARCHAR(32),
    clicks_count INT
);
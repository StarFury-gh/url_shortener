-- Переходы по ссылкам
CREATE TABLE clicks (
    slug VARCHAR(12) PRIMARY KEY,
    clicks_count INT
);

-- Интернет браузеры пользователей
CREATE TABLE users_agents (
    slug VARCHAR(12) REFERENCES clicks(slug),
    browser VARCHAR(32),
    clicks_count INT,
    raw_stat VARCHAR (255) UNIQUE
);

-- ОС пользователей
CREATE TABLE users_os (
    slug VARCHAR(12) REFERENCES clicks(slug),
    os VARCHAR(32),
    clicks_count INT,
    raw_stat VARCHAR (255) UNIQUE
);

-- Типы устройства пользователей
CREATE TABLE users_devices (
    slug VARCHAR(12) REFERENCES clicks(slug),
    device_type VARCHAR(32),
    clicks_count INT,
    raw_stat VARCHAR (255) UNIQUE
);
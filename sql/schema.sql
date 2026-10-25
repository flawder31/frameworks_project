-- =============================================
-- Сервис счетчиков: структура базы данных
-- =============================================

CREATE TABLE IF NOT EXISTS meters (
    code TEXT PRIMARY KEY,      -- Используем код (EL, CW) как первичный ключ
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    tariff REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_code TEXT NOT NULL,
    previous REAL NOT NULL,
    current REAL NOT NULL,
    reading_date TEXT NOT NULL,
    consumption REAL NOT NULL,
    cost REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meter_code) REFERENCES meters(code)
);
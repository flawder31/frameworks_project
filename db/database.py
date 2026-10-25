import sqlite3

DB_PATH = "data/meterly.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    # Включаем проверку внешних ключей (связей)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

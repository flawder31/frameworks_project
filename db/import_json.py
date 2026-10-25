import json
from db.database import get_connection

METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"


def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def import_meters(conn):
    meters = load_json(METERS_FILE)
    if not meters:
        print("Нет данных для импорта счетчиков.")
        return

    conn.executemany(
        """
        INSERT OR REPLACE INTO meters (code, name, unit, tariff)
        VALUES (?, ?, ?, ?)
        """,
        [
            (m["code"], m["name"], m["unit"], m["tariff"])
            for m in meters
        ],
    )
    print(f"Импортировано счетчиков: {len(meters)}")


def import_readings(conn):
    readings = load_json(READINGS_FILE)
    if not readings:
        print("Нет данных для импорта показаний.")
        return

    conn.executemany(
        """
        INSERT INTO readings (
            meter_code, previous, current, reading_date, consumption, cost
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r["meter_code"],
                r["previous"],
                r["current"],
                r["date"],
                r["consumption"],
                r["cost"],
            )
            for r in readings
        ],
    )
    print(f"Импортировано показаний: {len(readings)}")


def main():
    conn = get_connection()
    try:
        import_meters(conn)
        import_readings(conn)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

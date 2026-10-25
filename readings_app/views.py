import sqlite3
from datetime import datetime
from django.shortcuts import render, redirect

DB_PATH = "data/meterly.sqlite"


def readings_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    readings = conn.execute("""
        SELECT r.id, r.reading_date, m.name AS meter_name, m.unit,
               r.previous, r.current, r.consumption, r.cost
        FROM readings r
        JOIN meters m ON r.meter_code = m.code
        ORDER BY r.reading_date DESC, r.id DESC
    """).fetchall()
    conn.close()
    return render(request, "readings_app/reading_list.html",
                  {"readings": readings})


def add_reading(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    meters = conn.execute(
        "SELECT code, name, unit, tariff FROM meters"
    ).fetchall()

    if request.method == "POST":
        meter_code = request.POST.get("meter_code")
        previous = float(request.POST.get("previous"))
        current = float(request.POST.get("current"))
        reading_date = request.POST.get("reading_date")

        error = None
        meter = conn.execute(
            "SELECT tariff, unit FROM meters WHERE code = ?",
            (meter_code,)
        ).fetchone()

        if not meter:
            error = "Выберите счетчик."
        elif current < previous:
            error = "Текущее показание не может быть меньше предыдущего."
        elif previous < 0 or current < 0:
            error = "Показания не могут быть отрицательными."
        else:
            try:
                date_obj = datetime.strptime(
                    reading_date, "%Y-%m-%d"
                ).date()
                if date_obj > datetime.today().date():
                    error = "Дата снятия не может быть в будущем."
            except ValueError:
                error = "Некорректный формат даты."

        if not error:
            consumption = round(current - previous, 3)
            cost = round(consumption * meter["tariff"], 2)
            full_datetime = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            conn.execute("""
                INSERT INTO readings
                    (meter_code, previous, current, reading_date,
                     consumption, cost, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (meter_code, previous, current, reading_date,
                  consumption, cost, full_datetime))
            conn.commit()
            conn.close()
            return redirect("readings:list")

        conn.close()
        return render(request, "readings_app/reading_add.html", {
            "meters": meters,
            "error": error,
            "prev_val": previous,
            "curr_val": current,
            "sel_code": meter_code,
        })

    conn.close()
    return render(request, "readings_app/reading_add.html",
                  {"meters": meters})


def delete_reading(request, reading_id):
    """Удалить конкретное показание по его ID."""
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute(
                "DELETE FROM readings WHERE id = ?", (reading_id,)
            )
            conn.commit()
        finally:
            conn.close()
    return redirect("readings:list")

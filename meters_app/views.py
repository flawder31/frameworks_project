import sqlite3
from django.shortcuts import render, redirect

DB_PATH = "data/meterly.sqlite"


def meters_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    meters = conn.execute(
        "SELECT code, name, unit, tariff FROM meters ORDER BY name").fetchall()
    conn.close()
    return render(request, "meters_app/meter_list.html", {"meters": meters})


def meter_detail(request, meter_code):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    meter = conn.execute(
        "SELECT code, name, unit, tariff FROM meters WHERE code = ?", (meter_code,)).fetchone()
    conn.close()
    status_code = 404 if meter is None else 200
    return render(request, "meters_app/meter_detail.html", {"meter": meter}, status=status_code)


def add_meter(request):
    error = None
    if request.method == "POST":
        code = request.POST.get("code", "").strip().upper()
        name = request.POST.get("name", "").strip()
        unit = request.POST.get("unit", "").strip()
        tariff_str = request.POST.get("tariff", "")

        # Валидация
        if not code or not name or not unit:
            error = "Все текстовые поля обязательны."
        else:
            try:
                tariff = float(tariff_str)
                if tariff < 0:
                    error = "Тариф не может быть отрицательным."
            except ValueError:
                error = "Тариф должен быть числом."

        if not error:
            conn = sqlite3.connect(DB_PATH)
            try:
                conn.execute("""
                    INSERT INTO meters (code, name, unit, tariff)
                    VALUES (?, ?, ?, ?)
                """, (code, name, unit, tariff))
                conn.commit()
                conn.close()
                return redirect("meters:list")
            except sqlite3.IntegrityError:
                error = f"Счетчик с кодом '{code}' уже существует."
                conn.close()

    return render(request, "meters_app/meter_add.html", {"error": error})


def delete_meter(request, meter_code):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        try:
            # Проверяем, есть ли показания по этому счетчику
            count = conn.execute(
                "SELECT COUNT(*) FROM readings WHERE meter_code = ?", (meter_code,)).fetchone()[0]
            if count > 0:
                # Если есть, удалять нельзя (защита данных)
                return render(request, "meters_app/meter_list.html", {
                    "meters": conn.execute("SELECT * FROM meters").fetchall(),
                    "error": f"Нельзя удалить '{meter_code}': по нему есть {count} показаний."
                })

            conn.execute("DELETE FROM meters WHERE code = ?", (meter_code,))
            conn.commit()
        finally:
            conn.close()

    return redirect("meters:list")

"""Сервис учета показаний нескольких счетчиков.

Начальный сценарий ПР1: проверка корректности показания, расчет расхода
и стоимости потребленного ресурса.
"""

from datetime import date


# --- Справочник типов счетчиков -------------------------------------------

def get_meter_info(meter_code: str) -> tuple:
    """Возвращает название ресурса, единицу измерения и тариф по коду счетчика."""
    if meter_code == "EL":
        return "Электроэнергия", "кВт·ч", 5.50
    elif meter_code == "CW":
        return "Холодная вода", "м³", 42.30
    elif meter_code == "HW":
        return "Горячая вода", "м³", 198.75
    elif meter_code == "GS":
        return "Газ", "м³", 6.85
    else:
        return "Неизвестный ресурс", "-", 0.0


# --- Функция 1: проверка корректности показания ---------------------------

def is_reading_valid(previous: float, current: float) -> bool:
    """Проверяет, что новое показание не меньше предыдущего и не отрицательно."""
    if current < 0:
        return False
    if current < previous:
        return False
    return True


# --- Функция 2: расчет расхода --------------------------------------------

def calculate_consumption(previous: float, current: float) -> float:
    """Возвращает расход ресурса между двумя показаниями."""
    return round(current - previous, 3)


# --- Функция 3: расчет стоимости ------------------------------------------

def calculate_cost(consumption: float, tariff: float) -> float:
    """Возвращает стоимость потребленного ресурса по тарифу."""
    return round(consumption * tariff, 2)


# --- Функция 4: формирование итогового сообщения --------------------------

def build_report(meter_code: str, previous: float, current: float,
                 reading_date: date) -> str:
    """Формирует текстовый отчет по одному счетчику."""
    resource, unit, tariff = get_meter_info(meter_code)

    if not is_reading_valid(previous, current):
        return (
            f"[{resource}] Ошибка: показание {current} {unit} "
            f"меньше предыдущего {previous} {unit}."
        )

    consumption = calculate_consumption(previous, current)
    cost = calculate_cost(consumption, tariff)

    return (
        f"--- {resource} ({meter_code}) ---\n"
        f"Дата снятия: {reading_date}\n"
        f"Предыдущее показание: {previous} {unit}\n"
        f"Текущее показание:    {current} {unit}\n"
        f"Расход:               {consumption} {unit}\n"
        f"Тариф:                {tariff} руб./{unit}\n"
        f"Стоимость:            {cost} руб."
    )


# --- Точка входа -----------------------------------------------------------

def main() -> None:
    """Демонстрационный сценарий учета показаний по трем счетчикам."""
    today = date(2026, 9, 14)

    readings = [
        ("EL", 15420.0, 15580.5),   # электроэнергия
        ("CW", 320.4, 328.9),       # холодная вода
        ("GS", 1120.0, 1115.0),     # газ (некорректное показание)
    ]

    total_cost = 0.0

    for meter_code, prev_value, curr_value in readings:
        report = build_report(meter_code, prev_value, curr_value, today)
        print(report)
        print()

        resource, unit, tariff = get_meter_info(meter_code)
        if is_reading_valid(prev_value, curr_value):
            consumption = calculate_consumption(prev_value, curr_value)
            total_cost += calculate_cost(consumption, tariff)

    print(f"ИТОГО к оплате за период: {round(total_cost, 2)} руб.")


if __name__ == "__main__":
    main()
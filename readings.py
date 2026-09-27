"""Модуль работы с показаниями."""

from datetime import date


def is_reading_valid(previous: float, current: float) -> bool:
    """Проверить корректность нового показания."""
    if current < 0:
        return False
    if current < previous:
        return False
    return True


def calculate_consumption(previous: float, current: float) -> float:
    """Вернуть расход ресурса между двумя показаниями."""
    return round(current - previous, 3)


def calculate_cost(consumption: float, tariff: float) -> float:
    """Вернуть стоимость потребленного ресурса по тарифу."""
    return round(consumption * tariff, 2)


def add_reading(readings: list, meters: dict, meter_code: str,
                previous: float, current: float,
                reading_date: date) -> dict:
    """Добавить показание. Возбуждает ValueError при ошибке."""
    if meter_code not in meters:
        raise ValueError(f"Счётчик с кодом '{meter_code}' не найден")

    if not is_reading_valid(previous, current):
        raise ValueError(
            f"Некорректное показание: {current} меньше предыдущего {previous}"
        )

    consumption = calculate_consumption(previous, current)
    tariff = meters[meter_code]["tariff"]
    cost = calculate_cost(consumption, tariff)

    reading = {
        "meter_code": meter_code,
        "previous": previous,
        "current": current,
        "date": reading_date.isoformat(),
        "consumption": consumption,
        "cost": cost,
    }
    readings.append(reading)
    return reading


def filter_readings_by_meter(readings: list, meter_code: str) -> list:
    """Отобрать показания по коду счетчика."""
    return [r for r in readings if r["meter_code"] == meter_code]


def sort_readings_by_date(readings: list) -> list:
    """Отсортировать показания по дате (lambda)."""
    return sorted(readings, key=lambda r: r["date"])


def get_total_cost(readings: list) -> float:
    """Вернуть суммарную стоимость всех показаний."""
    total = 0.0
    for reading in readings:
        total += reading["cost"]
    return round(total, 2)


def get_statistics(readings: list) -> dict:
    """Вернуть статистику по показаниям."""
    count = len(readings)
    total_cost = get_total_cost(readings)
    average = round(total_cost / count, 2) if count > 0 else 0.0
    return {
        "count": count,
        "total_cost": total_cost,
        "average_cost": average,
    }


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус (функция перенесена из ПР1)."""
    if is_available:
        return "Показание можно внести"
    return "Показание внести нельзя"

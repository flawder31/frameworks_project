"""Модуль работы со справочником счетчиков."""


def get_meter_info(meter_code: str) -> tuple:
    """Вернуть название, единицу измерения и тариф по коду счетчика."""
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


def add_meter(meters: dict, meter_code: str, name: str,
              unit: str, tariff: float) -> None:
    """Добавить счётчик в словарь meters."""
    meters[meter_code] = {
        "name": name,
        "unit": unit,
        "tariff": tariff,
    }


def find_meter(meters: dict, query: str) -> list:
    """Найти счётчики по подстроке названия."""
    query_lower = query.lower()
    result = []
    for code, info in meters.items():
        if query_lower in info["name"].lower():
            result.append({
                "code": code,
                "name": info["name"],
                "unit": info["unit"],
                "tariff": info["tariff"],
            })
    return result


def filter_meters_by_tariff(meters: dict, max_tariff: float) -> list:
    """Отобрать счётчики с тарифом не выше max_tariff."""
    return [
        {"code": code, "name": info["name"], "tariff": info["tariff"]}
        for code, info in meters.items()
        if info["tariff"] <= max_tariff
    ]


def sort_meters(meters: dict) -> list:
    """Отсортировать счётчики по тарифу (lambda)."""
    items = [
        {"code": code, "name": info["name"], "tariff": info["tariff"]}
        for code, info in meters.items()
    ]
    return sorted(items, key=lambda item: item["tariff"])


def get_default_meters() -> dict:
    """Вернуть справочник счётчиков по умолчанию."""
    return {
        "EL": {"name": "Электроэнергия", "unit": "кВт·ч", "tariff": 5.50},
        "CW": {"name": "Холодная вода", "unit": "м³", "tariff": 42.30},
        "HW": {"name": "Горячая вода", "unit": "м³", "tariff": 198.75},
        "GS": {"name": "Газ", "unit": "м³", "tariff": 6.85},
    }

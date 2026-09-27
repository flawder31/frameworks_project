"""Тесты функций работы с показаниями (ПР2)."""
from datetime import date

from readings import (
    is_reading_valid,
    calculate_consumption,
    calculate_cost,
    add_reading,
    filter_readings_by_meter,
    sort_readings_by_date,
    get_total_cost,
    get_statistics,
)


def _make_meters():
    return {
        "EL": {"name": "Электроэнергия", "unit": "кВт·ч", "tariff": 5.50},
        "CW": {"name": "Холодная вода", "unit": "м³", "tariff": 42.30},
    }


def test_is_reading_valid_true():
    assert is_reading_valid(100.0, 150.0) is True


def test_is_reading_valid_false_lower():
    assert is_reading_valid(100.0, 90.0) is False


def test_is_reading_valid_false_negative():
    assert is_reading_valid(100.0, -5.0) is False


def test_calculate_consumption():
    assert calculate_consumption(15420.0, 15580.5) == 160.5


def test_calculate_cost():
    assert calculate_cost(160.5, 5.50) == 882.75


def test_add_reading_success():
    meters = _make_meters()
    readings = []
    reading = add_reading(
        readings, meters, "EL", 15420.0, 15580.5, date(2026, 9, 14)
    )
    assert len(readings) == 1
    assert reading["consumption"] == 160.5
    assert reading["cost"] == 882.75
    assert reading["date"] == "2026-09-14"


def test_add_reading_unknown_meter():
    meters = _make_meters()
    readings = []
    try:
        add_reading(readings, meters, "XX", 10.0, 20.0, date(2026, 9, 14))
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_add_reading_invalid_value():
    meters = _make_meters()
    readings = []
    try:
        add_reading(readings, meters, "EL", 100.0, 50.0, date(2026, 9, 14))
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_filter_readings_by_meter():
    readings = [
        {"meter_code": "EL", "cost": 100.0},
        {"meter_code": "CW", "cost": 50.0},
        {"meter_code": "EL", "cost": 200.0},
    ]
    result = filter_readings_by_meter(readings, "EL")
    assert len(result) == 2


def test_sort_readings_by_date():
    readings = [
        {"meter_code": "EL", "date": "2026-09-20", "cost": 1.0},
        {"meter_code": "EL", "date": "2026-09-10", "cost": 1.0},
        {"meter_code": "EL", "date": "2026-09-15", "cost": 1.0},
    ]
    sorted_r = sort_readings_by_date(readings)
    assert sorted_r[0]["date"] == "2026-09-10"
    assert sorted_r[-1]["date"] == "2026-09-20"


def test_get_total_cost():
    readings = [{"cost": 100.0}, {"cost": 200.5}, {"cost": 50.25}]
    assert get_total_cost(readings) == 350.75


def test_get_statistics():
    readings = [{"cost": 100.0}, {"cost": 200.0}]
    stats = get_statistics(readings)
    assert stats["count"] == 2
    assert stats["total_cost"] == 300.0
    assert stats["average_cost"] == 150.0


def test_get_statistics_empty():
    stats = get_statistics([])
    assert stats["count"] == 0
    assert stats["total_cost"] == 0.0
    assert stats["average_cost"] == 0.0

"""Тесты класса Reading."""
from datetime import date
from models import Meter, Reading
from models.readings import (add_reading, get_total_cost,
                             get_statistics)


def _meter():
    return Meter("EL", "Электроэнергия", "кВт·ч", 5.50)


def test_reading_creation():
    reading = Reading(_meter(), 15420.0, 15580.5, "2026-09-14")
    assert reading.consumption == 160.5
    assert reading.cost == 882.75


def test_reading_is_valid_true():
    reading = Reading(_meter(), 100.0, 150.0, "2026-09-14")
    assert reading.is_valid() is True


def test_reading_is_valid_false():
    reading = Reading(_meter(), 100.0, 90.0, "2026-09-14")
    assert reading.is_valid() is False


def test_reading_str():
    reading = Reading(_meter(), 100.0, 150.0, "2026-09-14")
    assert "Электроэнергия" in str(reading)


def test_add_reading_success():
    meters = [_meter()]
    readings = []
    reading = add_reading(readings, meters, "EL",
                          15420.0, 15580.5, date(2026, 9, 14))
    assert len(readings) == 1
    assert reading.cost == 882.75


def test_add_reading_invalid_raises():
    meters = [_meter()]
    readings = []
    try:
        add_reading(readings, meters, "EL",
                    100.0, 50.0, date(2026, 9, 14))
        assert False, "Ожидалось ValueError"
    except ValueError:
        pass


def test_reading_from_data():
    meters = [_meter()]
    data = {"meter_code": "EL", "previous": 100.0,
            "current": 150.0, "date": "2026-09-14"}
    reading = Reading.from_data(data, meters)
    assert reading is not None
    assert reading.meter.code == "EL"


def test_get_total_cost():
    meters = [_meter()]
    readings = [
        Reading(meters[0], 0.0, 100.0, "2026-09-14"),
        Reading(meters[0], 0.0, 200.0, "2026-09-15"),
    ]
    assert get_total_cost(readings) == round(100 * 5.5 + 200 * 5.5, 2)


def test_get_statistics_empty():
    stats = get_statistics([])
    assert stats["count"] == 0

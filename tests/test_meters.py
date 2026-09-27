"""Тесты класса Meter."""
from models import Meter
from models.meters import (add_meter, find_meter,
                           filter_meters_by_tariff, sort_meters)


def test_meter_creation():
    meter = Meter("EL", "Электроэнергия", "кВт·ч", 5.50)
    assert meter.code == "EL"
    assert meter.name == "Электроэнергия"
    assert meter.tariff == 5.50


def test_meter_str():
    meter = Meter("EL", "Электроэнергия", "кВт·ч", 5.50)
    assert "Электроэнергия" in str(meter)


def test_meter_matches_query():
    meter = Meter("CW", "Холодная вода", "м³", 42.30)
    assert meter.matches_query("вода")
    assert meter.matches_query("ВОДА")


def test_meter_is_tariff_within():
    meter = Meter("EL", "Электроэнергия", "кВт·ч", 5.50)
    assert meter.is_tariff_within(50.0) is True
    assert meter.is_tariff_within(1.0) is False


def test_meter_from_data():
    data = {"code": "EL", "name": "Электроэнергия",
            "unit": "кВт·ч", "tariff": 5.50}
    meter = Meter.from_data(data)
    assert meter.code == "EL"
    assert meter.tariff == 5.50


def test_meter_to_data():
    meter = Meter("EL", "Электроэнергия", "кВт·ч", 5.50)
    assert meter.to_data()["code"] == "EL"


def test_add_meter():
    meters = []
    add_meter(meters, "EL", "Электроэнергия", "кВт·ч", 5.50)
    assert len(meters) == 1


def test_find_meter():
    meters = [Meter("EL", "Электроэнергия", "кВт·ч", 5.50),
              Meter("CW", "Холодная вода", "м³", 42.30)]
    assert len(find_meter(meters, "вода")) == 1


def test_filter_meters_by_tariff():
    meters = [Meter("EL", "Электроэнергия", "кВт·ч", 5.50),
              Meter("HW", "Горячая вода", "м³", 198.75)]
    assert len(filter_meters_by_tariff(meters, 50.0)) == 1


def test_sort_meters():
    meters = [Meter("HW", "Горячая вода", "м³", 198.75),
              Meter("EL", "Электроэнергия", "кВт·ч", 5.50)]
    result = sort_meters(meters)
    assert result[0].code == "EL"

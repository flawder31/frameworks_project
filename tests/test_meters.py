"""Тесты функций работы со счётчиками."""
from meters import (add_meter, find_meter, filter_meters_by_tariff,
                    sort_meters, get_meter_info)


def test_add_meter():
    meters = {}
    add_meter(meters, "EL", "Электроэнергия", "кВт·ч", 5.50)
    assert len(meters) == 1
    assert meters["EL"]["tariff"] == 5.50


def test_find_meter():
    meters = {}
    add_meter(meters, "EL", "Электроэнергия", "кВт·ч", 5.50)
    add_meter(meters, "CW", "Холодная вода", "м³", 42.30)
    assert len(find_meter(meters, "вода")) == 1


def test_filter_meters_by_tariff():
    meters = {}
    add_meter(meters, "EL", "Электроэнергия", "кВт·ч", 5.50)
    add_meter(meters, "HW", "Горячая вода", "м³", 198.75)
    assert len(filter_meters_by_tariff(meters, 50.0)) == 1


def test_sort_meters():
    meters = {}
    add_meter(meters, "HW", "Горячая вода", "м³", 198.75)
    add_meter(meters, "EL", "Электроэнергия", "кВт·ч", 5.50)
    result = sort_meters(meters)
    assert result[0]["code"] == "EL"


def test_get_meter_info():
    name, unit, tariff = get_meter_info("EL")
    assert name == "Электроэнергия"
    assert tariff == 5.50

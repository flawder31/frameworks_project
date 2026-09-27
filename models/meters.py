"""Класс Meter и функции работы с коллекцией счётчиков."""

from typing import List


class Meter:
    """Счётчик ресурса."""

    def __init__(self, meter_code: str, name: str,
                 unit: str, tariff: float) -> None:
        """Создать объект счётчика."""
        self.code = meter_code
        self.name = name
        self.unit = unit
        self.tariff = tariff

    def matches_query(self, query: str) -> bool:
        """Проверить, содержит ли название подстроку query."""
        return query.lower() in self.name.lower()

    def is_tariff_within(self, max_tariff: float) -> bool:
        """Проверить, что тариф не выше max_tariff."""
        return self.tariff <= max_tariff

    @classmethod
    def from_data(cls, data: dict) -> "Meter":
        """Создать счётчик из данных JSON."""
        return cls(
            meter_code=data["code"],
            name=data["name"],
            unit=data["unit"],
            tariff=data["tariff"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в данные JSON."""
        return {
            "code": self.code,
            "name": self.name,
            "unit": self.unit,
            "tariff": self.tariff,
        }

    def __str__(self) -> str:
        """Строковое представление счётчика."""
        return (f"[{self.code}] {self.name} — "
                f"{self.tariff:.2f} руб./{self.unit}")


def add_meter(meters: List[Meter], meter_code: str, name: str,
              unit: str, tariff: float) -> Meter:
    """Создать объект Meter и добавить в коллекцию."""
    meter = Meter(meter_code, name, unit, tariff)
    meters.append(meter)
    return meter


def find_meter_by_code(meters: List[Meter], code: str) -> Meter:
    """Найти счётчик по коду."""
    for meter in meters:
        if meter.code == code:
            return meter
    return None


def find_meter(meters: List[Meter], query: str) -> List[Meter]:
    """Найти счётчики по подстроке названия."""
    return [m for m in meters if m.matches_query(query)]


def filter_meters_by_tariff(meters: List[Meter],
                            max_tariff: float) -> List[Meter]:
    """Отобрать счётчики по тарифу."""
    return [m for m in meters if m.is_tariff_within(max_tariff)]


def sort_meters(meters: List[Meter]) -> List[Meter]:
    """Отсортировать счётчики по тарифу."""
    return sorted(meters, key=lambda m: m.tariff)


def get_default_meters() -> List[Meter]:
    """Вернуть список счётчиков по умолчанию."""
    return [
        Meter("EL", "Электроэнергия", "кВт·ч", 5.50),
        Meter("CW", "Холодная вода", "м³", 42.30),
        Meter("HW", "Горячая вода", "м³", 198.75),
        Meter("GS", "Газ", "м³", 6.85),
    ]

"""Класс Reading и функции работы с коллекцией показаний."""

from datetime import date
from typing import List, Optional

from .meters import Meter


class Reading:
    """Показание счётчика."""

    def __init__(self, meter: Meter, previous: float,
                 current: float, reading_date: str) -> None:
        """Создать объект показания."""
        self.meter = meter
        self.previous = previous
        self.current = current
        self.reading_date = reading_date
        self.consumption = self._calc_consumption()
        self.cost = self._calc_cost()

    def _calc_consumption(self) -> float:
        """Рассчитать расход."""
        return round(self.current - self.previous, 3)

    def _calc_cost(self) -> float:
        """Рассчитать стоимость."""
        return round(self.consumption * self.meter.tariff, 2)

    def is_valid(self) -> bool:
        """Проверить корректность показания."""
        if self.current < 0:
            return False
        if self.current < self.previous:
            return False
        return True

    @classmethod
    def from_data(cls, data: dict, meters: List[Meter]) -> Optional["Reading"]:
        """Создать показание из данных JSON, найдя счётчик по коду."""
        meter = None
        for m in meters:
            if m.code == data["meter_code"]:
                meter = m
                break
        if meter is None:
            return None
        reading = cls(
            meter=meter,
            previous=data["previous"],
            current=data["current"],
            reading_date=data["date"],
        )
        return reading

    def to_data(self) -> dict:
        """Преобразовать в данные JSON."""
        return {
            "meter_code": self.meter.code,
            "previous": self.previous,
            "current": self.current,
            "date": self.reading_date,
            "consumption": self.consumption,
            "cost": self.cost,
        }

    def __str__(self) -> str:
        """Строковое представление показания."""
        return (f"{self.reading_date} | {self.meter.name} | "
                f"{self.previous} -> {self.current} | "
                f"расход {self.consumption} {self.meter.unit} | "
                f"{self.cost:.2f} руб.")


def add_reading(readings: List[Reading], meters: List[Meter],
                meter_code: str, previous: float, current: float,
                reading_date: date) -> Reading:
    """Создать показание и добавить его в коллекцию."""
    meter = None
    for m in meters:
        if m.code == meter_code:
            meter = m
            break
    if meter is None:
        raise ValueError(f"Счётчик '{meter_code}' не найден")

    reading = Reading(meter, previous, current, reading_date.isoformat())
    if not reading.is_valid():
        raise ValueError(
            f"Некорректное показание: {current} меньше предыдущего {previous}"
        )
    readings.append(reading)
    return reading


def filter_readings_by_meter(readings: List[Reading],
                             meter_code: str) -> List[Reading]:
    """Отобрать показания по коду счётчика."""
    return [r for r in readings if r.meter.code == meter_code]


def sort_readings_by_date(readings: List[Reading]) -> List[Reading]:
    """Отсортировать показания по дате."""
    return sorted(readings, key=lambda r: r.reading_date)


def get_total_cost(readings: List[Reading]) -> float:
    """Суммарная стоимость всех показаний."""
    total = 0.0
    for r in readings:
        total += r.cost
    return round(total, 2)


def get_statistics(readings: List[Reading]) -> dict:
    """Статистика по показаниям."""
    count = len(readings)
    total_cost = get_total_cost(readings)
    average = round(total_cost / count, 2) if count > 0 else 0.0
    return {
        "count": count,
        "total_cost": total_cost,
        "average_cost": average,
    }

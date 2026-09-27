"""Сохранение и загрузка объектов в JSON."""

import json
import os
from typing import List

from models.meters import Meter
from models.readings import Reading


def _ensure_dir(filename: str) -> None:
    """Создать каталог, если его нет."""
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def load_meters(filename: str) -> List[Meter]:
    """Загрузить счётчики из JSON и преобразовать в объекты."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Некорректный JSON в {filename}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в {filename}")
    return [Meter.from_data(item) for item in data]


def save_meters(filename: str, meters: List[Meter]) -> None:
    """Сохранить счётчики в JSON."""
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([m.to_data() for m in meters], file,
                  ensure_ascii=False, indent=2)


def load_readings(filename: str,
                  meters: List[Meter]) -> List[Reading]:
    """Загрузить показания, связав их с объектами счётчиков."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Некорректный JSON в {filename}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в {filename}")

    readings = []
    for item in data:
        reading = Reading.from_data(item, meters)
        if reading is not None:
            readings.append(reading)
    return readings


def save_readings(filename: str, readings: List[Reading]) -> None:
    """Сохранить показания в JSON."""
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([r.to_data() for r in readings], file,
                  ensure_ascii=False, indent=2)

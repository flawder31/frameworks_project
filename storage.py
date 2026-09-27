"""Модуль сохранения и загрузки данных в JSON."""

import json
import os


def load_data(filename: str) -> list:
    """Загрузить список из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Некорректный JSON в файле {filename}") from exc
    except OSError as exc:
        raise ValueError(f"Ошибка чтения {filename}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в {filename}")
    return data


def save_data(filename: str, data: list) -> None:
    """Сохранить список в JSON."""
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise ValueError(f"Ошибка записи {filename}: {exc}") from exc


def load_meters(filename: str) -> dict:
    """Загрузить справочник счетчиков."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Некорректный JSON в {filename}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Ожидался словарь в {filename}")
    return data


def save_meters(filename: str, meters: dict) -> None:
    """Сохранить справочник счетчиков."""
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(meters, file, ensure_ascii=False, indent=2)

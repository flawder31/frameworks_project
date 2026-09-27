"""Безопасный ввод с обработкой ошибок."""

from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"


def input_int(prompt: str, min_value: int = None,
              max_value: int = None) -> int:
    """Запросить целое число с повторением при ошибке."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  Ошибка: введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"  Ошибка: не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"  Ошибка: не больше {max_value}.")
            continue
        return value


def input_float(prompt: str, min_value: float = None) -> float:
    """Запросить число с плавающей точкой."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print("  Ошибка: введите число.")
            continue
        if min_value is not None and value < min_value:
            print(f"  Ошибка: не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, DATE_FORMAT).date()
        except ValueError:
            print(f"  Ошибка: формат {DATE_FORMAT}.")

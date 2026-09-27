"""Точка запуска приложения «Сервис учета показаний» (ООП)."""

from typing import List

from models.meters import (
    Meter, add_meter, find_meter, filter_meters_by_tariff,
    sort_meters, get_default_meters,
)
from models.readings import (
    Reading, add_reading, filter_readings_by_meter,
    sort_readings_by_date, get_statistics,
)
from storage import (
    load_meters, save_meters, load_readings, save_readings,
)
from utils import input_int, input_float, input_date

METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"


def show_meters(meters: List[Meter]) -> None:
    """Вывести список счётчиков."""
    if not meters:
        print("  Справочник пуст.")
        return
    for meter in meters:
        print(f"  {meter}")


def show_readings(readings: List[Reading]) -> None:
    """Вывести список показаний."""
    if not readings:
        print("  Показаний нет.")
        return
    for reading in readings:
        print(f"  {reading}")


def print_menu() -> None:
    """Вывести меню."""
    print()
    print("=" * 40)
    print("  СЕРВИС УЧЕТА ПОКАЗАНИЙ (ООП)")
    print("=" * 40)
    print("  1. Показать счетчики")
    print("  2. Найти счетчик")
    print("  3. Счетчики с тарифом не выше")
    print("  4. Сортировка счетчиков по тарифу")
    print("  5. Добавить счетчик")
    print("  6. Внести показание")
    print("  7. Показать все показания")
    print("  8. Показания по счетчику")
    print("  9. Сортировка показаний по дате")
    print(" 10. Статистика")
    print("  0. Выход")
    print("=" * 40)


def handle_add_reading(meters: List[Meter],
                       readings: List[Reading]) -> None:
    """Сценарий добавления показания."""
    if not meters:
        print("  Сначала добавьте счетчик.")
        return
    show_meters(meters)
    code = input("  Код счетчика: ").strip().upper()
    previous = input_float("  Предыдущее показание: ", min_value=0)
    current = input_float("  Текущее показание: ", min_value=0)
    reading_date = input_date("  Дата (ДД.ММ.ГГГГ): ")
    try:
        reading = add_reading(readings, meters, code,
                              previous, current, reading_date)
        print(f"  Добавлено: {reading}")
    except ValueError as exc:
        print(f"  Ошибка: {exc}")


def handle_add_meter(meters: List[Meter]) -> None:
    """Сценарий добавления счётчика."""
    code = input("  Код (например, EL): ").strip().upper()
    if not code:
        print("  Код не может быть пустым.")
        return
    name = input("  Название ресурса: ").strip()
    unit = input("  Единица измерения: ").strip()
    tariff = input_float("  Тариф: ", min_value=0)
    meter = add_meter(meters, code, name, unit, tariff)
    print(f"  Добавлен: {meter}")


def main() -> None:
    """Точка входа."""
    meters = load_meters(METERS_FILE)
    if not meters:
        meters = get_default_meters()
        save_meters(METERS_FILE, meters)
        print("  Загружен справочник по умолчанию.")

    readings = load_readings(READINGS_FILE, meters)

    while True:
        print_menu()
        choice = input_int("  Выберите действие: ")

        if choice == 0:
            save_meters(METERS_FILE, meters)
            save_readings(READINGS_FILE, readings)
            print("  Данные сохранены. До свидания!")
            break
        elif choice == 1:
            show_meters(meters)
        elif choice == 2:
            query = input("  Подстрока: ").strip()
            show_meters(find_meter(meters, query))
        elif choice == 3:
            max_t = input_float("  Макс. тариф: ", min_value=0)
            show_meters(filter_meters_by_tariff(meters, max_t))
        elif choice == 4:
            show_meters(sort_meters(meters))
        elif choice == 5:
            handle_add_meter(meters)
        elif choice == 6:
            handle_add_reading(meters, readings)
        elif choice == 7:
            show_readings(readings)
        elif choice == 8:
            code = input("  Код счетчика: ").strip().upper()
            show_readings(filter_readings_by_meter(readings, code))
        elif choice == 9:
            show_readings(sort_readings_by_date(readings))
        elif choice == 10:
            stats = get_statistics(readings)
            print(f"  Количество: {stats['count']}")
            print(f"  Общая стоимость: {stats['total_cost']:.2f} руб.")
            print(f"  Средняя: {stats['average_cost']:.2f} руб.")
        else:
            print("  Неизвестная команда.")


if __name__ == "__main__":
    main()

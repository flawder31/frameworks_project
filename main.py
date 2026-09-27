"""Точка запуска приложения «Сервис учета показаний»."""

from meters import (
    add_meter, find_meter, filter_meters_by_tariff,
    sort_meters, get_default_meters,
)
from readings import (
    add_reading, filter_readings_by_meter,
    sort_readings_by_date, get_statistics,
)
from storage import load_data, save_data, load_meters, save_meters
from utils import input_int, input_float, input_date

METERS_FILE = "data/meters.json"
READINGS_FILE = "data/readings.json"


def show_meters(meters: dict) -> None:
    """Вывести список счетчиков."""
    if not meters:
        print("  Справочник пуст.")
        return
    print(f"  {'Код':<6} {'Название':<20} {'Ед.':<8} {'Тариф':>8}")
    print("  " + "-" * 46)
    for code, info in meters.items():
        print(f"  {code:<6} {info['name']:<20} "
              f"{info['unit']:<8} {info['tariff']:>8.2f}")


def show_readings(readings: list, meters: dict) -> None:
    """Вывести список показаний."""
    if not readings:
        print("  Показаний нет.")
        return
    for r in readings:
        unit = meters.get(r["meter_code"], {}).get("unit", "-")
        print(f"  {r['date']} | {r['meter_code']} | "
              f"{r['previous']} -> {r['current']} | "
              f"расход {r['consumption']} {unit} | "
              f"{r['cost']:.2f} руб.")


def show_found(found: list) -> None:
    """Вывести найденные счетчики."""
    if not found:
        print("  Ничего не найдено.")
        return
    for item in found:
        print(f"  [{item['code']}] {item['name']} — {item['tariff']:.2f} руб.")


def print_menu() -> None:
    """Вывести меню."""
    print()
    print("=" * 40)
    print("  СЕРВИС УЧЕТА ПОКАЗАНИЙ")
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


def handle_add_reading(meters: dict, readings: list) -> None:
    """Сценарий добавления показания."""
    if not meters:
        print("  Сначала добавьте счетчик.")
        return
    show_meters(meters)
    code = input("  Код счетчика: ").strip().upper()
    if code not in meters:
        print(f"  Счетчик '{code}' не найден.")
        return
    previous = input_float("  Предыдущее показание: ", min_value=0)
    current = input_float("  Текущее показание: ", min_value=0)
    reading_date = input_date("  Дата (ДД.ММ.ГГГГ): ")
    try:
        reading = add_reading(readings, meters, code,
                              previous, current, reading_date)
        print(f"  Добавлено. Расход: {reading['consumption']}, "
              f"стоимость: {reading['cost']:.2f} руб.")
    except ValueError as exc:
        print(f"  Ошибка: {exc}")


def handle_add_meter(meters: dict) -> None:
    """Сценарий добавления счётчика."""
    code = input("  Код (например, EL): ").strip().upper()
    if not code:
        print("  Код не может быть пустым.")
        return
    name = input("  Название ресурса: ").strip()
    unit = input("  Единица измерения: ").strip()
    tariff = input_float("  Тариф: ", min_value=0)
    add_meter(meters, code, name, unit, tariff)
    print(f"  Счетчик '{code}' добавлен.")


def main() -> None:
    """Точка входа."""
    meters = load_meters(METERS_FILE)
    if not meters:
        meters = get_default_meters()
        save_meters(METERS_FILE, meters)
        print("  Загружен справочник по умолчанию.")

    readings = load_data(READINGS_FILE)

    while True:
        print_menu()
        choice = input_int("  Выберите действие: ")

        if choice == 0:
            save_meters(METERS_FILE, meters)
            save_data(READINGS_FILE, readings)
            print("  Данные сохранены. До свидания!")
            break
        elif choice == 1:
            show_meters(meters)
        elif choice == 2:
            query = input("  Подстрока: ").strip()
            show_found(find_meter(meters, query))
        elif choice == 3:
            max_t = input_float("  Макс. тариф: ", min_value=0)
            show_found(filter_meters_by_tariff(meters, max_t))
        elif choice == 4:
            show_found(sort_meters(meters))
        elif choice == 5:
            handle_add_meter(meters)
        elif choice == 6:
            handle_add_reading(meters, readings)
        elif choice == 7:
            show_readings(readings, meters)
        elif choice == 8:
            code = input("  Код счетчика: ").strip().upper()
            show_readings(filter_readings_by_meter(readings, code), meters)
        elif choice == 9:
            show_readings(sort_readings_by_date(readings), meters)
        elif choice == 10:
            stats = get_statistics(readings)
            print(f"  Количество: {stats['count']}")
            print(f"  Общая стоимость: {stats['total_cost']:.2f} руб.")
            print(f"  Средняя: {stats['average_cost']:.2f} руб.")
        else:
            print("  Неизвестная команда.")


if __name__ == "__main__":
    main()

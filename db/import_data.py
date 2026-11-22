import os
import sys
import sqlite3
from pathlib import Path
import django

# Настройка пути к проекту
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meterly.settings') # Убедись, что имя проекта meterly
django.setup()

from meters_app.models import Meter
from readings_app.models import Reading

SOURCE_DB = BASE_DIR / "data" / "meterly.sqlite"

def import_data():
    if not SOURCE_DB.exists():
        print(f"Ошибка: Исходная база не найдена по пути {SOURCE_DB}")
        return

    print("Начинаем перенос данных...")
    
    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        
        # 1. Переносим счетчики
        meters = conn.execute("SELECT code, name, unit, tariff FROM meters").fetchall()
        for m in meters:
            # update_or_create обновит запись, если код уже есть, или создаст новую
            Meter.objects.update_or_create(
                code=m['code'],
                defaults={
                    'name': m['name'],
                    'unit': m['unit'],
                    'tariff': m['tariff']
                }
            )
        print(f"Перенесено счетчиков: {Meter.objects.count()}")

        # 2. Переносим показания
        readings = conn.execute("SELECT id, meter_code, previous, current, reading_date, consumption, cost FROM readings").fetchall()
        for r in readings:
            try:
                # Находим объект счетчика по коду
                meter_obj = Meter.objects.get(code=r['meter_code'])
                
                Reading.objects.update_or_create(
                    # Так как ID могут конфликтовать или быть разными, 
                    # мы можем искать по уникальной комбинации или просто создавать новые.
                    # Для простоты создадим новые записи, сохранив старые ID если получится, 
                    # но лучше просто создать новые, так как ID автоинкрементный в новой базе.
                    # Однако, чтобы сохранить связи, мы используем meter_obj.
                    
                    # Внимание: если мы хотим сохранить точные ID из старой базы, 
                    # нужно использовать pk=r['id'], но это может вызвать конфликты.
                    # Давайте просто создадим новые записи через create, если их нет.
                    # Но update_or_create требует уникального ключа. 
                    # В новой модели нет уникального ограничения на дату+счетчик.
                    # Поэтому просто создадим их все заново.
                    
                    defaults={
                        'meter': meter_obj,
                        'previous': r['previous'],
                        'current': r['current'],
                        'reading_date': r['reading_date'],
                        'consumption': r['consumption'],
                        'cost': r['cost']
                    },
                    # Хак: чтобы не дублировать при повторном запуске, 
                    # можно попробовать найти по дате и счетчику, но это сложно.
                    # Проще всего очистить таблицу перед импортом или использовать pk.
                    # Попробуем использовать pk, если он свободен.
                    pk=r['id'] 
                )
            except Meter.DoesNotExist:
                print(f"Пропущено показание ID {r['id']}: счетчик {r['meter_code']} не найден.")
            except Exception as e:
                print(f"Ошибка при переносе показания ID {r['id']}: {e}")

    print(f"Всего показаний в новой базе: {Reading.objects.count()}")
    print("Перенос завершен!")

if __name__ == "__main__":
    import_data()
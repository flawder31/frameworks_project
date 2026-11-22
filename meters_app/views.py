from django.shortcuts import render, redirect, get_object_or_404
from .models import Meter

def meters_list(request):
    # Получаем все счетчики, отсортированные по имени (как в Meta модели)
    meters = Meter.objects.all()
    return render(request, "meters_app/meter_list.html", {"meters": meters})

def meter_detail(request, slug):
    # Ищем по слагу
    meter = get_object_or_404(Meter, slug=slug)
    return render(request, "meters_app/meter_detail.html", {"meter": meter})

def add_meter(request):
    error = None
    if request.method == "POST":
        code = request.POST.get("code", "").strip().upper()
        name = request.POST.get("name", "").strip()
        unit = request.POST.get("unit", "").strip()
        tariff_str = request.POST.get("tariff", "")

        # Валидация
        if not code or not name or not unit:
            error = "Все текстовые поля обязательны."
        else:
            try:
                tariff = float(tariff_str)
                if tariff < 0:
                    error = "Тариф не может быть отрицательным."
            except ValueError:
                error = "Тариф должен быть числом."

        if not error:
            try:
                # Создаем запись через ORM
                Meter.objects.create(
                    code=code, 
                    name=name, 
                    unit=unit, 
                    tariff=tariff
                )
                return redirect("meters:list")
            except Exception:
                # Если код уже существует (IntegrityError), Django сам обработает это, 
                # но можно поймать исключение для красивого сообщения
                error = f"Счетчик с кодом '{code}' уже существует."

    return render(request, "meters_app/meter_add.html", {"error": error})

def delete_meter(request, meter_code):
    if request.method == "POST":
        # Получаем объект счетчика или возвращаем 404
        meter = get_object_or_404(Meter, code=meter_code)
        
        # Проверяем, есть ли связанные показания (используем related_name="readings")
        if meter.readings.exists():
            count = meter.readings.count()
            meters = Meter.objects.all().order_by("name") # Получаем список для отображения ошибки
            return render(request, "meters_app/meter_list.html", {
                "meters": meters,
                "error": f"Нельзя удалить '{meter.code}': по нему есть {count} показаний."
            })
        
        # Если показаний нет, удаляем счетчик
        meter.delete()
        return redirect("meters:list")
    
    # Если метод не POST, просто перенаправляем на список
    return redirect("meters:list")
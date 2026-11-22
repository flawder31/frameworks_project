from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from django.core.paginator import Paginator
from .models import Reading
from meters_app.models import Meter

def readings_list(request):
    # 1. ФИЛЬТРАЦИЯ (используем новые методы менеджера)
    meter_code = request.GET.get("meter", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    
    # Начинаем с базового запроса через наш менеджер
    readings_qs = Reading.objects.select_related('meter').all()

    # Используем метод for_meter, если выбран счетчик
    if meter_code:
        readings_qs = readings_qs.for_meter(meter_code)

    # Фильтр по датам
    if date_from and date_to:
        try:
            dt_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            dt_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            readings_qs = readings_qs.for_date_range(dt_from, dt_to)
        except ValueError:
            pass
            
    # 2. СОРТИРОВКА
    sort_by = request.GET.get("sort", "-reading_date")
    allowed_sorts = ["reading_date", "-reading_date", "cost", "-cost", "consumption", "-consumption"]
    if sort_by not in allowed_sorts:
        sort_by = "-reading_date"
    
    readings_qs = readings_qs.order_by(sort_by)

    # Аннотирование
    readings_qs = readings_qs.annotate(
        meter_name=F('meter__name'),
        unit=F('meter__unit')
    )

    # 3. ПАГИНАЦИЯ
    paginator = Paginator(readings_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    meters = Meter.objects.all().order_by("name")

    context = {
        "page_obj": page_obj,
        "meters": meters,
        "current_meter": meter_code,
        "date_from": date_from,
        "date_to": date_to,
        "current_sort": sort_by,
    }
    
    return render(request, "readings_app/reading_list.html", context)


def add_reading(request):
    meters = Meter.objects.all() 
    
    if request.method == "POST":
        meter_code = request.POST.get("meter_code")
        previous = float(request.POST.get("previous"))
        current = float(request.POST.get("current"))
        reading_date = request.POST.get("reading_date")
        error = None
        
        try:
            meter = Meter.objects.get(code=meter_code)
        except Meter.DoesNotExist:
            meter = None
            error = "Выберите счетчик."

        if meter:
            if current < previous:
                error = "Текущее показание не может быть меньше предыдущего."
            elif previous < 0 or current < 0:
                error = "Показания не могут быть отрицательными."
            else:
                try:
                    date_obj = datetime.strptime(reading_date, "%Y-%m-%d").date()
                    if date_obj > datetime.today().date():
                        error = "Дата снятия не может быть в будущем."
                except ValueError:
                    error = "Некорректный формат даты."

        if not error and meter:
            consumption = round(current - previous, 3)
            cost = round(consumption * float(meter.tariff), 2)
            
            Reading.objects.create(
                meter=meter,
                previous=previous,
                current=current,
                reading_date=reading_date,
                consumption=consumption,
                cost=cost
            )
            return redirect("readings:list")

        return render(request, "readings_app/reading_add.html", {
            "meters": meters,
            "error": error,
            "prev_val": previous,
            "curr_val": current,
            "sel_code": meter_code,
        })

    return render(request, "readings_app/reading_add.html", {"meters": meters})

def delete_reading(request, reading_id):
    """Удалить конкретное показание по его ID."""
    if request.method == "POST":
        reading = get_object_or_404(Reading, id=reading_id)
        reading.delete()
        return redirect("readings:list")
from django.shortcuts import render, redirect
from .forms import ReadingForm
from .models import Reading
from meters_app.models import Meter
from django.db.models import F

def readings_list(request):
    # ... твой код списка показаний остается без изменений ...
    readings_qs = Reading.objects.select_related('meter').annotate(
        meter_name=F('meter__name'), unit=F('meter__unit')
    ).order_by('-reading_date', '-id')
    
    from django.core.paginator import Paginator
    paginator = Paginator(readings_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "readings_app/reading_list.html", {"page_obj": page_obj})

def delete_reading(request, reading_id):
    """Удалить конкретное показание по его ID."""
    if request.method == "POST":
        # Получаем объект или возвращаем 404, если не найден
        reading = get_object_or_404(Reading, id=reading_id)
        reading.delete()
        return redirect("readings:list")
    
    # Если запрос не POST, просто перенаправляем на список
    return redirect("readings:list")

def add_reading(request):
    if request.method == "POST":
        form = ReadingForm(request.POST)
        if form.is_valid():
            # Сохраняем объект, но пока не коммитим в БД
            reading = form.save(commit=False)
            
            # Вычисляем расход и стоимость (как было раньше)
            consumption = round(reading.current - reading.previous, 3)
            cost = round(consumption * float(reading.meter.tariff), 2)
            
            # Присваиваем вычисленные значения
            reading.consumption = consumption
            reading.cost = cost
            
            # Теперь сохраняем в базу
            reading.save()
            return redirect("readings:list")
    else:
        form = ReadingForm()

    return render(request, "readings_app/reading_add.html", {"form": form})

# delete_reading остается без изменений, там нет форм
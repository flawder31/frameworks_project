from django.shortcuts import render, redirect, get_object_or_404
from .forms import MeterForm
from .models import Meter

def meters_list(request):
    meters = Meter.objects.all()
    return render(request, "meters_app/meter_list.html", {"meters": meters})

def add_meter(request):
    if request.method == "POST":
        
        form = MeterForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect("meters:list")
    else:
        form = MeterForm()
    
    return render(request, "meters_app/meter_add.html", {"form": form})

def edit_meter(request, meter_code):
    # Получаем объект или 404
    meter = get_object_or_404(Meter, code=meter_code)
    
    if request.method == "POST":
        # ВАЖНО: передаем instance=meter, чтобы обновить, а не создать новый
        form = MeterForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect("meters:list")
    else:
        # При GET тоже передаем instance, чтобы поля заполнились текущими данными
        form = MeterForm(instance=meter)
        
    return render(request, "meters_app/meter_edit.html", {"form": form, "meter": meter})

def meter_detail(request, slug):
    """Отображение детальной информации о счетчике."""
    # Ищем по slug, так как мы перешли на красивые URL в ПР10
    meter = get_object_or_404(Meter, slug=slug)
    return render(request, "meters_app/meter_detail.html", {"meter": meter})



def delete_meter(request, meter_code):
    # ... твой код удаления остается без изменений ...
    if request.method == "POST":
        meter = get_object_or_404(Meter, code=meter_code)
        if meter.readings.exists():
            count = meter.readings.count()
            meters = Meter.objects.all()
            return render(request, "meters_app/meter_list.html", {
                "meters": meters,
                "error": f"Нельзя удалить '{meter.code}': по нему есть {count} показаний."
            })
        meter.delete()
        return redirect("meters:list")
    return redirect("meters:list")
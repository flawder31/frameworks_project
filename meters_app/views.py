from django.http import HttpResponse

from homepage.views import page
from storage import load_meters
# Нам нужно будет ее добавить в models/meters.py!
from models.meters import find_meter_by_code


def meters_list(request):
    """Страница со списком всех счетчиков."""
    meters = load_meters("data/meters.json")

    items = ""
    for meter in meters:
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <strong>{meter.name}</strong> ({meter.code}) 
                — Тариф: {meter.tariff} руб./{meter.unit}
            </div>
            <a href="/meters/{meter.code}/" class="btn btn-sm btn-outline-primary">Подробнее</a>
        </li>
        """

    content = f"""
    <h1>Справочник счетчиков</h1>
    <ul class="list-group mt-4">{items}</ul>
    """
    return HttpResponse(page("Счетчики", content))


def meter_detail(request, meter_code):
    """Страница конкретного счетчика."""
    meters = load_meters("data/meters.json")

    # Ищем счетчик по коду (EL, CW...)
    meter = None
    for m in meters:
        if m.code == meter_code:
            meter = m
            break

    if meter is None:
        content = """
        <h1 class="text-danger">Счетчик не найден</h1>
        <a href="/meters/" class="btn btn-outline-secondary">← К списку счетчиков</a>
        """
        return HttpResponse(page("Счетчик не найден", content), status=404)

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{meter.name}</h5>
            <p class="card-text"><strong>Код:</strong> {meter.code}</p>
            <p class="card-text"><strong>Единица измерения:</strong> {meter.unit}</p>
            <p class="card-text"><strong>Тариф:</strong> {meter.tariff} руб.</p>
            <a href="/meters/" class="btn btn-outline-secondary">← К списку счетчиков</a>
        </div>
    </div>
    """
    return HttpResponse(page(meter.name, content))

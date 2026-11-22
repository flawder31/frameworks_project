from .models import Meter

def meter_stats(request):
    """Возвращает общую статистику по счетчикам для всех шаблонов."""
    return {
        "total_meters": Meter.objects.count(),
        "site_name": "Сервис Счетчиков",
    }
from django.contrib import admin
from .models import Meter

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    # Столбцы в списке
    list_display = ('code', 'name', 'unit', 'tariff')
    # Поля для поиска
    search_fields = ('code', 'name')
    # Фильтры справа
    list_filter = ('unit',)
    # Сортировка по умолчанию
    ordering = ('name',)
    # Количество записей на странице
    list_per_page = 20
from django.contrib import admin
from .models import Reading

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'meter', 'reading_date', 'consumption', 'cost')
    list_filter = ('reading_date', 'meter')
    search_fields = ('meter__code', 'meter__name') # Поиск по связанным полям
    ordering = ('-reading_date',)
    date_hierarchy = 'reading_date' # Удобная навигация по датам сверху
    list_per_page = 20
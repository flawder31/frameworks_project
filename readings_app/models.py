from django.db import models
from meters_app.models import Meter
# Для GeneratedField нужны эти импорты
from django.db.models import F, Case, When, Value, BooleanField

class ReadingQuerySet(models.QuerySet):
    """Набор методов для фильтрации показаний."""
    
    def for_meter(self, meter_code):
        return self.filter(meter__code=meter_code)

    def for_date_range(self, start_date, end_date):
        return self.filter(reading_date__gte=start_date, reading_date__lte=end_date)

class ReadingManager(models.Manager.from_queryset(ReadingQuerySet)):
    pass

class Reading(models.Model):
    meter = models.ForeignKey(
        Meter, 
        on_delete=models.PROTECT, 
        related_name="readings",
        verbose_name="Счетчик"
    )
    previous = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Предыдущее показание")
    current = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Текущее показание")
    reading_date = models.DateField(verbose_name="Дата снятия")
    
    # Обычные поля, которые мы заполняем вручную
    consumption = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Расход")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    # НОВЫЙ ПОЛЕ: GeneratedField (вычисляется базой данных)
    # Оно будет автоматически пересчитываться при изменении previous или current
    consumption_db = models.GeneratedField(
        expression=F('current') - F('previous'),
        output_field=models.DecimalField(max_digits=10, decimal_places=3),
        db_persist=True, # Сохранять значение физически в таблице
        verbose_name="Расход (БД)"
    )

    objects = ReadingManager()

    class Meta:
        ordering = ["-reading_date", "-id"]
        verbose_name = "Показание"
        verbose_name_plural = "Показания"

    def __str__(self):
        return f"{self.meter.name} - {self.reading_date}"
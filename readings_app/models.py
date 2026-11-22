from django.db import models
# Импортируем модель Meter из другого приложения
from meters_app.models import Meter

class Reading(models.Model):
    meter = models.ForeignKey(
        Meter, 
        on_delete=models.PROTECT, # Защищаем счетчик от удаления, если есть показания
        related_name="readings",  # Позволит делать meter.readings.all()
        verbose_name="Счетчик"
    )
    previous = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Предыдущее показание")
    current = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Текущее показание")
    reading_date = models.DateField(verbose_name="Дата снятия")
    consumption = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Расход")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        ordering = ["-reading_date", "-id"] # Сортировка по убыванию даты
        verbose_name = "Показание"
        verbose_name_plural = "Показания"

    def __str__(self):
        return f"{self.meter.name} - {self.reading_date}"
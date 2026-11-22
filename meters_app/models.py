from django.db import models

class Meter(models.Model):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Код счетчика",
        help_text="Например: EL, CW, GAS"
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    unit = models.CharField(max_length=20, verbose_name="Единица измерения")
    tariff = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Тариф")

    class Meta:
        ordering = ["name"]
        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"

    def __str__(self):
        return f"{self.name} ({self.code})"
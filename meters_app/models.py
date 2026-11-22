from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Meter(models.Model):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        blank=False,
        verbose_name="Код счетчика",
        help_text="Например: EL, CW, GAS"
    )
    image = models.ImageField(
        upload_to="meters_photos/", 
        blank=True, 
        null=True, 
        verbose_name="Фото счетчика"
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    unit = models.CharField(max_length=20, verbose_name="Единица измерения")
    tariff = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Тариф")
    
    # Новое поле для красивого URL
    slug = models.SlugField(
        max_length=150, 

        blank=True, 
        verbose_name="URL-идентификатор"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"

    def save(self, *args, **kwargs):
        # Автоматически создаем slug, если он пуст
        if not self.slug:
            # Комбинируем название и код для уникальности
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{self.code}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Возвращает URL для страницы детального просмотра
        return reverse("meters:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} ({self.code})"
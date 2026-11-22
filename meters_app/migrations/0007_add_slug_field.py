from django.db import migrations, models
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    """Заполняем slug для существующих записей."""
    Meter = apps.get_model('meters_app', 'Meter')
    for meter in Meter.objects.all():
        if not meter.slug:
            base = slugify(meter.name) or f"meter-{meter.pk}"
            meter.slug = f"{base}-{meter.pk}"
            meter.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('meters_app', '0001_initial'), # УБЕДИСЬ, ЧТО ИМЯ ПРЕДЫДУЩЕЙ МИГРАЦИИ ВЕРНОЕ!
    ]

    operations = [
        # 1. Добавляем поле БЕЗ unique
        migrations.AddField(
            model_name='meter',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=150, verbose_name='URL-идентификатор'),
        ),
        # 2. Заполняем данные
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        # 3. Теперь делаем его уникальным (когда данные уже есть)
        migrations.AlterField(
            model_name='meter',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=150, unique=True, verbose_name='URL-идентификator'),
        ),
    ]
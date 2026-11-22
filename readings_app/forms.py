from django import forms
from .models import Reading
from meters_app.models import Meter
from datetime import date

class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        # Поля, которые пользователь может заполнять
        fields = ['meter', 'previous', 'current', 'reading_date']
        
        # Настройка виджетов для красоты и удобства
        widgets = {
            'reading_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'previous': forms.NumberInput(attrs={
                'step': '0.001', 
                'class': 'form-control'
            }),
            'current': forms.NumberInput(attrs={
                'step': '0.001', 
                'class': 'form-control'
            }),
            'meter': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'meter': 'Выберите счетчик',
            'previous': 'Предыдущее показание',
            'current': 'Текущее показание',
            'reading_date': 'Дата снятия',
        }

    def clean(self):
        """Кастомная валидация: проверяем логику показаний."""
        cleaned_data = super().clean()
        previous = cleaned_data.get("previous")
        current = cleaned_data.get("current")
        reading_date = cleaned_data.get("reading_date")

        if previous is not None and current is not None:
            if current < previous:
                self.add_error('current', "Текущее показание не может быть меньше предыдущего.")
        
        if reading_date and reading_date > date.today():
            self.add_error('reading_date', "Дата снятия не может быть в будущем.")

        return cleaned_data
from django import forms
from .models import Meter

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['code', 'name', 'unit', 'tariff', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EL, CW, GAS...'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'кВт·ч, м³...'}),
            'tariff': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'code': 'Код счетчика',
            'name': 'Название ресурса',
            'unit': 'Единица измерения',
            'tariff': 'Тариф (руб.)',
        }
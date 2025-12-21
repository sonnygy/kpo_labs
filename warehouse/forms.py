from django import forms
from warehouse.models import Device, Part

class DeviceForm(forms.ModelForm):
  class Meta:
    model = Device
    fields = ('type', 'brand', 'model')
    widgets = {
       'type': forms.Select(attrs={'class': 'form-control'}),
       'brand': forms.Select(attrs={'class': 'form-control'}),
       'model': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels = {
       'type': 'Тип устройства',
       'brand': 'Производитель',
       'model': 'Модель'
    }
class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('type', 'name', 'price', 'quantity', 'description')
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'type': 'Производитель',
            'name': 'Название',
            'price': 'Цена',
            'quantity': 'Количество',
            'description': 'Описание'
        }
       
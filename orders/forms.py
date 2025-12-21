from django import forms
from orders.models import Order, Estimate

class OrderForm(forms.ModelForm):
   class Meta:
     model = Order
     fields = ['problem_description']
     labels = {
         'problem_description': 'Описание проблемы',
     }
class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'parts', 'problem_description']
        widgets = {
            'parts': forms.SelectMultiple(attrs={
                'class': 'form-control parts-select'
            })
        }
class EstimateForm(forms.ModelForm):
   class Meta:
     model = Estimate
     fields = ['parts_cost', 'labor_cost', 'notes']
     labels = {
         'parts_cost': 'Стоимость деталей',
         'labor_cost': 'Стоимость работ',
         'notes': 'Заметки'
     }
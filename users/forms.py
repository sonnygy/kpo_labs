from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User
from warehouse.models import Device
from orders.models import Order

class UserRegisterForm(UserCreationForm):
  password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  password2 = forms.CharField(label='Подтверждение пароля',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  class Meta(UserCreationForm.Meta):
    model = User
    fields = ('username', 'email', 'password1', 'password2')
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }
    labels = {
      'username': 'Имя пользователя',
      'email': 'Email',
    }
  
class UserLoginForm(AuthenticationForm):
  class Meta:
    model = User
    fields = ('username', 'password')
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'password': forms.PasswordInput(attrs={'class': 'form-control'})
    }
    labels  = {
      'username': 'Имя пользователя',
      'password': 'Пароль'
    }

class ClientContactForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone')
    widgets = {
       'first_name': forms.TextInput(attrs={'class': 'form-control'}),
       'last_name': forms.TextInput(attrs={'class': 'form-control'}),
       'phone': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels  = {
       'first_name': 'Имя',
       'last_name': 'Фамилия',
       'phone': 'Телефон'
    }

class ClientForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone')
    widgets = {
       'first_name': forms.TextInput(attrs={'class': 'form-control'}),
       'last_name': forms.TextInput(attrs={'class': 'form-control'}),
       'phone': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels = {
       'first_name': 'Имя',
       'last_name': 'Фамилия',
       'phone': 'Телефон'
    }

class ClientOrderForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone')
    widgets = {
       'first_name': forms.TextInput(attrs={'class': 'form-control'}),
       'last_name': forms.TextInput(attrs={'class': 'form-control'}),
       'phone': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels = {
       'first_name': 'Имя',
       'last_name': 'Фамилия',
       'phone': 'Телефон'
    }

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

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ()

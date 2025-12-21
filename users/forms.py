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
  username = forms.CharField(
    label='Имя пользователя',
    widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  password = forms.CharField(
    label='Пароль',
    widget=forms.PasswordInput(attrs={'class': 'form-control'})
  )
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

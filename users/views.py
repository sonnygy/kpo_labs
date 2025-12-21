from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import User
from .forms import UserRegisterForm, UserLoginForm, ClientForm
from warehouse.forms import DeviceForm
from orders.forms import OrderForm
from django.contrib import messages

def get_client_for_user(user):
  return user
@login_required
def redirect_by_role(request):
    try:
        client = get_client_for_user(request.user)
    except User.DoesNotExist:
        return redirect('home')
    if client.role == 'admin':
        return redirect('admin_page')
    if client.role == 'master':
        return redirect('master_page')
    return redirect('orders_list')
#user
def home(request):
  return render(request, "home.html")

def user_login(request):
  if request.method == 'POST':
      form = UserLoginForm(request, data=request.POST)
      if form.is_valid():
          user = form.get_user()
          login(request, user)
          return redirect('redirect_by_role')
  else:
      form = UserLoginForm()
  return render(request, 'login.html', {'form': form})
def user_signup(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('redirect_by_role')
  else:
    form = UserRegisterForm()
  return render(request, 'sign_up.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('home')
def create_order(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            'Для оформления заявки необходимо войти или зарегистрироваться'
        )
        client_form = ClientForm()
        device_form = DeviceForm()
        order_form = OrderForm()

        return render(request, 'create_order.html', {
            'client_form': client_form,
            'device_form': device_form,
            'order_form': order_form,
        })
    client = request.user

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        device_form = DeviceForm(request.POST)
        order_form = OrderForm(request.POST)

        if client_form.is_valid() and device_form.is_valid() and order_form.is_valid():
            client_form.save()
            device = device_form.save()

            order = order_form.save(commit=False)
            order.client = client
            order.device = device
            order.save()

            return redirect('create_order_success')
    else:
        client_form = ClientForm(instance=client)
        device_form = DeviceForm()
        order_form = OrderForm()

    return render(request, 'create_order.html', {
        'client_form': client_form,
        'device_form': device_form,
        'order_form': order_form,
    })
def create_order_success(request):
  return render(request, 'create_order_success.html')

#admin
@login_required(login_url='user_login')
def master_home(request):
    client = request.user
    if client.role != 'master':
        return redirect('home')
    return render(request, "master/home.html")
#master
@login_required(login_url='user_login')
def admin_home(request):
    client = request.user
    if client.role != 'admin':
        return redirect('home')
    return render(request, "administrator/home.html")
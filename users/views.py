from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, ClientForm
from orders.views import orders_list
from django.views.generic import ListView, DetailView, CreateView, UpdateView

def get_client_for_user(user):
  return User.objects.get(user=user)
@login_required
def redirect_by_role(request):
    try:
        client = get_client_for_user(request.user)
    except User.DoesNotExist:
        return redirect('home')
    if client.user_type == 'admin':
        return redirect('admin_page')
    if client.user_type == 'master':
        return redirect('master_page')
    return redirect('orders_list')

#user
def home(request):
  return render(request, "home.html")
def user_login(request):
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('redirect_by_role')
  else:
    form = UserLoginForm()
  return render(request, 'login.html', {'form': form})
def user_signup(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('redirect_by_role')
  else:
    form = UserRegistrationForm()
  return render(request, 'sign_up.html', {'form': form})
def create_order(request):
  if not request.user.is_authenticated:
    return redirect('user_login')
  client = get_client_for_user(request.user)
  if request.method == 'POST':
    client_form = ClientForm(request.POST, instance=client)
    device_form = DeviceForm(request.POST)
    order_form = OrderForm(request.POST)
    if client_form.is_valid() and device_form.is_valid() and order_form.is_valid():
      client.first_name = client_form.cleaned_data['first_name']
      client.last_name = client_form.cleaned_data['last_name']
      client.phone = client_form.cleaned_data['phone']
      device = device_form.save()
      order = order_form.save(commit=False)
      client_form.save()
      order.client = client
      order.device = device
      order.save()
      return redirect('create_order_success')
  else:
    client_form = ClientOrderForm(initial={
    'first_name': client.first_name,
    'last_name': client.last_name,
    'phone': client.phone,
    })
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
class MasterListView(ListView):
  model = User
  template_name = 'administrator/masters.html'
  context_object_name = 'masters'
  paginate_by = 10

  def get_queryset(self):
      return User.objects.filter(user_type='master').order_by('last_name', 'first_name')
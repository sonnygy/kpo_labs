from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Part
from orders.models import Order
from django.contrib.auth.decorators import login_required
from users.models import User
from users.views import get_client_for_user
class WarehouseListView(ListView):
  model = Part
  template_name = 'administrator/warehouse.html'
  context_object_name = 'parts'
  paginate_by = 10
  ordering = ['name']

class WarehouseCreateView(CreateView):
  model = Part
  fields = ['name', 'device', 'type', 'price', 'quantity', 'description']
  template_name = "administrator/warehouse_add.html"
  success_url = reverse_lazy('warehouse_list')
  def form_valid(self, form):
      return super().form_valid(form)

class WarehouseUpdateView(UpdateView):
  model = Part
  fields = ['name', 'device', 'type', 'price', 'quantity']
  template_name = "administrator/warehouse_update.html"
  success_url = reverse_lazy('warehouse_list')
  def form_valid(self, form):
      return super().form_valid(form)
@login_required
def admin_page(request):
    try:
        user = get_client_for_user(request.user)
    except User.DoesNotExist:
        return redirect('home')

    if user.role != 'admin':
        return redirect('home')
    stats = {
        'total_orders': Order.objects.count(),
        'created_orders': Order.objects.filter(status='created').count(),
        'in_progress_orders': Order.objects.filter(status='in_progress').count(),
        'completed_orders': Order.objects.filter(status='completed').count(),
        'cancelled_orders': Order.objects.filter(status='cancelled').count(),
        'total_parts': Part.objects.count(),
        'missing_parts': Part.objects.filter(quantity=0).count(),
        'masters_count': User.objects.filter(role='master').count(),
    }
    return render(request, "administrator/home.html", {'stats': stats})
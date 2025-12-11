from django.shortcuts import render, redirect
from .models import Order
from users.views import get_client_for_user
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from users.models import User
from django.urls import reverse_lazy

def orders_list(request):
  if not request.user.is_authenticated:
      return redirect('user_login')
  client = get_client_for_user(request.user)
  orders = Order.objects.filter(client=client).select_related('device', 'client')
  return render(request, 'order_list.html', {'orders': orders})

@login_required
def master_page(request):
    try:
        client = get_client_for_user(request.user)
    except User.DoesNotExist:
        return redirect('home')

    if client.user_type != 'master':
        return redirect('home')
    recent_requests = Order.objects.all()
    context = {
        'recent_requests': recent_requests,
        'total_requests': Order.objects.count(),
        'created': Order.objects.filter(status='created').count(),
        'in_progress': Order.objects.filter(status='in_progress').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    return render(request, "master/home.html", context)
class order_assign_master_view(UpdateView):
  model = Order
  fields = ['master', 'status']
  template_name = 'administrator/order_assign.html'
  success_url = reverse_lazy('admin_requests')

  def form_valid(self, form):
      return super().form_valid(form)
class order_request_list_view(ListView):
  model = Order
  template_name = 'master/order_list.html'
  context_object_name = 'orders'
  paginate_by = 10
class order_request_detail_view(DetailView):
  model = Order
  template_name = 'master/order_detail.html'
  context_object_name = 'order'
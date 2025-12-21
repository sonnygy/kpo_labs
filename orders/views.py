from django.shortcuts import render, redirect
from orders.models import Order, Estimate
from orders.forms import OrderForm, OrderUpdateForm, EstimateForm
from users.models import User
from users.views import get_client_for_user, master_home
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse_lazy

#user
def orders_list(request):
  if not request.user.is_authenticated:
      return redirect('user_login')
  client = get_client_for_user(request.user)
  orders = Order.objects.filter(client=client).select_related('device', 'client')
  return render(request, 'order_list.html', {'orders': orders})
@login_required
#master
def master_page(request):
    master = get_client_for_user(request.user)
    if master.role != 'master':
        return redirect('home')
    orders = Order.objects.filter(master=master).order_by('-created_at')
    context = {
        'orders': orders[:5],
        'total_requests': orders.count(),
        'new_requests': orders.filter(status='created').count(),
        'in_progress': orders.filter(status='in_progress').count(),
        'completed': orders.filter(status='completed').count(),
        'cancelled': orders.filter(status='cancelled').count(),
    }

    return render(request, 'master/home.html', context)
class order_list_view(ListView):
  model = Order
  template_name = 'master/order_list.html'
  context_object_name = 'orders'
  paginate_by = 10
class order_detail_view(DetailView):
  model = Order
  template_name = 'master/order_detail.html'
  context_object_name = 'order'
class order_update_view(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'master/order_update.html'
    success_url = reverse_lazy('master_orders')

    def form_valid(self, form):
        order = form.save(commit=False)

        if order.status == Order.OrderStatus.COMPLETED:
            order.completed_at = timezone.now()

        order.save()
        form.save_m2m()

        for part in order.parts.all():
            if part.quantity <= 0:
                form.add_error(
                    'parts',
                    f'Запчасть "{part.name}" закончилась на складе'
                )
                return self.form_invalid(form)

            part.quantity -= 1
            part.save()

        return redirect(self.success_url)

class create_estimate_view(CreateView):
    model = Estimate
    template_name = 'master/estimate.html'
    fields = ['parts_cost', 'labor_cost', 'notes']
    success_url = reverse_lazy('master_orders')
    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        estimate = form.save(commit=False)
        estimate.order = order
        estimate.save()
        return super().form_valid(form)
#admin
class admin_order_list_view(ListView):
    model = Order
    template_name = 'administrator/orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = User.objects.filter(role=User.Roles.MASTER)
        return context
class order_assign_master_view(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        master_id = request.POST.get('master')

        if master_id:
            order.master = User.objects.get(pk=master_id)
            order.status = Order.OrderStatus.IN_PROGRESS
        else:
            order.master = None
            order.status = Order.OrderStatus.CREATED

        order.save()
        return redirect('admin_orders')

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import PKPart

class WarehouseListView(ListView):
  model = PKPart
  template_name = 'administrator/warehouse.html'
  context_object_name = 'parts'
  paginate_by = 10
  ordering = ['name']

class WarehouseCreateView(CreateView):
  model = PKPart
  fields = ['name', 'device', 'type', 'price', 'quantity', 'description']
  template_name = "administrator/warehouse_add.html"
  success_url = reverse_lazy('warehouse_list')
  def form_valid(self, form):
      return super().form_valid(form)

class WarehouseUpdateView(UpdateView):
  model = PKPart
  fields = ['name', 'device', 'type', 'price', 'quantity', 'description']
  template_name = "administrator/warehouse_update.html"
  success_url = reverse_lazy('warehouse_list')

  def form_valid(self, form):
      return super().form_valid(form)

from django.db import models
from users.models import User
from warehouse.models import Device, PKPart, PhonePart

class Order(models.Model):
   class OrderStatus(models.TextChoices):
      CREATED = 'created', 'Создан'
      IN_PROGRESS = 'in_progress', 'В работе'
      COMPLETED = 'completed', 'Завершен'
      CANCELLED = 'cancelled', 'Отменен'
   client = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': User.Roles.CLIENT}, verbose_name='Клиент')
   master = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Roles.MASTER}, verbose_name='Мастер', related_name='master_orders', null=True, blank=True)
   device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
   status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED, verbose_name='Статус')
   created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
   updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
   completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
   @property
   def number(self):
      return f"ORD-{self.pk:05d}"
   @property
   def master_name(self):
     return self.master.full_name if self.master else "Не назначен"
   @property
   def client_name(self):
      return self.client.full_name
   @property
   def device_name(self):
      return f"{self.device.number} —{self.device.full_name}"
   @property
   def is_completed(self):
      return self.status == self.status.COMPLETED
   @property
   def __str__(self):
      return f"{self.number} {self.device.full_name}"
   def __str__(self):
      if self.master:
          return f"Заказ {self.number} - {self.status} {self.master.full_name} {self.updated_at}"
      return f"Заказ {self.number} - {self.status} {self.created_at}"
class Estimate(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='estimates', verbose_name='Заявка')
   total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
   parts_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость деталей')
   labor_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость работ')
   notes = models.TextField(blank=True, verbose_name='Заметки по смете')
   @property
   def get_total_cost(self):
      if not self.total_cost:
         self.total_cost = (self.parts_cost or 0) + (self.labor_cost or 0)
         self.save()
      return self.total_cost
   def __str__(self):
      return f"Смета для {self.order.full_name} — {self.total_cost} руб."
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  class Roles(models.TextChoices):
    MASTER = 'master', 'Мастер'
    ADMIN = 'admin', 'Администратор'
    CLIENT = 'client', 'Клиент'
  role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENT, verbose_name='Роль')
  phone = models.CharField(max_length=15, blank=True, null=True)
  @property
  def is_master(self):
    return self.role == self.Roles.MASTER
  @property
  def is_admin(self):
    return self.role == self.Roles.ADMIN
  @property
  def is_client(self):
    return self.role == self.Roles.CLIENT
  @property
  def fill_name(self):
    if self.first_name and self.last_name:
      return f'{self.first_name} {self.last_name}'
    return self.username      
  def __str__(self):
    if self.phone:
      return f'{self.fill_name} {self.role} {self.phone}'
    return f'{self.fill_name} {self.role} {self.email}'
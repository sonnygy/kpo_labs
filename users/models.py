from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-яЁё]+$',
    message='Разрешены только буквы'
)
class User(AbstractUser):
  class Roles(models.TextChoices):
    MASTER = 'master', 'Мастер'
    ADMIN = 'admin', 'Администратор'
    CLIENT = 'client', 'Клиент'
  role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENT, verbose_name='Роль')
  phone = models.CharField(max_length=15, blank=True, null=True)
  first_name = models.CharField(max_length=50, blank=True, null=True, validators=[name_validator])
  last_name = models.CharField(max_length=50, blank=True, null=True, validators=[name_validator])
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
  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)
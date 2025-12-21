from django.db import models
from django.core.validators import RegexValidator

name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-яЁё0-9]+$',
    message='Разрешены только буквы и цифры'
)
class Device(models.Model):
  class DeviceType(models.TextChoices):
    PHONE = 'phone', 'Телефон'
    TABLET = 'tablet', 'Планшет'
    LAPTOP = 'laptop', 'Ноутбук'
    DESKTOP = 'desktop', 'ПК'
    OTHER = 'other', 'Другое'
  class DeviceBrand(models.TextChoices):
     APPLE = 'apple', 'Apple'
     SAMSUNG = 'samsung', 'Samsung'
     HUAWEI = 'huawei', 'Huawei'
     XIAOMI = 'xiaomi', 'Xiaomi'
     HONOR = 'honor', 'Honor'
     ASUS = 'asus', 'Asus'
     LENOVO = 'lenovo', 'Lenovo'
     MSI = 'msi', 'MSI'
     ACER = 'acer', 'Acer'
     DELL = 'dell', 'Dell'
     LG = 'lg', 'LG'
     HP = 'hp', 'HP'
     OTHER = 'other', 'Другое'
  type = models.CharField(max_length=20, choices=DeviceType.choices, verbose_name='Тип устройства')
  brand = models.CharField(max_length=20, choices=DeviceBrand.choices, verbose_name='Производитель')
  model = models.CharField(max_length=50, verbose_name='Модель',validators=[name_validator])
  @property
  def number(self):
      return f"DEV-{self.pk:05d}"
  @property
  def full_name(self):
      brand_display = dict(self.DeviceBrand.choices).get(self.brand, self.brand)
      return f"{brand_display} {self.model}"
  def __str__(self):
      type_display = dict(self.DeviceType.choices).get(self.type, self.type)
      return f"{type_display} {self.full_name}"
  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)
def validate_even(value):
  if value % 2 != 0:
      raise ValidationError(f'{value} не является чётным числом!')
class Part(models.Model):
  class PartType(models.TextChoices):
    SCREEN = 'screen', 'Экран'
    BATTERY = 'battery', 'Батарея'
    CAMERA = 'camera', 'Камера'
    KEYBOARD = 'keyboard', 'Клавиатура'
    PROCESSOR = 'processor', 'Процессор'
    RAM = 'ram', 'Оперативная память'
    STORAGE = 'storage', 'Накопитель'
    POWER_SUPPLY = 'power_supply', 'Блок питания'
    MOTHERBOARD = 'motherboard', 'Материнская плата'
    CASE = 'case', 'Корпус'
    GRAPHICS_CARD = 'graphics_card', 'Видеокарта'
    OTHER = 'other', 'Другое'
  type = models.CharField(max_length=20, choices=PartType.choices, verbose_name='Тип комплектующей')
  name = models.CharField(max_length=50, verbose_name='Название', validators=[name_validator])
  device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
  quantity = models.PositiveIntegerField(verbose_name='Количество')
  description = models.TextField(verbose_name='Описание')
  @property
  def number(self):
    return f"PART-{self.pk:05d}"
  @property
  def in_stock(self):
      return self.quantity > 0
  @property
  def stock_status(self):
      return "В наличии" if self.in_stock else "Нет в наличии"
  @property
  def full_name(self):
    return f"{self.name} {self.device.full_name}"
  def __str__(self):
    return f"{self.full_name} - {self.price} руб. (остаток: {self.quantity})"
  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)
from django.db import models

class Device(models.Model):
  class DeviceType(models.TextChoices):
    PHONE = 'phone', 'Телефон'
    TABLET = 'tablet', 'Планшет'
    LAPTOP = 'laptop', 'Ноутбук'
    DESKTOP = 'desktop', 'ПК'
  class DeviceBrand(models.TextChoices):
     APPLE = 'apple', 'Apple'
     SAMSUNG = 'samsung', 'Samsung'
     HUAWEI = 'huawei', 'Huawei'
     XIAOMI = 'xiaomi', 'Xiaomi'
     OTHER = 'other', 'Другое'
  type = models.CharField(max_length=20, choices=DeviceType.choices, verbose_name='Тип устройства')
  brand = models.CharField(max_length=20, choices=DeviceBrand.choices, verbose_name='Производитель')
  model = models.CharField(max_length=50, verbose_name='Модель')
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

class Part(models.Model):
  name = models.CharField(max_length=50, verbose_name='Название')
  device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
  quantity = models.PositiveIntegerField(verbose_name='Количество')
  description = models.TextField(verbose_name='Описание')
  class Meta:
    abstract = True
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

class PKPart(Part):
  class PartType(models.TextChoices):
    PROCESSOR = 'processor', 'Процессор'
    RAM = 'ram', 'Оперативная память'
    STORAGE = 'storage', 'Накопитель'
    POWER_SUPPLY = 'power_supply', 'Блок питания'
    MOTHERBOARD = 'motherboard', 'Материнская плата'
    CASE = 'case', 'Корпус'
    GRAPHICS_CARD = 'graphics_card', 'Видеокарта'
    OTHER = 'other', 'Другое'
  type = models.CharField(max_length=20, choices=PartType.choices, verbose_name='Тип комплектующей')
  def __str__(self):
    type_display = dict(self.PartType.choices).get(self.type, self.type)
    return f"{type_display}: {super().__str__()}"
class PhonePart(Part):
  class PartType(models.TextChoices):
     SCREEN = 'screen', 'Экран'
     BATTERY = 'battery', 'Батарея'
     CAMERA = 'camera', 'Камера'
     KEYBOARD = 'keyboard', 'Клавиатура'
     OTHER = 'other', 'Другое'
  type = models.CharField(max_length=20, choices=PartType.choices, verbose_name='Тип комплектующей')
  def __str__(self):
    type_display = dict(self.PartType.choices).get(self.type, self.type)
    return f"{type_display}: {super().__str__()}"
     
    
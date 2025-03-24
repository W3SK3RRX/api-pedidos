from django.db import models
from users.models import User
from django.utils.text import slugify
import uuid

class CategoryRestaurant(models.Model):
    """Model para armazenar tipos de restaurantes (ex: Pizzaria, Hamburgueria, Sushi, etc.)"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CategoryMenuItem(models.Model):
    """Model para armazenar categorias dos itens do menu (ex: Prato Principal, Bebidas, Sobremesas)"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    """Model para armazenar endereços"""
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.neighborhood}, {self.city} - {self.cep}"


class Restaurant(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('ativo', 'Ativo'),
        ('rejeitado', 'Rejeitado'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")
    category = models.ForeignKey(CategoryRestaurant, on_delete=models.SET_NULL, null=True, blank=True, related_name="restaurants")  # 🔹 Tipo do restaurante
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name="restaurant")
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="restaurant_images/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Gera um slug único para cada restaurante baseado no nome"""
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    

class OperatingHours(models.Model):
    """Model para armazenar horários de funcionamento dos restaurantes"""

    DIAS_DA_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="operating_hours"
    )
    
    day_of_week = models.CharField(max_length=10, choices=DIAS_DA_SEMANA)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        ordering = ["day_of_week", "open_time"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_of_week_display()} ({self.open_time} às {self.close_time})"


class MenuItem(models.Model):
    """Model para armazenar os itens do menu"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    category = models.ForeignKey(CategoryMenuItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="menu_items")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_images/", null=True, blank=True)  # 🔹 Adicionando o campo opcional para imagens

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

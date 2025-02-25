from django.db import models
from users.models import User


class Restaurant(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('ativo', 'Ativo'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")
    address = models.TextField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

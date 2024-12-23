from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    image = models.ImageField(upload_to='car_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rented {self.car.brand} {self.car.model}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

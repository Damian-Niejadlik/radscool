from django.contrib import admin
from .models import User, Car, Rental

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'balance')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'fuel_type', 'price', 'is_available')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rented_at')

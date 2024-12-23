from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Car

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'fuel_type', 'image', 'price']

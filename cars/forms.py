from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from datetime import timedelta
from .models import User, Car


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Adres e-mail',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło',
        }


class CarForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        initial=lambda: now() + timedelta(hours=24),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Termin zwrotu"
    )

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'fuel_type', 'image', 'price', 'due_date']
        labels = {
            'brand': 'Marka',
            'model': 'Model',
            'year': 'Rok produkcji',
            'fuel_type': 'Rodzaj paliwa',
            'image': 'Zdjęcie samochodu',
            'price': 'Cena za wypożyczenie',
            'due_date': 'Termin zwrotu',
        }
        error_messages = {
            'brand': {
                'required': 'To pole jest wymagane.',
                'max_length': 'Marka nie może być dłuższa niż 100 znaków.',
            },
            'model': {
                'required': 'To pole jest wymagane.',
                'max_length': 'Model nie może być dłuższy niż 100 znaków.',
            },
            'price': {
                'invalid': 'Podaj prawidłową kwotę.',
            },
            'year': {
                'invalid': 'Podaj prawidłowy rok.',
            },
        }

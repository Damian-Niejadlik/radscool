from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from decimal import Decimal
from .forms import CustomUserCreationForm, CarForm
from .models import User, Car, Rental
from django.utils.timezone import now

@login_required
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'cars/car_list.html', {'cars': cars})

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    if request.user.balance >= car.price:
        car.is_available = False
        car.save()
        Rental.objects.create(user=request.user, car=car)
        request.user.balance -= car.price
        request.user.save()
        messages.success(request, f'You rented {car.brand} {car.model} successfully!')
    else:
        messages.error(request, 'Insufficient balance to rent this car.')
    return redirect('car_list')

@login_required
def add_balance(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', 0))
            if amount > 0:
                request.user.balance += amount
                request.user.save()
                messages.success(request, f'Added {amount} zł to your balance.')
            else:
                messages.error(request, 'Please enter a valid amount.')
        except (ValueError, Decimal.InvalidOperation):
            messages.error(request, 'Invalid amount entered.')
        return redirect('add_balance')
    return render(request, 'cars/add_balance.html')

@staff_member_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            due_date = form.cleaned_data['due_date']
            Rental.objects.create(car=car, due_date=due_date, user=request.user)  # Opcjonalnie
            messages.success(request, 'Ogłoszenie zostało dodane.')
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@staff_member_required
def view_rentals(request):
    rentals = Rental.objects.select_related('car', 'user')
    return render(request, 'cars/view_rentals.html', {'rentals': rentals})

@staff_member_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, f"Car {car.brand} {car.model} has been deleted.")
    return redirect('car_list')

@staff_member_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, f"{car.brand} {car.model} has been updated.")
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/edit_car.html', {'form': form})

def return_expired_rentals():
    expired_rentals = Rental.objects.filter(due_date__lt=now())
    for rental in expired_rentals:
        rental.car.is_available = True
        rental.car.save()
        rental.delete()

@login_required
def my_rentals(request):
    return_expired_rentals()
    rentals = Rental.objects.filter(user=request.user)
    current_time = now()
    return render(request, 'cars/my_rentals.html', {'rentals': rentals, 'current_time': current_time})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

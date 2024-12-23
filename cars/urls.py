from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
    path('add_balance/', views.add_balance, name='add_balance'),
    path('add_car/', views.add_car, name='add_car'),
    path('view_rentals/', views.view_rentals, name='view_rentals'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

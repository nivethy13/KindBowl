from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donation_list, name='list'),
    path('create/', views.create_donation, name='create'),
    path('<int:pk>/', views.donation_detail, name='detail'),
    path('<int:pk>/accept/', views.accept_donation, name='accept'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('ngo-donations/', views.ngo_donations, name='ngo_donations'),
]

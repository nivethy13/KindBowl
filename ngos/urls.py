from django.urls import path
from . import views

app_name = 'ngos'

urlpatterns = [
    path('', views.ngo_list, name='list'),
    path('profile/', views.ngo_profile, name='profile'),
    path('<int:pk>/', views.ngo_detail, name='detail'),
]

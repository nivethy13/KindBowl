from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_read'),
    path('clear-all/', views.clear_all_notifications, name='clear_all'),
]

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('manager/', views.manager_dashboard, name='manager'),
    path('cashier/', views.cashier_dashboard, name='cashier'),
    path('waiter/', views.waiter_dashboard, name='waiter'),
]

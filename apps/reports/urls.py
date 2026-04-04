from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.sales_report, name='sales_report'), # Default to sales
    path('sales/', views.sales_report, name='sales_report'),
    path('cashier/', views.cashier_report, name='cashier_report'),
    path('pending/', views.pending_report, name='pending_report'),
    path('cancelled/', views.cancelled_report, name='cancelled_report'),
    path('top-items/', views.top_items_report, name='top_items_report'),
    path('waiter-perf/', views.waiter_perf_report, name='waiter_perf_report'),
]

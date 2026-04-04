from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('new/', views.pos_terminal, name='order_create'), # Map original 'new' to new POS
    path('pos/', views.pos_terminal, name='pos_terminal'),
    path('submit-ajax/', views.submit_order_ajax, name='submit_order_ajax'),
    path('reports/', views.report_dashboard, name='reports'),
    path('print/<int:pk>/', views.print_receipt, name='print_receipt'),
]

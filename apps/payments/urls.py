from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('unpaid/', views.unpaid_orders, name='unpaid_orders'),
    path('confirm/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]

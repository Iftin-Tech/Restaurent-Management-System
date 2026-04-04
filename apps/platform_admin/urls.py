from django.urls import path
from . import views

app_name = 'platform_admin'

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('new/', views.restaurant_create, name='restaurant_create'),
    path('<int:pk>/edit/', views.restaurant_update, name='restaurant_update'),
    path('<int:pk>/toggle/', views.restaurant_toggle, name='restaurant_toggle'),
]

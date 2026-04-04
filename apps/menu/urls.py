from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('categories/', views.category_list, name='category_list'),
    path('category/add/', views.category_create, name='category_create'),
    path('item/add/', views.item_create, name='item_create'),
]

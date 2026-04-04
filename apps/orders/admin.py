from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'waiter', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['receipt_number']
    inlines = [OrderItemInline]
    readonly_fields = ['receipt_number', 'total_amount']

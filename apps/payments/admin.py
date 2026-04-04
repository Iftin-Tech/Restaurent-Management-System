from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'cashier', 'method', 'amount_paid', 'confirmed_at']
    list_filter = ['method', 'confirmed_at']
    search_fields = ['order__receipt_number']

from django.db import models
from django.conf import settings
from apps.orders.models import Order

class Payment(models.Model):
    METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('edahab', 'eDahab'),
        ('zaad', 'Zaad'),
        ('card', 'Card'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='confirmed_payments', on_delete=models.SET_NULL, null=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.receipt_number}"

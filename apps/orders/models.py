from django.db import models
from django.conf import settings
from apps.menu.models import MenuItem

class Order(models.Model):
    STATUS_CHOICES = (
        ('BILLED', 'Billed'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    receipt_number = models.CharField(max_length=50, unique=True, editable=False)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.SET_NULL, null=True)
    table_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BILLED')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            import uuid
            # Format: RCT-XXXXXX
            self.receipt_number = "RCT-" + str(uuid.uuid4().hex)[:6].upper()
        super().save(*args, **kwargs)

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"{self.receipt_number} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name if self.menu_item else 'Unknown'}"

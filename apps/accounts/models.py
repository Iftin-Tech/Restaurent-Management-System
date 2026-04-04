from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Expanded profile for restaurant personnel
    full_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.full_name or 'Unassigned'})"

class Role(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('waiter', 'Waiter'),
        ('cashier', 'Cashier'),
    )
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class UserRole(models.Model):
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')
        verbose_name_plural = 'User Roles'

from django.db import models

class Restaurant(models.Model):
    # Core Routing Fields
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=50, unique=True, help_text="Used for routing e.g., 'subdomain.saas.com'")
    
    # White-Label Customization
    primary_color = models.CharField(max_length=7, default='#2563eb', help_text="Hex code for primary brand color")
    secondary_color = models.CharField(max_length=7, default='#f59e0b', help_text="Hex code for secondary brand color")
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    
    # DB Isolation Details
    db_name = models.CharField(max_length=50, unique=True)
    db_user = models.CharField(max_length=100)
    db_password = models.CharField(max_length=255)
    db_host = models.CharField(max_length=100, default='localhost')
    db_port = models.IntegerField(default=5432)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'platform_restaurant'

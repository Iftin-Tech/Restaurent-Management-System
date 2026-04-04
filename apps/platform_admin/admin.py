from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subdomain',
        'db_name',
        'db_host',
        'db_port',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'subdomain', 'db_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    class Media:
        js = ('admin/js/restaurant_admin.js',)

    fieldsets = (
        ('Restaurant Identity', {
            'fields': ('name', 'subdomain', 'is_active')
        }),
        ('Branding', {
            'fields': ('logo', 'primary_color', 'secondary_color')
        }),
        ('Database Connection', {
            'fields': ('db_name', 'db_user', 'db_password', 'db_host', 'db_port')
        }),
        ('Audit', {
            'fields': ('created_at',)
        }),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.update({
            'db_user': 'postgres',
            'db_password': '2182821Gooni!',
            'db_host': 'localhost',
            'db_port': 5432,
            'db_name': 'tenant_restaurant_db',
        })
        return initial

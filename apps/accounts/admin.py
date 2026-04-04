from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, UserRole


class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [UserRoleInline]
    list_display = (
        'username',
        'full_name',
        'email',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('username', 'full_name', 'email', 'phone_number')

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('full_name', 'phone_number')}),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__full_name', 'role__name')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)

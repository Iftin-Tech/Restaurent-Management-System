from django.core.management.base import BaseCommand
from django.core.management import call_command
from apps.platform_admin.models import Restaurant
from django.conf import settings

class Command(BaseCommand):
    help = 'Run migrations for all tenant databases'

    def handle(self, *args, **kwargs):
        restaurants = Restaurant.objects.using('default').filter(is_active=True)
        for restaurant in restaurants:
            self.stdout.write(f"Migrating tenant: {restaurant.name} (DB: {restaurant.db_name})")
            
            # Dynamically add to DATABASES setting
            if restaurant.db_name not in settings.DATABASES:
                settings.DATABASES[restaurant.db_name] = {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': restaurant.db_name,
                    'USER': restaurant.db_user,
                    'PASSWORD': restaurant.db_password,
                    'HOST': restaurant.db_host,
                    'PORT': restaurant.db_port,
                }
            
            try:
                call_command('migrate', database=restaurant.db_name)
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {restaurant.name}!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error migrating {restaurant.name}: {e}"))
            
        self.stdout.write(self.style.SUCCESS("All tenants processed!"))

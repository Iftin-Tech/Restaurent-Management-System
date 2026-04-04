import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
from django.db import connections

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.platform_admin.models import Restaurant

def migrate_all_tenants():
    print("--- Starting Multi-Tenant Schema Sync ---")
    
    # 1. Fetch all active tenants from default platform DB
    tenants = Restaurant.objects.using('default').filter(is_active=True)
    
    if not tenants.exists():
        print("No active tenants found to migrate.")
        return

    for tenant in tenants:
        db_name = tenant.db_name
        print(f"\n[Tenant: {tenant.name}]")
        print(f"Targeting Database: {db_name}...")
        
        # 2. Dynamically register tenant DB config in Django context
        db_config = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': tenant.db_user,
            'PASSWORD': tenant.db_password,
            'HOST': tenant.db_host,
            'PORT': tenant.db_port,
        }
        
        # Inject into settings and connection registry
        settings.DATABASES[db_name] = db_config
        connections.databases[db_name] = db_config
        
        try:
            # 3. Execute Migration
            call_command('migrate', database=db_name, interactive=False)
            print(f"✅ Schema synced successfully for {tenant.name}")
        except Exception as e:
            print(f"❌ Failed to migrate {tenant.name}: {str(e)}")

    print("\n--- Multi-Tenant Schema Sync Complete ---")

if __name__ == "__main__":
    migrate_all_tenants()

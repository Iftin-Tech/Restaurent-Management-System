import os
import sys
import django
from django.conf import settings
from django.db import connections

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.accounts.models import Role
from apps.platform_admin.models import Restaurant

def seed_database(db_alias):
    print(f"Ensuring roles exist in '{db_alias}'...")
    roles = ['manager', 'waiter', 'cashier']
    for role_name in roles:
        obj, created = Role.objects.using(db_alias).get_or_create(name=role_name)
        if created:
            print(f"  + Added role: {role_name}")
        else:
            print(f"  . {role_name} exists")

def seed_all():
    # 1. Default DB
    seed_database('default')
    
    # 2. Tenants
    tenants = Restaurant.objects.using('default').filter(is_active=True)
    for tenant in tenants:
        db_name = tenant.db_name
        
        # Inject FULL config
        db_config = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': 'postgres',
            'PASSWORD': '2182821Gooni!',
            'HOST': 'localhost',
            'PORT': '5432',
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
            'CONN_MAX_AGE': 0,
            'CONN_HEALTH_CHECKS': False,
            'TIME_ZONE': None,
            'OPTIONS': {},
            'TEST': {},
        }
        settings.DATABASES[db_name] = db_config
        connections.databases[db_name] = db_config
        
        try:
            seed_database(db_name)
        except Exception as e:
            print(f"  ❌ Seed failed for {db_name}: {str(e)}")

if __name__ == "__main__":
    seed_all()

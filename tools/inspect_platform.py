import os
import sys
import django
from django.conf import settings

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.platform_admin.models import Restaurant

def inspect_platform():
    tenants = Restaurant.objects.using('default').all()
    print(f"Found {len(tenants)} total tenants.")
    for t in tenants:
        print(f"Name: {t.name} | Subdomain: {t.subdomain} | DB: {t.db_name} | Active: {t.is_active}")

if __name__ == "__main__":
    inspect_platform()

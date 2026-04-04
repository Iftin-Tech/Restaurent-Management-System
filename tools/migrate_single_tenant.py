import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
from django.db import connections

# Get DB name from argument
if len(sys.argv) < 2:
    print("Please provide a database name.")
    sys.exit(1)

db_name = sys.argv[1]

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

# Define Full Standard Config
tenant_config = {
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

# 🚨 CRITICAL: Force dynamic registration in memory
settings.DATABASES[db_name] = tenant_config
connections.databases[db_name] = tenant_config

try:
    print(f"Propagating schema to {db_name} context...")
    # Explicitly run accounts migration if that's what failed
    call_command('migrate', 'accounts', database=db_name, interactive=False)
    # Then run the rest
    call_command('migrate', database=db_name, interactive=False)
    print(f"🚀 Success! {db_name} schema is now at the platform standard.")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"🚨 Migration Failed: {str(e)}")

from django.http import Http404
from django.conf import settings
from .models import Restaurant
from django.db import connections
from apps.core.tenant import set_current_tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]
        
        # 'admin' subdomain logic or localhost logic
        if subdomain in ['admin', 'localhost', '127']:
            set_current_tenant(None)
            response = self.get_response(request)
            return response

        try:
            # Query default platform DB
            restaurant = Restaurant.objects.using('default').get(subdomain=subdomain, is_active=True)
        except Restaurant.DoesNotExist:
            raise Http404("Restaurant not found or inactive.")
        
        # Register the dynamic db connection globally for this thread
        db_config = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': restaurant.db_name,
            'USER': restaurant.db_user,
            'PASSWORD': restaurant.db_password,
            'HOST': restaurant.db_host,
            'PORT': restaurant.db_port,
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
            'CONN_MAX_AGE': 0,
            'CONN_HEALTH_CHECKS': False,
            'TIME_ZONE': None,
            'OPTIONS': {},
            'TEST': {},
        }
        
        # 🚨 CRITICAL: Force settings and connection handler to see the database
        settings.DATABASES[restaurant.db_name] = db_config
        if restaurant.db_name not in connections.databases:
             connections.databases[restaurant.db_name] = db_config
        
        set_current_tenant(restaurant.db_name)
        request.tenant = restaurant
        
        response = self.get_response(request)
        return response

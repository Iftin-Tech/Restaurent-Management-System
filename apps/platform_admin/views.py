import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.conf import settings
from django.core.management import call_command
from .models import Restaurant
from .forms import RestaurantForm
from apps.accounts.models import User, Role, UserRole

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superadmin)
def restaurant_list(request):
    restaurants = Restaurant.objects.using('default').all().order_by('-created_at')
    return render(request, 'platform_admin/restaurant_list.html', {'restaurants': restaurants})

@user_passes_test(is_superadmin)
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            rest = form.save(commit=False)
            
            # Step 1: Generate internal DB identifiers automatically
            db_name = f"tenant_{rest.subdomain}_db"
            rest.db_name = db_name
            rest.db_user = 'postgres'
            rest.db_password = '2182821Gooni!'
            rest.db_host = 'localhost'
            rest.db_port = '5432'
            
            try:
                # Step 2: Auto-Create PostgreSQL Database
                conn = psycopg2.connect(
                    dbname='postgres', user='postgres',
                    password='2182821Gooni!', host='localhost', port='5432'
                )
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = conn.cursor()
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                cursor.close()
                conn.close()

                # Save client profile to central platform
                rest.save(using='default')

                # Step 3: Fast-Register new DB into Django memory and Migrate
                db_config = {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': db_name, 'USER': rest.db_user, 'PASSWORD': rest.db_password,
                    'HOST': rest.db_host, 'PORT': rest.db_port,
                    'ATOMIC_REQUESTS': False,
                    'AUTOCOMMIT': True,
                    'CONN_MAX_AGE': 0,
                    'CONN_HEALTH_CHECKS': False,
                    'TIME_ZONE': None,
                    'OPTIONS': {},
                    'TEST': {},
                }
                settings.DATABASES[db_name] = db_config
                from django.db import connections
                connections.databases[db_name] = db_config
                
                print(f"Applying schema migrations to {db_name}...")
                call_command('migrate', database=db_name, interactive=False)

                # Step 4: Provision Manager User Account directly into Tenant DB
                mgr_uname = form.cleaned_data['manager_username']
                mgr_pass = form.cleaned_data['manager_password']
                
                # Fetch/Create the 'manager' role in the new DB context
                manager_role, _ = Role.objects.using(db_name).get_or_create(name='manager')
                # Create the Manager User
                new_manager = User.objects.db_manager(db_name).create_user(
                    username=mgr_uname, password=mgr_pass, is_staff=True
                )
                # Attach UserRole mapping
                UserRole.objects.using(db_name).create(user=new_manager, role=manager_role)

                messages.success(request, f"🚀 Success! Client '{rest.name}' is fully deployed on {rest.subdomain}.localhost:8000")
                return redirect('platform_admin:restaurant_list')

            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f"Deployment Automation Failed: {str(e)}")
    else:
        form = RestaurantForm(initial={'primary_color': '#2563eb', 'secondary_color': '#f59e0b'})
        
    return render(request, 'platform_admin/restaurant_form.html', {'form': form, 'title': 'Deploy Custom White-Label Restaurant'})

@user_passes_test(is_superadmin)
def restaurant_update(request, pk):
    restaurant = get_object_or_404(Restaurant.objects.using('default'), pk=pk)
    if request.method == 'POST':
        # Don't require manager provisioning fields when just editing client colors
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if 'manager_username' in form.fields: del form.fields['manager_username']
        if 'manager_password' in form.fields: del form.fields['manager_password']
        
        # We manually process POST since we mutated form conditionally
        # It's cleaner to instantiate correctly directly based on request type
        pass
        
    # Standard Update
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        # Hack to skip required fields on edit
        form.fields['manager_username'].required = False
        form.fields['manager_password'].required = False
        
        if form.is_valid():
            rest = form.save(commit=False)
            rest.save(using='default')
            messages.success(request, f"Branding for '{rest.name}' updated successfully.")
            return redirect('platform_admin:restaurant_list')
    else:
        form = RestaurantForm(instance=restaurant)
        form.fields['manager_username'].required = False
        form.fields['manager_password'].required = False
        
    return render(request, 'platform_admin/restaurant_form.html', {'form': form, 'title': 'Edit Tenant Branding', 'restaurant': restaurant})

@user_passes_test(is_superadmin)
def restaurant_toggle(request, pk):
    restaurant = get_object_or_404(Restaurant.objects.using('default'), pk=pk)
    if request.method == 'POST':
        restaurant.is_active = not restaurant.is_active
        restaurant.save(using='default')
        status = "activated" if restaurant.is_active else "suspended"
        messages.success(request, f"Tenant '{restaurant.name}' has been {status}.")
    return redirect('platform_admin:restaurant_list')

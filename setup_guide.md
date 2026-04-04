# 🚀 Restaurant SaaS - System Setup Guide

## 1. Prerequisites Setup
You need PostgreSQL installed and running locally.

1. Create the central platform database:
```sql
CREATE DATABASE Restaurant_platform_db;
```

2. Open `config/settings/base.py` and modify the `DATABASES['default']` password if your local Postgres uses a specific password.

## 2. Initialize Central Platform
Run the migrations for the central platform:
```bash
python manage.py makemigrations accounts platform_admin menu orders payments core
python manage.py migrate --database=default
```

*Note: You will migrate tenant databases dynamically later, this step creates the platform and shared tables.*

## 3. Creating the Super Admin (SaaS Owner)
```bash
python manage.py createsuperuser
```
(Login details for the platform dashboard).

## 4. How to Create the First Restaurant
1. Before anything, create a blank new PostgreSQL database for your first restaurant:
```sql
CREATE DATABASE tenant_restaurant1;
```

2. Run the server:
```bash
python manage.py runserver
```

3. Go to `http://localhost:8000/superadmin/`
4. Login globally using your Super Admin.
5. In the `Platform_Admin > Restaurants` admin panel, create a new Restaurant record:
   - **Name**: My First Restaurant
   - **Subdomain**: myresto
   - **Db Name**: tenant_restaurant1
   - **Db User**: postgres
   - **Db Password**: [your password]
   - *Active*: Checked

## 5. Migrate Tenant Database
Now that the platform knows about the restaurant, trigger migrations on the individual restaurant:
```bash
python manage.py migrate_tenants
```
*This command natively looks up all registered restaurants and builds the schema directly into their `tenant_restaurant1` database.*

## 6. Accessing the Restaurant
You're fully operational!

Because we use subdomains for multi-tenant awareness (`myresto.localhost:8000`), you will need to:
1. Access the app locally by utilizing: `http://myresto.localhost:8000/`
2. Create user roles via super-admin dashboard mapped inside the tenant DB, or login and start configuring Menu items!

## Important Notes:
- To access local subdomains on Windows smoothly, you might want to add `127.0.0.1 myresto.localhost` inside your `C:\Windows\System32\drivers\etc\hosts` file.
- The Middleware reads the `subdomain` string ("myresto"), queries `platform_db`, finds credentials for `tenant_restaurant1`, and forcefully redirects the active Thread request to that DB.

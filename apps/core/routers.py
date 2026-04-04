from .tenant import get_current_tenant

class TenantDatabaseRouter:
    """
    Routes platform_admin strictly to 'default'.
    Everything else routes to the current tenant DB if set, 
    otherwise falls back to 'default' (e.g. for superadmin login).
    """
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'platform_admin':
            return 'default'
        return get_current_tenant() or 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'platform_admin':
            return 'default'
        return get_current_tenant() or 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Platform_admin app is ONLY ever migrated to the central platform_db
        if app_label == 'platform_admin':
            return db == 'default'
        
        # All other apps can be migrated to both (platform needs them for superadmin, 
        # tenants need them for their own data)
        return True

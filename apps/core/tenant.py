import threading

_thread_local = threading.local()

def set_current_tenant(db_name):
    _thread_local.tenant_db_name = db_name

def get_current_tenant():
    return getattr(_thread_local, 'tenant_db_name', None)

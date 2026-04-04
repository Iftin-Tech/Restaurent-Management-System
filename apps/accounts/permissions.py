from functools import wraps
from django.core.exceptions import PermissionDenied

def has_permission(user, permission):
    """
    Evaluates if the given user has the requested permission
    based on their assigned roles.
    """
    if user.is_superuser:
        return True
        
    roles = user.roles.values_list('role__name', flat=True)
    
    # Manager has full access
    if 'manager' in roles:
        return True
        
    # Waiter permissions
    if permission in ['create_order', 'print_receipt']:
        return 'waiter' in roles
        
    # Cashier permissions
    if permission == 'confirm_payment':
        return 'cashier' in roles
        
    # Shared permissions (e.g. view personal orders vs view all orders)
    if permission == 'view_orders':
        return 'waiter' in roles or 'cashier' in roles
        
    # Read-only or specific reports
    if permission == 'view_reports':
        # Example: perhaps cashier can see shift report, but mostly manager
        return False 
        
    return False

def requires_permission(permission):
    """
    Decorator for views that checks whether a user has a specific permission.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
                
            if has_permission(request.user, permission):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this module.")
        return _wrapped_view
    return decorator

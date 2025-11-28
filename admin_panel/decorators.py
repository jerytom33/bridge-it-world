from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import RoleUser

def is_admin_user(user):
    """Check if user is an admin user"""
    if not user.is_authenticated:
        return False
    
    try:
        role_user = RoleUser.objects.get(user=user)
        return role_user.role == 'admin' and user.is_staff
    except RoleUser.DoesNotExist:
        return False

def admin_required(view_func):
    """Decorator to require admin access for views"""
    decorated_view_func = user_passes_test(
        is_admin_user,
        login_url='/accounts/login/',
        redirect_field_name='next'
    )(view_func)
    
    # Also apply login_required to ensure user is authenticated
    return login_required(decorated_view_func)
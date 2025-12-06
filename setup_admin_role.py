import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from admin_panel.models import RoleUser

# Get the admin user
try:
    admin_user = User.objects.get(username='admin')
    
    # Create or update RoleUser for admin
    role_user, created = RoleUser.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'admin',
            'is_approved': True,
            'is_blocked': False
        }
    )
    
    if not created:
        # Update existing role user
        role_user.role = 'admin'
        role_user.is_approved = True
        role_user.is_blocked = False
        role_user.save()
        print('✓ Admin role updated for user "admin"')
    else:
        print('✓ Admin role created for user "admin"')
    
    # Ensure user is staff
    if not admin_user.is_staff:
        admin_user.is_staff = True
        admin_user.save()
        print('✓ User marked as staff')
    
    print('\n✅ Admin user is now fully configured!')
    print('  Username: admin')
    print('  Password: admin123')
    print('  Role: Admin')
    print('  Status: Approved')
    print('\nYou can now login at: http://127.0.0.1:8000/accounts/login/')
    
except User.DoesNotExist:
    print('❌ Admin user not found. Please run create_admin.py first.')

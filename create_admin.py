import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bridgeit.com', 'admin123')
    print('✓ Superuser created successfully!')
    print('  Username: admin')
    print('  Password: admin123')
    print('\nYou can now login at: http://127.0.0.1:8000/accounts/login/')
else:
    print('ℹ Superuser "admin" already exists')

from django.contrib.auth.models import User

# Check if test user exists
try:
    user = User.objects.get(username='rahul123')
    print(f"Test user exists: {user.username}")
    print(f"Email: {user.email}")
    print("Login credentials:")
    print("  Username: rahul123")
    print("  Password: 123456")
except User.DoesNotExist:
    print("Test user does not exist")
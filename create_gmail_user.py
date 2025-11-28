from django.contrib.auth.models import User

# Create a test user with Gmail
username = 'testuser'
email = 'testuser@gmail.com'
password = 'testpass123'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists")
    user = User.objects.get(username=username)
else:
    # Create the user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"Created user '{username}' with email '{email}' and password '{password}'")

print("\nLogin credentials:")
print(f"Username: {username}")
print(f"Email: {email}")
print(f"Password: {password}")
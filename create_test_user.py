from django.contrib.auth.models import User

# Create the test user
user = User.objects.create_user(
    username='rahul123',
    email='rahul@gmail.com',
    password='123456'
)
user.save()

print(f"User {user.username} created successfully!")
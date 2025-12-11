import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def setup_user():
    username = 'rahul@gmail.com' # LoginAPI uses email as username
    email = 'rahul@gmail.com'
    password = '123456'
    
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists.")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print("Password reset to 123456")
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"User {username} created.")
    
    # Generate token to verify it works
    refresh = RefreshToken.for_user(user)
    print(f"Access Token: {str(refresh.access_token)}")

if __name__ == "__main__":
    setup_user()

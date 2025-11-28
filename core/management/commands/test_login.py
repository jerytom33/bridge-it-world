from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class Command(BaseCommand):
    help = 'Test user login'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username')
        parser.add_argument('--password', type=str, help='Password')

    def handle(self, *args, **options):
        username = options['username'] or 'testuser'
        password = options['password'] or 'testpass123'
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully authenticated user: {username}')
            )
            self.stdout.write(f'Token: {str(refresh.access_token)}')
            self.stdout.write(f'User ID: {user.id}')
        else:
            self.stdout.write(
                self.style.ERROR('Invalid credentials')
            )
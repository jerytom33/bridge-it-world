from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a test user with Gmail'

    def handle(self, *args, **options):
        # User details
        username = 'testuser'
        email = 'testuser@gmail.com'
        password = 'testpass123'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists')
            )
            user = User.objects.get(username=username)
        else:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created user "{username}" with email "{email}" and password "{password}"')
            )

        self.stdout.write('\nLogin credentials:')
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: {password}')
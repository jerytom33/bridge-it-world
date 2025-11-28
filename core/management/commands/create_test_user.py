from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a test student user'

    def handle(self, *args, **options):
        # Check if user already exists
        if User.objects.filter(username='rahul123').exists():
            self.stdout.write(
                self.style.WARNING('Test user "rahul123" already exists')
            )
            return

        # Create the test user
        user = User.objects.create_user(
            username='rahul123',
            email='rahul@gmail.com',
            password='123456'
        )
        user.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully created test user "rahul123" with password "123456"')
        )
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bridge_core.models import UserProfile
from company.models import CompanyProfile

class Command(BaseCommand):
    help = 'Create a company user for testing'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='companyuser', help='Company username')
        parser.add_argument('--email', type=str, default='company@example.com', help='Company email')
        parser.add_argument('--password', type=str, default='companypass123', help='Company password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
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
        
        # Check if user profile already exists
        if UserProfile.objects.filter(user=user).exists():
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role != 'company':
                user_profile.role = 'company'
                user_profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated user profile role to "company"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User profile already exists with company role')
                )
        else:
            # Create user profile
            user_profile = UserProfile.objects.create(
                user=user,
                role='company',
                is_approved=True  # Auto-approve for testing
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created user profile with company role (auto-approved)')
            )
        
        # Check if company profile already exists
        if CompanyProfile.objects.filter(user=user).exists():
            self.stdout.write(
                self.style.WARNING(f'Company profile already exists')
            )
        else:
            # Create company profile
            company_profile = CompanyProfile.objects.create(
                user=user,
                company_name=f'{username} Corp',
                description=f'Test company for {username}'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created company profile')
            )
        
        self.stdout.write('\nCompany user credentials:')
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write('\nNote: This company user is auto-approved for testing purposes.')
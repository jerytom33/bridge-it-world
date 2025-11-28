from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'email', 'phone', 'date_of_birth', 
                  'current_level', 'stream', 'interests', 'career_goals', 
                  'created_at', 'updated_at')


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Check if user with this email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("User with this email already exists")
            
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        email = validated_data['email']
        
        # Create user with email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Auto-create empty profile so onboarding can update it later
        StudentProfile.objects.get_or_create(user=user)
        return user


class ProfileSetupSerializer(serializers.ModelSerializer):
    interests = serializers.ListField(
        child=serializers.CharField(max_length=50), allow_empty=True, required=False
    )

    class Meta:
        model = StudentProfile
        fields = [
            'current_level', 'stream', 'interests', 'career_goals',
            'phone', 'date_of_birth'
        ]
        extra_kwargs = {
            'current_level': {'required': True},
            'stream': {'required': False},
            'career_goals': {'required': False},
        }
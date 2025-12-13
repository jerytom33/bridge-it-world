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


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student profile (supports both User and StudentProfile fields)"""
    name = serializers.SerializerMethodField()
    email = serializers.EmailField(required=False)
    dob = serializers.DateField(source='date_of_birth', required=False, allow_null=True)
    education_level = serializers.CharField(source='current_level', required=False, allow_blank=True)  # Alias for onboarding
    interests = serializers.ListField(
        child=serializers.CharField(max_length=50), 
        allow_empty=True, 
        required=False
    )
    
    class Meta:
        model = StudentProfile
        fields = [
            'name', 'email', 'phone', 'gender', 'dob', 
            'state', 'district', 'place', 'address',
            'current_level', 'education_level',  # Both fields supported
            'stream', 'career_goals', 'interests'
        ]
    
    def get_name(self, obj):
        """Get full name from User model"""
        user = obj.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        return full_name or user.username or user.email

    
    def validate_phone(self, value):
        """Validate phone number format"""
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits")
        return value
    
    def validate_gender(self, value):
        """Validate gender"""
        if value:
            valid_genders = ['Male', 'Female', 'Other']
            if value not in valid_genders:
                raise serializers.ValidationError(f"Gender must be one of: {', '.join(valid_genders)}")
        return value
    
    def validate_email(self, value):
        """Ensure email is unique (except for current user)"""
        user = self.context.get('user')
        if user and User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already in use")
        return value
    
    def to_internal_value(self, data):
        """Handle name field for write operations"""
        # Store name temporarily if provided
        self._name = data.get('name')
        # Remove name from data dict so it doesn't cause validation errors
        data_copy = data.copy()
        if 'name' in data_copy:
            data_copy.pop('name')
        return super().to_internal_value(data_copy)
    
    def update(self, instance, validated_data):
        """Update both User and StudentProfile"""
        user = instance.user
        
        # Update User fields
        if hasattr(self, '_name') and self._name:
            name_parts = self._name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        if 'email' in validated_data:
            email = validated_data.pop('email')
            user.email = email
            user.username = email  # Keep username in sync
        
        user.save()
        
        # Update StudentProfile fields
        return super().update(instance, validated_data)

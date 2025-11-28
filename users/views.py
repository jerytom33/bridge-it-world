from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import StudentProfile
from .serializers import ProfileSetupSerializer, StudentProfileSerializer, UserSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name', '').strip()
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Basic validation
        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already taken"}, status=400)

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name.split()[0] if name else "",
            last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else ""
        )

        # Create empty profile
        StudentProfile.objects.get_or_create(user=user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "Account created!",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id
        }, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=email, password=password)
        if user:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'message': 'Login successful!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileSetupView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSetupSerializer

    def create(self, request, *args, **kwargs):
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Profile saved successfully!",
            "profile": serializer.data
        }, status=200)


# ... (Your existing SignupView, LoginView, ProfileSetupView classes stay the same)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create profile
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile)
        return Response({
            'user': UserSerializer(request.user).data,
            'profile': serializer.data
        })
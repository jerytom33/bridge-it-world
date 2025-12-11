from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication  # ← ONLY ADDED THIS LINE
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Exam
from .serializers import ProfileSerializer, ExamSerializer, UserSerializer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    ProfileQuerySet = QuerySet[Profile]
    ExamQuerySet = QuerySet[Exam]
else:
    ProfileQuerySet = object
    ExamQuerySet = object


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset: ProfileQuerySet = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset: ProfileQuerySet = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ExamListCreateView(generics.ListCreateAPIView):
    queryset: ExamQuerySet = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset: ExamQuerySet = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user_id': user.id,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        GET /api/profile/me/
        Get current student profile
        """
        # Check if user is a student
        if hasattr(request.user, 'profile') and request.user.profile.role != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create profile for the user
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /api/profile/setup/
        First-time profile setup after registration
        """
        # Check if user is a student
        if hasattr(request.user, 'profile') and request.user.profile.role != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create profile for the user
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        # Update profile fields
        profile.education_level = request.data.get('education_level', profile.education_level)
        profile.stream = request.data.get('stream', profile.stream)
        profile.interests = request.data.get('interests', profile.interests)
        profile.career_goals = request.data.get('career_goals', profile.career_goals)
        profile.phone = request.data.get('phone', profile.phone)
        profile.save()
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


class ResumeUploadAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from resume.models import Resume
        
        pdf = request.FILES['pdf']
        resume = Resume.objects.create(user=request.user, file=pdf)

        import fitz
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        import google.generativeai as genai
        genai.configure(api_key='your_gemini_api_key_here')
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze this resume: {text}\nSuggest career paths, skill gaps, recommended courses.")
        
        resume.gemini_analysis = {'response': response.text}
        resume.save()

        return Response({'analysis': response.text})

# FIXED: Added signup_view
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([name, email, password, confirm_password]):
        return Response({'error': 'All fields are required'}, status=400)

    if password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=400)

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=name
    )
    
    # Create a profile for the user with student role
    Profile.objects.get_or_create(user=user, defaults={'role': 'student'})

    refresh = RefreshToken.for_user(user)
    return Response({
        'token': str(refresh.access_token),
        'user_id': user.id,
    }, status=201)


# Notification Views
class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all notifications for the current user"""
        from .models import Notification
        from .serializers import NotificationSerializer
        
        notifications = Notification.objects.filter(recipient=request.user)
        unread_count = notifications.filter(is_read=False).count()
        
        serializer = NotificationSerializer(notifications, many=True)
        
        return Response({
            'notifications': serializer.data,
            'unread_count': unread_count
        })


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        """Mark a specific notification as read"""
        from .models import Notification
        
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response({'success': True, 'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)


class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Mark all notifications as read for the current user"""
        from .models import Notification
        
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

class FCMTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Register or update FCM token"""
        from .models import FCMToken
        from .serializers import FCMTokenSerializer
        
        token = request.data.get('token')
        device_type = request.data.get('device_type', 'android')
        
        if not token:
            return Response({'error': 'Token is required'}, status=400)
            
        # Update or create token
        fcm_token, created = FCMToken.objects.update_or_create(
            user=request.user,
            token=token,
            defaults={'device_type': device_type}
        )
        
        # Optional: remove old tokens from this user if you want single device policy
        # FCMToken.objects.filter(user=request.user).exclude(id=fcm_token.id).delete()
        
        serializer = FCMTokenSerializer(fcm_token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Send a test notification to the current user"""
        from core.utils import create_notification
        
        try:
            notification = create_notification(
                recipient=request.user,
                notification_type='test_notification',
                title="Test Notification",
                message="This is a test notification from BridgeIT backend!",
                related_user=request.user
            )
            return Response({'success': True, 'message': 'Test notification sent'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


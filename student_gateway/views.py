from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from courses.models import Course, SavedCourse
from courses.serializers import CourseSerializer
from exams.models import Exam, SavedExam
from exams.serializers import ExamSerializer
from users.models import StudentProfile
from users.serializers import StudentProfileSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Get Profile
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        profile_data = StudentProfileSerializer(profile).data
        # Add basic user info that might not be in profile serializer depending on implementation
        profile_data['username'] = user.username
        profile_data['email'] = user.email
        profile_data['first_name'] = user.first_name
        
        # 2. Get Featured/Active Courses (Limit 5)
        # You might want to filter by user's stream/level in the future
        courses = Course.objects.filter(is_active=True).order_by('-created_at')[:5]
        courses_data = CourseSerializer(courses, many=True).data

        # 3. Get Active Exams (Limit 5)
        exams = Exam.objects.filter(is_active=True).order_by('-created_at')[:5]
        exams_data = ExamSerializer(exams, many=True).data

        # 4. Get Saved IDs for UI state
        saved_course_ids = SavedCourse.objects.filter(user=user).values_list('course_id', flat=True)
        saved_exam_ids = SavedExam.objects.filter(user=user).values_list('exam_id', flat=True)


from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class StudentRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name', '').strip()
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Basic validation
        if not email or not password:
            return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name.split()[0] if name else "",
                last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else ""
            )

            # Create empty profile - Explicitly enforcing StudentProfile creation
            StudentProfile.objects.get_or_create(user=user)

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            return Response({"success": True,
                "message": "Student account created successfully!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentProfileView(APIView):
    """
    GET: Retrieve current student's profile
    PATCH: Update current student's profile
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user's profile"""
        user = request.user
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        
        # Prepare response data
        from users.serializers import StudentProfileUpdateSerializer
        
        # Build name from User model
        name = f"{user.first_name} {user.last_name}".strip() or user.username
        
        response_data = {
            'success': True,
            'user': {
                'id': user.id,
                'name': name,
                'email': user.email,
                'phone': profile.phone or '',
                'gender': profile.gender or '',
                'dob': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
                'state': profile.state or '',
                'district': profile.district or '',
                'place': profile.place or '',
                'address': profile.address or '',
                'current_level': profile.current_level or '',
                'stream': profile.stream or '',
                'career_goals': profile.career_goals or '',
                'interests': profile.interests or []
            }
        }
        
        return Response(response_data)
    
    def patch(self, request):
        """Update current user's profile"""
        try:
            user = request.user
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            
            from users.serializers import StudentProfileUpdateSerializer
            
            serializer = StudentProfileUpdateSerializer(
                profile,
                data=request.data,
                partial=True,
                context={'user': user}
            )
            
            if serializer.is_valid():
                serializer.save()
                
                # Refresh from DB to get updated values
                profile.refresh_from_db()
                user.refresh_from_db()
                
                # Return updated data
                name = f"{user.first_name} {user.last_name}".strip() or user.username
                
                return Response({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'user': {
                        'id': user.id,
                        'name': name,
                        'email': user.email,
                        'phone': profile.phone or '',
                        'gender': profile.gender or '',
                        'dob': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
                        'state': profile.state or '',
                        'district': profile.district or '',
                        'place': profile.place or '',
                        'address': profile.address or '',
                        'current_level': profile.current_level or '',
                        'stream': profile.stream or '',
                        'career_goals': profile.career_goals or '',
                        'interests': profile.interests or []
                    }
                })
            else:
                return Response({
                    'success': False,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Profile update error: {str(e)}", exc_info=True)
            
            return Response({
                'success': False,
                'error': f"Profile update failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


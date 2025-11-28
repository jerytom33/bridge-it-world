from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Course, SavedCourse
from .serializers import CourseSerializer, SavedCourseSerializer

class CourseListView(generics.ListAPIView):
    """
    GET /api/courses/
    Return only approved courses
    """
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        return Course.objects.filter(is_active=True)

class SaveCourseView(APIView):
    """
    POST /api/courses/<pk>/save/
    Save a course for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, is_active=True)
            saved_course, created = SavedCourse.objects.get_or_create(
                user=request.user,
                course=course
            )
            
            if created:
                return Response(
                    {'message': 'Course saved successfully'}, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Course already saved'}, 
                    status=status.HTTP_200_OK
                )
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UnsaveCourseView(APIView):
    """
    DELETE /api/courses/<pk>/unsave/
    Remove a course from user's saved list
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            saved_course = SavedCourse.objects.get(
                user=request.user,
                course_id=pk
            )
            saved_course.delete()
            return Response(
                {'message': 'Course unsaved successfully'}, 
                status=status.HTTP_200_OK
            )
        except SavedCourse.DoesNotExist:
            return Response(
                {'error': 'Saved course not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class SavedCoursesView(generics.ListAPIView):
    """
    GET /api/courses/saved/
    List all courses saved by the current user
    """
    serializer_class = SavedCourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedCourse.objects.filter(user=self.request.user).select_related('course')
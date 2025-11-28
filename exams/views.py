from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Exam, SavedExam
from .serializers import ExamSerializer, SavedExamSerializer

class ExamListView(generics.ListAPIView):
    """
    GET /api/exams/?level=UG
    Return only approved exams
    """
    serializer_class = ExamSerializer
    
    def get_queryset(self):
        level = self.request.query_params.get('level', None)
        queryset = Exam.objects.filter(is_active=True)
        
        if level:
            queryset = queryset.filter(level=level)
            
        return queryset

class SaveExamView(APIView):
    """
    POST /api/exams/<pk>/save/
    Save an exam for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk, is_active=True)
            saved_exam, created = SavedExam.objects.get_or_create(
                user=request.user,
                exam=exam
            )
            
            if created:
                return Response(
                    {'message': 'Exam saved successfully'}, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Exam already saved'}, 
                    status=status.HTTP_200_OK
                )
        except Exam.DoesNotExist:
            return Response(
                {'error': 'Exam not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UnsaveExamView(APIView):
    """
    DELETE /api/exams/<pk>/unsave/
    Remove an exam from user's saved list
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            saved_exam = SavedExam.objects.get(
                user=request.user,
                exam_id=pk
            )
            saved_exam.delete()
            return Response(
                {'message': 'Exam unsaved successfully'}, 
                status=status.HTTP_200_OK
            )
        except SavedExam.DoesNotExist:
            return Response(
                {'error': 'Saved exam not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class SavedExamsView(generics.ListAPIView):
    """
    GET /api/exams/saved/
    List all exams saved by the current user
    """
    serializer_class = SavedExamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedExam.objects.filter(user=self.request.user).select_related('exam')
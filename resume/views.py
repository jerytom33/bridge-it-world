from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from django.conf import settings
import json
import PyPDF2
import io
import os
import google.generativeai as genai

from .models import ResumeAnalysis
from .serializers import ResumeAnalysisSerializer

# Import the Gemini helper function
from core.utils import call_gemini_api

# Import simplified resume analyzer (no pyresparser dependency)
from .analyzer_simple import analyze_resume_simple

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        POST /api/resume/upload/
        Upload a PDF resume, extract text, call Gemini API and resume_analyzer, and save analysis
        """
        if 'pdf_file' not in request.FILES:
            return Response(
                {'error': 'No PDF file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        pdf_file = request.FILES['pdf_file']
        
        # Check if file is PDF
        if not pdf_file.name.endswith('.pdf'):
            return Response(
                {'error': 'Only PDF files are allowed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Extract text from PDF for Gemini
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Prepare prompt for Gemini
            prompt = f"""You are a senior career counselor. Analyze this resume and return strict JSON with keys: 
suitable_career_paths (list of strings), skill_gaps (list), recommended_courses (list), suggested_next_steps (list), overall_summary (string)

Resume text:
{text}"""
            
            
            # Call Gemini API
            gemini_response_text = call_gemini_api(prompt)
            
            # Parse the response - it can be either string or dict (in case of error)
            if isinstance(gemini_response_text, dict):
                # Already a dict (error response)
                gemini_response_json = gemini_response_text
            else:
                # String response - try to parse as JSON
                try:
                    gemini_response_json = json.loads(gemini_response_text)
                except json.JSONDecodeError:
                    # If not valid JSON, store as text in a JSON structure
                    gemini_response_json = {
                        "raw_response": gemini_response_text,
                        "suitable_career_paths": [],
                        "skill_gaps": [],
                        "recommended_courses": [],
                        "suggested_next_steps": [],
                        "overall_summary": "Unable to parse structured response"
                    }
            
            
            # Analyze with simplified resume analyzer (no temp file needed)
            pdf_file.seek(0)  # Reset file pointer
            analyzer_result = analyze_resume_simple(pdf_file)
            
            # Save to database with both Gemini and analyzer results
            pdf_file.seek(0)  # Reset file pointer again for saving
            resume_analysis = ResumeAnalysis.objects.create(
                user=request.user,
                pdf_file=pdf_file,
                gemini_response=gemini_response_json,
                # Add analyzer fields
                candidate_name=analyzer_result['basic_details'].get('name', ''),
                candidate_email=analyzer_result['basic_details'].get('email', ''),
                candidate_phone=analyzer_result['basic_details'].get('mobile_number', ''),
                candidate_level=analyzer_result['candidate_level'],
                predicted_field=analyzer_result['predicted_field'],
                resume_score=analyzer_result['resume_score'],
                detected_skills=analyzer_result['basic_details'].get('skills', []),
                recommended_skills=analyzer_result['recommended_skills'],
                recommended_courses=analyzer_result['recommended_courses'],
                score_breakdown=analyzer_result['score_breakdown'],
                analyzer_response=analyzer_result
            )
            
            # Return the analysis
            serializer = ResumeAnalysisSerializer(resume_analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to process resume: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ResumeHistoryView(generics.ListAPIView):
    """
    GET /api/resume/history/
    List all past analyses of logged-in student
    """
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ResumeAnalysis.objects.filter(user=self.request.user)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random
import json

from .models import Question, UserAptitudeResult
from .serializers import QuestionSerializer, UserAptitudeResultSerializer
from core.utils import call_gemini_api

class AptitudeQuestionsView(APIView):
    """
    GET /api/aptitude/questions/
    Return 25 random questions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get all questions
        all_questions = Question.objects.all()
        
        # Select 25 random questions
        if all_questions.count() >= 25:
            questions = random.sample(list(all_questions), 25)
        else:
            questions = list(all_questions)
        
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class SubmitAptitudeTestView(APIView):
    """
    POST /api/aptitude/submit/
    Receive answers, calculate score, call Gemini, save & return
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        answers = request.data.get('answers', {})
        
        if not answers:
            return Response(
                {'error': 'No answers provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Calculate score
            correct_answers = 0
            total_questions = len(answers)
            
            # Get questions and check answers
            for question_id, user_answer in answers.items():
                try:
                    question = Question.objects.get(id=question_id)
                    if question.correct_option == user_answer.upper():
                        correct_answers += 1
                except Question.DoesNotExist:
                    # Skip invalid question IDs
                    continue
            
            score = correct_answers
            
            # Prepare prompt for Gemini
            prompt = f"""Student scored {score}/25 in aptitude test. Here are their answers: {answers}. 
Analyze strengths, weaknesses and suggest top 5 suitable careers. Return JSON with keys: strengths, weaknesses, suggested_careers, improvement_tips"""
            
            # Call Gemini API
            gemini_response_text = call_gemini_api(prompt)
            
            # Parse the response to ensure it's valid JSON
            try:
                gemini_response_json = json.loads(gemini_response_text)
            except json.JSONDecodeError:
                # If not valid JSON, store as text in a JSON structure
                gemini_response_json = {
                    "raw_response": gemini_response_text,
                    "strengths": [],
                    "weaknesses": [],
                    "suggested_careers": [],
                    "improvement_tips": []
                }
            
            # Save to database
            aptitude_result = UserAptitudeResult.objects.create(
                user=request.user,
                score=score,
                answers=answers,
                gemini_analysis=gemini_response_json
            )
            
            # Return the result
            serializer = UserAptitudeResultSerializer(aptitude_result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to process aptitude test: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AptitudeHistoryView(generics.ListAPIView):
    """
    GET /api/aptitude/history/
    List past results
    """
    serializer_class = UserAptitudeResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserAptitudeResult.objects.filter(user=self.request.user)


# ========== MegaLLM AI-Powered Endpoints ==========

class PersonalizedAptitudeQuestionsView(APIView):
    """
    GET /api/aptitude/personalized-questions/
    Generate AI-powered personalized aptitude questions based on education level
    Query params: level (default: 10th), count (default: 10)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            education_level = request.GET.get('level', '10th')
            num_questions = min(int(request.GET.get('count', 10)), 25)  # Max 25 questions
            
            # Get user profile data if available
            user_profile = {
                'interests': request.user.profile.interests if hasattr(request.user, 'profile') else 'General'
            }
            
            # Import and use MegaLLM service
            from services.megallm_service import get_megallm_service
            megallm_service = get_megallm_service()
            
            questions = megallm_service.generate_aptitude_questions(
                education_level=education_level,
                num_questions=num_questions,
                user_profile=user_profile
            )
            
            return Response({
                'success': True,
                'data': {
                    'questions': questions,
                    'education_level': education_level,
                    'total_questions': len(questions)
                }
            })
            
        except Exception as e:
            print(f"DEBUG: View Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Failed to generate questions: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalyzeAptitudeResultsView(APIView):
    """
    POST /api/aptitude/analyze-results/
    Analyze aptitude test results with AI
    Body: { "questions": [...], "answers": {0: "A", 1: "B", ...} }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            questions = request.data.get('questions', [])
            answers = request.data.get('answers', {})
            
            if not questions or not answers:
                return Response(
                    {'error': 'Questions and answers are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get user profile
            user_profile = {}
            if hasattr(request.user, 'profile'):
                user_profile = {
                    'education': getattr(request.user.profile, 'education_level', 'Unknown'),
                    'skills': getattr(request.user.profile, 'skills', [])
                }
            
            # Import and use MegaLLM service
            from services.megallm_service import get_megallm_service
            megallm_service = get_megallm_service()
            
            analysis = megallm_service.analyze_aptitude_results(
                questions=questions,
                answers=answers,
                user_profile=user_profile
            )
            
            # Save to database
            aptitude_result = UserAptitudeResult.objects.create(
                user=request.user,
                score=analysis['score'],
                answers=answers,
                gemini_analysis=analysis['ai_analysis']
            )
            
            return Response({
                'success': True,
                'data': {
                    'score': analysis['score'],
                    'correct_answers': analysis['correct_answers'],
                    'total_questions': analysis['total_questions'],
                    'category_breakdown': analysis['category_breakdown'],
                    'ai_analysis': analysis['ai_analysis'],
                    'result_id': aptitude_result.id
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to analyze results: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ========== Browser Test Page ==========

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def aptitude_test_page(request):
    """
    Browser-based test page for MegaLLM aptitude test
    Accessible at /aptitude/test/
    """
    return render(request, 'aptitude_test.html')

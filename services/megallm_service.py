"""
MegaLLM Service (Powered by Gemini)
Handles resume analysis, aptitude questions generation, and career guidance.
Note: Named "MegaLLMService" to maintain compatibility with existing views.
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class MegaLLMService:
    """Service class for AI integration (Powered by Google Gemini)"""
    
    def __init__(self):
        """Initialize Gemini client with API credentials"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
            
        genai.configure(api_key=self.api_key)
        
        # Configure model fallback list
        self.models_to_try = [
            'gemini-2.5-flash', 
            'gemini-2.0-flash', 
            'gemini-flash-latest'
        ]
        self.model_name = self.models_to_try[0]
        self.model = genai.GenerativeModel(self.model_name)
    
    def _call_api(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Make API call to Gemini with fallback"""
        # Convert OpenAI-style messages to Gemini prompt
        user_prompt = ""
        system_prompt = ""
        
        for msg in messages:
            if msg['role'] == 'user':
                user_prompt += msg['content'] + "\n"
            elif msg['role'] == 'system':
                system_prompt += msg['content'] + "\n"
        
        full_prompt = f"{system_prompt}\n{user_prompt}".strip()
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature
        )
        
        last_error = None
        
        for model_name in self.models_to_try:
            try:
                # logger.info(f"Calling Gemini model {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                return response.text
                
            except Exception as e:
                # logger.warning(f"Model {model_name} failed: {str(e)}")
                last_error = e
                continue
        
        logger.error(f"All models failed. Last error: {str(last_error)}")
        raise Exception(f"AI Service error (All models failed): {str(last_error)}")
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume and extract key information
        """
        prompt = f"""Analyze this resume and extract information in JSON format:

Resume:
{resume_text}

Provide a JSON response with:
- extracted_skills: List of technical and soft skills
- education_level: Highest education (10th/12th/Diploma/Bachelors/Masters/PhD)
- experience_years: Years of experience (0 if fresher)
- career_summary: Brief summary (2-3 sentences)
- recommended_courses: List of 3-5 recommended course topics
- strengths: List of key strengths
- areas_to_improve: List of areas to improve

Return ONLY valid JSON, no additional text (no markdown backticks)."""

        messages = [
            {"role": "system", "content": "You are an expert resume analyzer and career counselor."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.3)
        return self._parse_json(response)
    
    def generate_career_path(self, resume_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized career path recommendations"""
        skills = resume_analysis.get('extracted_skills', [])
        education = resume_analysis.get('education_level', 'Unknown')
        experience = resume_analysis.get('experience_years', 0)
        
        prompt = f"""Based on this profile, suggest career paths:

Skills: {', '.join(skills)}
Education: {education}
Experience: {experience} years

Provide JSON response with:
- career_paths: List of 3-5 suitable career paths with descriptions
- short_term_goals: List of goals for next 6 months
- long_term_goals: List of goals for 1-3 years
- skill_gaps: Skills to acquire for career advancement
- certifications: Recommended certifications

Return ONLY valid JSON, no markdown backticks."""

        messages = [
            {"role": "system", "content": "You are a career counselor."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.5)
        return self._parse_json(response)
    
    def generate_aptitude_questions(
        self, 
        education_level: str = "10th",
        num_questions: int = 10,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate personalized aptitude test questions with level-appropriate difficulty"""
        
        # Level-specific context and difficulty guidance
        level_context = {
            '10th': {
                'description': '10th standard (secondary school)',
                'difficulty_mix': 'easy (60%), medium (30%), hard (10%)',
                'content_guidance': 'Age-appropriate for 15-16 year olds, focus on fundamental concepts',
                'topics': 'Basic arithmetic, simple reasoning, general awareness suitable for teenagers'
            },
            '12th': {
                'description': '12th standard (higher secondary/pre-university)',
                'difficulty_mix': 'easy (30%), medium (50%), hard (20%)',
                'content_guidance': 'Pre-university level, preparation for competitive exams',
                'topics': 'Advanced mathematics, logical reasoning, current affairs, science concepts'
            },
            'Diploma': {
                'description': 'Diploma/Polytechnic level',
                'difficulty_mix': 'easy (25%), medium (50%), hard (25%)',
                'content_guidance': 'Technical and vocational focus, practical problem-solving',
                'topics': 'Technical aptitude, practical reasoning, industry-relevant knowledge'
            },
            'Bachelor': {
                'description': "Bachelor's degree (undergraduate)",
                'difficulty_mix': 'easy (20%), medium (40%), hard (40%)',
                'content_guidance': 'Undergraduate-level analytical thinking and reasoning',
                'topics': 'Complex problem solving, analytical reasoning, professional scenarios'
            },
            'Master': {
                'description': "Master's degree (postgraduate)",
                'difficulty_mix': 'easy (10%), medium (30%), hard (60%)',
                'content_guidance': 'Advanced postgraduate-level critical thinking',
                'topics': 'Advanced analytics, strategic thinking, research-oriented problems, complex scenarios'
            }
        }
        
        context = level_context.get(education_level, level_context['10th'])
        
        profile_context = ""
        if user_profile:
            profile_context = f"\nUser interests: {user_profile.get('interests', 'General')}"

        prompt = f"""Generate {num_questions} aptitude test questions for {context['description']} level.{profile_context}

IMPORTANT - Level-Appropriate Content:
- Target difficulty distribution: {context['difficulty_mix']}
- Content guidance: {context['content_guidance']}
- Recommended topics: {context['topics']}

Question Categories (include mix of):
- Logical reasoning (30%)
- Quantitative aptitude (30%)
- Verbal ability (20%)
- General knowledge (20%)

Provide a JSON array with each question having:
- question: The question text (appropriate for {education_level} level)
- options: Array of 4 options (A, B, C, D)
- correct_answer: The correct option letter (A, B, C, or D)
- difficulty: easy/medium/hard (follow the distribution above)
- category: The category name (Logical reasoning, Quantitative aptitude, Verbal ability, or General knowledge)
- explanation: Brief explanation of correct answer

CRITICAL: Ensure questions are genuinely appropriate for {context['description']}. 
Adjust vocabulary, complexity, and context to match the education level.

Return ONLY valid JSON array, no markdown backticks."""

        messages = [
            {"role": "system", "content": "You are an expert aptitude test creator who tailors questions precisely to education levels."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.7)
        return self._parse_json(response)
    
    def analyze_aptitude_results(
        self,
        questions: List[Dict[str, Any]],
        answers: Dict[int, str],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze aptitude test results and provide insights"""
        # Calculate score
        total = len(questions)
        correct = 0
        category_stats = {}
        
        for idx in range(len(questions)):
            question = questions[idx]
            # Handle string/int key mismatch
            user_answer = answers.get(str(idx), '')
            if not user_answer:
                 user_answer = answers.get(idx, '')
                 
            is_correct = user_answer == question.get('correct_answer', '')
            
            if is_correct:
                correct += 1
            
            # Track by category
            category = question.get('category', 'Other')
            if category not in category_stats:
                category_stats[category] = {'correct': 0, 'total': 0}
            
            category_stats[category]['total'] += 1
            if is_correct:
                category_stats[category]['correct'] += 1
        
        score_percentage = (correct / total * 100) if total > 0 else 0
        
        # Get AI insights
        stats_text = "\n".join([
            f"{cat}: {stats['correct']}/{stats['total']} correct" 
            for cat, stats in category_stats.items()
        ])
        
        prompt = f"""Analyze this aptitude test performance:

Total Score: {score_percentage:.1f}% ({correct}/{total})
Category breakdown:
{stats_text}

Provide JSON response with:
- overall_performance: Brief assessment
- strong_areas: List of strengths
- weak_areas: List of areas needing improvement
- study_recommendations: List of specific study recommendations
- career_suggestions: Suitable career fields based on performance
- confidence_level: Estimated confidence (Low/Medium/High)

Return ONLY valid JSON, no markdown backticks."""

        messages = [
            {"role": "system", "content": "You are an educational counselor."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.4)
        ai_analysis = self._parse_json(response)
        
        return {
            'score': score_percentage,
            'correct_answers': correct,
            'total_questions': total,
            'category_breakdown': category_stats,
            'ai_analysis': ai_analysis
        }
    
    def chat_with_career_advisor(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Interactive chat with AI career advisor"""
        context_msg = ""
        if user_context:
            context_msg = f"User context: Education: {user_context.get('education', 'Unknown')}, Skills: {', '.join(user_context.get('skills', []))}\n"
        
        full_message = f"{context_msg}User asks: {user_message}"
        
        messages = [
            {"role": "system", "content": "You are a friendly and knowledgeable career advisor."},
            {"role": "user", "content": full_message}
        ]
        
        return self._call_api(messages, temperature=0.7)

    def _parse_json(self, response_text: str) -> Any:
        """Helper to parse JSON from AI response, handling markdown code blocks"""
        text = response_text.strip()
        # Remove markdown code blocks if present
        if text.startswith("```"):
            import re
            # Match ```json ... ``` or just ``` ... ```
            match = re.search(r'```(?:json)?\s*(.*)\s*```', text, re.DOTALL)
            if match:
                text = match.group(1)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object/array via regex fallback
            import re
            json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except:
                    pass
            # If all fails
            print(f"DEBUG: Failed to parse JSON: {text[:100]}...")
            return {"error": "Failed to parse AI response", "raw_text": text}


# Singleton instance
_megallm_service = None

def get_megallm_service() -> MegaLLMService:
    """Get or create MegaLLM service instance"""
    global _megallm_service
    if _megallm_service is None:
        _megallm_service = MegaLLMService()
    return _megallm_service

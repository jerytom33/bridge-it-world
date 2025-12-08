import google.generativeai as genai
import os
import logging
import json

logger = logging.getLogger(__name__)

def call_gemini_api(prompt):
    """
    Reusable function to call Gemini API with error handling
    """
    try:
        # Configure Gemini API key  
        api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyD_Foa_APEbSGIpusGOjQI2eB5_jYUtduY')
        genai.configure(api_key=api_key)
        
        # Try multiple model names in order of preference
        models_to_try = [
            'gemini-pro',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                # Create the model
                model = genai.GenerativeModel(model_name)
                
                # Generate content
                response = model.generate_content(prompt)
                
                logger.info(f"Successfully used model: {model_name}")
                return response.text
            
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model_name} failed: {str(e)}")
                continue
        
        # If all models failed, raise the last error
        raise last_error if last_error else Exception("All model attempts failed")
    
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Gemini API Error: {str(e)}")
        
        # Return a JSON error response instead of dict
        error_response = {
            "error": "AI service temporarily unavailable",
            "details": str(e),
            "suitable_career_paths": ["Unable to analyze at this time"],
            "skill_gaps": [],
            "recommended_courses": [],
            "suggested_next_steps": ["Please try again later"],
            "overall_summary": "Analysis unavailable due to AI service error"
        }
        return json.dumps(error_response)

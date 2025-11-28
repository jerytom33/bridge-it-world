import google.generativeai as genai
import os

def call_gemini_api(prompt):
    """
    Reusable function to call Gemini API
    """
    # Configure Gemini API key (should be set in environment variables)
    api_key = os.environ.get('GEMINI_API_KEY', 'your_gemini_api_key_here')
    genai.configure(api_key=api_key)
    
    # Create the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Generate content
    response = model.generate_content(prompt)
    
    return response.text
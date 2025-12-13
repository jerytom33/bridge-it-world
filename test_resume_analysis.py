
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

# Ensure env var is set (though utils.py has fallback, we want to test the flow)
os.environ['GEMINI_API_KEY'] = "AIzaSyDYKCaq8y69q3MPouPLPNyki9UBAVS-x5Q"

from core.utils import call_gemini_api

print("Testing Resume Analysis (Gemini)...")

mock_resume_text = """
John Doe
Software Engineer
Skills: Python, Django, JavaScript, React, AWS
Experience: 3 years at Tech Corp building web apps.
Education: B.S. Computer Science
"""

prompt = f"""You are a senior career counselor. Analyze this resume and return strict JSON with keys: 
suitable_career_paths (list of strings), skill_gaps (list), recommended_courses (list), suggested_next_steps (list), overall_summary (string)

Resume text:
{mock_resume_text}"""

try:
    print("Sending request to Gemini...")
    response = call_gemini_api(prompt)
    print("\n✅ Success! Response:")
    print(response[:500] + "..." if len(response) > 500 else response)
except Exception as e:
    print(f"\n❌ FAILED: {str(e)}")

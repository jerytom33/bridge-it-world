
import google.generativeai as genai
import os

api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyD_Foa_APEbSGIpusGOjQI2eB5_jYUtduY')
genai.configure(api_key=api_key)

print(f"Checking models for key: {api_key[:10]}...") 

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Error listing models: {e}")


import os
import sys

# Add project root to path so we can import services
sys.path.append(os.getcwd())

from services.megallm_service import MegaLLMService

print("Initializing MegaLLMService (Bytez)...")
try:
    service = MegaLLMService()
    print("Service initialized.")

    print("\n--- Testing generate_aptitude_questions ---")
    print("Sending request to Bytez (this may take 30s+)...")
    
    questions = service.generate_aptitude_questions(
        education_level="12th",
        num_questions=3  # Small number for speed
    )
    
    print("\n✅ Success! Received questions:")
    print(questions)

except Exception as e:
    print(f"\n❌ FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

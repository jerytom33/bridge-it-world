"""
Quick test script to verify MegaLLM service integration
Run with: python test_megallm.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeit_backend.settings')
django.setup()

def test_service_initialization():
    """Test if MegaLLM service can be initialized"""
    print("Testing MegaLLM service initialization...")
    
    try:
        from services.megallm_service import get_megallm_service
        service = get_megallm_service()
        print("✅ Service initialized successfully!")
        print(f"   API Base URL: {service.base_url}")
        print(f"   Model: {service.model}")
        return True
    except Exception as e:
        print(f"❌ Service initialization failed: {str(e)}")
        return False

def test_resume_analysis():
    """Test resume analysis with sample text"""
    print("\nTesting resume analysis...")
    
    try:
        from services.megallm_service import get_megallm_service
        service = get_megallm_service()
        
        sample_resume = """
        John Doe
        Software Engineer
        Email: john@example.com
        
        Experience: 3 years in Python and Django development
        Skills: Python, Django, REST APIs, PostgreSQL, Docker
        Education: B.Tech in Computer Science
        """
        
        result = service.analyze_resume(sample_resume)
        print("✅ Resume analysis successful!")
        print(f"   Extracted Skills: {result.get('extracted_skills', [])[:3]}...")
        print(f"   Education Level: {result.get('education_level', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Resume analysis failed: {str(e)}")
        return False

def test_aptitude_questions():
    """Test aptitude question generation"""
    print("\nTesting aptitude question generation...")
    
    try:
        from services.megallm_service import get_megallm_service
        service = get_megallm_service()
        
        questions = service.generate_aptitude_questions(
            education_level="10th",
            num_questions=3
        )
        
        print("✅ Aptitude question generation successful!")
        print(f"   Generated {len(questions)} questions")
        if questions:
            print(f"   First question: {questions[0].get('question', 'N/A')[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Aptitude question generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MegaLLM Service Integration Test")
    print("=" * 60)
    
    tests = [
        test_service_initialization,
        test_resume_analysis,
        test_aptitude_questions
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test crashed: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n🎉 All tests passed! MegaLLM integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")

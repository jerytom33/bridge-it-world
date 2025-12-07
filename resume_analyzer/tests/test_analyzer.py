"""
Simple Test for Resume Analyzer Module

Basic smoke tests to verify the module can be imported and used.
"""

def test_import():
    """Test that the module can be imported."""
    try:
        from resume_analyzer import analyze_resume
        print("✓ Module import successful")
        return True
    except ImportError as e:
        print(f"✗ Module import failed: {e}")
        return False


def test_dependencies():
    """Test that all required dependencies are installed."""
    dependencies = [
        ('pyresparser', 'pyresparser'),
        ('pdfminer3', 'pdfminer'),
        ('spacy', 'spacy'),
        ('nltk', 'nltk'),
    ]
    
    all_installed = True
    for name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            all_installed = False
    
    return all_installed


def test_analyze_function():
    """Test that analyze_resume function exists and has correct signature."""
    try:
        from resume_analyzer import analyze_resume
        import inspect
        
        sig = inspect.signature(analyze_resume)
        params = list(sig.parameters.keys())
        
        if 'file_path' in params:
            print("✓ analyze_resume function has correct signature")
            return True
        else:
            print("✗ analyze_resume function signature is incorrect")
            return False
    except Exception as e:
        print(f"✗ Error checking function: {e}")
        return False


def test_with_sample_resume():
    """Test analysis with a sample resume if available."""
    import os
    from resume_analyzer import analyze_resume
    
    # Look for sample resumes in the App/Uploaded_Resumes directory
    sample_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'App', 'Uploaded_Resumes')
    
    if not os.path.exists(sample_dir):
        print("⚠ No sample resumes directory found - skipping real analysis test")
        return True
    
    # Get first PDF file
    pdf_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("⚠ No sample PDF resumes found - skipping real analysis test")
        return True
    
    sample_resume = os.path.join(sample_dir, pdf_files[0])
    
    try:
        print(f"Testing with sample resume: {pdf_files[0]}")
        result = analyze_resume(sample_resume)
        
        # Check that all expected keys are present
        expected_keys = [
            'basic_details', 'candidate_level', 'predicted_field',
            'recommended_skills', 'recommended_courses', 'resume_score',
            'score_breakdown'
        ]
        
        missing_keys = [key for key in expected_keys if key not in result]
        
        if missing_keys:
            print(f"✗ Result missing keys: {missing_keys}")
            return False
        
        print("✓ Analysis completed successfully")
        print(f"  - Candidate: {result['basic_details'].get('name', 'N/A')}")
        print(f"  - Score: {result['resume_score']}/100")
        print(f"  - Field: {result['predicted_field']}")
        print(f"  - Level: {result['candidate_level']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("="*60)
    print("RESUME ANALYZER MODULE - BASIC TESTS")
    print("="*60)
    print()
    
    tests = [
        ("Import Test", test_import),
        ("Dependencies Test", test_dependencies),
        ("Function Signature Test", test_analyze_function),
        ("Sample Resume Test", test_with_sample_resume),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-"*60)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status:6} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(run_all_tests())

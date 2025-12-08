"""
Quick Test Script for Resume Analyzer Module

This script tests the module with a sample resume from the App directory.
"""

import sys
sys.path.insert(0, '..')

from resume_analyzer import analyze_resume
import os
import json

def main():
    # Find first available resume in App/Uploaded_Resumes
    resumes_dir = '../App/Uploaded_Resumes'
    
    if not os.path.exists(resumes_dir):
        print("Error: Resumes directory not found")
        return
    
    pdf_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("Error: No PDF files found in", resumes_dir)
        return
    
    sample_resume = os.path.join(resumes_dir, pdf_files[0])
    
    print("="*60)
    print("TESTING RESUME ANALYZER MODULE")
    print("="*60)
    print(f"\nAnalyzing: {pdf_files[0]}")
    print("-"*60)
    
    try:
        result = analyze_resume(sample_resume)
        
        print("\n✓ ANALYSIS SUCCESSFUL!")
        print("\nBASIC DETAILS:")
        basic = result['basic_details']
        print(f"  Name: {basic.get('name', 'N/A')}")
        print(f"  Email: {basic.get('email', 'N/A')}")
        print(f"  Phone: {basic.get('mobile_number', 'N/A')}")
        print(f"  Pages: {basic.get('no_of_pages', 'N/A')}")
        
        print("\nANALYSIS RESULTS:")
        print(f"  Experience Level: {result['candidate_level']}")
        print(f"  Predicted Field: {result['predicted_field']}")
        print(f"  Resume Score: {result['resume_score']}/100")
        
        print("\nDETECTED SKILLS:")
        skills = basic.get('skills', [])
        for skill in skills[:10]:  # Show first 10
            print(f"  • {skill}")
        
        print("\nRECOMMENDED SKILLS (Top 5):")
        for skill in result['recommended_skills'][:5]:
            print(f"  • {skill}")
        
        print("\nRECOMMENDED COURSES:")
        for course in result['recommended_courses'][:3]:
            print(f"  • {course['name']}")
        
        print("\n" + "="*60)
        print("✓ MODULE TEST PASSED!")
        print("="*60)
        
        # Save full result
        with open('test_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\nFull results saved to test_result.json")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

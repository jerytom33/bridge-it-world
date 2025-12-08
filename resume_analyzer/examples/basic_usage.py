"""
Basic Usage Example for Resume Analyzer

This example demonstrates the simplest way to use the resume_analyzer module.
"""

from resume_analyzer import analyze_resume
import json

def main():
    # Path to your resume PDF
    resume_path = 'sample_resume.pdf'
    
    try:
        print("Analyzing resume...")
        result = analyze_resume(resume_path)
        
        # Print basic details
        print("\n" + "="*50)
        print("BASIC INFORMATION")
        print("="*50)
        basic = result['basic_details']
        print(f"Name: {basic.get('name', 'N/A')}")
        print(f"Email: {basic.get('email', 'N/A')}")
        print(f"Phone: {basic.get('mobile_number', 'N/A')}")
        print(f"Pages: {basic.get('no_of_pages', 'N/A')}")
        
        # Print skills
        print("\n" + "="*50)
        print("DETECTED SKILLS")
        print("="*50)
        skills = basic.get('skills', [])
        if skills:
            for skill in skills:
                print(f"  • {skill}")
        else:
            print("  No skills detected")
        
        # Print analysis results
        print("\n" + "="*50)
        print("ANALYSIS RESULTS")
        print("="*50)
        print(f"Experience Level: {result['candidate_level']}")
        print(f"Predicted Field: {result['predicted_field']}")
        print(f"Resume Score: {result['resume_score']}/100")
        
        # Print score breakdown
        print("\n" + "="*50)
        print("SCORE BREAKDOWN")
        print("="*50)
        for feedback in result['score_breakdown']:
            print(f"  {feedback}")
        
        # Print recommended skills
        print("\n" + "="*50)
        print("RECOMMENDED SKILLS")
        print("="*50)
        rec_skills = result['recommended_skills']
        if rec_skills and rec_skills[0] != 'No Recommendations':
            for skill in rec_skills[:10]:  # Show first 10
                print(f"  • {skill}")
        else:
            print("  No recommendations available")
        
        # Print recommended courses
        print("\n" + "="*50)
        print("RECOMMENDED COURSES")
        print("="*50)
        courses = result['recommended_courses']
        if courses:
            for i, course in enumerate(courses, 1):
                print(f"  {i}. {course['name']}")
                print(f"     {course['link']}")
        else:
            print("  No course recommendations")
        
        # Optionally save full results to JSON
        print("\n" + "="*50)
        print("Saving full results to 'analysis_result.json'...")
        with open('analysis_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("Done!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the resume file exists at the specified path.")
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

"""
Resume Analyzer Core Module

Provides the main resume analysis functionality.
"""

import os
from pyresparser import ResumeParser
from .utils import pdf_reader, course_recommender, check_section_presence
from .courses import ds_course, web_course, android_course, ios_course, uiux_course
from .config import (
    DS_KEYWORDS, WEB_KEYWORDS, ANDROID_KEYWORDS, IOS_KEYWORDS, UIUX_KEYWORDS,
    NON_SPECIFIC_KEYWORDS, RECOMMENDED_SKILLS, SCORING_WEIGHTS,
    CANDIDATE_LEVEL_KEYWORDS, SECTION_KEYWORDS
)


def detect_candidate_level(resume_text, num_pages):
    """
    Determine the candidate's experience level.
    
    Args:
        resume_text (str): Full text content of the resume
        num_pages (int): Number of pages in the resume
        
    Returns:
        str: "Fresher", "Intermediate", or "Experienced"
    """
    if num_pages < 1:
        return "Fresher"
    
    # Check for internship keywords
    if check_section_presence(resume_text, CANDIDATE_LEVEL_KEYWORDS['internship']):
        return "Intermediate"
    
    # Check for experience keywords
    if check_section_presence(resume_text, CANDIDATE_LEVEL_KEYWORDS['experience']):
        return "Experienced"
    
    return "Fresher"


def predict_field_and_recommendations(skills):
    """
    Predict career field based on skills and provide recommendations.
    
    Args:
        skills (list): List of skills from the resume
        
    Returns:
        tuple: (predicted_field, recommended_skills, recommended_courses)
    """
    if not skills:
        return 'NA', ['No Recommendations'], []
    
    for skill in skills:
        skill_lower = skill.lower()
        
        # Data Science
        if skill_lower in DS_KEYWORDS:
            return (
                'Data Science',
                RECOMMENDED_SKILLS['Data Science'],
                course_recommender(ds_course)
            )
        
        # Web Development
        elif skill_lower in WEB_KEYWORDS:
            return (
                'Web Development',
                RECOMMENDED_SKILLS['Web Development'],
                course_recommender(web_course)
            )
        
        # Android Development
        elif skill_lower in ANDROID_KEYWORDS:
            return (
                'Android Development',
                RECOMMENDED_SKILLS['Android Development'],
                course_recommender(android_course)
            )
        
        # iOS Development
        elif skill_lower in IOS_KEYWORDS:
            return (
                'IOS Development',
                RECOMMENDED_SKILLS['IOS Development'],
                course_recommender(ios_course)
            )
        
        # UI/UX Development
        elif skill_lower in UIUX_KEYWORDS:
            return (
                'UI-UX Development',
                RECOMMENDED_SKILLS['UI-UX Development'],
                course_recommender(uiux_course)
            )
        
        # Non-specific skills
        elif skill_lower in NON_SPECIFIC_KEYWORDS:
            return 'NA', ['No Recommendations'], []
    
    # No matching field found
    return 'NA', ['No Recommendations'], []


def calculate_resume_score(resume_text):
    """
    Calculate resume score based on presence of key sections.
    
    Args:
        resume_text (str): Full text content of the resume
        
    Returns:
        tuple: (score, score_breakdown)
            - score (int): Total score from 0-100
            - score_breakdown (list): List of feedback strings
    """
    score = 0
    breakdown = []
    
    # Objective/Summary
    if check_section_presence(resume_text, SECTION_KEYWORDS['objective']):
        score += SCORING_WEIGHTS['objective_summary']
        breakdown.append("[+] Added Objective/Summary")
    else:
        breakdown.append("[-] Missing Objective/Summary")
    
    # Education
    if check_section_presence(resume_text, SECTION_KEYWORDS['education']):
        score += SCORING_WEIGHTS['education']
        breakdown.append("[+] Added Education Details")
    else:
        breakdown.append("[-] Missing Education Details")
    
    # Experience
    if check_section_presence(resume_text, SECTION_KEYWORDS['experience']):
        score += SCORING_WEIGHTS['experience']
        breakdown.append("[+] Added Experience")
    else:
        breakdown.append("[-] Missing Experience")
    
    # Internships
    if check_section_presence(resume_text, SECTION_KEYWORDS['internship']):
        score += SCORING_WEIGHTS['internships']
        breakdown.append("[+] Added Internships")
    else:
        breakdown.append("[-] Missing Internships")
    
    # Skills
    if check_section_presence(resume_text, SECTION_KEYWORDS['skills']):
        score += SCORING_WEIGHTS['skills']
        breakdown.append("[+] Added Skills")
    else:
        breakdown.append("[-] Missing Skills")
    
    # Hobbies
    if check_section_presence(resume_text, SECTION_KEYWORDS['hobbies']):
        score += SCORING_WEIGHTS['hobbies']
        breakdown.append("[+] Added Hobbies")
    else:
        breakdown.append("[-] Missing Hobbies")
    
    # Interests
    if check_section_presence(resume_text, SECTION_KEYWORDS['interests']):
        score += SCORING_WEIGHTS['interests']
        breakdown.append("[+] Added Interests")
    else:
        breakdown.append("[-] Missing Interests")
    
    # Achievements
    if check_section_presence(resume_text, SECTION_KEYWORDS['achievements']):
        score += SCORING_WEIGHTS['achievements']
        breakdown.append("[+] Added Achievements")
    else:
        breakdown.append("[-] Missing Achievements")
    
    # Certifications
    if check_section_presence(resume_text, SECTION_KEYWORDS['certifications']):
        score += SCORING_WEIGHTS['certifications']
        breakdown.append("[+] Added Certifications")
    else:
        breakdown.append("[-] Missing Certifications")
    
    # Projects
    if check_section_presence(resume_text, SECTION_KEYWORDS['projects']):
        score += SCORING_WEIGHTS['projects']
        breakdown.append("[+] Added Projects")
    else:
        breakdown.append("[-] Missing Projects")
    
    return score, breakdown


def analyze_resume(file_path):
    """
    Analyze a resume and provide comprehensive feedback.
    
    This is the main entry point for resume analysis. It parses the resume,
    extracts information, predicts the career field, recommends skills and courses,
    and calculates a resume score.
    
    Args:
        file_path (str): Absolute path to the PDF resume file
        
    Returns:
        dict: Analysis results containing:
            - basic_details (dict): Name, email, phone, skills, education, experience, etc.
            - candidate_level (str): "Fresher", "Intermediate", or "Experienced"
            - predicted_field (str): Predicted career field
            - recommended_skills (list): Skills to add
            - recommended_courses (list): Course recommendations
            - resume_score (int): Score from 0-100
            - score_breakdown (list): Detailed feedback
            
    Raises:
        FileNotFoundError: If the resume file doesn't exist
        Exception: If resume parsing fails
        
    Example:
        >>> result = analyze_resume('/path/to/resume.pdf')
        >>> print(f"Score: {result['resume_score']}")
        >>> print(f"Field: {result['predicted_field']}")
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    # Extract resume data using pyresparser
    resume_data = ResumeParser(file_path).get_extracted_data()
    
    if not resume_data:
        raise Exception("Failed to parse resume. The file may be corrupted or in an unsupported format.")
    
    # Extract full text from PDF
    resume_text = pdf_reader(file_path)
    
    # Get basic details
    num_pages = resume_data.get('no_of_pages', 0)
    skills = resume_data.get('skills', [])
    
    # Detect candidate level
    candidate_level = detect_candidate_level(resume_text, num_pages)
    
    # Predict field and get recommendations
    predicted_field, recommended_skills, recommended_courses = predict_field_and_recommendations(skills)
    
    # Calculate resume score
    resume_score, score_breakdown = calculate_resume_score(resume_text)
    
    # Compile results
    return {
        "basic_details": resume_data,
        "candidate_level": candidate_level,
        "predicted_field": predicted_field,
        "recommended_skills": recommended_skills,
        "recommended_courses": recommended_courses,
        "resume_score": resume_score,
        "score_breakdown": score_breakdown
    }

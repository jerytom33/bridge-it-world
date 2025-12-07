"""
Simplified Resume Analyzer for Bridge-IT-World

Standalone analyzer that doesn't require pyresparser or spaCy.
Uses PyPDF2 for text extraction and manual parsing.
"""

import re
import random
import PyPDF2


# Configuration - Field Detection Keywords

DS_KEYWORDS = [
    'tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 
    'flask', 'streamlit', 'scikit-learn', 'pandas', 'numpy', 'data science',
    'data analysis', 'data visualization', 'neural network', 'nlp'
]

WEB_KEYWORDS = [
    'react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 
    'wordpress', 'javascript', 'angular js', 'c#', 'asp.net', 'flask',
    'vue', 'vue.js', 'express', 'express.js', 'html', 'css', 'bootstrap',
    'tailwind', 'next.js', 'nuxt.js'
]

ANDROID_KEYWORDS = [
    'android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy',
    'java', 'android studio', 'gradle', 'material design'
]

IOS_KEYWORDS = [
    'ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode',
    'objective-c', 'swiftui', 'uikit'
]

UIUX_KEYWORDS = [
    'ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 
    'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 
    'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 
    'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 
    'wireframe', 'solid', 'grasp', 'user research', 'user experience',
    'sketch', 'invision', 'user interface'
]

# Recommended Skills by Field
RECOMMENDED_SKILLS = {
    'Data Science': [
        'Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
        'Data Mining', 'Clustering & Classification', 'Data Analytics',
        'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
        'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', 'Flask',
        'Streamlit'
    ],
    'Web Development': [
        'React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
        'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK'
    ],
    'Android Development': [
        'Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
        'Kivy', 'GIT', 'SDK', 'SQLite'
    ],
    'IOS Development': [
        'IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
        'Objective-C', 'SQLite', 'Plist', 'StoreKit', 'UI-Kit', 'AV Foundation',
        'Auto-Layout'
    ],
    'UI-UX Development': [
        'UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
        'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
        'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
        'Solid', 'Grasp', 'User Research'
    ]
}

# Resume Scoring Configuration
SCORING_WEIGHTS = {
    'objective': 6,
    'education': 12,
    'experience': 16,
    'internship': 6,
    'skills': 7,
    'hobbies': 4,
    'interests': 5,
    'achievements': 13,
    'certifications': 12,
    'projects': 19
}

#Resume Section Keywords
SECTION_KEYWORDS = {
    'objective': ['Objective', 'Summary', 'OBJECTIVE', 'SUMMARY'],
    'education': ['Education', 'School', 'College', 'EDUCATION', 'SCHOOL', 'COLLEGE'],
    'experience': ['EXPERIENCE', 'Experience', 'WORK EXPERIENCE', 'Work Experience'],
    'internship': ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships'],
    'skills': ['SKILLS', 'SKILL', 'Skills', 'Skill'],
    'hobbies': ['HOBBIES', 'Hobbies'],
    'interests': ['INTERESTS', 'Interests'],
    'achievements': ['ACHIEVEMENTS', 'Achievements'],
    'certifications': ['CERTIFICATIONS', 'Certifications', 'Certification'],
    'projects': ['PROJECTS', 'PROJECT', 'Projects', 'Project']
}

CANDIDATE_LEVEL_KEYWORDS = {
    'internship': ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships'],
    'experience': ['EXPERIENCE', 'WORK EXPERIENCE', 'Experience', 'Work Experience']
}

# Course data (simplified - only a few courses per field)
COURSE_DATA = {
    'Data Science': [
        ['Machine Learning by Andrew NG', 'https://www.coursera.org/learn/machine-learning'],
        ['Data Science Specialization', 'https://www.coursera.org/specializations/jhu-data-science'],
        ['Python for Data Science', 'https://www.edx.org/course/python-for-data-science'],
    ],
    'Web Development': [
        ['Django Crash Course [Free]', 'https://youtu.be/e1IyzVyrLSU'],
        ['Full Stack Web Developer by Udacity', 'https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044'],
        ['ReactJS Development Training', 'https://www.edureka.co/reactjs-redux-certification-training'],
    ],
    'Android Development': [
        ['Android Development for Beginners', 'https://www.udacity.com/course/android-development-for-beginners--ud837'],
        ['Android App Development', 'https://www.edx.org/professional-certificate/google-android-app-development'],
    ],
    'IOS Development': [
        ['iOS App Development with Swift', 'https://www.coursera.org/specializations/app-development'],
        ['iOS Development Course', 'https://www.udemy.com/course/ios-13-app-development-bootcamp/'],
    ],
    'UI-UX Development': [
        ['UI/UX Design Specialization', 'https://www.coursera.org/specializations/ui-ux-design'],
        ['User Experience Design Fundamentals', 'https://www.udemy.com/course/ui-ux-web-design-using-adobe-xd/'],
    ]
}


# Utility Functions

def check_section_presence(resume_text, section_keywords):
    """Check if any section keywords are present in resume text"""
    return any(keyword in resume_text for keyword in section_keywords)


def course_recommender(course_list, num_recommendations=5):
    """Select random courses from a course list"""
    rec_course = []
    random.shuffle(course_list)
    
    for c_name, c_link in course_list:
        rec_course.append({"name": c_name, "link": c_link})
        if len(rec_course) == num_recommendations:
            break
    
    return rec_course


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file object"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text, len(pdf_reader.pages)
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_email(text):
    """Extract email address from resume text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else ""


def extract_phone(text):
    """Extract phone number from resume text"""
    patterns = [
        r'\b\d{10}\b',
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b'
    ]
    for pattern in patterns:
        phones = re.findall(pattern, text)
        if phones:
            return phones[0]
    return ""


def extract_name(text):
    """Extract candidate name (first non-empty line usually)"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        return lines[0][:100]
    return ""


def extract_skills(text):
    """Extract skills from resume text using keyword matching"""
    skills = []
    text_lower = text.lower()
    
    all_keywords = (
        list(DS_KEYWORDS) + list(WEB_KEYWORDS) + 
        list(ANDROID_KEYWORDS) + list(IOS_KEYWORDS) + 
        list(UIUX_KEYWORDS)
    )
    
    for keyword in all_keywords:
        if keyword in text_lower and keyword not in skills:
            skills.append(keyword.capitalize())
    
    return skills[:15]


def detect_candidate_level(resume_text, num_pages):
    """Determine candidate's experience level"""
    if num_pages < 1:
        return "Fresher"
    
    if check_section_presence(resume_text, CANDIDATE_LEVEL_KEYWORDS['internship']):
        return "Intermediate"
    
    if check_section_presence(resume_text, CANDIDATE_LEVEL_KEYWORDS['experience']):
        return "Experienced"
    
    return "Fresher"


def predict_field_and_recommendations(skills):
    """Predict career field and provide recommendations"""
    if not skills:
        return 'NA', [], []
    
    for skill in skills:
        skill_lower = skill.lower()
        
        if skill_lower in DS_KEYWORDS:
            return (
                'Data Science',
                RECOMMENDED_SKILLS['Data Science'],
                course_recommender(COURSE_DATA['Data Science'])
            )
        elif skill_lower in WEB_KEYWORDS:
            return (
                'Web Development',
                RECOMMENDED_SKILLS['Web Development'],
                course_recommender(COURSE_DATA['Web Development'])
            )
        elif skill_lower in ANDROID_KEYWORDS:
            return (
                'Android Development',
                RECOMMENDED_SKILLS['Android Development'],
                course_recommender(COURSE_DATA['Android Development'])
            )
        elif skill_lower in IOS_KEYWORDS:
            return (
                'IOS Development',
                RECOMMENDED_SKILLS['IOS Development'],
                course_recommender(COURSE_DATA['IOS Development'])
            )
        elif skill_lower in UIUX_KEYWORDS:
            return (
                'UI-UX Development',
                RECOMMENDED_SKILLS['UI-UX Development'],
                course_recommender(COURSE_DATA['UI-UX Development'])
            )
    
    return 'NA', [], []


def calculate_resume_score(resume_text):
    """Calculate resume score based on key sections"""
    score = 0
    breakdown = []
    
    sections = [
        ('objective', 'Objective/Summary'),
        ('education', 'Education Details'),
        ('experience', 'Experience'),
        ('internship', 'Internships'),
        ('skills', 'Skills'),
        ('hobbies', 'Hobbies'),
        ('interests', 'Interests'),
        ('achievements', 'Achievements'),
        ('certifications', 'Certifications'),
        ('projects', 'Projects'),
    ]
    
    for key, label in sections:
        if check_section_presence(resume_text, SECTION_KEYWORDS[key]):
            score += SCORING_WEIGHTS[key]
            breakdown.append(f"[+] Added {label}")
        else:
            breakdown.append(f"[-] Missing {label}")
    
    return score, breakdown


def analyze_resume_simple(pdf_file):
    """
    Simplified resume analysis without pyresparser dependency
    
    Args:
        pdf_file: Django UploadedFile object (PDF)
    
    Returns:
        dict: Analysis results
    """
    try:
        # Extract text and page count
        resume_text, num_pages = extract_text_from_pdf(pdf_file)
        
        # Extract basic details
        name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)
        
        # Detect candidate level
        candidate_level = detect_candidate_level(resume_text, num_pages)
        
        # Predict field and get recommendations
        predicted_field, recommended_skills, recommended_courses = predict_field_and_recommendations(skills)
        
        # Calculate resume score
        resume_score, score_breakdown = calculate_resume_score(resume_text)
        
        # Compile results
        return {
            "basic_details": {
                "name": name,
                "email": email,
                "mobile_number": phone,
                "skills": skills,
                "no_of_pages": num_pages,
            },
            "candidate_level": candidate_level,
            "predicted_field": predicted_field,
            "recommended_skills": recommended_skills,
            "recommended_courses": recommended_courses,
            "resume_score": resume_score,
            "score_breakdown": score_breakdown
        }
    
    except Exception as e:
        raise Exception(f"Resume analysis failed: {str(e)}")

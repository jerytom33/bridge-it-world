"""
Configuration for Resume Analyzer Module

Contains keywords, scoring weights, and configurable parameters.
"""

# Field Detection Keywords
# These keywords are used to predict the career field based on resume skills

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

# Generic keywords that don't indicate a specific field
NON_SPECIFIC_KEYWORDS = [
    'english', 'communication', 'writing', 'microsoft office', 'leadership',
    'customer management', 'social media', 'teamwork', 'problem solving'
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
# Points awarded for each section present in the resume
SCORING_WEIGHTS = {
    'objective_summary': 6,
    'education': 12,
    'experience': 16,
    'internships': 6,
    'skills': 7,
    'hobbies': 4,
    'interests': 5,
    'achievements': 13,
    'certifications': 12,
    'projects': 19
}

# Candidate Level Detection Keywords
CANDIDATE_LEVEL_KEYWORDS = {
    'internship': ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships'],
    'experience': ['EXPERIENCE', 'WORK EXPERIENCE', 'Experience', 'Work Experience']
}

# Course Recommendations Configuration
DEFAULT_NUM_COURSE_RECOMMENDATIONS = 5

# Resume Section Keywords
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

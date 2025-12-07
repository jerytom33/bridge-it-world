"""
Utility Functions for Resume Analyzer

Provides helper functions for PDF reading and course recommendations.
"""

import io
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import random
from .config import DEFAULT_NUM_COURSE_RECOMMENDATIONS


def pdf_reader(file_path):
    """
    Extract text content from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If PDF reading fails
    """
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    
    return text


def course_recommender(course_list, num_recommendations=None):
    """
    Select random courses from a course list.
    
    Args:
        course_list (list): List of [course_name, course_link] pairs
        num_recommendations (int, optional): Number of courses to recommend.
                                            Defaults to DEFAULT_NUM_COURSE_RECOMMENDATIONS
        
    Returns:
        list: List of dictionaries with 'name' and 'link' keys
        
    Example:
        >>> courses = course_recommender(ds_course, 3)
        >>> print(courses[0])
        {'name': 'Machine Learning by Andrew NG', 'link': 'https://...'}
    """
    if num_recommendations is None:
        num_recommendations = DEFAULT_NUM_COURSE_RECOMMENDATIONS
    
    rec_course = []
    random.shuffle(course_list)
    
    for c_name, c_link in course_list:
        rec_course.append({"name": c_name, "link": c_link})
        if len(rec_course) == num_recommendations:
            break
    
    return rec_course


def check_section_presence(resume_text, section_keywords):
    """
    Check if any of the section keywords are present in the resume text.
    
    Args:
        resume_text (str): Full text content of the resume
        section_keywords (list): List of keywords to search for
        
    Returns:
        bool: True if any keyword is found, False otherwise
    """
    return any(keyword in resume_text for keyword in section_keywords)

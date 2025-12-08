"""
Resume Analyzer Module

A standalone Python module for analyzing resumes and providing recommendations.

This module extracts information from PDF resumes, predicts career fields,
recommends skills and courses, and scores resume quality.

Example:
    >>> from resume_analyzer import analyze_resume
    >>> result = analyze_resume('path/to/resume.pdf')
    >>> print(f"Score: {result['resume_score']}")
"""

__version__ = '1.0.0'
__author__ = 'Extracted from AI-Resume-Analyzer by Deepak Padhi'

from .analyzer import analyze_resume

__all__ = ['analyze_resume']

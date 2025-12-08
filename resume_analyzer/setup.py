"""
Setup script for resume_analyzer module
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='resume_analyzer',
    version='1.0.0',
    author='Extracted from AI-Resume-Analyzer',
    author_email='',
    description='A standalone Python module for analyzing resumes and providing recommendations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python ::3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)

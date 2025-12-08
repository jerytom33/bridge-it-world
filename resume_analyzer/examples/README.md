# Resume Analyzer Examples

This directory contains example scripts demonstrating how to use the resume_analyzer module.

## Files

### basic_usage.py
A simple standalone example showing the most basic way to use the module. Run with:
```bash
python basic_usage.py
```
Make sure to update the `resume_path` variable to point to your PDF resume.

### django_integration.py
Complete Django integration example including:
- Models for storing analysis results
- Views for handling file upload and displaying results
- URL configuration
- Admin panel setup
- Template examples

This file serves as a reference guide - copy the relevant sections into your Django project.

### batch_processing.py
Script for processing multiple resumes at once. Usage:
```bash
python batch_processing.py <directory_path> [output_file]
```

Example:
```bash
python batch_processing.py ./resumes results.json
```

This will:
- Analyze all PDF files in the directory
- Save detailed results to JSON
- Generate a summary report with statistics

## Getting Started

1. Make sure the module is installed:
```bash
cd ..
pip install -r requirements.txt
```

2. Download required models:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
```

3. Run an example:
```bash
cd examples
python basic_usage.py
```

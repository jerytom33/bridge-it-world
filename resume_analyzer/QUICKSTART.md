# Quick Start Guide for Resume Analyzer Module

This guide will help you get started with the resume_analyzer module.

## Installation Steps

### 1. Navigate to the module directory
```bash
cd resume_analyzer
```

### 2. Install in development mode (recommended for local use)
```bash
pip install -e .
```

Or install normally:
```bash
pip install .
```

### 3. Download required models
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
```

## Quick Test

After installation, test the module:

```bash
python tests/test_analyzer.py
```

## Basic Usage

Create a test script `test.py`:

```python
from resume_analyzer import analyze_resume

result = analyze_resume('path/to/your/resume.pdf')
print(f"Name: {result['basic_details']['name']}")
print(f"Score: {result['resume_score']}/100")
print(f"Field: {result['predicted_field']}")
```

Run it:
```bash
python test.py
```

## Using in Django

1. Install the module in your Django project's virtual environment
2. See `examples/django_integration.py` for complete integration code
3. Copy the models, views, and templates into your Django app

## Directory Structure

```
resume_analyzer/
├── __init__.py           # Main API export
├── analyzer.py           # Core analysis logic
├── courses.py            # Course recommendations
├── config.py             # Configuration & keywords
├── utils.py              # Utility functions
├── requirements.txt      # Dependencies
├── setup.py              # Installation script
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── examples/             # Usage examples
│   ├── basic_usage.py
│   ├── django_integration.py
│   └── batch_processing.py
└── tests/                # Test files
    └── test_analyzer.py
```

## Troubleshooting

### Import Error

If you get "No module named 'resume_analyzer'":
- Make sure you installed the module: `pip install -e .`
- Or add the parent directory to PYTHONPATH

### PyResParser Errors

If you encounter spaCy compatibility issues:
```bash
pip install spacy==2.3.5
python -m spacy download en_core_web_sm
```

### PDF Reading Errors

- Make sure the PDF is not password-protected
- The PDF must contain extractable text (not scanned images)

## Next Steps

- Read the full [README.md](README.md) for complete documentation
- Check out the [examples](examples/) directory
- Review the [Django integration example](examples/django_integration.py)

## Support

For issues related to:
- **pyresparser**: Check the [pyresparser GitHub](https://github.com/OmkarPathak/pyresparser)
- **spaCy**: See [spaCy documentation](https://spacy.io/usage)
- **Module issues**: Review the original [AI-Resume-Analyzer](https://github.com/dnoobnerd/AI-Resume-Analyzer)

# Installing Resume Analyzer Module

There are two ways to use this module:

## Option 1: Use with Existing Virtual Environment (Recommended)

Since the dependencies are already installed in the main project's virtual environment, you can simply add the module path to your Django project:

### Step 1: Activate the existing venv
```bash
# On Windows
l:\ALTASH\AI-Resume-Analyzer\venv\Scripts\Activate.ps1

# On Linux/Mac
source l:/ALTASH/AI-Resume-Analyzer/venv/bin/activate
```

### Step 2: Add module to PYTHONPATH in your Django settings.py
```python
import sys
import os

# Add resume_analyzer module to path
MODULE_PATH = r'l:\ALTASH\AI-Resume-Analyzer'
if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)
```

### Step 3: Use the module
```python
from resume_analyzer import analyze_resume

result = analyze_resume('path/to/resume.pdf')
```

## Option 2: Standalone Installation

If you want to install in a different environment:

### Requirements
- Python 3.7+
- Microsoft Visual C++ 14.0+ Build Tools (for Windows)
  - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Installation Steps
```bash
# Navigate to module directory
cd resume_analyzer

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('stopwords')"

# Install module in development mode
pip install -e .
```

### Troubleshooting Build Issues

If you encounter errors building `blis` or other C extensions:

**Option A: Use pre-built wheels**
```bash
# Use existing venv that already has packages
# See Option 1 above
```

**Option B: Install build tools (Windows)**
1. Download Microsoft C++ Build Tools
2. Install with "Desktop development with C++" workload
3. Retry `pip install -r requirements.txt`

**Option C: Use conda** (easier on Windows)
```bash
conda create -n resume_analyzer python=3.9
conda activate resume_analyzer
conda install -c conda-forge spacy
pip install pyresparser pdfminer3
python -m spacy download en_core_web_sm
```

## Quickest Way to Test

Use the existing venv with sample code:

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Create test script
cd resume_analyzer
```

Create `test_quick.py`:
```python
import sys
sys.path.insert(0, '..')

from resume_analyzer import analyze_resume
import os

# Use a sample resume from App
sample = '../App/Uploaded_Resumes/[filename].pdf'
if os.path.exists(sample):
    result = analyze_resume(sample)
    print(f"Name: {result['basic_details']['name']}")
    print(f"Score: {result['resume_score']}/100")
else:
    print("No sample resume found")
```

Run:
```bash
python test_quick.py
```

## For Django Integration

Since your Django project likely has its own virtual environment:

1. **Copy the module** to your Django project:
   ```bash
   cp -r resume_analyzer /path/to/your/django/project/
   ```

2. **Ensure dependencies** are in your Django requirements.txt:
   ```
   pyresparser==1.0.6
   pdfminer3==2018.12.3.0
   spacy==2.3.5
   nltk==3.7
   docx2txt==0.8
   ```

3. **Install** in your Django venv:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Import and use** in your views:
   ```python
   from resume_analyzer import analyze_resume
   ```

See `examples/django_integration.py` for complete Django integration code.

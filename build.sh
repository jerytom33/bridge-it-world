#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "======================================"
echo "Starting BridgeIT Backend Build Process"
echo "======================================"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy language model for resume analyzer
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm || echo "Warning: spaCy model download failed, continuing..."

# Download NLTK data for resume parsing
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')" || echo "Warning: NLTK data download failed, continuing..."

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p staticfiles_build/static
mkdir -p media/resumes
mkdir -p media/profile_pictures

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

echo "======================================"
echo "Build process completed successfully!"
echo "======================================"

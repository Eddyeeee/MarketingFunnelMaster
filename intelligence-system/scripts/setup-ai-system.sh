#!/bin/bash

# Setup script for Python AI Research System
echo "🐍 Setting up Python AI Research System..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
cd ai-research
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Download SpaCy model
echo "🔤 Downloading SpaCy language model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "📊 Downloading NLTK data..."
python -c "
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
print('✅ NLTK data downloaded')
"

echo "✅ Python AI Research System setup complete!"
echo ""
echo "To activate the environment manually:"
echo "cd ai-research && source venv/bin/activate"
echo ""
echo "To start the AI system:"
echo "npm run start:ai"
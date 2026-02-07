#!/bin/bash
# Quick setup script for AI Memory System

echo "🧠 AI Memory System Setup"
echo "========================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Install requirements
echo
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

# Check API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo
    echo "⚠️  GEMINI_API_KEY not set!"
    echo
    echo "Get a free API key from:"
    echo "  https://aistudio.google.com/app/apikey"
    echo
    echo "Then run:"
    echo "  export GEMINI_API_KEY='your-key-here'"
    echo
    echo "Or add to ~/.bashrc:"
    echo "  echo 'export GEMINI_API_KEY=\"your-key\"' >> ~/.bashrc"
else
    echo "✅ GEMINI_API_KEY is set"
fi

# Make scripts executable
chmod +x scripts/memory
chmod +x scripts/gemini-compress.py

echo
echo "📁 Creating memory directory..."
mkdir -p ~/memory/index/embeddings

echo
echo "✅ Setup complete!"
echo
echo "Quick start:"
echo "  python3 scripts/gemini-compress.py compress 'Your first memory'"
echo "  python3 scripts/gemini-compress.py search 'find something'"
echo "  python3 scripts/gemini-compress.py list"
echo
echo "Or use the shortcut:"
echo "  ./scripts/memory compress 'Your text'"

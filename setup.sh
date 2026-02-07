#!/bin/bash
#
# AI Memory System - Quick Setup
# https://github.com/jamesarslan/ai-memory-system
#

set -e

echo "🧠 AI Memory System - Setup"
echo "==========================="
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    echo "   Install it from https://www.python.org/ or your package manager"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Check/install requests
if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}Installing requests library...${NC}"
    pip3 install requests --quiet
fi
echo -e "${GREEN}✓${NC} requests library available"

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo
    echo -e "${YELLOW}⚠️  GEMINI_API_KEY not set${NC}"
    echo
    echo "Get a free API key from: https://aistudio.google.com/app/apikey"
    echo
    read -p "Enter your Gemini API key (or press Enter to skip): " api_key
    
    if [ -n "$api_key" ]; then
        # Detect shell
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        else
            SHELL_RC="$HOME/.bashrc"
        fi
        
        echo "export GEMINI_API_KEY=\"$api_key\"" >> "$SHELL_RC"
        export GEMINI_API_KEY="$api_key"
        echo -e "${GREEN}✓${NC} API key added to $SHELL_RC"
    else
        echo -e "${YELLOW}⚠️  Skipping API key setup. Set GEMINI_API_KEY later.${NC}"
    fi
else
    echo -e "${GREEN}✓${NC} GEMINI_API_KEY is set"
fi

# Create symlink
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/scripts/gemini-compress.py"

echo
echo "Creating 'memory' command..."

if [ -w /usr/local/bin ]; then
    # Can write to /usr/local/bin
    ln -sf "$SCRIPT_PATH" /usr/local/bin/memory
    echo -e "${GREEN}✓${NC} Created symlink: /usr/local/bin/memory"
elif command -v sudo &> /dev/null; then
    # Need sudo
    sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/memory
    echo -e "${GREEN}✓${NC} Created symlink: /usr/local/bin/memory (with sudo)"
else
    # Fallback to alias
    SHELL_RC="${SHELL_RC:-$HOME/.bashrc}"
    echo "alias memory='python3 $SCRIPT_PATH'" >> "$SHELL_RC"
    echo -e "${GREEN}✓${NC} Created alias in $SHELL_RC"
fi

# Create memory directories
mkdir -p ~/memory/index/embeddings
mkdir -p ~/memory/index/topics
echo -e "${GREEN}✓${NC} Created ~/memory/index/"

# Verify installation
echo
echo "Verifying installation..."
if [ -n "$GEMINI_API_KEY" ]; then
    if python3 "$SCRIPT_PATH" list &>/dev/null; then
        echo -e "${GREEN}✓${NC} Installation verified!"
    else
        echo -e "${YELLOW}⚠️  Could not verify. Check API key and try again.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Set GEMINI_API_KEY to complete verification.${NC}"
fi

# Print success message
echo
echo "========================================"
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo "========================================"
echo
echo "Quick start:"
echo "  memory compress \"We decided to use PostgreSQL for the project.\""
echo "  memory search \"database choice\""
echo "  memory list"
echo
echo "Documentation: https://github.com/jamesarslan/ai-memory-system"
echo
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}Remember to set GEMINI_API_KEY and restart your shell.${NC}"
    echo
fi

# Reload shell hint
if [ -n "$SHELL_RC" ]; then
    echo "Run 'source $SHELL_RC' or restart your terminal to use the 'memory' command."
fi

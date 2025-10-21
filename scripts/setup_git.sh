#!/bin/bash

echo "AI Information Extraction Tool - Git Setup"
echo "=========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git first."
    echo "Installation instructions:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  macOS: brew install git"
    echo "  Or download from: https://git-scm.com/downloads"
    exit 1
fi

echo "Git is installed. Proceeding with setup..."

# Initialize git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "Git repository initialized."
else
    echo "Git repository already exists."
fi

# Add all files
echo "Adding files to Git..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: AI Information Extraction Tool"

echo ""
echo "=========================================="
echo "Git setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository at https://github.com/new"
echo "2. Copy the repository URL"
echo "3. Run these commands:"
echo "   git remote add origin YOUR_REPOSITORY_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Or run: python scripts/setup_git.py --github-url YOUR_REPOSITORY_URL"
echo ""

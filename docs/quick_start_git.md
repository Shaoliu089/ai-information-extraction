# Quick Start: Git and GitHub Setup

This is a quick guide to get your AI Information Extraction Tool project on GitHub for version control and remote testing.

## 🚀 Quick Setup (Choose One)

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
python scripts/setup_git.py

# Follow the instructions to create GitHub repository
# Then run with your repository URL:
python scripts/setup_git.py --github-url https://github.com/your-username/ai-information-extraction.git
```

### Option 2: Windows Batch Script
```cmd
# Double-click or run:
scripts\setup_git.bat
```

### Option 3: Linux/macOS Shell Script
```bash
# Make executable and run:
chmod +x scripts/setup_git.sh
./scripts/setup_git.sh
```

## 📋 Manual Setup (Step by Step)

### 1. Initialize Git Repository
```bash
# Navigate to your project directory
cd activity_project

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Information Extraction Tool"
```

### 2. Create GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click **"+"** → **"New repository"**
3. Repository name: `ai-information-extraction`
4. Description: `AI tool for information extraction from text notes using open-source LLMs`
5. **Important**: Don't initialize with README, .gitignore, or license
6. Click **"Create repository"**

### 3. Connect to GitHub
```bash
# Add GitHub remote (replace with your URL)
git remote add origin https://github.com/your-username/ai-information-extraction.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## 🔄 Daily Development Workflow

### Start New Feature
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... edit files ...

# Stage and commit
git add .
git commit -m "feat: add your feature description"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Update from Remote
```bash
# Pull latest changes
git checkout main
git pull origin main
```

## 🛠️ Prerequisites

### Install Git
- **Windows**: Download from [git-scm.com](https://git-scm.com/downloads)
- **macOS**: `brew install git`
- **Linux**: `sudo apt install git`

### Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📁 What Gets Uploaded

The following files will be included in your GitHub repository:
- ✅ **Source code**: All Python modules and scripts
- ✅ **Documentation**: README, guides, and docs
- ✅ **Configuration**: Model configs and settings
- ✅ **Dependencies**: requirements.txt and setup.py
- ❌ **Large files**: Model files, data files (excluded by .gitignore)
- ❌ **Cache files**: Python cache, temporary files
- ❌ **Sensitive data**: API keys, personal information

## 🔒 Security Features

### .gitignore Protection
Your `.gitignore` file automatically excludes:
- Model files (large binary files)
- Data files (training/test data)
- Cache and temporary files
- Environment files
- OS-specific files

### Safe for Public Repositories
- No sensitive information included
- No API keys or secrets
- No personal data
- Only source code and documentation

## 🎯 Benefits of GitHub Setup

### 1. **Version Control**
- Track all changes to your code
- Rollback to previous versions
- See what changed and when

### 2. **Remote Backup**
- Your code is safely stored on GitHub
- Access from anywhere
- Never lose your work

### 3. **Collaboration**
- Share with team members
- Code review process
- Issue tracking and project management

### 4. **Testing & Deployment**
- GitHub Actions for automated testing
- Easy deployment to cloud platforms
- Integration with CI/CD pipelines

### 5. **Documentation**
- README files for project description
- Wiki for detailed documentation
- Issue tracking for bugs and features

## 🚨 Troubleshooting

### Common Issues

#### "Git is not installed"
```bash
# Install Git first, then retry
# Windows: Download from git-scm.com
# macOS: brew install git
# Linux: sudo apt install git
```

#### "Authentication failed"
```bash
# Use personal access token instead of password
# Go to GitHub Settings > Developer settings > Personal access tokens
# Create new token and use it as password
```

#### "Repository already exists"
```bash
# Remove existing remote
git remote remove origin
# Add new remote
git remote add origin https://github.com/your-username/ai-information-extraction.git
```

### Useful Commands
```bash
# Check status
git status

# View changes
git diff

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Check remote repositories
git remote -v
```

## 📚 Next Steps After Setup

1. **Explore GitHub Features**
   - Issues: Track bugs and feature requests
   - Projects: Organize tasks and milestones
   - Actions: Set up automated testing
   - Wiki: Create detailed documentation

2. **Set Up Development Environment**
   - Install dependencies: `pip install -r requirements.txt`
   - Download models: `python scripts/download_models.py --all`
   - Run tests: `python main.py`

3. **Start Development**
   - Create feature branches for new work
   - Use pull requests for code review
   - Follow the development workflow

4. **Collaboration**
   - Invite team members to the repository
   - Set up branch protection rules
   - Configure automated testing

## 🎉 Success!

Once you've completed the setup, you'll have:
- ✅ Git repository with version control
- ✅ GitHub repository for remote access
- ✅ All your code safely backed up
- ✅ Ready for collaboration and deployment
- ✅ Professional development workflow

Your AI Information Extraction Tool is now ready for remote testing, version control, and collaboration! 🚀

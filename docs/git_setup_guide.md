# Git and GitHub Setup Guide

This guide will help you set up Git version control and upload your AI Information Extraction Tool to GitHub for remote testing and collaboration.

## Prerequisites

### 1. Install Git
- **Windows**: Download from [git-scm.com](https://git-scm.com/downloads)
- **macOS**: Install via Homebrew: `brew install git`
- **Linux**: Install via package manager: `sudo apt install git` (Ubuntu/Debian)

### 2. Create GitHub Account
- Go to [github.com](https://github.com) and create an account
- Verify your email address

### 3. Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Quick Setup (Automated)

### Option 1: Use the Setup Script
```bash
# Run the automated setup script
python scripts/setup_git.py

# Follow the instructions to create GitHub repository
# Then run with your repository URL:
python scripts/setup_git.py --github-url https://github.com/your-username/ai-information-extraction.git
```

## Manual Setup (Step by Step)

### Step 1: Initialize Git Repository

```bash
# Navigate to your project directory
cd activity_project

# Initialize Git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: AI Information Extraction Tool"
```

### Step 2: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click the '+' button** in the top right corner
3. **Select 'New repository'**
4. **Fill in repository details:**
   - Repository name: `ai-information-extraction`
   - Description: `AI tool for information extraction from text notes using open-source LLMs`
   - Visibility: Public or Private (your choice)
   - **Important**: DO NOT initialize with README, .gitignore, or license (we already have these)
5. **Click 'Create repository'**

### Step 3: Connect Local Repository to GitHub

```bash
# Add GitHub remote (replace with your actual repository URL)
git remote add origin https://github.com/your-username/ai-information-extraction.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## Development Workflow

### Daily Development Process

```bash
# 1. Check current status
git status

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... edit files ...

# 4. Stage changes
git add .

# 5. Commit changes
git commit -m "feat: add your feature description"

# 6. Push to GitHub
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

### Branching Strategy

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/*`**: Feature development branches
- **`bugfix/*`**: Bug fix branches
- **`hotfix/*`**: Critical bug fixes

### Example Workflow

```bash
# Start new feature
git checkout -b feature/add-new-model

# Make changes
# ... edit code ...

# Commit changes
git add .
git commit -m "feat: add support for new model X"

# Push feature branch
git push origin feature/add-new-model

# Create Pull Request on GitHub
# After review and approval, merge to main
```

## Collaboration Features

### 1. Issues and Bug Tracking
- **Create issues** for bugs and feature requests
- **Assign labels** (bug, enhancement, documentation)
- **Assign to team members**
- **Link to pull requests**

### 2. Pull Requests
- **Code review** process
- **Automated testing** (if set up)
- **Discussion and feedback**
- **Merge after approval**

### 3. Project Management
- **GitHub Projects** for task management
- **Milestones** for version planning
- **Labels** for categorization

## Advanced Git Features

### 1. Stashing Changes
```bash
# Save current work without committing
git stash

# Apply stashed changes
git stash pop

# List stashes
git stash list
```

### 2. Branch Management
```bash
# List all branches
git branch -a

# Switch between branches
git checkout branch-name

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name
```

### 3. Merging and Rebasing
```bash
# Merge feature branch into main
git checkout main
git merge feature/your-feature

# Rebase feature branch onto main
git checkout feature/your-feature
git rebase main
```

## GitHub Actions (CI/CD)

### Set up Automated Testing
Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/
    - name: Check code style
      run: |
        black --check .
        flake8 .
```

## Security and Access Control

### 1. Repository Settings
- **Visibility**: Public or Private
- **Branch protection**: Require reviews for main branch
- **Security alerts**: Enable Dependabot
- **Access control**: Manage team permissions

### 2. SSH Keys (Recommended)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and paste into GitHub Settings > SSH and GPG keys
```

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
```bash
# Use personal access token instead of password
git remote set-url origin https://username:token@github.com/username/repo.git
```

#### 2. Merge Conflicts
```bash
# Resolve conflicts in files
# Then stage resolved files
git add resolved-file.txt
git commit -m "resolve merge conflict"
```

#### 3. Large Files
```bash
# Add large files to .gitignore
echo "large-file.bin" >> .gitignore
git rm --cached large-file.bin
git commit -m "remove large file"
```

### Useful Commands

```bash
# View commit history
git log --oneline

# View file changes
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# View remote repositories
git remote -v

# Update from remote
git fetch origin
git pull origin main
```

## Best Practices

### 1. Commit Messages
- Use clear, descriptive messages
- Follow conventional commit format: `type: description`
- Examples: `feat: add new model`, `fix: resolve parsing error`, `docs: update README`

### 2. Branch Naming
- Use descriptive names: `feature/add-mistral-support`
- Include type prefix: `feature/`, `bugfix/`, `hotfix/`
- Use kebab-case: `add-new-model` not `addNewModel`

### 3. Code Quality
- Run tests before committing
- Check code style with `black` and `flake8`
- Update documentation for new features
- Keep commits focused and atomic

### 4. Collaboration
- Always pull latest changes before starting work
- Create feature branches for new work
- Use pull requests for code review
- Communicate changes in commit messages

## Next Steps

1. **Set up the repository** using the steps above
2. **Invite collaborators** if working in a team
3. **Configure branch protection** for the main branch
4. **Set up GitHub Actions** for automated testing
5. **Create issues** for planned features and bugs
6. **Start development** using the workflow described above

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Documentation](https://docs.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub CLI](https://cli.github.com/) (optional but useful)

Happy coding! 🚀

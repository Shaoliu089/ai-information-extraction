@echo off
echo AI Information Extraction Tool - Git Setup
echo ==========================================

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed. Please install Git first.
    echo Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git is installed. Proceeding with setup...

REM Initialize git repository if it doesn't exist
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo Git repository initialized.
) else (
    echo Git repository already exists.
)

REM Add all files
echo Adding files to Git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: AI Information Extraction Tool"

echo.
echo ==========================================
echo Git setup complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Create a GitHub repository at https://github.com/new
echo 2. Copy the repository URL
echo 3. Run these commands:
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo Or run: python scripts/setup_git.py --github-url YOUR_REPOSITORY_URL
echo.
pause

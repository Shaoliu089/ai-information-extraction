"""
Script to set up Git repository and GitHub integration.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {description}: {e.stderr}")
        return None


def setup_git_repository():
    """Set up Git repository with initial commit."""
    print("Setting up Git repository...")
    
    # Initialize git repository
    if not Path(".git").exists():
        run_command("git init", "Initialize Git repository")
    else:
        print("Git repository already exists")
    
    # Add all files
    run_command("git add .", "Add all files to staging")
    
    # Create initial commit
    run_command('git commit -m "Initial commit: AI Information Extraction Tool"', "Create initial commit")
    
    print("✓ Git repository setup complete")


def setup_github_remote(repo_url=None):
    """Set up GitHub remote repository."""
    if repo_url:
        print(f"Setting up GitHub remote: {repo_url}")
        run_command(f"git remote add origin {repo_url}", "Add GitHub remote")
        run_command("git branch -M main", "Set main branch")
        run_command("git push -u origin main", "Push to GitHub")
        print("✓ GitHub remote setup complete")
    else:
        print("No GitHub URL provided. You can add it later with:")
        print("git remote add origin https://github.com/your-username/your-repo.git")
        print("git push -u origin main")


def create_github_repo_instructions():
    """Print instructions for creating GitHub repository."""
    print("\n" + "="*60)
    print("GITHUB REPOSITORY SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("1. Go to https://github.com and sign in to your account")
    print("2. Click the '+' button in the top right corner")
    print("3. Select 'New repository'")
    print("4. Fill in the repository details:")
    print("   - Repository name: ai-information-extraction")
    print("   - Description: AI tool for information extraction from text notes using open-source LLMs")
    print("   - Visibility: Public or Private (your choice)")
    print("   - DO NOT initialize with README, .gitignore, or license (we already have these)")
    print("5. Click 'Create repository'")
    print("6. Copy the repository URL (it will look like: https://github.com/your-username/ai-information-extraction.git)")
    print("7. Run this script again with the repository URL:")
    print("   python scripts/setup_git.py --github-url https://github.com/your-username/ai-information-extraction.git")
    print()


def main():
    """Main function to set up Git and GitHub."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up Git repository and GitHub integration")
    parser.add_argument("--github-url", type=str, help="GitHub repository URL")
    parser.add_argument("--create-instructions", action="store_true", help="Show GitHub repository creation instructions")
    
    args = parser.parse_args()
    
    if args.create_instructions:
        create_github_repo_instructions()
        return
    
    print("AI Information Extraction Tool - Git Setup")
    print("="*50)
    
    # Check if git is installed
    if run_command("git --version", "Check Git installation") is None:
        print("Error: Git is not installed. Please install Git first.")
        print("Download from: https://git-scm.com/downloads")
        return
    
    # Set up Git repository
    setup_git_repository()
    
    # Set up GitHub remote if URL provided
    if args.github_url:
        setup_github_remote(args.github_url)
    else:
        create_github_repo_instructions()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print()
    print("Next steps:")
    print("1. If you haven't created a GitHub repository yet, follow the instructions above")
    print("2. Add your GitHub remote:")
    print("   git remote add origin https://github.com/your-username/ai-information-extraction.git")
    print("3. Push your code:")
    print("   git push -u origin main")
    print()
    print("For development workflow:")
    print("- Create feature branches: git checkout -b feature/your-feature-name")
    print("- Make changes and commit: git add . && git commit -m 'your message'")
    print("- Push changes: git push origin feature/your-feature-name")
    print("- Create pull requests on GitHub")
    print()


if __name__ == "__main__":
    main()

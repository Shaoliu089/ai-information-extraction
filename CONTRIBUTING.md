# Contributing to AI Information Extraction Tool

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the AI Information Extraction Tool.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- CUDA-compatible GPU (recommended for model testing)
- 8GB+ RAM (for local model deployment)

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ai-information-extraction.git
   cd ai-information-extraction
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest black flake8 jupyter
   ```

## Development Workflow

### Branching Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Critical bug fixes

### Creating a New Feature

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code style
   black --check .
   flake8 .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Code Formatting
```bash
# Format code with black
black .

# Check for style issues
flake8 .
```

### Documentation
- Update README.md for significant changes
- Add docstrings to new functions/classes
- Update type hints for new code
- Include examples in docstrings

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=src tests/
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### Example Test Structure
```python
def test_model_loading():
    """Test that models can be loaded successfully."""
    # Arrange
    model_name = "llama2_7b"
    
    # Act
    model = ModelLoader().load_model(model_name)
    
    # Assert
    assert model is not None
    assert model.model is not None
```

## Pull Request Process

### Before Submitting
1. **Test your changes thoroughly**
2. **Update documentation**
3. **Add tests for new functionality**
4. **Ensure all tests pass**
5. **Check code style compliance**

### Pull Request Template
When creating a pull request, please include:

- **Description**: What changes were made and why
- **Type of change**: Bug fix, feature, documentation, etc.
- **Testing**: How the changes were tested
- **Checklist**: Ensure all items are completed

### Review Process
1. **Automated checks** must pass (tests, linting)
2. **Code review** by maintainers
3. **Approval** from at least one maintainer
4. **Merge** after approval

## Issue Reporting

### Bug Reports
When reporting bugs, please include:
- **Description** of the bug
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** and logs

### Feature Requests
For feature requests, please include:
- **Use case** and motivation
- **Proposed solution**
- **Alternatives considered**
- **Additional context**

## Model Contributions

### Adding New Models
1. **Update model configurations** in `config/model_configs.yaml`
2. **Add model-specific handling** if needed
3. **Test model loading and inference**
4. **Update documentation**

### Model Requirements
- Must be open-source
- Should support local deployment
- Should be reasonably sized (< 20GB)
- Must have good performance on the task

## Documentation

### Updating Documentation
- **README.md**: Main project documentation
- **docs/**: Detailed documentation
- **Code comments**: Inline documentation
- **Type hints**: Function signatures

### Documentation Standards
- Use clear, concise language
- Include code examples
- Keep documentation up-to-date
- Use markdown formatting consistently

## Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
1. **Update version numbers**
2. **Update CHANGELOG.md**
3. **Run full test suite**
4. **Create release notes**
5. **Tag the release**
6. **Update documentation**

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

### Communication
- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Pull Requests**: Use PRs for code changes
- **Email**: For sensitive or private matters

## Getting Help

### Resources
- **Documentation**: Check the docs/ directory
- **Examples**: Look at the notebooks/ directory
- **Issues**: Search existing issues
- **Discussions**: Ask questions in GitHub discussions

### Contact
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Email**: For private or sensitive matters

## Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to the AI Information Extraction Tool!

# Changelog

All notable changes to the AI Information Extraction Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Model loading and inference framework
- Evaluation metrics and comparison tools
- Prompt engineering templates
- Data processing utilities
- Jupyter notebook for performance analysis

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.0] - 2024-01-XX

### Added
- **Core Framework**
  - Multi-model support for open-source LLMs
  - Local deployment with memory optimization
  - Comprehensive evaluation framework
  - Advanced prompt engineering system

- **Model Support**
  - Llama 2 7B
  - Mistral 7B
  - Phi-3 3.8B
  - Gemma 7B
  - Qwen 7B

- **Evaluation Metrics**
  - Field-level accuracy (exact match, normalized match, partial match)
  - Document-level success rates
  - Performance metrics (processing time, memory usage)
  - Statistical analysis tools

- **Prompt Templates**
  - Zero-shot prompting
  - Few-shot prompting
  - Chain-of-thought prompting
  - Role-based prompting
  - Format-emphasis prompting

- **Data Processing**
  - Text cleaning and normalization
  - Date format standardization
  - JSON output validation
  - Error handling and recovery

- **Tools and Utilities**
  - Model download script
  - Command-line interface
  - Jupyter notebook for analysis
  - Visualization tools
  - Comparison reports

- **Documentation**
  - Comprehensive README
  - API documentation
  - Usage examples
  - Contributing guidelines

### Features
- **Information Extraction**: Extract structured data from unstructured text
- **Model Comparison**: Compare performance across different LLMs
- **Template Testing**: Test different prompt engineering strategies
- **Performance Analysis**: Detailed metrics and visualization
- **Local Deployment**: Privacy-focused local model execution

### Target Use Case
- Extract employee record information from text notes
- Support for fields: LastDayWorked, FirstDayMissed, DeliveryDate, ReturnToWork
- JSON output format for structured data
- High accuracy and reliability requirements

### Performance Targets
- Overall Accuracy: >85% for field extraction
- Processing Speed: <5 seconds per document
- Memory Usage: <8GB RAM for model deployment
- Reliability: >95% successful JSON parsing

### Installation
```bash
# Clone repository
git clone https://github.com/your-username/ai-information-extraction.git
cd ai-information-extraction

# Install dependencies
pip install -r requirements.txt

# Download models
python scripts/download_models.py --all
```

### Usage
```bash
# Single extraction
python main.py --mode extract --model llama2_7b --text "your text here"

# Model evaluation
python main.py --mode evaluate --model llama2_7b

# Model comparison
python main.py --mode compare --models llama2_7b mistral_7b
```

### API Usage
```python
from models.inference import InformationExtractor

extractor = InformationExtractor("llama2_7b")
result = extractor.extract("your text here")
```

## [0.1.0] - 2024-01-XX

### Added
- Initial project setup
- Basic project structure
- Core documentation
- Development environment setup

# AI Information Extraction Tool - Project Summary

## Project Overview

This project provides a comprehensive framework for evaluating and comparing different open-source Large Language Models (LLMs) for information extraction tasks. The tool is specifically designed to extract structured information from unstructured text notes related to employee records and administrative documentation.

## Key Features

### 1. **Multi-Model Support**
- Support for 5+ open-source LLMs (Llama 2, Mistral, Phi-3, Gemma, Qwen)
- Local deployment with memory optimization
- Quantization support (4-bit/8-bit) for efficient inference

### 2. **Comprehensive Evaluation Framework**
- Field-level accuracy metrics (exact match, normalized match, partial match)
- Document-level success rates
- Performance metrics (processing time, memory usage)
- Statistical analysis and comparison tools

### 3. **Advanced Prompt Engineering**
- 5 different prompt templates (zero-shot, few-shot, chain-of-thought, role-based, format-emphasis)
- Template performance comparison
- Custom prompt creation capabilities

### 4. **Robust Data Processing**
- Text cleaning and normalization
- Date format standardization
- JSON output validation
- Error handling and recovery

## Project Structure

```
activity_project/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── setup.py                    # Package setup
├── main.py                     # Main execution script
├── config/
│   └── model_configs.yaml      # Model configurations
├── docs/
│   ├── extraction_process.md   # Process design document
│   └── project_summary.md     # This summary
├── models/
│   ├── model_loader.py        # Model loading utilities
│   ├── prompt_templates.py    # Prompt templates
│   └── inference.py          # Inference pipeline
├── utils/
│   ├── text_processor.py      # Text preprocessing
│   ├── json_parser.py        # Output parsing
│   └── data_loader.py        # Data loading utilities
├── evaluation/
│   ├── metrics.py            # Evaluation metrics
│   ├── evaluator.py          # Main evaluator
│   └── comparison.py         # Model comparison tools
├── scripts/
│   └── download_models.py    # Model download script
└── notebooks/
    └── performance_analysis.ipynb  # Analysis notebook
```

## Target Use Case

### Input Example:
```
"last day worked 04/25/2023 full shift
first day missed 04/26/2023 induced tomorrow
employee returned to work august 1
advice caller paperwork pending delivery date 05/16/2023"
```

### Expected Output:
```json
{
  "LastDayWorked": "4/25/23",
  "FirstDayMissed": "4/26/23",
  "DeliveryDate": "5/16/23",
  "ReturnToWork": "8/1/23"
}
```

## Key Components

### 1. **Model Loading System**
- Automatic model downloading from Hugging Face
- Memory-efficient loading with quantization
- Support for multiple model formats
- Configuration management

### 2. **Information Extraction Pipeline**
- Text preprocessing and cleaning
- Prompt formatting and generation
- Model inference with error handling
- Output parsing and validation

### 3. **Evaluation Framework**
- Comprehensive metrics calculation
- Statistical analysis tools
- Performance benchmarking
- Visualization capabilities

### 4. **Comparison Tools**
- Model performance comparison
- Template effectiveness analysis
- Speed vs accuracy trade-offs
- Resource usage analysis

## Usage Examples

### Basic Extraction
```python
from models.inference import InformationExtractor

extractor = InformationExtractor("llama2_7b")
result = extractor.extract("your text here")
```

### Model Comparison
```python
from evaluation.evaluator import InformationExtractionEvaluator

evaluator = InformationExtractionEvaluator()
results = evaluator.evaluate_multiple_models(
    ["llama2_7b", "mistral_7b"], 
    test_data
)
```

### Command Line Usage
```bash
# Single extraction
python main.py --mode extract --model llama2_7b --text "your text here"

# Model evaluation
python main.py --mode evaluate --model llama2_7b

# Model comparison
python main.py --mode compare --models llama2_7b mistral_7b
```

## Evaluation Metrics

### 1. **Field-Level Metrics**
- **Exact Match**: Perfect field extraction
- **Normalized Match**: Correct information with format differences
- **Partial Match**: Contains same date information
- **Precision/Recall**: Standard classification metrics

### 2. **Document-Level Metrics**
- **Complete Success**: All fields correctly extracted
- **Partial Success**: Some fields correctly extracted
- **Completeness**: Percentage of fields successfully extracted

### 3. **Performance Metrics**
- **Processing Time**: Average inference time per document
- **Memory Usage**: Peak memory consumption
- **Success Rate**: Percentage of successful extractions
- **Error Analysis**: Common failure patterns

## Model Candidates

### Small-Sized Open Source Models
1. **Llama 2 7B** - Meta's open-source model
2. **Mistral 7B** - Efficient French model
3. **Phi-3 3.8B** - Microsoft's compact model
4. **Gemma 7B** - Google's open model
5. **Qwen 7B** - Alibaba's multilingual model

## Installation and Setup

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended)
- 8GB+ RAM (for local model deployment)

### Installation
```bash
# Clone repository
git clone <repository-url>
cd activity_project

# Install dependencies
pip install -r requirements.txt

# Download models
python scripts/download_models.py --all
```

### Quick Start
```bash
# Run sample evaluation
python main.py

# Extract from text
python main.py --mode extract --model llama2_7b --text "your text here"
```

## Development Roadmap

### Phase 1: Setup and Baseline ✅
- [x] Project structure setup
- [x] Basic model loading and inference
- [x] Simple prompt engineering
- [x] Initial evaluation framework

### Phase 2: Model Comparison
- [ ] Implement multiple model support
- [ ] Advanced prompt engineering
- [ ] Comprehensive evaluation metrics
- [ ] Performance benchmarking

### Phase 3: Optimization
- [ ] Model fine-tuning (if needed)
- [ ] Prompt optimization
- [ ] Performance tuning
- [ ] Production deployment

## Expected Performance Targets

- **Overall Accuracy**: >85% for field extraction
- **Processing Speed**: <5 seconds per document
- **Memory Usage**: <8GB RAM for model deployment
- **Reliability**: >95% successful JSON parsing

## Key Benefits

1. **Local Deployment**: Privacy and cost efficiency
2. **Model Comparison**: Systematic evaluation of different LLMs
3. **Prompt Engineering**: Optimized prompts for better performance
4. **Comprehensive Metrics**: Detailed performance analysis
5. **Scalable Framework**: Easy to add new models and metrics

## Next Steps

1. **Download Models**: Use the provided script to download models
2. **Prepare Data**: Add your training data in the specified format
3. **Run Evaluation**: Execute comprehensive model comparison
4. **Analyze Results**: Use the provided notebook for detailed analysis
5. **Optimize**: Fine-tune prompts and models based on results

This framework provides a solid foundation for evaluating and comparing different open-source LLMs for information extraction tasks, with a focus on local deployment and comprehensive performance analysis.

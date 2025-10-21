# AI Information Extraction Tool

## Project Overview

This project is designed to extract structured information from unstructured text notes using various open-source Large Language Models (LLMs). The tool focuses on extracting specific fields from employee-related text notes and converting them into structured JSON format.

## Problem Statement

The tool processes text notes containing information about employee work schedules, claims, and administrative details. The input consists of multiple sentences with mixed information, and the output should be a structured JSON with specific fields.

### Example Input:
```
"last day worked \n employee claim initiation letter to advice of last day worked and induction\n last day worked 04/25/2023 full shift\n first day missed 04/26/2023 induced tomorrow\n employee returned to work august 1 advice caller to call and comfirm her add\n advice caller paperwork pending delivery date 05/16/2023\n advcice caller can obtain on portal a"
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

## Project Goals

1. **Model Comparison**: Test and compare performance of different small-sized open-source LLMs
2. **Local Deployment**: Ensure all models can run locally for privacy and cost efficiency
3. **Prompt Engineering**: Optimize prompts for better extraction accuracy
4. **Performance Evaluation**: Develop comprehensive metrics to evaluate model performance
5. **Training Data Utilization**: Use paired training data (text notes + JSON field pairs) for evaluation

## Target Fields

The extraction tool focuses on the following key fields:
- `LastDayWorked`: Date when employee last worked
- `FirstDayMissed`: Date when employee first missed work
- `DeliveryDate`: Date for document delivery
- `ReturnToWork`: Date when employee returned to work

## Technical Approach

### 1. Information Extraction Process
- **Text Preprocessing**: Clean and normalize input text
- **Prompt Engineering**: Design effective prompts for different models
- **Model Inference**: Run extraction using various LLMs
- **Output Parsing**: Convert model responses to structured JSON
- **Validation**: Ensure output format consistency

### 2. Evaluation Framework
- **Accuracy Metrics**: Field-level and document-level accuracy
- **Precision/Recall**: For each target field
- **F1 Score**: Overall performance metric
- **Processing Speed**: Inference time per document
- **Memory Usage**: Resource consumption analysis

### 3. Model Testing Strategy
- **Baseline Models**: Start with smaller models (7B parameters or less)
- **Prompt Variations**: Test different prompt engineering techniques
- **Cross-Validation**: Use training data for performance evaluation
- **A/B Testing**: Compare models side-by-side

## Project Structure

```
activity_project/
├── README.md
├── requirements.txt
├── data/
│   ├── training/
│   │   ├── text_notes.txt
│   │   └── json_labels.json
│   └── test/
├── models/
│   ├── model_loader.py
│   ├── prompt_templates.py
│   └── inference.py
├── evaluation/
│   ├── metrics.py
│   ├── evaluator.py
│   └── comparison.py
├── utils/
│   ├── text_processor.py
│   ├── json_parser.py
│   └── data_loader.py
├── config/
│   └── model_configs.yaml
└── notebooks/
    └── performance_analysis.ipynb
```

## Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended)
- 8GB+ RAM (for local model deployment)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd activity_project

# Install dependencies
pip install -r requirements.txt

# Download models (will be implemented)
python scripts/download_models.py
```

## Usage

### Basic Information Extraction
```python
from models.inference import InformationExtractor

# Initialize extractor with specific model
extractor = InformationExtractor(model_name="llama-7b")

# Extract information from text
text = "last day worked 04/25/2023 full shift..."
result = extractor.extract(text)
print(result)
```

### Model Comparison
```python
from evaluation.comparison import ModelComparator

# Compare multiple models
comparator = ModelComparator()
results = comparator.compare_models(
    models=["llama-7b", "mistral-7b", "phi-3"],
    test_data="data/test/"
)
```

## Evaluation Metrics

### 1. Field-Level Accuracy
- **Exact Match**: Perfect field extraction
- **Partial Match**: Date format variations
- **No Match**: Missing or incorrect fields

### 2. Document-Level Metrics
- **Complete Extraction**: All fields successfully extracted
- **Partial Extraction**: Some fields extracted correctly
- **Failed Extraction**: No fields extracted

### 3. Performance Metrics
- **Inference Time**: Average processing time per document
- **Memory Usage**: Peak memory consumption
- **Throughput**: Documents processed per minute

## Model Candidates

### Small-Sized Open Source Models
1. **Llama 2 7B** - Meta's open-source model
2. **Mistral 7B** - Efficient French model
3. **Phi-3 3.8B** - Microsoft's compact model
4. **Gemma 7B** - Google's open model
5. **Qwen 7B** - Alibaba's multilingual model

## Training Data Format

### Input Format (text_notes.txt)
```
last day worked 04/25/2023 full shift
first day missed 04/26/2023 induced tomorrow
employee returned to work august 1
paperwork pending delivery date 05/16/2023
```

### Output Format (json_labels.json)
```json
{
  "LastDayWorked": "4/25/23",
  "FirstDayMissed": "4/26/23",
  "ReturnToWork": "8/1/23",
  "DeliveryDate": "5/16/23"
}
```

## Development Roadmap

### Phase 1: Setup and Baseline
- [ ] Project structure setup
- [ ] Basic model loading and inference
- [ ] Simple prompt engineering
- [ ] Initial evaluation framework

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in the repository.

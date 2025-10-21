"""
Main script for information extraction evaluation.
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

from utils.data_loader import DataLoader
from evaluation.evaluator import InformationExtractionEvaluator
from evaluation.comparison import ModelComparison
from models.inference import InformationExtractor


def main():
    """Main function for information extraction evaluation."""
    parser = argparse.ArgumentParser(description="AI Information Extraction Tool")
    parser.add_argument("--mode", type=str, choices=["extract", "evaluate", "compare"], 
                       required=True, help="Mode to run")
    parser.add_argument("--model", type=str, help="Model name for extraction")
    parser.add_argument("--text", type=str, help="Text to extract from")
    parser.add_argument("--template", type=str, default="zero_shot", 
                       help="Prompt template to use")
    parser.add_argument("--models", nargs="+", help="List of models to compare")
    parser.add_argument("--data-dir", type=str, default="data", 
                       help="Data directory path")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    if args.mode == "extract":
        # Single extraction mode
        if not args.model or not args.text:
            print("Error: --model and --text are required for extraction mode")
            return
        
        print(f"Extracting information using model: {args.model}")
        print(f"Template: {args.template}")
        print(f"Text: {args.text[:100]}...")
        
        try:
            extractor = InformationExtractor(args.model)
            result = extractor.extract(args.text, args.template)
            
            print("\nExtraction Result:")
            print(json.dumps(result, indent=2))
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResult saved to: {args.output}")
            
            extractor.cleanup()
            
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
    
    elif args.mode == "evaluate":
        # Evaluation mode
        if not args.model:
            print("Error: --model is required for evaluation mode")
            return
        
        print(f"Evaluating model: {args.model}")
        print(f"Template: {args.template}")
        
        try:
            # Load test data
            data_loader = DataLoader(args.data_dir)
            test_data = data_loader.load_test_data()
            
            if not test_data:
                print("No test data found. Creating sample data...")
                data_loader.create_sample_data()
                test_data = data_loader.load_test_data()
            
            print(f"Loaded {len(test_data)} test examples")
            
            # Run evaluation
            evaluator = InformationExtractionEvaluator(args.data_dir)
            results = evaluator.evaluate_model(args.model, test_data, args.template)
            
            print("\nEvaluation Results:")
            print(json.dumps(results, indent=2, default=str))
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print(f"\nResults saved to: {args.output}")
            
        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
    
    elif args.mode == "compare":
        # Comparison mode
        if not args.models:
            print("Error: --models is required for comparison mode")
            return
        
        print(f"Comparing models: {args.models}")
        
        try:
            # Load test data
            data_loader = DataLoader(args.data_dir)
            test_data = data_loader.load_test_data()
            
            if not test_data:
                print("No test data found. Creating sample data...")
                data_loader.create_sample_data()
                test_data = data_loader.load_test_data()
            
            print(f"Loaded {len(test_data)} test examples")
            
            # Run comparison
            evaluator = InformationExtractionEvaluator(args.data_dir)
            results = evaluator.evaluate_multiple_models(args.models, test_data, args.template)
            
            print("\nComparison Results:")
            print(json.dumps(results, indent=2, default=str))
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print(f"\nResults saved to: {args.output}")
            
        except Exception as e:
            print(f"Error during comparison: {str(e)}")


def run_sample_evaluation():
    """Run a sample evaluation with sample data."""
    print("Running sample evaluation...")
    
    # Create sample data
    data_loader = DataLoader("data")
    data_loader.create_sample_data()
    
    # Load test data
    test_data = data_loader.load_test_data()
    print(f"Created {len(test_data)} sample test examples")
    
    # Sample text for extraction
    sample_text = """last day worked 04/25/2023 full shift
first day missed 04/26/2023 induced tomorrow
employee returned to work august 1
advice caller paperwork pending delivery date 05/16/2023"""
    
    print(f"\nSample text: {sample_text}")
    
    # Try to run extraction (this will fail if models aren't downloaded)
    try:
        # This is just a demonstration - actual models need to be downloaded
        print("\nNote: To run actual extraction, you need to:")
        print("1. Download models using: python scripts/download_models.py --all")
        print("2. Install required dependencies: pip install -r requirements.txt")
        print("3. Run: python main.py --mode extract --model llama2_7b --text \"your text here\"")
        
    except Exception as e:
        print(f"Note: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments provided, run sample evaluation
        run_sample_evaluation()
    else:
        main()

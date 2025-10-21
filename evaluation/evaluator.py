"""
Main evaluation framework for information extraction models.
"""

import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from .metrics import EvaluationMetrics
from utils.data_loader import DataLoader
from models.inference import InformationExtractor, ModelComparator


class InformationExtractionEvaluator:
    """Main evaluator for information extraction models."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_loader = DataLoader(data_dir)
        self.metrics_calculator = EvaluationMetrics()
        self.results_dir = Path(data_dir) / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def evaluate_model(self, model_name: str, test_data: List[Dict[str, Any]], 
                      template_name: str = 'zero_shot', save_results: bool = True) -> Dict[str, Any]:
        """
        Evaluate a single model on test data.
        
        Args:
            model_name: Name of the model to evaluate
            test_data: List of test examples
            template_name: Prompt template to use
            save_results: Whether to save results to file
            
        Returns:
            Evaluation results
        """
        print(f"Evaluating model: {model_name}")
        print(f"Using template: {template_name}")
        print(f"Test data size: {len(test_data)}")
        
        start_time = time.time()
        
        try:
            # Initialize extractor
            extractor = InformationExtractor(model_name)
            
            # Run extraction
            results = []
            for i, example in enumerate(test_data):
                print(f"Processing example {i+1}/{len(test_data)}")
                
                # Extract information
                extraction_result = extractor.extract(example['text'], template_name)
                
                # Add ground truth for evaluation
                evaluation_result = {
                    'example_id': example.get('id', f"example_{i}"),
                    'text': example['text'],
                    'ground_truth': example['labels'],
                    'extraction': extraction_result['extraction'],
                    'metadata': extraction_result['metadata']
                }
                
                results.append(evaluation_result)
            
            # Calculate metrics
            aggregate_metrics = self.metrics_calculator.calculate_aggregate_metrics(results)
            performance_metrics = self.metrics_calculator.calculate_performance_metrics(results)
            
            # Compile final results
            evaluation_results = {
                'model_name': model_name,
                'template_name': template_name,
                'test_data_size': len(test_data),
                'evaluation_time': time.time() - start_time,
                'results': results,
                'aggregate_metrics': aggregate_metrics,
                'performance_metrics': performance_metrics
            }
            
            # Save results if requested
            if save_results:
                self._save_results(evaluation_results, f"{model_name}_{template_name}_evaluation.json")
            
            # Cleanup
            extractor.cleanup()
            
            return evaluation_results
            
        except Exception as e:
            print(f"Error evaluating model {model_name}: {str(e)}")
            return {
                'model_name': model_name,
                'template_name': template_name,
                'error': str(e),
                'evaluation_time': time.time() - start_time
            }
    
    def evaluate_multiple_models(self, model_names: List[str], test_data: List[Dict[str, Any]], 
                                template_name: str = 'zero_shot') -> Dict[str, Any]:
        """
        Evaluate multiple models and compare their performance.
        
        Args:
            model_names: List of model names to evaluate
            test_data: List of test examples
            template_name: Prompt template to use
            
        Returns:
            Comparison results
        """
        print(f"Evaluating {len(model_names)} models")
        print(f"Test data size: {len(test_data)}")
        
        model_results = {}
        
        for model_name in model_names:
            print(f"\n{'='*50}")
            print(f"Evaluating model: {model_name}")
            print(f"{'='*50}")
            
            result = self.evaluate_model(model_name, test_data, template_name, save_results=True)
            model_results[model_name] = result
        
        # Compare models
        comparison_results = self.metrics_calculator.compare_models(model_results)
        
        # Save comparison results
        self._save_results(comparison_results, "model_comparison.json")
        
        return comparison_results
    
    def evaluate_template_performance(self, model_name: str, test_data: List[Dict[str, Any]], 
                                     template_names: List[str] = None) -> Dict[str, Any]:
        """
        Evaluate different prompt templates for a single model.
        
        Args:
            model_name: Name of the model to evaluate
            test_data: List of test examples
            template_names: List of template names to test
            
        Returns:
            Template comparison results
        """
        if template_names is None:
            from models.prompt_templates import PromptTemplates
            template_names = PromptTemplates().get_all_templates()
        
        print(f"Evaluating templates for model: {model_name}")
        print(f"Templates: {template_names}")
        print(f"Test data size: {len(test_data)}")
        
        template_results = {}
        
        for template_name in template_names:
            print(f"\n{'='*30}")
            print(f"Testing template: {template_name}")
            print(f"{'='*30}")
            
            result = self.evaluate_model(model_name, test_data, template_name, save_results=True)
            template_results[template_name] = result
        
        # Compare templates
        comparison_results = self.metrics_calculator.compare_models(template_results)
        
        # Save template comparison results
        self._save_results(comparison_results, f"{model_name}_template_comparison.json")
        
        return comparison_results
    
    def run_comprehensive_evaluation(self, model_names: List[str], test_data: List[Dict[str, Any]], 
                                   template_names: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation across models and templates.
        
        Args:
            model_names: List of model names to evaluate
            test_data: List of test examples
            template_names: List of template names to test
            
        Returns:
            Comprehensive evaluation results
        """
        if template_names is None:
            from models.prompt_templates import PromptTemplates
            template_names = PromptTemplates().get_all_templates()
        
        print(f"Running comprehensive evaluation")
        print(f"Models: {model_names}")
        print(f"Templates: {template_names}")
        print(f"Test data size: {len(test_data)}")
        
        comprehensive_results = {}
        
        for model_name in model_names:
            print(f"\n{'='*60}")
            print(f"Comprehensive evaluation for model: {model_name}")
            print(f"{'='*60}")
            
            model_results = self.evaluate_template_performance(model_name, test_data, template_names)
            comprehensive_results[model_name] = model_results
        
        # Save comprehensive results
        self._save_results(comprehensive_results, "comprehensive_evaluation.json")
        
        return comprehensive_results
    
    def load_evaluation_results(self, filename: str) -> Dict[str, Any]:
        """
        Load previously saved evaluation results.
        
        Args:
            filename: Name of the results file
            
        Returns:
            Loaded evaluation results
        """
        results_file = self.results_dir / filename
        
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    
    def generate_evaluation_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """
        Generate a human-readable evaluation report.
        
        Args:
            results: Evaluation results
            output_file: Optional output file path
            
        Returns:
            Report text
        """
        report_lines = []
        report_lines.append("# Information Extraction Evaluation Report")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Overall summary
        if 'aggregate_metrics' in results:
            metrics = results['aggregate_metrics']
            report_lines.append("## Overall Performance")
            report_lines.append(f"- Test Data Size: {results.get('test_data_size', 'N/A')}")
            report_lines.append(f"- Evaluation Time: {results.get('evaluation_time', 'N/A'):.2f} seconds")
            report_lines.append("")
            
            # Document-level metrics
            if 'document_level' in metrics:
                doc_metrics = metrics['document_level']
                report_lines.append("### Document-Level Performance")
                report_lines.append(f"- Complete Success Rate: {doc_metrics.get('complete_success_rate', 0):.2%}")
                report_lines.append(f"- Partial Success Rate: {doc_metrics.get('partial_success_rate', 0):.2%}")
                report_lines.append(f"- Complete Failure Rate: {doc_metrics.get('complete_failure_rate', 0):.2%}")
                report_lines.append(f"- Average Completeness: {doc_metrics.get('average_completeness', 0):.2%}")
                report_lines.append("")
            
            # Field-level metrics
            if 'field_level' in metrics:
                report_lines.append("### Field-Level Performance")
                for field, field_metrics in metrics['field_level'].items():
                    report_lines.append(f"#### {field}")
                    report_lines.append(f"- Exact Match Rate: {field_metrics.get('exact_match_rate', 0):.2%}")
                    report_lines.append(f"- Normalized Match Rate: {field_metrics.get('normalized_match_rate', 0):.2%}")
                    report_lines.append(f"- Precision: {field_metrics.get('precision', 0):.2%}")
                    report_lines.append(f"- Recall: {field_metrics.get('recall', 0):.2%}")
                    report_lines.append("")
        
        # Performance metrics
        if 'performance_metrics' in results:
            perf_metrics = results['performance_metrics']
            report_lines.append("## Performance Metrics")
            report_lines.append(f"- Success Rate: {perf_metrics.get('success_rate', 0):.2%}")
            report_lines.append(f"- Error Count: {perf_metrics.get('error_count', 0)}")
            
            if 'processing_time' in perf_metrics:
                proc_time = perf_metrics['processing_time']
                report_lines.append(f"- Average Processing Time: {proc_time.get('mean', 0):.2f} seconds")
                report_lines.append(f"- Median Processing Time: {proc_time.get('median', 0):.2f} seconds")
            report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text
    
    def _save_results(self, results: Dict[str, Any], filename: str):
        """Save results to file."""
        results_file = self.results_dir / filename
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to: {results_file}")

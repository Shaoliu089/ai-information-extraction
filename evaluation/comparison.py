"""
Model and template comparison utilities.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional
from pathlib import Path
from .metrics import EvaluationMetrics


class ModelComparison:
    """Compare performance of different models and templates."""
    
    def __init__(self, results_dir: str = "data/results"):
        self.results_dir = Path(results_dir)
        self.metrics_calculator = EvaluationMetrics()
    
    def compare_models(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare performance across different models.
        
        Args:
            model_results: Dictionary mapping model names to their results
            
        Returns:
            Comparison analysis
        """
        comparison = {
            'model_rankings': {},
            'performance_summary': {},
            'detailed_comparison': {}
        }
        
        # Extract metrics for each model
        model_metrics = {}
        for model_name, results in model_results.items():
            if 'error' in results:
                continue
            
            metrics = results.get('aggregate_metrics', {})
            performance = results.get('performance_metrics', {})
            
            model_metrics[model_name] = {
                'metrics': metrics,
                'performance': performance
            }
        
        # Calculate rankings
        comparison['model_rankings'] = self._calculate_model_rankings(model_metrics)
        
        # Performance summary
        comparison['performance_summary'] = self._create_performance_summary(model_metrics)
        
        # Detailed comparison
        comparison['detailed_comparison'] = self._create_detailed_comparison(model_metrics)
        
        return comparison
    
    def compare_templates(self, template_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare performance across different templates.
        
        Args:
            template_results: Dictionary mapping template names to their results
            
        Returns:
            Template comparison analysis
        """
        comparison = {
            'template_rankings': {},
            'performance_summary': {},
            'detailed_comparison': {}
        }
        
        # Extract metrics for each template
        template_metrics = {}
        for template_name, results in template_results.items():
            if 'error' in results:
                continue
            
            metrics = results.get('aggregate_metrics', {})
            performance = results.get('performance_metrics', {})
            
            template_metrics[template_name] = {
                'metrics': metrics,
                'performance': performance
            }
        
        # Calculate rankings
        comparison['template_rankings'] = self._calculate_template_rankings(template_metrics)
        
        # Performance summary
        comparison['performance_summary'] = self._create_performance_summary(template_metrics)
        
        # Detailed comparison
        comparison['detailed_comparison'] = self._create_detailed_comparison(template_metrics)
        
        return comparison
    
    def create_comparison_plots(self, model_results: Dict[str, Any], output_dir: str = "plots"):
        """
        Create visualization plots for model comparison.
        
        Args:
            model_results: Model comparison results
            output_dir: Directory to save plots
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Extract data for plotting
        plot_data = self._extract_plot_data(model_results)
        
        # Create plots
        self._create_performance_plot(plot_data, output_path)
        self._create_field_accuracy_plot(plot_data, output_path)
        self._create_processing_time_plot(plot_data, output_path)
    
    def generate_comparison_report(self, comparison_results: Dict[str, Any], 
                                  output_file: str = "comparison_report.md") -> str:
        """
        Generate a comprehensive comparison report.
        
        Args:
            comparison_results: Results from model/template comparison
            output_file: Output file path
            
        Returns:
            Report text
        """
        report_lines = []
        report_lines.append("# Model Comparison Report")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Model rankings
        if 'model_rankings' in comparison_results:
            report_lines.append("## Model Rankings")
            report_lines.append("")
            
            rankings = comparison_results['model_rankings']
            for metric, ranking in rankings.items():
                report_lines.append(f"### {metric.replace('_', ' ').title()}")
                for i, (model, score) in enumerate(ranking, 1):
                    report_lines.append(f"{i}. {model}: {score:.3f}")
                report_lines.append("")
        
        # Performance summary
        if 'performance_summary' in comparison_results:
            report_lines.append("## Performance Summary")
            report_lines.append("")
            
            summary = comparison_results['performance_summary']
            for model, metrics in summary.items():
                report_lines.append(f"### {model}")
                for metric, value in metrics.items():
                    report_lines.append(f"- {metric}: {value:.3f}")
                report_lines.append("")
        
        # Detailed comparison
        if 'detailed_comparison' in comparison_results:
            report_lines.append("## Detailed Comparison")
            report_lines.append("")
            
            detailed = comparison_results['detailed_comparison']
            for section, data in detailed.items():
                report_lines.append(f"### {section.replace('_', ' ').title()}")
                report_lines.append("")
                report_lines.append("| Model | Metric | Value |")
                report_lines.append("|-------|--------|-------|")
                
                for model, metrics in data.items():
                    for metric, value in metrics.items():
                        report_lines.append(f"| {model} | {metric} | {value:.3f} |")
                report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text
    
    def _calculate_model_rankings(self, model_metrics: Dict[str, Any]) -> Dict[str, List[tuple]]:
        """Calculate rankings for different metrics."""
        rankings = {}
        
        # Extract scores for each metric
        metric_scores = {}
        for model_name, data in model_metrics.items():
            metrics = data.get('metrics', {})
            
            # Document-level metrics
            if 'document_level' in metrics:
                doc_metrics = metrics['document_level']
                for metric, value in doc_metrics.items():
                    if metric not in metric_scores:
                        metric_scores[metric] = {}
                    metric_scores[metric][model_name] = value
            
            # Field-level metrics
            if 'field_level' in metrics:
                field_metrics = metrics['field_level']
                for field, field_data in field_metrics.items():
                    for metric, value in field_data.items():
                        key = f"{field}_{metric}"
                        if key not in metric_scores:
                            metric_scores[key] = {}
                        metric_scores[key][model_name] = value
        
        # Create rankings
        for metric, scores in metric_scores.items():
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            rankings[metric] = sorted_scores
        
        return rankings
    
    def _calculate_template_rankings(self, template_metrics: Dict[str, Any]) -> Dict[str, List[tuple]]:
        """Calculate rankings for different templates."""
        return self._calculate_model_rankings(template_metrics)
    
    def _create_performance_summary(self, metrics_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Create performance summary for each model/template."""
        summary = {}
        
        for name, data in metrics_data.items():
            metrics = data.get('metrics', {})
            performance = data.get('performance', {})
            
            summary[name] = {}
            
            # Document-level metrics
            if 'document_level' in metrics:
                doc_metrics = metrics['document_level']
                summary[name].update(doc_metrics)
            
            # Performance metrics
            if 'success_rate' in performance:
                summary[name]['success_rate'] = performance['success_rate']
            
            if 'processing_time' in performance:
                proc_time = performance['processing_time']
                summary[name]['avg_processing_time'] = proc_time.get('mean', 0)
        
        return summary
    
    def _create_detailed_comparison(self, metrics_data: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Create detailed comparison data."""
        detailed = {
            'field_accuracy': {},
            'processing_performance': {},
            'error_analysis': {}
        }
        
        for name, data in metrics_data.items():
            metrics = data.get('metrics', {})
            performance = data.get('performance', {})
            
            # Field accuracy
            if 'field_level' in metrics:
                field_metrics = metrics['field_level']
                detailed['field_accuracy'][name] = {}
                for field, field_data in field_metrics.items():
                    detailed['field_accuracy'][name][field] = field_data.get('exact_match_rate', 0)
            
            # Processing performance
            if 'processing_time' in performance:
                proc_time = performance['processing_time']
                detailed['processing_performance'][name] = {
                    'mean_time': proc_time.get('mean', 0),
                    'std_time': proc_time.get('std', 0),
                    'min_time': proc_time.get('min', 0),
                    'max_time': proc_time.get('max', 0)
                }
            
            # Error analysis
            detailed['error_analysis'][name] = {
                'error_count': performance.get('error_count', 0),
                'success_rate': performance.get('success_rate', 0)
            }
        
        return detailed
    
    def _extract_plot_data(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data for plotting."""
        plot_data = {
            'models': [],
            'metrics': {},
            'field_accuracy': {},
            'processing_times': {}
        }
        
        for model_name, results in model_results.items():
            if 'error' in results:
                continue
            
            plot_data['models'].append(model_name)
            
            # Extract metrics
            metrics = results.get('aggregate_metrics', {})
            if 'document_level' in metrics:
                doc_metrics = metrics['document_level']
                for metric, value in doc_metrics.items():
                    if metric not in plot_data['metrics']:
                        plot_data['metrics'][metric] = []
                    plot_data['metrics'][metric].append(value)
            
            # Extract field accuracy
            if 'field_level' in metrics:
                field_metrics = metrics['field_level']
                for field, field_data in field_metrics.items():
                    if field not in plot_data['field_accuracy']:
                        plot_data['field_accuracy'][field] = []
                    plot_data['field_accuracy'][field].append(field_data.get('exact_match_rate', 0))
            
            # Extract processing times
            performance = results.get('performance_metrics', {})
            if 'processing_time' in performance:
                proc_time = performance['processing_time']
                plot_data['processing_times'][model_name] = proc_time.get('mean', 0)
        
        return plot_data
    
    def _create_performance_plot(self, plot_data: Dict[str, Any], output_path: Path):
        """Create performance comparison plot."""
        if not plot_data['metrics']:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Model Performance Comparison', fontsize=16)
        
        # Plot document-level metrics
        metrics_to_plot = ['complete_success_rate', 'partial_success_rate', 'average_completeness']
        for i, metric in enumerate(metrics_to_plot):
            if metric in plot_data['metrics']:
                ax = axes[i//2, i%2]
                ax.bar(plot_data['models'], plot_data['metrics'][metric])
                ax.set_title(metric.replace('_', ' ').title())
                ax.set_ylabel('Rate')
                ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_path / 'performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_field_accuracy_plot(self, plot_data: Dict[str, Any], output_path: Path):
        """Create field accuracy comparison plot."""
        if not plot_data['field_accuracy']:
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create heatmap data
        heatmap_data = []
        field_names = list(plot_data['field_accuracy'].keys())
        model_names = plot_data['models']
        
        for field in field_names:
            row = []
            for model in model_names:
                if model in plot_data['field_accuracy'][field]:
                    row.append(plot_data['field_accuracy'][field][model])
                else:
                    row.append(0)
            heatmap_data.append(row)
        
        # Create heatmap
        sns.heatmap(heatmap_data, 
                   xticklabels=model_names, 
                   yticklabels=field_names,
                   annot=True, 
                   fmt='.2f',
                   cmap='YlOrRd')
        
        plt.title('Field-Level Accuracy Comparison')
        plt.xlabel('Models')
        plt.ylabel('Fields')
        plt.tight_layout()
        plt.savefig(output_path / 'field_accuracy_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_processing_time_plot(self, plot_data: Dict[str, Any], output_path: Path):
        """Create processing time comparison plot."""
        if not plot_data['processing_times']:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        models = list(plot_data['processing_times'].keys())
        times = list(plot_data['processing_times'].values())
        
        ax.bar(models, times)
        ax.set_title('Processing Time Comparison')
        ax.set_xlabel('Models')
        ax.set_ylabel('Average Processing Time (seconds)')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_path / 'processing_time_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

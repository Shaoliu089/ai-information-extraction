"""
Evaluation metrics for information extraction performance.
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from sklearn.metrics import precision_score, recall_score, f1_score
from utils.json_parser import JSONParser


class EvaluationMetrics:
    """Calculate various metrics for information extraction performance."""
    
    def __init__(self):
        self.json_parser = JSONParser()
        self.required_fields = ['LastDayWorked', 'FirstDayMissed', 'DeliveryDate', 'ReturnToWork']
    
    def calculate_field_metrics(self, predicted: Dict[str, Any], ground_truth: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate field-level metrics for a single example.
        
        Args:
            predicted: Predicted extraction result
            ground_truth: Ground truth result
            
        Returns:
            Field-level metrics
        """
        field_metrics = {}
        
        for field in self.required_fields:
            pred_value = predicted.get(field)
            true_value = ground_truth.get(field)
            
            # Exact match
            exact_match = pred_value == true_value
            
            # Normalized match (dates normalized to same format)
            normalized_match = False
            if pred_value and true_value:
                norm_pred = self.json_parser.normalize_date(str(pred_value))
                norm_true = self.json_parser.normalize_date(str(true_value))
                normalized_match = norm_pred == norm_true
            
            # Partial match (contains same date information)
            partial_match = False
            if pred_value and true_value:
                # Extract date patterns from both values
                pred_dates = self._extract_date_patterns(str(pred_value))
                true_dates = self._extract_date_patterns(str(true_value))
                partial_match = len(set(pred_dates) & set(true_dates)) > 0
            
            # False positive/negative
            false_positive = pred_value is not None and true_value is None
            false_negative = pred_value is None and true_value is not None
            
            field_metrics[field] = {
                'exact_match': exact_match,
                'normalized_match': normalized_match,
                'partial_match': partial_match,
                'false_positive': false_positive,
                'false_negative': false_negative,
                'predicted_value': pred_value,
                'true_value': true_value
            }
        
        return field_metrics
    
    def calculate_document_metrics(self, predicted: Dict[str, Any], ground_truth: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate document-level metrics for a single example.
        
        Args:
            predicted: Predicted extraction result
            ground_truth: Ground truth result
            
        Returns:
            Document-level metrics
        """
        field_metrics = self.calculate_field_metrics(predicted, ground_truth)
        
        # Count matches
        exact_matches = sum(1 for field_metric in field_metrics.values() if field_metric['exact_match'])
        normalized_matches = sum(1 for field_metric in field_metrics.values() if field_metric['normalized_match'])
        partial_matches = sum(1 for field_metric in field_metrics.values() if field_metric['partial_match'])
        
        # Document-level success
        complete_success = exact_matches == len(self.required_fields)
        partial_success = exact_matches > 0 or normalized_matches > 0 or partial_matches > 0
        complete_failure = exact_matches == 0 and normalized_matches == 0 and partial_matches == 0
        
        # Completeness
        completeness = exact_matches / len(self.required_fields)
        
        return {
            'exact_matches': exact_matches,
            'normalized_matches': normalized_matches,
            'partial_matches': partial_matches,
            'total_fields': len(self.required_fields),
            'complete_success': complete_success,
            'partial_success': partial_success,
            'complete_failure': complete_failure,
            'completeness': completeness
        }
    
    def calculate_aggregate_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics across multiple examples.
        
        Args:
            results: List of evaluation results
            
        Returns:
            Aggregate metrics
        """
        if not results:
            return {}
        
        # Field-level aggregates
        field_metrics = {field: {'exact': 0, 'normalized': 0, 'partial': 0, 'fp': 0, 'fn': 0, 'total': 0} 
                        for field in self.required_fields}
        
        # Document-level aggregates
        doc_metrics = {'complete_success': 0, 'partial_success': 0, 'complete_failure': 0, 'total': 0}
        completeness_scores = []
        
        for result in results:
            if 'error' in result:
                continue
            
            predicted = result.get('extraction', {})
            ground_truth = result.get('ground_truth', {})
            
            # Field-level metrics
            field_metrics_result = self.calculate_field_metrics(predicted, ground_truth)
            for field, metrics in field_metrics_result.items():
                field_metrics[field]['total'] += 1
                if metrics['exact_match']:
                    field_metrics[field]['exact'] += 1
                if metrics['normalized_match']:
                    field_metrics[field]['normalized'] += 1
                if metrics['partial_match']:
                    field_metrics[field]['partial'] += 1
                if metrics['false_positive']:
                    field_metrics[field]['fp'] += 1
                if metrics['false_negative']:
                    field_metrics[field]['fn'] += 1
            
            # Document-level metrics
            doc_metrics_result = self.calculate_document_metrics(predicted, ground_truth)
            doc_metrics['total'] += 1
            if doc_metrics_result['complete_success']:
                doc_metrics['complete_success'] += 1
            elif doc_metrics_result['partial_success']:
                doc_metrics['partial_success'] += 1
            else:
                doc_metrics['complete_failure'] += 1
            
            completeness_scores.append(doc_metrics_result['completeness'])
        
        # Calculate percentages and averages
        aggregate_metrics = {
            'field_level': {},
            'document_level': {},
            'overall': {}
        }
        
        # Field-level percentages
        for field, metrics in field_metrics.items():
            total = metrics['total']
            if total > 0:
                aggregate_metrics['field_level'][field] = {
                    'exact_match_rate': metrics['exact'] / total,
                    'normalized_match_rate': metrics['normalized'] / total,
                    'partial_match_rate': metrics['partial'] / total,
                    'false_positive_rate': metrics['fp'] / total,
                    'false_negative_rate': metrics['fn'] / total,
                    'precision': metrics['exact'] / (metrics['exact'] + metrics['fp']) if (metrics['exact'] + metrics['fp']) > 0 else 0,
                    'recall': metrics['exact'] / (metrics['exact'] + metrics['fn']) if (metrics['exact'] + metrics['fn']) > 0 else 0
                }
        
        # Document-level percentages
        total_docs = doc_metrics['total']
        if total_docs > 0:
            aggregate_metrics['document_level'] = {
                'complete_success_rate': doc_metrics['complete_success'] / total_docs,
                'partial_success_rate': doc_metrics['partial_success'] / total_docs,
                'complete_failure_rate': doc_metrics['complete_failure'] / total_docs,
                'average_completeness': np.mean(completeness_scores) if completeness_scores else 0
            }
        
        # Overall metrics
        if completeness_scores:
            aggregate_metrics['overall'] = {
                'average_completeness': np.mean(completeness_scores),
                'median_completeness': np.median(completeness_scores),
                'std_completeness': np.std(completeness_scores)
            }
        
        return aggregate_metrics
    
    def calculate_performance_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate performance metrics (speed, memory, etc.).
        
        Args:
            results: List of evaluation results
            
        Returns:
            Performance metrics
        """
        if not results:
            return {}
        
        processing_times = []
        memory_usage = []
        error_count = 0
        
        for result in results:
            if 'error' in result:
                error_count += 1
                continue
            
            metadata = result.get('metadata', {})
            if 'processing_time' in metadata:
                processing_times.append(metadata['processing_time'])
            if 'memory_usage' in metadata:
                memory_usage.append(metadata['memory_usage'])
        
        performance_metrics = {
            'total_examples': len(results),
            'error_count': error_count,
            'success_rate': (len(results) - error_count) / len(results) if results else 0
        }
        
        if processing_times:
            performance_metrics['processing_time'] = {
                'mean': np.mean(processing_times),
                'median': np.median(processing_times),
                'std': np.std(processing_times),
                'min': np.min(processing_times),
                'max': np.max(processing_times)
            }
        
        if memory_usage:
            performance_metrics['memory_usage'] = {
                'mean': np.mean(memory_usage),
                'median': np.median(memory_usage),
                'std': np.std(memory_usage),
                'min': np.min(memory_usage),
                'max': np.max(memory_usage)
            }
        
        return performance_metrics
    
    def _extract_date_patterns(self, text: str) -> List[str]:
        """Extract date patterns from text."""
        import re
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
            r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        return dates
    
    def compare_models(self, model_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Compare metrics across different models.
        
        Args:
            model_results: Dictionary mapping model names to their results
            
        Returns:
            Model comparison metrics
        """
        comparison = {}
        
        for model_name, results in model_results.items():
            if 'error' in results:
                comparison[model_name] = {'error': results['error']}
                continue
            
            aggregate_metrics = self.calculate_aggregate_metrics(results)
            performance_metrics = self.calculate_performance_metrics(results)
            
            comparison[model_name] = {
                'aggregate_metrics': aggregate_metrics,
                'performance_metrics': performance_metrics
            }
        
        return comparison

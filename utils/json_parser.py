"""
JSON parsing utilities for information extraction output.
"""

import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
import dateutil.parser


class JSONParser:
    """Handles parsing and validation of model outputs."""
    
    def __init__(self):
        self.required_fields = [
            'LastDayWorked',
            'FirstDayMissed', 
            'DeliveryDate',
            'ReturnToWork'
        ]
    
    def parse_model_output(self, output: str) -> Dict[str, Any]:
        """
        Parse model output and extract JSON.
        
        Args:
            output: Raw model output
            
        Returns:
            Parsed JSON dictionary
        """
        # Try to extract JSON from output
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed = json.loads(json_str)
                return self.validate_and_normalize(parsed)
            except json.JSONDecodeError:
                pass
        
        # If no valid JSON found, return empty result
        return self.create_empty_result()
    
    def validate_and_normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize extracted data.
        
        Args:
            data: Raw extracted data
            
        Returns:
            Validated and normalized data
        """
        result = {}
        
        for field in self.required_fields:
            value = data.get(field)
            
            if value is None or value == "null" or value == "":
                result[field] = None
            else:
                # Normalize date format
                normalized_date = self.normalize_date(str(value))
                result[field] = normalized_date
        
        return result
    
    def normalize_date(self, date_str: str) -> Optional[str]:
        """
        Normalize date string to standard format.
        
        Args:
            date_str: Raw date string
            
        Returns:
            Normalized date string or None if invalid
        """
        if not date_str or date_str.lower() in ['null', 'none', '']:
            return None
        
        try:
            # Parse the date
            parsed_date = dateutil.parser.parse(date_str, fuzzy=True)
            # Format as MM/DD/YY
            return parsed_date.strftime('%m/%d/%y')
        except:
            # If parsing fails, try to extract date patterns
            date_patterns = [
                r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
                r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
                r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, date_str)
                if match:
                    try:
                        parsed_date = dateutil.parser.parse(match.group(0))
                        return parsed_date.strftime('%m/%d/%y')
                    except:
                        continue
            
            return None
    
    def create_empty_result(self) -> Dict[str, Any]:
        """
        Create empty result structure.
        
        Returns:
            Empty result dictionary
        """
        return {field: None for field in self.required_fields}
    
    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate result structure and add metadata.
        
        Args:
            result: Extracted result
            
        Returns:
            Validated result with metadata
        """
        validation_info = {
            'extracted_fields': sum(1 for v in result.values() if v is not None),
            'total_fields': len(self.required_fields),
            'completeness': sum(1 for v in result.values() if v is not None) / len(self.required_fields),
            'valid_dates': sum(1 for v in result.values() if v is not None and self.is_valid_date(v))
        }
        
        return {
            'data': result,
            'metadata': validation_info
        }
    
    def is_valid_date(self, date_str: str) -> bool:
        """
        Check if date string is valid.
        
        Args:
            date_str: Date string to validate
            
        Returns:
            True if valid date, False otherwise
        """
        if not date_str:
            return False
        
        try:
            dateutil.parser.parse(date_str)
            return True
        except:
            return False
    
    def compare_results(self, predicted: Dict[str, Any], ground_truth: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare predicted results with ground truth.
        
        Args:
            predicted: Predicted extraction result
            ground_truth: Ground truth result
            
        Returns:
            Comparison metrics
        """
        comparison = {}
        
        for field in self.required_fields:
            pred_value = predicted.get(field)
            true_value = ground_truth.get(field)
            
            if pred_value == true_value:
                comparison[field] = 'exact_match'
            elif pred_value and true_value and self.normalize_date(pred_value) == self.normalize_date(true_value):
                comparison[field] = 'normalized_match'
            elif pred_value and true_value:
                comparison[field] = 'partial_match'
            elif pred_value and not true_value:
                comparison[field] = 'false_positive'
            elif not pred_value and true_value:
                comparison[field] = 'false_negative'
            else:
                comparison[field] = 'both_null'
        
        return comparison

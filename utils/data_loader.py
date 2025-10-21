"""
Data loading utilities for training and evaluation.
"""

import json
import pandas as pd
from typing import List, Dict, Any, Tuple
from pathlib import Path
import random


class DataLoader:
    """Handles loading and preprocessing of training data."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.training_dir = self.data_dir / "training"
        self.test_dir = self.data_dir / "test"
    
    def load_training_data(self) -> List[Dict[str, Any]]:
        """
        Load training data from files.
        
        Returns:
            List of training examples
        """
        training_data = []
        
        # Load text notes
        text_file = self.training_dir / "text_notes.txt"
        if text_file.exists():
            with open(text_file, 'r', encoding='utf-8') as f:
                text_notes = f.read().strip().split('\n\n')
        else:
            text_notes = []
        
        # Load JSON labels
        json_file = self.training_dir / "json_labels.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                json_labels = json.load(f)
        else:
            json_labels = []
        
        # Combine text and labels
        for i, text in enumerate(text_notes):
            if i < len(json_labels):
                training_data.append({
                    'text': text.strip(),
                    'labels': json_labels[i],
                    'id': f"train_{i}"
                })
        
        return training_data
    
    def load_test_data(self) -> List[Dict[str, Any]]:
        """
        Load test data from files.
        
        Returns:
            List of test examples
        """
        test_data = []
        
        # Load test text notes
        text_file = self.test_dir / "text_notes.txt"
        if text_file.exists():
            with open(text_file, 'r', encoding='utf-8') as f:
                text_notes = f.read().strip().split('\n\n')
        else:
            text_notes = []
        
        # Load test JSON labels
        json_file = self.test_dir / "json_labels.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                json_labels = json.load(f)
        else:
            json_labels = []
        
        # Combine text and labels
        for i, text in enumerate(text_notes):
            if i < len(json_labels):
                test_data.append({
                    'text': text.strip(),
                    'labels': json_labels[i],
                    'id': f"test_{i}"
                })
        
        return test_data
    
    def split_data(self, data: List[Dict[str, Any]], train_ratio: float = 0.8) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Split data into training and validation sets.
        
        Args:
            data: Input data
            train_ratio: Ratio of data to use for training
            
        Returns:
            Tuple of (training_data, validation_data)
        """
        random.shuffle(data)
        split_idx = int(len(data) * train_ratio)
        
        train_data = data[:split_idx]
        val_data = data[split_idx:]
        
        return train_data, val_data
    
    def create_sample_data(self) -> None:
        """
        Create sample training data for testing.
        """
        # Create directories if they don't exist
        self.training_dir.mkdir(parents=True, exist_ok=True)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample training data
        sample_texts = [
            "last day worked 04/25/2023 full shift\nfirst day missed 04/26/2023 induced tomorrow\nemployee returned to work august 1\nadvice caller paperwork pending delivery date 05/16/2023",
            "employee claim initiation letter to advice of last day worked and induction\nlast day worked 04/25/2023 full shift\nfirst day missed 04/26/2023 induced tomorrow",
            "advice caller to call and confirm her address\nemployee returned to work august 1\npaperwork pending delivery date 05/16/2023\nadvice caller can obtain on portal"
        ]
        
        sample_labels = [
            {
                "LastDayWorked": "4/25/23",
                "FirstDayMissed": "4/26/23",
                "DeliveryDate": "5/16/23",
                "ReturnToWork": "8/1/23"
            },
            {
                "LastDayWorked": "4/25/23",
                "FirstDayMissed": "4/26/23",
                "DeliveryDate": None,
                "ReturnToWork": None
            },
            {
                "LastDayWorked": None,
                "FirstDayMissed": None,
                "DeliveryDate": "5/16/23",
                "ReturnToWork": "8/1/23"
            }
        ]
        
        # Save training data
        with open(self.training_dir / "text_notes.txt", 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(sample_texts))
        
        with open(self.training_dir / "json_labels.json", 'w', encoding='utf-8') as f:
            json.dump(sample_labels, f, indent=2)
        
        # Save test data (subset)
        test_texts = sample_texts[:2]
        test_labels = sample_labels[:2]
        
        with open(self.test_dir / "text_notes.txt", 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(test_texts))
        
        with open(self.test_dir / "json_labels.json", 'w', encoding='utf-8') as f:
            json.dump(test_labels, f, indent=2)
    
    def save_results(self, results: List[Dict[str, Any]], filename: str) -> None:
        """
        Save extraction results to file.
        
        Args:
            results: Extraction results
            filename: Output filename
        """
        output_file = self.data_dir / "results" / filename
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    
    def load_results(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load extraction results from file.
        
        Args:
            filename: Results filename
            
        Returns:
            Loaded results
        """
        results_file = self.data_dir / "results" / filename
        
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

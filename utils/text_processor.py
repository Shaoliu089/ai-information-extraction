"""
Text processing utilities for information extraction.
"""

import re
import string
from typing import List, Dict, Any
from datetime import datetime
import dateutil.parser


class TextProcessor:
    """Handles text cleaning and preprocessing for information extraction."""
    
    def __init__(self):
        self.date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY or MM/DD/YY
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # MM-DD-YYYY or MM-DD-YY
            r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b', # MM.DD.YYYY or MM.DD.YY
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{2,4}\b',  # Month DD, YYYY
            r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},?\s+\d{2,4}\b',  # Mon DD, YYYY
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize input text.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep alphanumeric, spaces, and common punctuation
        text = re.sub(r'[^\w\s.,/:-]', '', text)
        
        # Normalize multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_dates(self, text: str) -> List[str]:
        """
        Extract all date-like patterns from text.
        
        Args:
            text: Input text
            
        Returns:
            List of extracted dates
        """
        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        return dates
    
    def normalize_date(self, date_str: str) -> str:
        """
        Normalize date string to standard format (MM/DD/YY).
        
        Args:
            date_str: Raw date string
            
        Returns:
            Normalized date string
        """
        try:
            # Parse the date
            parsed_date = dateutil.parser.parse(date_str, fuzzy=True)
            # Format as MM/DD/YY
            return parsed_date.strftime('%m/%d/%y')
        except:
            return date_str
    
    def preprocess_for_extraction(self, text: str) -> Dict[str, Any]:
        """
        Preprocess text for information extraction.
        
        Args:
            text: Raw input text
            
        Returns:
            Dictionary with processed text and metadata
        """
        cleaned_text = self.clean_text(text)
        extracted_dates = self.extract_dates(cleaned_text)
        normalized_dates = [self.normalize_date(date) for date in extracted_dates]
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'extracted_dates': extracted_dates,
            'normalized_dates': normalized_dates,
            'word_count': len(cleaned_text.split()),
            'date_count': len(extracted_dates)
        }
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences for better processing.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK/spaCy)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases that might contain relevant information.
        
        Args:
            text: Input text
            
        Returns:
            List of key phrases
        """
        key_phrases = []
        
        # Look for phrases containing target fields
        target_patterns = [
            r'last day worked[^.]*',
            r'first day missed[^.]*',
            r'delivery date[^.]*',
            r'returned to work[^.]*',
            r'return to work[^.]*'
        ]
        
        for pattern in target_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            key_phrases.extend(matches)
        
        return key_phrases

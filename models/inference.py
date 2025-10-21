"""
Inference utilities for information extraction using different LLM models.
"""

import time
import json
from typing import Dict, Any, List, Optional
from .model_loader import ModelLoader
from .prompt_templates import PromptTemplates
from utils.text_processor import TextProcessor
from utils.json_parser import JSONParser


class InformationExtractor:
    """Main class for information extraction using LLM models."""
    
    def __init__(self, model_name: str, config_path: str = "config/model_configs.yaml"):
        self.model_name = model_name
        self.model_loader = ModelLoader(config_path)
        self.prompt_templates = PromptTemplates()
        self.text_processor = TextProcessor()
        self.json_parser = JSONParser()
        
        # Load model
        self.model_info = self.model_loader.load_model(model_name)
        if not self.model_info:
            raise ValueError(f"Failed to load model: {model_name}")
        
        self.model = self.model_info['model']
        self.tokenizer = self.model_info['tokenizer']
        self.generator = self.model_info['generator']
        self.config = self.model_info['config']
    
    def extract(self, text: str, template_name: str = 'zero_shot', **kwargs) -> Dict[str, Any]:
        """
        Extract information from text using the loaded model.
        
        Args:
            text: Input text to extract from
            template_name: Name of prompt template to use
            **kwargs: Additional parameters for generation
            
        Returns:
            Dictionary containing extracted information and metadata
        """
        start_time = time.time()
        
        # Preprocess text
        processed_text = self.text_processor.preprocess_for_extraction(text)
        
        # Format prompt
        prompt = self.prompt_templates.format_prompt(template_name, processed_text['cleaned_text'])
        
        # Generate response
        generation_params = {
            'max_new_tokens': self.config.get('max_new_tokens', 512),
            'temperature': self.config.get('temperature', 0.1),
            'top_p': self.config.get('top_p', 0.9),
            'do_sample': True,
            'pad_token_id': self.tokenizer.eos_token_id,
            **kwargs
        }
        
        try:
            response = self.generator(
                prompt,
                max_new_tokens=generation_params['max_new_tokens'],
                temperature=generation_params['temperature'],
                top_p=generation_params['top_p'],
                do_sample=generation_params['do_sample'],
                pad_token_id=generation_params['pad_token_id']
            )
            
            # Extract generated text
            generated_text = response[0]['generated_text']
            model_output = generated_text[len(prompt):].strip()
            
            # Parse output
            parsed_result = self.json_parser.parse_model_output(model_output)
            validated_result = self.json_parser.validate_result(parsed_result)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                'extraction': validated_result['data'],
                'metadata': {
                    **validated_result['metadata'],
                    'processing_time': processing_time,
                    'model_name': self.model_name,
                    'template_name': template_name,
                    'input_length': len(text),
                    'output_length': len(model_output)
                }
            }
            
        except Exception as e:
            return {
                'extraction': self.json_parser.create_empty_result(),
                'metadata': {
                    'error': str(e),
                    'processing_time': time.time() - start_time,
                    'model_name': self.model_name,
                    'template_name': template_name
                }
            }
    
    def batch_extract(self, texts: List[str], template_name: str = 'zero_shot', **kwargs) -> List[Dict[str, Any]]:
        """
        Extract information from multiple texts.
        
        Args:
            texts: List of input texts
            template_name: Name of prompt template to use
            **kwargs: Additional parameters for generation
            
        Returns:
            List of extraction results
        """
        results = []
        for i, text in enumerate(texts):
            print(f"Processing text {i+1}/{len(texts)}")
            result = self.extract(text, template_name, **kwargs)
            results.append(result)
        
        return results
    
    def extract_with_multiple_templates(self, text: str, template_names: List[str] = None) -> Dict[str, Any]:
        """
        Extract information using multiple prompt templates and compare results.
        
        Args:
            text: Input text to extract from
            template_names: List of template names to use
            
        Returns:
            Dictionary containing results from all templates
        """
        if template_names is None:
            template_names = self.prompt_templates.get_all_templates()
        
        results = {}
        for template_name in template_names:
            print(f"Testing template: {template_name}")
            result = self.extract(text, template_name)
            results[template_name] = result
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Model information dictionary
        """
        return {
            'model_name': self.model_name,
            'model_id': self.model_info['model_id'],
            'config': self.config,
            'memory_usage': self.model_loader.get_memory_usage()
        }
    
    def cleanup(self):
        """Clean up model resources."""
        self.model_loader.unload_model(self.model_name)


class ModelComparator:
    """Compare performance of different models."""
    
    def __init__(self, config_path: str = "config/model_configs.yaml"):
        self.model_loader = ModelLoader(config_path)
        self.prompt_templates = PromptTemplates()
        self.text_processor = TextProcessor()
        self.json_parser = JSONParser()
    
    def compare_models(self, model_names: List[str], test_data: List[Dict[str, Any]], 
                      template_name: str = 'zero_shot') -> Dict[str, Any]:
        """
        Compare performance of multiple models.
        
        Args:
            model_names: List of model names to compare
            test_data: List of test examples
            template_name: Prompt template to use
            
        Returns:
            Comparison results
        """
        results = {}
        
        for model_name in model_names:
            print(f"Testing model: {model_name}")
            try:
                extractor = InformationExtractor(model_name)
                model_results = []
                
                for i, example in enumerate(test_data):
                    print(f"  Processing example {i+1}/{len(test_data)}")
                    result = extractor.extract(example['text'], template_name)
                    model_results.append(result)
                
                results[model_name] = model_results
                extractor.cleanup()
                
            except Exception as e:
                print(f"Error with model {model_name}: {str(e)}")
                results[model_name] = {'error': str(e)}
        
        return results
    
    def compare_templates(self, model_name: str, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare performance of different prompt templates.
        
        Args:
            model_name: Name of the model to use
            test_data: List of test examples
            
        Returns:
            Template comparison results
        """
        try:
            extractor = InformationExtractor(model_name)
            template_names = self.prompt_templates.get_all_templates()
            results = {}
            
            for template_name in template_names:
                print(f"Testing template: {template_name}")
                template_results = []
                
                for example in test_data:
                    result = extractor.extract(example['text'], template_name)
                    template_results.append(result)
                
                results[template_name] = template_results
            
            extractor.cleanup()
            return results
            
        except Exception as e:
            return {'error': str(e)}

"""
Model loading utilities for different open-source LLMs.
"""

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    pipeline
)
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path


class ModelLoader:
    """Handles loading and configuration of different LLM models."""
    
    def __init__(self, config_path: str = "config/model_configs.yaml"):
        self.config_path = Path(config_path)
        self.loaded_models = {}
        self.load_config()
    
    def load_config(self):
        """Load model configurations from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default configuration
            self.config = {
                'models': {
                    'llama2_7b': {
                        'model_id': 'meta-llama/Llama-2-7b-hf',
                        'max_length': 2048,
                        'temperature': 0.1,
                        'top_p': 0.9,
                        'max_new_tokens': 512,
                        'quantization': '4bit',
                        'device_map': 'auto'
                    }
                }
            }
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model configuration dictionary
        """
        return self.config['models'].get(model_name, {})
    
    def load_model(self, model_name: str, device: str = "auto") -> Dict[str, Any]:
        """
        Load a specific model and tokenizer.
        
        Args:
            model_name: Name of the model to load
            device: Device to load model on
            
        Returns:
            Dictionary containing model and tokenizer
        """
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]
        
        config = self.get_model_config(model_name)
        model_id = config.get('model_id', model_name)
        
        try:
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                trust_remote_code=True
            )
            
            # Configure quantization if specified
            quantization_config = None
            if config.get('quantization') == '4bit':
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True
                )
            elif config.get('quantization') == '8bit':
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True
                )
            
            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=quantization_config,
                device_map=config.get('device_map', 'auto'),
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            # Create generation pipeline
            generator = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map=config.get('device_map', 'auto')
            )
            
            model_info = {
                'model': model,
                'tokenizer': tokenizer,
                'generator': generator,
                'config': config,
                'model_id': model_id
            }
            
            self.loaded_models[model_name] = model_info
            return model_info
            
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            return None
    
    def unload_model(self, model_name: str):
        """
        Unload a model to free memory.
        
        Args:
            model_name: Name of the model to unload
        """
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            torch.cuda.empty_cache()
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available model configurations.
        
        Returns:
            List of model names
        """
        return list(self.config['models'].keys())
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a model without loading it.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information dictionary
        """
        config = self.get_model_config(model_name)
        return {
            'name': config.get('name', model_name),
            'model_id': config.get('model_id', model_name),
            'max_length': config.get('max_length', 2048),
            'quantization': config.get('quantization', 'none'),
            'device_map': config.get('device_map', 'auto')
        }
    
    def check_model_availability(self, model_name: str) -> bool:
        """
        Check if a model is available for loading.
        
        Args:
            model_name: Name of the model
            
        Returns:
            True if model is available, False otherwise
        """
        return model_name in self.config['models']
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Get current memory usage information.
        
        Returns:
            Memory usage dictionary
        """
        if torch.cuda.is_available():
            return {
                'gpu_memory_allocated': torch.cuda.memory_allocated(),
                'gpu_memory_reserved': torch.cuda.memory_reserved(),
                'gpu_memory_max': torch.cuda.max_memory_allocated(),
                'loaded_models': list(self.loaded_models.keys())
            }
        else:
            return {
                'gpu_available': False,
                'loaded_models': list(self.loaded_models.keys())
            }
    
    def clear_cache(self):
        """Clear GPU cache to free memory."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def get_recommended_models(self, memory_limit_gb: int = 8) -> List[str]:
        """
        Get recommended models based on memory constraints.
        
        Args:
            memory_limit_gb: Maximum memory in GB
            
        Returns:
            List of recommended model names
        """
        # Simple heuristic based on model size
        model_sizes = {
            'phi3_3_8b': 3.8,
            'llama2_7b': 7.0,
            'mistral_7b': 7.0,
            'gemma_7b': 7.0,
            'qwen_7b': 7.0
        }
        
        recommended = []
        for model_name, size_gb in model_sizes.items():
            if size_gb <= memory_limit_gb and self.check_model_availability(model_name):
                recommended.append(model_name)
        
        return recommended

"""
Script to download and setup models for local deployment.
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
import yaml


def download_model(model_name: str, config_path:  str = "config/model_configs.yaml", local_dir: str = None):
    """
    Download a model from Hugging Face Hub.
    
    Args:
        model_id: Hugging Face model ID
        local_dir: Local directory to save model
    """
    if not Path(config_path).exists():
        print(f"Configuration file not found: {config_path}")
        return
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    models = config.get('models', {})
    if model_name in models:
        model_id = models[model_name].get('model_id')
    else:
        print(f'model name {model_name} not found')
    print(model_id)
    if local_dir is None:
        local_dir = f"models/{model_id.replace('/', '_')}"
    print(f"Downloading model: {model_name}")
    print(f"Local directory: {local_dir}")

    try:
        # Download model files
        snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"Model downloaded successfully to: {local_dir}")
        return local_dir
        
    except Exception as e:
        print(f"Error downloading model {model_id}: {str(e)}")
        return None


def setup_models_from_config(config_path: str = "config/model_configs.yaml"):
    """
    Download all models specified in configuration.
    
    Args:
        config_path: Path to model configuration file
    """
    if not Path(config_path).exists():
        print(f"Configuration file not found: {config_path}")
        return
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    models = config.get('models', {})
    
    for model_name, model_config in models.items():
        model_id = model_config.get('model_id')
        if model_id:
            print(f"\n{'='*50}")
            print(f"Setting up model: {model_name}")
            print(f"Model ID: {model_id}")
            print(f"{'='*50}")
            
            download_model(model_id)


def main():
    """Main function to setup models."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download models for local deployment")
    parser.add_argument("--model", type=str, help="Specific model to download")
    parser.add_argument("--config", type=str, default="config/model_configs.yaml", 
                       help="Path to configuration file")
    parser.add_argument("--all", action="store_true", help="Download all models from config")
    
    args = parser.parse_args()
    
    if args.model:
        # Download specific model
        download_model(args.model, args.config)
    elif args.all:
        # Download all models from config
        setup_models_from_config(args.config)
    else:
        print("Please specify --model <model_id> or --all")
        print("Available models from config:")
        if Path(args.config).exists():
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f)
            for model_name, model_config in config.get('models', {}).items():
                print(f"  {model_name}: {model_config.get('model_id', 'N/A')}")


if __name__ == "__main__":
    main()

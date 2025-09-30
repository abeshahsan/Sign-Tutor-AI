#!/usr/bin/env python3
"""
Sign Tutor AI - Entry Point
Professional AI-powered tutor for learning sign language using advanced computer vision.

Usage:
    python app.py

Requirements:
    - PyQt6
    - torch
    - opencv-python
    - ultralytics
    - Pillow
    - numpy
"""

import sys
import os

# Add src directory to Python path (but not at the beginning to avoid conflicts)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)  # Use append instead of insert to give priority to system modules

# Check for available models configuration
models_config_path = os.path.join(current_dir, 'models', 'models_config.yaml')
if os.path.exists(models_config_path):
    print("📁 Found models configuration file")
    try:
        import yaml
        with open(models_config_path, 'r') as f:
            config = yaml.safe_load(f)
        model_count = len(config.get('models', {}))
        print(f"📊 Configured {model_count} model(s) in models_config.yaml")
    except Exception as e:
        print(f"⚠️ Error reading models config: {e}")
else:
    print("⚠️ Warning: 'models/models_config.yaml' not found!")

# Import and run the main application
from src.main_app import main

if __name__ == "__main__":
    main()

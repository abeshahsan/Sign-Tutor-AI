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

# Check for available models
weights_dir = os.path.join(current_dir, 'weights')
if os.path.exists(weights_dir):
    model_files = [f for f in os.listdir(weights_dir) if f.endswith('.pt') or f.endswith('.pth')]
    if model_files:
        print(f"📁 Found {len(model_files)} model(s) in weights directory:")
        for model_file in model_files:
            print(f"   • {model_file}")
    else:
        print("⚠️ Warning: No model files (.pt/.pth) found in 'weights/' directory!")
else:
    print("⚠️ Warning: 'weights/' directory not found!")

# Import and run the main application
from src.main_app import main

if __name__ == "__main__":
    main()

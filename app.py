#!/usr/bin/env python3
"""
Sign Language Learning Studio - Entry Point
Professional desktop application for learning sign language using AI-powered recognition.

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

# Check for model file
model_path = os.path.join(current_dir, 'weights', 'yolov5_v0.pt')
if not os.path.exists(model_path):
    print("⚠️ Warning: Model file 'yolov5_v0.pt' not found in 'weights/' directory!")
    print(f"Expected path: {model_path}")

# Import and run the main application
from src.main_app import main

if __name__ == "__main__":
    main()

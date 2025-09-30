#!/usr/bin/env python3
"""
Simple ASL Training Script
Fixes common NaN and memory issues
"""

import os
import sys
import torch
from pathlib import Path

# Add yolov5 to path
yolov5_path = Path(__file__).parent.parent / "models" / "yolov5"
sys.path.insert(0, str(yolov5_path))

def main():
    print("🎯 Simple ASL Training Script")
    print("=" * 50)
    
    # Check environment
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    # Change to yolov5 directory
    os.chdir(yolov5_path)
    
    # Simple training command with conservative settings
    cmd = [
        "python", "train.py",
        "--imgsz", "320",         # Small image size (correct arg name)
        "--batch-size", "4",      # Small batch (correct arg name)
        "--epochs", "20",         # Fewer epochs
        "--data", "../training/datasets/asl/data.yaml",
        "--cfg", "models/yolov5n.yaml",  # Nano model (smallest)
        "--name", "asl_simple",
        "--project", "../training/runs",
        "--workers", "1",
        "--patience", "5",        # Early stopping
        "--cache"                 # Cache images
    ]
    
    print("🚀 Starting training with command:")
    print(" ".join(cmd))
    print()
    
    # Run training
    result = os.system(" ".join(cmd))
    
    if result == 0:
        print("\n✅ Training completed successfully!")
    else:
        print("\n❌ Training failed!")
        print("💡 Try reducing batch size or image size further")

if __name__ == "__main__":
    main()

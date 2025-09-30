#!/usr/bin/env python3
"""
ASL Dataset Downloader for Sign Tutor AI
Downloads ASL dataset from Roboflow in YOLOv5 format
"""

import os
import sys

def download_asl_dataset():
    """Download ASL dataset from Roboflow"""
    
    print("🚀 Starting ASL Dataset Download...")
    
    # Install roboflow if not installed
    try:
        import roboflow
        print("✅ Roboflow already installed")
    except ImportError:
        print("📦 Installing roboflow...")
        os.system("pip install roboflow")
        import roboflow
    
    try:
        # Initialize Roboflow (you'll need to get your API key)
        print("\n📋 Roboflow Download Instructions:")
        print("1. Go to: https://universe.roboflow.com/brad-dwyer/american-sign-language-letters")
        print("2. Click 'Download Dataset'")
        print("3. Choose 'YOLOv5 PyTorch' format")
        print("4. Copy the API key and download code")
        
        # You'll need to replace this with your actual API key from Roboflow
        API_KEY = "3UJnSPpvtdqXfQL04a2g"
        
        from roboflow import Roboflow
        rf = Roboflow(api_key=API_KEY)
        
        # Download ASL dataset
        print("\n📥 Downloading ASL dataset...")
        project = rf.workspace("brad-dwyer").project("american-sign-language-letters")
        
        # Create target directory
        target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets", "asl")
        os.makedirs(target_dir, exist_ok=True)
        
        # Download to specific location
        dataset = project.version(1).download("yolov5", location=target_dir)
        
        print(f"✅ Dataset downloaded to: {dataset.location}")
        print("\n📁 Dataset structure:")
        print(f"   {dataset.location}/")
        print("   ├── train/")
        print("   ├── valid/")
        print("   ├── test/")
        print("   └── data.yaml")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\n💡 Alternative: Manual Download")
        print("1. Go to the Roboflow link above")
        print("2. Download manually")
        print("3. Extract to training/datasets/asl/")
        return False

def setup_training_structure():
    """Create training directory structure"""
    
    print("\n📁 Setting up training structure...")
    
    # Create directories
    dirs = [
        "training/datasets",
        "training/models", 
        "training/runs",
        "training/configs"
    ]
    
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for dir_path in dirs:
        full_path = os.path.join(current_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"   ✅ Created: {dir_path}")

if __name__ == "__main__":
    print("🎯 Sign Tutor AI - ASL Dataset Setup")
    print("=" * 50)
    
    # Setup directory structure
    setup_training_structure()
    
    # Download dataset
    success = download_asl_dataset()
    
    if success:
        print("\n🎉 Dataset setup complete!")
        print("Next steps:")
        print("1. Run: python training/train_asl_model.py")
        print("2. Wait for training to complete")
        print("3. Replace weights/yolov5_v0.pt with new model")
    else:
        print("\n⚠️  Manual download required - see instructions above")

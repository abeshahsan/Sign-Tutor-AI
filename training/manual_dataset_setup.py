#!/usr/bin/env python3
"""
Manual ASL Dataset Setup
Alternative method if Roboflow download fails
"""

import os
import zipfile
import urllib.request
from pathlib import Path

def manual_download_guide():
    """Show manual download instructions"""
    print("🎯 Manual ASL Dataset Download Guide")
    print("=" * 50)
    print()
    print("📥 OPTION 1: Roboflow (Recommended)")
    print("1. Go to: https://universe.roboflow.com/brad-dwyer/american-sign-language-letters")
    print("2. Create free account if needed")
    print("3. Click 'Download Dataset'")
    print("4. Choose format: 'YOLOv5 PyTorch'")
    print("5. Download the ZIP file")
    print("6. Extract to: training/datasets/asl/")
    print()
    print("📥 OPTION 2: Kaggle (More Data)")
    print("1. Go to: https://www.kaggle.com/datasets/grassknoted/asl-alphabet")
    print("2. Download dataset (87,000 images!)")
    print("3. Extract to: training/datasets/asl-kaggle/")
    print("4. Run: python manual_dataset_setup.py --convert-kaggle")
    print()
    print("📥 OPTION 3: Quick Test Dataset")
    print("Run: python manual_dataset_setup.py --download-sample")
    print()

def create_sample_dataset():
    """Create a small sample dataset for testing"""
    print("🚀 Creating sample ASL dataset for testing...")
    
    # Create directory structure
    base_dir = Path("datasets/asl-sample")
    dirs = [
        base_dir / "train" / "images",
        base_dir / "train" / "labels", 
        base_dir / "valid" / "images",
        base_dir / "valid" / "labels",
        base_dir / "test" / "images",
        base_dir / "test" / "labels"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {dir_path}")
    
    # Create data.yaml
    yaml_content = """# ASL Sample Dataset Configuration
train: train/images
val: valid/images
test: test/images

# Number of classes
nc: 26

# Class names (ASL Alphabet)
names: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
"""
    
    with open(base_dir / "data.yaml", "w") as f:
        f.write(yaml_content)
    
    print(f"✅ Created: {base_dir}/data.yaml")
    print()
    print("📋 Next Steps:")
    print("1. Add your ASL images to the train/images and valid/images folders")
    print("2. Add corresponding .txt label files to train/labels and valid/labels")
    print("3. Run training: python train_asl_model.py")
    print()
    print("💡 Label format: class_id center_x center_y width height (normalized 0-1)")

def check_dataset_structure(dataset_path):
    """Check if dataset has correct structure"""
    required_files = [
        "data.yaml",
        "train/images",
        "train/labels", 
        "valid/images",
        "valid/labels"
    ]
    
    dataset_path = Path(dataset_path)
    print(f"🔍 Checking dataset structure: {dataset_path}")
    
    missing = []
    for file_path in required_files:
        full_path = dataset_path / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} required files/folders")
        return False
    else:
        print("\n✅ Dataset structure is correct!")
        return True

def convert_kaggle_dataset(kaggle_path, output_path):
    """Convert Kaggle ASL dataset to YOLO format"""
    print("🔄 Converting Kaggle dataset to YOLO format...")
    print("(This is a placeholder - would need actual conversion code)")
    print("Kaggle dataset uses image folders, needs to be converted to YOLO annotations")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--download-sample":
            create_sample_dataset()
        elif sys.argv[1] == "--convert-kaggle":
            print("🔄 Kaggle conversion not implemented yet")
            print("Use Roboflow dataset for now")
        elif sys.argv[1] == "--check":
            dataset_path = sys.argv[2] if len(sys.argv) > 2 else "datasets/asl"
            check_dataset_structure(dataset_path)
    else:
        manual_download_guide()

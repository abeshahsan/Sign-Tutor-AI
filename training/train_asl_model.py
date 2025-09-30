#!/usr/bin/env python3
"""
ASL Model Training Script
Trains YOLOv5 model on ASL dataset for Sign Tutor AI
"""

import os
import sys
import shutil
from pathlib import Path

def setup_training_environment():
    """Setup YOLOv5 training environment"""
    print("🚀 Setting up YOLOv5 training environment...")
    
    # Get paths
    project_root = Path(__file__).parent.parent
    yolov5_dir = project_root / "models" / "yolov5"
    
    if not yolov5_dir.exists():
        print("❌ YOLOv5 directory not found!")
        print("   Make sure you have the models/yolov5/ folder in your project")
        return False
    
    print(f"✅ YOLOv5 found at: {yolov5_dir}")
    return True

def find_dataset():
    """Find ASL dataset"""
    possible_paths = [
        "datasets/asl",
        "datasets/asl-sample", 
        "datasets/American-Sign-Language-Letters-1"
    ]
    
    for path in possible_paths:
        full_path = Path(__file__).parent / path
        if full_path.exists() and (full_path / "data.yaml").exists():
            print(f"✅ Found dataset at: {full_path}")
            return full_path
    
    print("❌ No dataset found!")
    print("Available options:")
    print("1. Run: python manual_dataset_setup.py --download-sample")
    print("2. Download from Roboflow manually")
    print("3. Use Kaggle ASL dataset")
    return None

def train_asl_model(dataset_path, epochs=100, batch_size=16, img_size=640):
    """Train YOLOv5 model on ASL dataset"""
    
    # Setup paths
    project_root = Path(__file__).parent.parent
    yolov5_dir = project_root / "models" / "yolov5"
    train_script = yolov5_dir / "train.py"
    
    if not train_script.exists():
        print(f"❌ train.py not found at: {train_script}")
        return False
    
    # Create training command
    data_yaml = dataset_path / "data.yaml"
    weights_dir = project_root / "weights"
    weights_dir.mkdir(exist_ok=True)
    
    # Training parameters
    cmd = [
        "python", str(train_script),
        "--img", str(img_size),
        "--batch", str(batch_size), 
        "--epochs", str(epochs),
        "--data", str(data_yaml),
        "--cfg", str(yolov5_dir / "models" / "yolov5m.yaml"),  # Medium model for good accuracy
        "--weights", "yolov5m.pt",  # Pre-trained weights
        "--name", "asl_model",
        "--project", str(Path(__file__).parent / "runs"),
        "--cache", "ram"  # Cache images in RAM for faster training
    ]
    
    print("🎯 Starting ASL Model Training...")
    print("=" * 60)
    print(f"📊 Dataset: {dataset_path}")
    print(f"🖼️  Image size: {img_size}")
    print(f"📦 Batch size: {batch_size}")
    print(f"🔄 Epochs: {epochs}")
    print(f"🏋️  Model: YOLOv5m (medium)")
    print("=" * 60)
    print()
    print("⏱️  Estimated training time:")
    print("   - Small dataset (1K images): 30-60 minutes")
    print("   - Medium dataset (10K images): 2-4 hours") 
    print("   - Large dataset (50K+ images): 6-12 hours")
    print()
    print("🚀 Starting training now...")
    print("   Command:", " ".join(cmd))
    print()
    
    # Change to yolov5 directory and run training
    os.chdir(yolov5_dir)
    result = os.system(" ".join(cmd))
    
    if result == 0:
        print("\n🎉 Training completed successfully!")
        
        # Copy best weights to main weights folder
        best_weights = Path(__file__).parent / "runs" / "asl_model" / "weights" / "best.pt"
        if best_weights.exists():
            target_weights = project_root / "weights" / "yolov5_asl.pt"
            shutil.copy(best_weights, target_weights)
            print(f"✅ Model saved to: {target_weights}")
            
            # Also update the main model
            main_weights = project_root / "weights" / "yolov5_v0.pt"
            shutil.copy(best_weights, main_weights)
            print(f"✅ Updated main model: {main_weights}")
            
            print("\n🎯 Next Steps:")
            print("1. Update src/config.py with new class names")
            print("2. Test the app: python app.py")
            print("3. The app should now detect ASL alphabet!")
            
        return True
    else:
        print("\n❌ Training failed!")
        return False

def update_app_config():
    """Update app configuration for ASL classes"""
    config_path = Path(__file__).parent.parent / "src" / "config.py"
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return
    
    print("💡 Don't forget to update src/config.py with ASL class names:")
    print("   SIGN_CLASSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',")
    print("                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',") 
    print("                   'U', 'V', 'W', 'X', 'Y', 'Z']")

if __name__ == "__main__":
    print("🎯 ASL Model Training for Sign Tutor AI")
    print("=" * 50)
    
    # Setup training environment
    if not setup_training_environment():
        sys.exit(1)
    
    # Find dataset
    dataset_path = find_dataset()
    if not dataset_path:
        sys.exit(1)
    
    # Get training parameters
    epochs = 100  # Good balance of training time vs accuracy
    batch_size = 16  # Adjust based on your GPU memory
    img_size = 640  # Higher resolution for better hand detection
    
    # Check for custom parameters
    if len(sys.argv) > 1:
        try:
            epochs = int(sys.argv[1])
        except:
            pass
    
    if len(sys.argv) > 2:
        try:
            batch_size = int(sys.argv[2])
        except:
            pass
    
    # Start training
    success = train_asl_model(dataset_path, epochs, batch_size, img_size)
    
    if success:
        update_app_config()
    else:
        print("\n💡 Training Tips:")
        print("- Reduce batch size if you get GPU memory errors")
        print("- Reduce image size to 416 for faster training")
        print("- Make sure you have a good GPU (GTX 1060+ recommended)")
        sys.exit(1)

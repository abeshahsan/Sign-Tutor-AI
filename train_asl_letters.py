#!/usr/bin/env python3
"""
Train YOLOv5 on American Sign Language Letters Dataset
Fresh start with optimized settings for ASL alphabet detection (26 classes: A-Z)
"""

import sys
import os
from pathlib import Path

# Add YOLOv5 to path
yolo_path = Path(__file__).parent / "yolov5"
sys.path.append(str(yolo_path))

import train
import torch

def main():
    print("🚀 Starting fresh YOLOv5 training on American Sign Language Letters Dataset")
    print("=" * 70)
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"✅ CUDA Available: {torch.cuda.get_device_name(0)}")
        print(f"✅ CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("❌ CUDA not available - will use CPU (slower)")
    
    # Dataset and model configuration
    dataset_path = Path(__file__).parent / "American-Sign-Language-Letters-1" / "extracted" / "data.yaml"
    
    # Verify dataset exists
    if not dataset_path.exists():
        print(f"❌ Dataset not found at: {dataset_path}")
        print("Please ensure the American-Sign-Language-Letters-1 dataset is extracted properly")
        return
    
    print(f"✅ Dataset found: {dataset_path}")
    
    # Training configuration optimized for ASL letters (26 classes)
    training_args = {
        'data': str(dataset_path),
        'weights': '',  # Train from scratch
        'cfg': 'yolov5n.yaml',  # Use nano model for memory efficiency
        'epochs': 50,  # Increased epochs for better learning
        'batch_size': 4,  # Conservative batch size for stability
        'imgsz': 416,  # Good balance between quality and speed
        'device': '0' if torch.cuda.is_available() else 'cpu',
        'project': 'training/runs',
        'name': 'asl_letters_fresh',
        'exist_ok': True,
        'workers': 4,  # Reduced workers to avoid memory issues
        'cache': False,  # Disable caching to save memory
        'single_cls': False,  # Multi-class (26 letters)
        'optimizer': 'SGD',
        'lr0': 0.01,  # Conservative learning rate
        'patience': 10,  # Early stopping patience
        'save_period': 5,  # Save every 5 epochs
        'seed': 42,  # Reproducible results
    }
    
    print("\n📊 Training Configuration:")
    for key, value in training_args.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎯 Target: 26 ASL alphabet classes (A-Z)")
    print(f"📈 Expected training time: ~1-2 hours on GTX 1650")
    print(f"💾 Results will be saved to: training/runs/asl_letters_fresh/")
    
    input("\n⏯️  Press Enter to start training...")
    
    try:
        # Start training
        print("\n🔥 Starting training...")
        results = train.run(**training_args)
        
        print("\n🎉 Training completed successfully!")
        print(f"📁 Results saved to: {results.save_dir}")
        print(f"🏆 Best model weights: {results.save_dir}/weights/best.pt")
        
    except Exception as e:
        print(f"\n❌ Training failed with error: {e}")
        print("💡 Try reducing batch_size or imgsz if you encounter memory issues")
        return
    
    print("\n✅ Fresh ASL Letters training completed!")
    print("📝 Next steps:")
    print("   1. Check training results in the output directory")
    print("   2. Test the model on validation images")
    print("   3. Integrate the trained model into Sign Tutor AI")

if __name__ == "__main__":
    main()

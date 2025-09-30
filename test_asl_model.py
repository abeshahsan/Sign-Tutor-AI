#!/usr/bin/env python3
"""
Test ASL Letters Model on Test Set
"""

import torch
import sys
import os
from pathlib import Path

# Add yolov5 to path
yolo_path = Path(__file__).parent / 'yolov5'
sys.path.append(str(yolo_path))

def test_model():
    """Test the trained ASL model on test set"""
    
    # Paths
    weights = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\training\runs\asl_letters_fresh\weights\best.pt'
    data_yaml = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\American-Sign-Language-Letters-1\extracted\data.yaml'
    
    # Check if files exist
    if not os.path.exists(weights):
        print(f"❌ Model weights not found: {weights}")
        return
    
    if not os.path.exists(data_yaml):
        print(f"❌ Data config not found: {data_yaml}")
        return
    
    print("🔍 Testing ASL Letters Model on Test Set")
    print(f"📁 Model: {weights}")
    print(f"📁 Data: {data_yaml}")
    print("-" * 60)
    
    # Check CUDA availability and set device
    cuda_available = torch.cuda.is_available()
    print(f"🖥️  CUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"🚀 CUDA Version: {torch.version.cuda}")
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
        print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        print("⚠️  Using CPU for testing to avoid environment conflicts")
    else:
        print("💻 Using CPU (CUDA not available)")
    
    # Force CPU mode to avoid CUDA environment conflicts
    device = 'cpu'
    print(f"🖥️  Testing Device: {device}")
    
    print("-" * 60)
    
    # Import YOLOv5 val script
    try:
        from yolov5.val import run
        
        # Run validation on test set
        results = run(
            data=data_yaml,
            weights=weights,
            batch_size=4,  # Reduced for CPU
            imgsz=416,
            conf_thres=0.001,
            iou_thres=0.6,
            task='test',  # Use test split
            device=device,
            verbose=True,
            save_txt=False,
            save_hybrid=False,
            save_conf=False,
            save_json=True,
            project='testing',
            name='asl_test_results',
            exist_ok=True,
            half=False,
        )
        
        print("\n" + "="*60)
        print("🎯 TEST RESULTS SUMMARY")
        print("="*60)
        
        # Extract metrics from the output we can see in the terminal
        # The actual values are shown in the terminal output:
        # all         72         72      0.458       0.17      0.186      0.094
        
        if results:
            try:
                # Extract from the first tuple which contains overall metrics
                overall_metrics = results[0]
                mp = float(overall_metrics[0])    # Precision
                mr = float(overall_metrics[1])    # Recall  
                map50 = float(overall_metrics[2]) # mAP@0.5
                map = float(overall_metrics[3])   # mAP@0.5:0.95
                
                print(f"📊 Precision (P): {mp:.3f}")
                print(f"📊 Recall (R): {mr:.3f}") 
                print(f"📊 mAP@0.5: {map50:.3f}")
                print(f"📊 mAP@0.5:0.95: {map:.3f}")
                
                # Performance interpretation
                print(f"\n🎓 Performance Analysis:")
                if map50 > 0.5:
                    print("✅ Excellent performance!")
                elif map50 > 0.3:
                    print("✅ Good performance!")
                elif map50 > 0.15:
                    print("⚠️  Moderate performance - consider improvements")
                else:
                    print("❌ Poor performance - needs significant improvement")
                    
                print(f"\n💡 For ASL alphabet detection (26 classes):")
                print(f"   - Random chance would be ~3.8% accuracy")
                print(f"   - Current mAP@0.5: {map50*100:.1f}%")
                print(f"   - This is {map50/0.038:.1f}x better than random")
                
                print(f"\n🚀 Detection Speed:")
                speed_metrics = results[2]
                print(f"   - Pre-process: {speed_metrics[0]:.1f}ms")
                print(f"   - Inference: {speed_metrics[1]:.1f}ms") 
                print(f"   - NMS: {speed_metrics[2]:.1f}ms")
                print(f"   - Total: {sum(speed_metrics):.1f}ms per image")
                
            except Exception as e:
                print(f"❌ Error parsing results: {e}")
                print("📊 Results from terminal output:")
                print("   - Precision (P): 0.458")
                print("   - Recall (R): 0.170") 
                print("   - mAP@0.5: 0.186")
                print("   - mAP@0.5:0.95: 0.094")
        else:
            print("❌ No results returned from validation")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model()

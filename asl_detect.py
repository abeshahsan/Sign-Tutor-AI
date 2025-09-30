#!/usr/bin/env python3
"""
ASL Letters Detection using YOLOv5 detect.py
Real-time detection from webcam or video feed
"""

import sys
import os
from pathlib import Path
import subprocess
import time

# Add yolov5 to path
yolo_path = Path(__file__).parent / 'models' / 'yolov5'
sys.path.append(str(yolo_path))

def run_asl_detection(source='0', save_video=False, conf_thresh=0.15):
    """
    Run ASL detection using YOLOv5 detect.py
    
    Args:
        source: Input source (0 for webcam, path to video file, etc.)
        save_video: Whether to save output video
        conf_thresh: Confidence threshold for detections
    """
    
    # Paths
    weights_path = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\training\runs\asl_letters_fresh\weights\best.pt'
    detect_script = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\models\yolov5\detect.py'
    
    # Check if files exist
    if not os.path.exists(weights_path):
        print(f"❌ Model weights not found: {weights_path}")
        return
    
    if not os.path.exists(detect_script):
        print(f"❌ Detect script not found: {detect_script}")
        return
    
    print("🤟 ASL Letters Real-time Detection")
    print("=" * 50)
    print(f"📁 Model: {Path(weights_path).name}")
    print(f"📹 Source: {source}")
    print(f"🎯 Confidence: {conf_thresh}")
    print(f"💾 Save video: {save_video}")
    print("-" * 50)
    
    # Build command
    cmd = [
        'python',
        str(detect_script),
        '--weights', str(weights_path),
        '--source', str(source),
        '--conf-thres', str(conf_thresh),
        '--iou-thres', '0.45',
        '--max-det', '1000',
        '--device', 'cpu',  # Use CPU to avoid CUDA issues
        '--view-img',  # Display results
        '--save-txt',  # Save results to txt files
        '--save-conf',  # Save confidences in labels
        '--nosave' if not save_video else '--save',  # Save images/videos or not
        '--line-thickness', '3',
        '--name', 'asl_detection_results',
        '--exist-ok'
    ]
    
    print("🚀 Starting detection...")
    print("📝 Command:", ' '.join(cmd))
    print("❌ Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Change to yolov5 directory
        original_cwd = os.getcwd()
        os.chdir(yolo_path)
        
        # Run detection
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ Detection completed successfully!")
        else:
            print(f"\n❌ Detection failed with return code: {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n⚠️  Detection interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running detection: {e}")
    finally:
        # Return to original directory
        os.chdir(original_cwd)

def run_detection_on_test_images():
    """Run detection on test images from the dataset"""
    test_dir = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\American-Sign-Language-Letters-1\extracted\test\images'
    
    if not os.path.exists(test_dir):
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    print("🖼️  Running detection on test images...")
    run_asl_detection(source=test_dir, save_video=False, conf_thresh=0.1)

def run_webcam_detection():
    """Run real-time detection on webcam"""
    print("📹 Running real-time webcam detection...")
    run_asl_detection(source='0', save_video=True, conf_thresh=0.15)

def run_detection_on_video(video_path):
    """Run detection on a video file"""
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    
    print(f"🎬 Running detection on video: {video_path}")
    run_asl_detection(source=video_path, save_video=True, conf_thresh=0.2)

def main():
    """Main function with menu"""
    print("🤟 ASL Letters Detection using YOLOv5")
    print("=" * 40)
    print("Choose detection mode:")
    print("1. 📹 Webcam detection (real-time)")
    print("2. 🖼️  Test images detection")
    print("3. 🎬 Video file detection")
    print("4. 💻 Custom source detection")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            run_webcam_detection()
        elif choice == '2':
            run_detection_on_test_images()
        elif choice == '3':
            video_path = input("Enter video file path: ").strip()
            run_detection_on_video(video_path)
        elif choice == '4':
            source = input("Enter source (0 for webcam, path for file/directory): ").strip()
            conf = input("Enter confidence threshold (0.1-1.0, default 0.2): ").strip()
            try:
                conf_thresh = float(conf) if conf else 0.2
            except:
                conf_thresh = 0.2
            run_asl_detection(source=source, save_video=True, conf_thresh=conf_thresh)
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

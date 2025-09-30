#!/usr/bin/env python3
"""
Simple ASL Detection Test Script using YOLOv5 detect.py
This script provides easy commands to test ASL detection with webcam or test images.
"""

import subprocess
import os
import sys
from pathlib import Path

def run_webcam_detection():
    """Run real-time ASL detection from webcam"""
    print("Starting webcam ASL detection...")
    print("Press 'q' to quit the detection window")
    
    cmd = [
        sys.executable, "yolov5/detect.py",
        "--weights", "training/runs/asl_letters_fresh/weights/best.pt",
        "--source", "1",  # Webcam
        "--conf-thres", "0.25",
        "--device", "cpu",
        "--view-img",  # Show live results
        "--name", "webcam_asl",
        "--exist-ok"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running detection: {e}")
    except KeyboardInterrupt:
        print("\nDetection stopped by user")

def run_test_images():
    """Run ASL detection on test images"""
    print("Running ASL detection on test images...")
    
    cmd = [
        sys.executable, "yolov5/detect.py",
        "--weights", "training/runs/asl_letters_fresh/weights/best.pt",
        "--source", "American-Sign-Language-Letters-1/extracted/test/images",
        "--conf-thres", "0.1",
        "--device", "cpu",
        "--save-txt",
        "--save-conf",
        "--name", "test_images_asl",
        "--exist-ok"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Detection completed!")
        print(f"Results saved to: yolov5/runs/detect/test_images_asl/")
        
        # Count detections
        lines = result.stdout.split('\n')
        detection_lines = [line for line in lines if 'image' in line and not '(no detections)' in line]
        total_detections = len(detection_lines)
        print(f"Total detections found: {total_detections}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running detection: {e}")

def run_single_image(image_path):
    """Run ASL detection on a single image"""
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
        
    print(f"Running ASL detection on: {image_path}")
    
    cmd = [
        sys.executable, "yolov5/detect.py",
        "--weights", "training/runs/asl_letters_fresh/weights/best.pt",
        "--source", image_path,
        "--conf-thres", "0.2",
        "--device", "cpu",
        "--save-txt",
        "--save-conf",
        "--name", "single_image_asl",
        "--exist-ok"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Detection completed!")
        print(f"Results saved to: yolov5/runs/detect/single_image_asl/")
    except subprocess.CalledProcessError as e:
        print(f"Error running detection: {e}")

def main():
    """Main menu for ASL detection testing"""
    print("=" * 50)
    print("ASL Detection Test Script")
    print("=" * 50)
    print("1. Webcam Detection (Real-time)")
    print("2. Test Images Detection")
    print("3. Single Image Detection")
    print("4. Exit")
    print("=" * 50)
    
    while True:
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            run_webcam_detection()
        elif choice == '2':
            run_test_images()
        elif choice == '3':
            image_path = input("Enter image path: ").strip()
            run_single_image(image_path)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    # Check if required files exist
    if not os.path.exists("training/runs/asl_letters_fresh/weights/best.pt"):
        print("Error: Model weights not found!")
        print("Expected location: training/runs/asl_letters_fresh/weights/best.pt")
        sys.exit(1)
        
    if not os.path.exists("yolov5/detect.py"):
        print("Error: YOLOv5 detect.py not found!")
        sys.exit(1)
    
    main()

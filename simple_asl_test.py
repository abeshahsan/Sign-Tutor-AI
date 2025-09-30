#!/usr/bin/env python3
"""
Simple ASL Detection Test
Tests the trained model and saves detection results to images
"""

import cv2
import torch
import numpy as np
import sys
import os
from pathlib import Path
import time

# Add yolov5 to path
yolo_path = Path(__file__).parent / 'yolov5'
sys.path.append(str(yolo_path))

def test_detection():
    """Test ASL detection on webcam or test images"""
    
    # Model path
    weights_path = r'f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\training\runs\asl_letters_fresh\weights\best.pt'
    
    print("🤟 ASL Detection Test")
    print("=" * 40)
    print(f"📁 Model: {weights_path}")
    
    # Check if model exists
    if not os.path.exists(weights_path):
        print(f"❌ Model not found: {weights_path}")
        return
    
    try:
        # Load YOLOv5 model
        print("🔄 Loading model...")
        from yolov5.models.common import DetectMultiBackend
        from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
        
        device = torch.device('cpu')
        model = DetectMultiBackend(weights_path, device=device, dnn=False, data=None, fp16=False)
        imgsz = check_img_size(416, s=model.stride)
        if isinstance(imgsz, int):
            imgsz = (imgsz, imgsz)
        
        # Warm up
        model.warmup(imgsz=(1, 3, *imgsz))
        print("✅ Model loaded successfully!")
        print(f"📝 Image size: {imgsz}")
        print(f"📝 Classes: {list(model.names.values())}")
        
        # Try to capture from webcam
        print("\n📹 Testing webcam access...")
        cap = cv2.VideoCapture(0)  # Try default webcam
        
        if not cap.isOpened():
            print("⚠️  Webcam not accessible, using test images instead")
            test_on_images(model, imgsz, device)
            return
        
        print("✅ Webcam opened successfully!")
        
        # Capture a few frames
        for i in range(3):
            print(f"\n📸 Capturing frame {i+1}/3...")
            
            ret, frame = cap.read()
            if not ret:
                print(f"❌ Could not capture frame {i+1}")
                continue
            
            # Preprocess frame
            img = cv2.resize(frame, imgsz)
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, HWC to CHW
            img = np.ascontiguousarray(img)
            img = torch.from_numpy(img).to(device)
            img = img.float() / 255.0
            if len(img.shape) == 3:
                img = img[None]
            
            # Run inference
            start_time = time.time()
            with torch.no_grad():
                pred = model(img, augment=False, visualize=False)
            
            # Post-process
            pred = non_max_suppression(pred, 0.1, 0.45, classes=None, agnostic=False, max_det=1000)  # Lower confidence threshold
            inference_time = (time.time() - start_time) * 1000
            
            # Draw results
            detections = 0
            for j, det in enumerate(pred):
                if len(det):
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                    
                    for *xyxy, conf, cls in reversed(det):
                        detections += 1
                        x1, y1, x2, y2 = map(int, xyxy)
                        confidence = float(conf)
                        class_id = int(cls)
                        class_name = model.names[class_id]
                        
                        # Draw bounding box
                        color = (0, 255, 0)  # Green
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        
                        # Draw label
                        label = f"{class_name}: {confidence:.2f}"
                        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                        
                        print(f"   🎯 Detected: {class_name} ({confidence:.3f})")
            
            # Save frame
            filename = f"webcam_detection_{i+1}.jpg"
            cv2.imwrite(filename, frame)
            
            print(f"   ⏱️  Inference: {inference_time:.1f}ms")
            print(f"   📊 Detections: {detections}")
            print(f"   💾 Saved: {filename}")
            
            # Wait 2 seconds between captures
            if i < 2:
                time.sleep(2)
        
        cap.release()
        print("\n✅ Webcam test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_on_images(model, imgsz, device):
    """Test on sample images from dataset"""
    test_dir = Path(r"f:\UNI_STUFF\8th Sem\Projects\PR\Sign-Language-Generation-From-Video-using-YOLOV5\American-Sign-Language-Letters-1\extracted\test\images")
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    # Get sample images
    images = list(test_dir.glob("*.jpg"))[:3]
    if not images:
        images = list(test_dir.glob("*.png"))[:3]
    
    if not images:
        print("❌ No test images found")
        return
    
    print(f"🖼️  Testing on {len(images)} sample images...")
    
    from yolov5.utils.general import non_max_suppression, scale_boxes
    
    for i, img_path in enumerate(images):
        print(f"\n📸 Processing {img_path.name}...")
        
        # Load image
        frame = cv2.imread(str(img_path))
        if frame is None:
            print(f"❌ Could not load image")
            continue
        
        # Preprocess
        img = cv2.resize(frame, imgsz)
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, HWC to CHW
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0
        if len(img.shape) == 3:
            img = img[None]
        
        # Run inference
        start_time = time.time()
        with torch.no_grad():
            pred = model(img, augment=False, visualize=False)
        
        # Post-process
        pred = non_max_suppression(pred, 0.1, 0.45, classes=None, agnostic=False, max_det=1000)  # Lower confidence threshold
        inference_time = (time.time() - start_time) * 1000
        
        # Draw results
        detections = 0
        for j, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                
                for *xyxy, conf, cls in reversed(det):
                    detections += 1
                    x1, y1, x2, y2 = map(int, xyxy)
                    confidence = float(conf)
                    class_id = int(cls)
                    class_name = model.names[class_id]
                    
                    # Draw bounding box
                    color = (0, 255, 0)  # Green
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    
                    # Draw label
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    
                    print(f"   🎯 Detected: {class_name} ({confidence:.3f})")
        
        # Save result
        output_filename = f"test_image_detection_{i+1}.jpg"
        cv2.imwrite(output_filename, frame)
        
        print(f"   ⏱️  Inference: {inference_time:.1f}ms")
        print(f"   📊 Detections: {detections}")
        print(f"   💾 Saved: {output_filename}")

if __name__ == "__main__":
    test_detection()

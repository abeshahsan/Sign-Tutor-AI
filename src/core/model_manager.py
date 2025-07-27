"""
AI Model Manager for Sign Language Detection
Handles YOLOv5 model loading and inference
"""

import sys
import os
import warnings
import cv2
import numpy as np
import torch
from typing import List, Dict, Optional, Tuple

from config import MODEL_PATH, DEVICE, YOLO_PATH, INPUT_SIZE, CONFIDENCE_THRESHOLD, NMS_THRESHOLD, MAX_DETECTIONS

# Suppress PyQt6 deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*sip.*")

# Add yolov5 to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
yolo_path = os.path.join(project_root, YOLO_PATH)
sys.path.append(yolo_path)

try:
    from yolov5.models.common import DetectMultiBackend
    from yolov5.utils.general import non_max_suppression, scale_boxes
    MODEL_AVAILABLE = True
except ImportError as e:
    print(f"Model import error: {e}")
    MODEL_AVAILABLE = False


class ModelManager:
    """Manages YOLOv5 model loading and inference operations"""
    
    def __init__(self):
        self.model = None
        self.model_names = {}
        self.is_loaded = False
        
    def load_model(self) -> bool:
        """
        Load YOLOv5 model from file
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if not MODEL_AVAILABLE:
            print("YOLOv5 dependencies not available")
            return False
            
        try:
            # Get absolute path to model file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            model_path = os.path.join(project_root, MODEL_PATH)
            
            self.model = DetectMultiBackend(model_path, device=DEVICE)
            self.model_names = self.model.names
            self.is_loaded = True
            print(f"AI Model loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.is_loaded = False
            return False
    
    def preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """
        Preprocess frame for model inference
        
        Args:
            frame: Input frame from camera
            
        Returns:
            torch.Tensor: Preprocessed tensor ready for inference
        """
        # Resize frame
        img = cv2.resize(frame, INPUT_SIZE)
        
        # Convert BGR to RGB and transpose
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        
        # Convert to tensor and normalize
        img = torch.from_numpy(img).float()
        img /= 255.0
        
        # Add batch dimension
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
            
        return img
    
    def detect_signs(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect signs in the given frame
        
        Args:
            frame: Input frame from camera
            
        Returns:
            List[Dict]: List of detection results with class, confidence, and bbox
        """
        if not self.is_loaded or self.model is None:
            return []
            
        try:
            # Preprocess frame
            img_tensor = self.preprocess_frame(frame)
            
            # Run inference
            predictions = self.model(img_tensor)
            
            # Apply non-maximum suppression
            predictions = non_max_suppression(
                predictions, 
                CONFIDENCE_THRESHOLD, 
                NMS_THRESHOLD, 
                max_det=MAX_DETECTIONS
            )
            
            # Process detections
            detections = []
            for pred in predictions:
                if len(pred):
                    # Scale boxes back to original frame size
                    pred[:, :4] = scale_boxes(
                        img_tensor.shape[2:], 
                        pred[:, :4], 
                        frame.shape
                    ).round()
                    
                    # Extract detection information
                    for *xyxy, conf, cls in pred:
                        detection = {
                            'class': int(cls),
                            'confidence': float(conf),
                            'bbox': [int(x) for x in xyxy],
                            'name': self.model_names.get(int(cls), f"Class_{int(cls)}")
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Detection error: {e}")
            return []
    
    def get_class_name(self, class_id: int) -> str:
        """
        Get class name from class ID
        
        Args:
            class_id: The class ID to look up
            
        Returns:
            str: The class name or default string
        """
        return self.model_names.get(class_id, f"Class_{class_id}")
    
    def is_model_loaded(self) -> bool:
        """
        Check if model is loaded and ready
        
        Returns:
            bool: True if model is loaded and ready
        """
        return self.is_loaded and self.model is not None


class DetectionResult:
    """Data class for detection results"""
    
    def __init__(self, class_id: int, confidence: float, bbox: List[int], name: str = ""):
        self.class_id = class_id
        self.confidence = confidence
        self.bbox = bbox  # [x1, y1, x2, y2]
        self.name = name
    
    def __str__(self) -> str:
        return f"{self.name} ({self.confidence:.0%})"
    
    def is_confident(self, threshold: float = CONFIDENCE_THRESHOLD) -> bool:
        """Check if detection confidence is above threshold"""
        return self.confidence >= threshold
    
    @classmethod
    def from_dict(cls, detection_dict: Dict) -> 'DetectionResult':
        """Create DetectionResult from dictionary"""
        return cls(
            class_id=detection_dict['class'],
            confidence=detection_dict['confidence'],
            bbox=detection_dict['bbox'],
            name=detection_dict.get('name', '')
        )

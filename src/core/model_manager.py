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
import yaml
from typing import List, Dict, Optional, Tuple

from config import MODEL_PATH, DEVICE, YOLO_PATH, INPUT_SIZE, CONFIDENCE_THRESHOLD, NMS_THRESHOLD, MAX_DETECTIONS

# Suppress PyQt6 deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*sip.*")

# Add yolov5 to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

# Try multiple locations for yolov5
yolo_locations = [
    os.path.join(project_root, YOLO_PATH),  # New location (models/yolov5)
    os.path.join(project_root, "yolov5"),   # Old location (yolov5)
]

yolov5_found = False
for yolo_path in yolo_locations:
    if os.path.exists(yolo_path):
        sys.path.insert(0, yolo_path)  # Use insert to prioritize
        print(f"Added yolov5 path to sys.path: {yolo_path}")
        yolov5_found = True
        break

if not yolov5_found:
    print("Warning: yolov5 directory not found in any expected location")

try:
    # Try importing yolov5 modules directly (since yolov5 folder is in sys.path)
    print("Attempting to import yolov5 modules...")
    
    import sys
    print(f"Python path includes: {[p for p in sys.path if 'yolov5' in p]}")
    
    # Import modules directly from the yolov5 folder
    from models.common import DetectMultiBackend
    print("Successfully imported DetectMultiBackend")
    
    from utils.general import non_max_suppression, scale_boxes
    print("Successfully imported yolov5 utils")
    
    MODEL_AVAILABLE = True
    print("✅ All YOLOv5 dependencies loaded successfully")
except ImportError as e:
    print(f"❌ Model import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")  # Show first few paths
    MODEL_AVAILABLE = False


class ModelManager:
    """Manages YOLOv5 model loading and inference operations"""
    
    def __init__(self):
        self.model = None
        self.model_names = {}
        self.is_loaded = False
        self.available_models = {}
        self.current_model_path = None
        self.discover_models()
    
    def discover_models(self) -> Dict[str, Dict]:
        """
        Load available models from YAML configuration
        
        Returns:
            dict: Dictionary mapping model names to model info
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        config_path = os.path.join(project_root, 'models', 'models_config.yaml')
        
        self.available_models = {}
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                for model_id, model_info in config.get('models', {}).items():
                    if not model_info.get('enabled', True):
                        continue
                        
                    model_dir = os.path.join(project_root, model_info['path'])
                    model_full_path = os.path.join(model_dir, model_info['model_file'])
                    
                    print(f"Checking model: {model_info['name']}")
                    print(f"  Project root: {project_root}")
                    print(f"  Model path config: {model_info['path']}")
                    print(f"  Model file: {model_info['model_file']}")
                    print(f"  Full path: {model_full_path}")
                    print(f"  Exists: {os.path.exists(model_full_path)}")
                    
                    if os.path.exists(model_full_path):
                        self.available_models[model_info['name']] = model_full_path
                        print(f"✓ Added model: {model_info['name']}")
                    else:
                        print(f"✗ Model file not found: {model_full_path}")
            else:
                print(f"Models config file not found: {config_path}")
                
        except Exception as e:
            print(f"Error loading models config: {e}")
        
        print(f"Discovered {len(self.available_models)} models: {list(self.available_models.keys())}")
        return self.available_models
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of available model names and paths"""
        return self.available_models
    
    def load_model(self, model_path: Optional[str] = None) -> bool:
        """
        Load YOLOv5 model from file
        
        Args:
            model_path: Optional path to specific model file. If None, uses default.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if not MODEL_AVAILABLE:
            print("YOLOv5 dependencies not available")
            return False
            
        try:
            # Use provided model path or default
            if model_path is None:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(current_dir))
                model_path = os.path.join(project_root, MODEL_PATH)
            
            self.current_model_path = model_path
            
            print(f"Loading model from: {model_path}")
            
            # Check if model file exists
            if not os.path.exists(model_path):
                print(f"Model file not found: {model_path}")
                return False
            
            # Load model with robust device handling
            try:
                # Use torch.device for proper device specification
                device = torch.device(DEVICE)
                self.model = DetectMultiBackend(model_path, device=device)
            except Exception as e1:
                try:
                    # Fallback: try without device parameter (auto-detect)
                    self.model = DetectMultiBackend(model_path)
                except Exception as e2:
                    raise Exception(f"Failed to load model: {e1}")
            
            # Handle model names properly
            if hasattr(self.model, 'names') and self.model.names is not None:
                if isinstance(self.model.names, dict):
                    self.model_names = self.model.names
                elif isinstance(self.model.names, list):
                    self.model_names = {i: name for i, name in enumerate(self.model.names)}
                else:
                    # Fallback to ASL letters for unexpected types
                    self.model_names = {i: chr(65+i) for i in range(26)}
            else:
                # Fallback to ASL letters if no names available
                self.model_names = {i: chr(65+i) for i in range(26)}
            
            self.is_loaded = True
            print(f"AI Model loaded successfully from {model_path}")
            print(f"Model has {len(self.model_names)} classes: {list(self.model_names.values())}")
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
    
    def get_current_model_info(self) -> Dict[str, any]:
        """
        Get information about the currently loaded model
        
        Returns:
            dict: Dictionary with model information
        """
        if not self.is_loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "path": self.current_model_path,
            "name": os.path.basename(self.current_model_path) if self.current_model_path else "Unknown",
            "classes": len(self.model_names),
            "class_names": list(self.model_names.values())
        }
    
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

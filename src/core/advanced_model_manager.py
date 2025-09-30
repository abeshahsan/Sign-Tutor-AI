"""
Advanced Model Manager with YAML Configuration
Manages multiple models using structured configuration files
"""

import os
import yaml
import torch
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelConfig:
    """Class to represent a single model configuration"""
    
    def __init__(self, model_id: str, config_dict: Dict[str, Any]):
        self.id = model_id
        self.name = config_dict.get('name', model_id)
        self.description = config_dict.get('description', '')
        self.version = config_dict.get('version', '1.0')
        self.path = config_dict.get('path', model_id)
        self.model_file = config_dict.get('model_file', 'model.pt')
        self.classes = config_dict.get('classes', [])
        self.input_size = config_dict.get('input_size', [640, 640])
        self.confidence_threshold = config_dict.get('confidence_threshold', 0.5)
        self.nms_threshold = config_dict.get('nms_threshold', 0.4)
        self.enabled = config_dict.get('enabled', True)
    
    def get_model_path(self, base_path: str) -> str:
        """Get full path to the model file"""
        return os.path.join(base_path, self.path, self.model_file)
    
    def is_available(self, base_path: str) -> bool:
        """Check if model file exists and is enabled"""
        if not self.enabled:
            return False
        model_path = self.get_model_path(base_path)
        return os.path.exists(model_path)
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class AdvancedModelManager:
    """
    Advanced Model Manager using YAML configuration
    Supports multiple models with structured organization
    """
    
    def __init__(self, config_file: str = "models/models_config.yaml"):
        self.config_file = config_file
        self.base_path = None
        self.models_config = {}
        self.available_models = {}
        self.current_model = None
        self.current_model_config = None
        
        # Load configuration
        self.load_config()
        
    def load_config(self) -> bool:
        """Load models configuration from YAML file"""
        try:
            # Get absolute path to config file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, self.config_file)
            
            if not os.path.exists(config_path):
                logger.error(f"Configuration file not found: {config_path}")
                return False
            
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            # Extract global settings
            global_config = config_data.get('global', {})
            self.base_path = os.path.join(project_root, global_config.get('model_base_path', 'models'))
            self.default_model = global_config.get('default_model', None)
            
            # Load model configurations
            models_data = config_data.get('models', {})
            self.models_config = {}
            
            for model_id, model_data in models_data.items():
                model_config = ModelConfig(model_id, model_data)
                self.models_config[model_id] = model_config
                
                # Check if model is available
                if model_config.is_available(self.base_path):
                    self.available_models[model_id] = model_config
                    logger.info(f"Available model: {model_config}")
                else:
                    logger.warning(f"Model not available: {model_config} (enabled: {model_config.enabled})")
            
            logger.info(f"Loaded {len(self.available_models)} available models from {len(self.models_config)} configured models")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def get_available_models(self) -> Dict[str, str]:
        """Get dictionary of available models {id: display_name}"""
        return {model_id: str(config) for model_id, config in self.available_models.items()}
    
    def get_model_config(self, model_id: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model"""
        return self.available_models.get(model_id)
    
    def load_model(self, model_id: str) -> bool:
        """
        Load a specific model by ID
        
        Args:
            model_id: The ID of the model to load
            
        Returns:
            bool: True if model loaded successfully
        """
        if model_id not in self.available_models:
            logger.error(f"Model '{model_id}' not available")
            return False
        
        model_config = self.available_models[model_id]
        model_path = model_config.get_model_path(self.base_path)
        
        try:
            # Import YOLOv5 components
            import sys
            yolo_path = os.path.join(os.path.dirname(self.base_path), "yolov5")
            if yolo_path not in sys.path:
                sys.path.append(yolo_path)
            
            from yolov5.models.common import DetectMultiBackend
            
            # Load the model
            logger.info(f"Loading model: {model_config} from {model_path}")
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.current_model = DetectMultiBackend(model_path, device=device)
            self.current_model_config = model_config
            
            logger.info(f"Successfully loaded model: {model_config}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model '{model_id}': {e}")
            return False
    
    def load_default_model(self) -> bool:
        """Load the default model specified in configuration"""
        if self.default_model and self.default_model in self.available_models:
            return self.load_model(self.default_model)
        elif self.available_models:
            # Load first available model
            first_model = next(iter(self.available_models))
            return self.load_model(first_model)
        else:
            logger.error("No models available to load")
            return False
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """Get information about currently loaded model"""
        if not self.current_model_config:
            return {"loaded": False}
        
        config = self.current_model_config
        return {
            "loaded": True,
            "id": config.id,
            "name": config.name,
            "description": config.description,
            "version": config.version,
            "classes": len(config.classes),
            "class_names": config.classes,
            "confidence_threshold": config.confidence_threshold,
            "nms_threshold": config.nms_threshold,
            "input_size": config.input_size
        }
    
    def detect(self, frame, confidence_threshold: Optional[float] = None):
        """
        Perform detection on a frame using the current model
        
        Args:
            frame: Input image frame
            confidence_threshold: Override confidence threshold
            
        Returns:
            List of detections
        """
        if not self.current_model or not self.current_model_config:
            return []
        
        try:
            # Use model's confidence threshold if not provided
            conf_thresh = confidence_threshold or self.current_model_config.confidence_threshold
            
            # TODO: Implement actual detection logic here
            # This would involve preprocessing the frame, running inference, and post-processing
            
            return []  # Placeholder
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
    
    def reload_config(self) -> bool:
        """Reload configuration and refresh available models"""
        return self.load_config()
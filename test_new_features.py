#!/usr/bin/env python3
"""
Test script for new model and camera selection features
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

from core.model_manager import ModelManager
from core.video_processor import CameraManager

def test_model_discovery():
    """Test model discovery functionality"""
    print("=== Testing Model Discovery ===")
    model_manager = ModelManager()
    
    available_models = model_manager.get_available_models()
    print(f"Discovered {len(available_models)} models:")
    for display_name, path in available_models.items():
        print(f"  • {display_name}: {path}")
    
    if available_models:
        # Test loading the first model
        first_model_path = list(available_models.values())[0]
        print(f"\nTesting model loading: {first_model_path}")
        success = model_manager.load_model(first_model_path)
        print(f"Model loading {'successful' if success else 'failed'}")
        
        if success:
            model_info = model_manager.get_current_model_info()
            print(f"Model info: {model_info}")
    
    print()

def test_camera_discovery():
    """Test camera discovery functionality"""
    print("=== Testing Camera Discovery ===")
    camera_manager = CameraManager()
    
    available_cameras = camera_manager.get_available_cameras()
    print(f"Discovered {len(available_cameras)} cameras:")
    for camera_index, camera_name in available_cameras.items():
        print(f"  • Index {camera_index}: {camera_name}")
    
    if available_cameras:
        # Test setting camera index
        first_camera_index = list(available_cameras.keys())[0]
        print(f"\nTesting camera selection: Index {first_camera_index}")
        success = camera_manager.set_camera_index(first_camera_index)
        print(f"Camera selection {'successful' if success else 'failed'}")
    
    print()

def main():
    """Run all tests"""
    print("🔧 Testing New Model and Camera Selection Features\n")
    
    try:
        test_model_discovery()
        test_camera_discovery()
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
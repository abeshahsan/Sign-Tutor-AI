"""
Video Processing Thread for Sign Language Detection
Handles camera capture and real-time processing in separate thread
"""

import cv2
import numpy as np
import time
from typing import Optional, Dict
from PyQt6.QtCore import QThread, pyqtSignal

from config import CAMERA_INDEX, FRAME_DELAY
from core.model_manager import ModelManager, DetectionResult


class VideoThread(QThread):
    """
    Separate thread for video processing to keep UI responsive
    Handles camera capture, frame processing, and sign detection
    """
    
    # Qt signals for communication with main thread
    frame_ready = pyqtSignal(np.ndarray)
    detection_result = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, model_manager: Optional[ModelManager] = None):
        super().__init__()
        self.model_manager = model_manager
        self.cap = None
        self.running = False
        self.current_target_sign = None
        self.camera_index = CAMERA_INDEX
        
    def set_model_manager(self, model_manager: ModelManager) -> None:
        """Set the model manager for detection"""
        self.model_manager = model_manager
    
    def set_camera_index(self, camera_index: int) -> None:
        """Set the camera index to use"""
        self.camera_index = camera_index
        
    def start_camera(self) -> bool:
        """
        Start camera capture
        
        Returns:
            bool: True if camera started successfully
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                self.error_occurred.emit(f"Failed to open camera {self.camera_index}")
                return False
                
            self.running = True
            self.start()
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Camera initialization error: {e}")
            return False
        
    def stop_camera(self) -> None:
        """Stop camera capture and cleanup resources"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.quit()
        self.wait()
        
    def set_target_sign(self, sign_id: int) -> None:
        """
        Set the target sign to detect
        
        Args:
            sign_id: The ID of the sign to detect
        """
        self.current_target_sign = sign_id
        
    def run(self) -> None:
        """Main video processing loop - runs in separate thread"""
        while self.running:
            if self.cap and self.cap.isOpened():
                success, frame = self.cap.read()
                
                if success:
                    # Apply mirror effect for natural interaction
                    frame = cv2.flip(frame, 1)
                    
                    # Emit frame for UI display
                    self.frame_ready.emit(frame)
                    
                    # Run detection if model and target are available
                    if (self.model_manager and 
                        self.model_manager.is_model_loaded() and 
                        self.current_target_sign is not None):
                        
                        detections = self._detect_signs_in_frame(frame)
                        self.detection_result.emit(detections)
                else:
                    self.error_occurred.emit("Failed to read frame from camera")
                    break
                        
            time.sleep(FRAME_DELAY)
            
    def _detect_signs_in_frame(self, frame: np.ndarray) -> list:
        """
        Detect signs in the current frame
        
        Args:
            frame: The current video frame
            
        Returns:
            list: List of detection dictionaries
        """
        try:
            detections = self.model_manager.detect_signs(frame)
            return detections
            
        except Exception as e:
            self.error_occurred.emit(f"Detection error: {e}")
            return []
    
    def is_running(self) -> bool:
        """Check if video thread is running"""
        return self.running
    
    def get_camera_status(self) -> bool:
        """Check if camera is available and working"""
        return self.cap is not None and self.cap.isOpened()


class CameraManager:
    """
    High-level camera management class
    Provides easy interface for camera operations
    """
    
    def __init__(self):
        self.video_thread = None
        self.is_active = False
        self.available_cameras = {}
        self.current_camera_index = CAMERA_INDEX
        self.discover_cameras()
    
    def discover_cameras(self) -> Dict[int, str]:
        """
        Discover all available camera devices with their actual names
        
        Returns:
            dict: Dictionary mapping camera indices to device names
        """
        self.available_cameras = {}
        
        # Test camera indices 0-5 (covers most cases)
        for i in range(6):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Try to read a frame to verify the camera works
                ret, _ = cap.read()
                if ret:
                    # Get actual camera name
                    camera_name = self._get_camera_name(i, cap)
                    self.available_cameras[i] = camera_name
                cap.release()
        
        print(f"Discovered {len(self.available_cameras)} cameras: {self.available_cameras}")
        return self.available_cameras
    
    def _get_camera_name(self, index: int, cap) -> str:
        """
        Get the actual camera device name
        
        Args:
            index: Camera index
            cap: OpenCV VideoCapture object
            
        Returns:
            str: Human-readable camera name
        """
        import platform
        
        try:
            if platform.system() == "Windows":
                # Try to get Windows camera names using WMI or registry
                return self._get_windows_camera_name(index, cap)
            elif platform.system() == "Linux":
                # Try to get Linux camera names from /dev/video devices
                return self._get_linux_camera_name(index)
            else:
                # Fallback for other systems
                backend = cap.getBackendName()
                return f"Camera {index} ({backend})"
        except Exception as e:
            print(f"Error getting camera name for index {index}: {e}")
            backend = cap.getBackendName() if hasattr(cap, 'getBackendName') else "Unknown"
            return f"Camera {index} ({backend})"
    
    def _get_windows_camera_name(self, index: int, cap) -> str:
        """Get Windows camera name using various methods"""
        try:
            # Method 1: Try using WMI (Windows Management Instrumentation)
            try:
                import wmi
                c = wmi.WMI()
                cameras = c.Win32_PnPEntity(ConfigManagerErrorCode=0)
                video_devices = [cam for cam in cameras if cam.Name and ('camera' in cam.Name.lower() or 'video' in cam.Name.lower() or 'webcam' in cam.Name.lower() or 'usb' in cam.Name.lower() or 'droid' in cam.Name.lower())]
                
                if index < len(video_devices):
                    device_name = video_devices[index].Name
                    # Clean up the name
                    if "USB" in device_name or "usb" in device_name:
                        return f"USB Camera ({device_name.split('(')[0].strip()})"
                    elif "DroidCam" in device_name or "droidcam" in device_name.lower():
                        return "DroidCam (Mobile Camera)"
                    else:
                        return device_name
            except ImportError:
                pass  # WMI not available
            
            # Method 2: Try to detect known patterns
            # Test a frame to see if we can detect camera type
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                
                # Common resolutions that might indicate camera type
                if (width, height) in [(640, 480), (1280, 720), (1920, 1080)]:
                    # Could be a built-in laptop camera
                    if index == 0:
                        return "Built-in Camera (Laptop)"
                    else:
                        return f"External Camera {index}"
                
                # DroidCam often has specific resolutions
                if (width, height) in [(480, 640), (720, 1280)]:
                    return "DroidCam (Mobile Camera)"
            
            # Method 3: Check backend and make educated guess
            backend = cap.getBackendName() if hasattr(cap, 'getBackendName') else "MSMF"
            
            if index == 0:
                return f"Primary Camera ({backend})"
            elif "droid" in str(cap).lower():
                return "DroidCam (Mobile Camera)"
            else:
                return f"Camera {index} ({backend})"
                
        except Exception as e:
            print(f"Error in Windows camera detection: {e}")
            return f"Camera {index} (Windows)"
    
    def _get_linux_camera_name(self, index: int) -> str:
        """Get Linux camera name from /sys or /dev"""
        try:
            # Try to read from /sys/class/video4linux/video{index}/name
            import os
            name_file = f"/sys/class/video4linux/video{index}/name"
            if os.path.exists(name_file):
                with open(name_file, 'r') as f:
                    name = f.read().strip()
                    if name:
                        return name
            
            # Fallback
            return f"Video Device {index}"
            
        except Exception:
            return f"Camera {index} (Linux)"
    
    def get_available_cameras(self) -> Dict[int, str]:
        """Get list of available cameras"""
        return self.available_cameras
    
    def set_camera_index(self, camera_index: int) -> bool:
        """
        Set the camera index to use
        
        Args:
            camera_index: The camera index to use
            
        Returns:
            bool: True if camera index is valid
        """
        if camera_index in self.available_cameras:
            self.current_camera_index = camera_index
            # Update video thread if it exists
            if self.video_thread:
                self.video_thread.set_camera_index(camera_index)
            return True
        return False
        
    def initialize(self, model_manager: ModelManager) -> VideoThread:
        """
        Initialize camera with model manager
        
        Args:
            model_manager: The model manager for detection
            
        Returns:
            VideoThread: The initialized video thread
        """
        self.video_thread = VideoThread(model_manager)
        return self.video_thread
    
    def start(self) -> bool:
        """
        Start camera capture
        
        Returns:
            bool: True if started successfully
        """
        if self.video_thread:
            success = self.video_thread.start_camera()
            if success:
                self.is_active = True
            return success
        return False
    
    def stop(self) -> None:
        """Stop camera capture"""
        if self.video_thread:
            self.video_thread.stop_camera()
            self.is_active = False
    
    def set_target_sign(self, sign_id: int) -> None:
        """Set target sign for detection"""
        if self.video_thread:
            self.video_thread.set_target_sign(sign_id)
    
    def is_camera_active(self) -> bool:
        """Check if camera is currently active"""
        return self.is_active and self.video_thread and self.video_thread.is_running()

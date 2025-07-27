"""
Video Processing Thread for Sign Language Detection
Handles camera capture and real-time processing in separate thread
"""

import cv2
import numpy as np
import time
from typing import Optional
from PyQt6.QtCore import QThread, pyqtSignal

from config import CAMERA_INDEX, FRAME_DELAY
from model_manager import ModelManager, DetectionResult


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
        
    def set_model_manager(self, model_manager: ModelManager) -> None:
        """Set the model manager for detection"""
        self.model_manager = model_manager
        
    def start_camera(self) -> bool:
        """
        Start camera capture
        
        Returns:
            bool: True if camera started successfully
        """
        try:
            self.cap = cv2.VideoCapture(CAMERA_INDEX)
            if not self.cap.isOpened():
                self.error_occurred.emit("Failed to open camera")
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

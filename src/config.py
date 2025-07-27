"""
Configuration file for Sign Language Learning App
Contains all constants and configuration settings
"""

import os

# Application Configuration
APP_NAME = "Sign Language Learning Studio"
APP_VERSION = "2.0"
ORGANIZATION_NAME = "AI Learning Labs"

# UI Configuration
WINDOW_TITLE = "🤟 Sign Language Learning Studio"
WINDOW_SIZE = (1400, 900)
WINDOW_MIN_SIZE = (1200, 800)

# Camera Configuration
CAMERA_INDEX = 0
TARGET_FPS = 30
FRAME_DELAY = 0.033  # 1/30 seconds

# Detection Configuration
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
MAX_DETECTIONS = 1000
REQUIRED_DETECTIONS = 15
INPUT_SIZE = (416, 416)

# Model Configuration
MODEL_PATH = "weights/yolov5_v0.pt"
DEVICE = "cpu"

# File Paths
YOLO_PATH = "yolov5"

# Sign Language Data
SIGNS_DATABASE = {
    0: {
        "name": "Hello",
        "instruction": "Wave your hand or raise it in greeting",
        "tip": "Keep your hand visible and move it gently"
    },
    1: {
        "name": "I Love You",
        "instruction": "Extend thumb, index, and pinky fingers up",
        "tip": "Make sure all three fingers are clearly extended"
    },
    2: {
        "name": "No",
        "instruction": "Shake your head or wave hand side to side",
        "tip": "Make a clear side-to-side motion"
    },
    3: {
        "name": "Please",
        "instruction": "Place hand on chest, make circular motion",
        "tip": "Keep the circular motion smooth and visible"
    },
    4: {
        "name": "Thanks",
        "instruction": "Touch chin with fingertips, move hand forward",
        "tip": "Start at chin and move hand away from face"
    },
    5: {
        "name": "Yes",
        "instruction": "Nod your head or give thumbs up",
        "tip": "Make the gesture clear and deliberate"
    }
}

# UI Colors and Styling
COLORS = {
    "primary": "#3498db",
    "primary_hover": "#2980b9",
    "primary_pressed": "#21618c",
    "secondary": "#2c3e50",
    "success": "#27ae60",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "light": "#f8f9fa",
    "dark": "#495057",
    "muted": "#7f8c8d",
    "background": "#f5f6fa",
    "white": "#ffffff",
    "border": "#bdc3c7"
}

# Font Configuration
FONTS = {
    "title": ("Arial", 20, "bold"),
    "subtitle": ("Arial", 10, "normal"),
    "header": ("Arial", 16, "bold"),
    "large": ("Arial", 14, "bold"),
    "medium": ("Arial", 12, "bold"),
    "normal": ("Arial", 11, "normal"),
    "small": ("Arial", 10, "normal"),
    "tiny": ("Arial", 9, "normal")
}

# UI Messages
MESSAGES = {
    "welcome": "Welcome! Ready to start learning sign language.",
    "camera_start": "📹 Camera started! Show me your signs!",
    "camera_stop": "📹 Camera stopped",
    "camera_off": "📷 Camera is off\n\nClick 'Start Camera' to begin learning!",
    "no_detection": "🔍 No signs detected\nTry adjusting your position or lighting",
    "perfect_detection": "✅ Perfect! Keep holding '{}'",
    "wrong_detection": "❌ Detected: {}\nTarget: {}",
    "completion": "🎉 Excellent! You mastered '{}'!\nGet ready for the next challenge...",
    "new_challenge": "🎯 New challenge: Learn '{}' sign!",
    "ready_detect": "Ready to detect signs...",
    "congratulations": "🎉 Congratulations! You learned '{}'!"
}

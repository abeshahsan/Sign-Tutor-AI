"""
UI Components for Sign Language Learning App
Modular UI components for better organization and reusability
"""

import cv2
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QFrame, QGroupBox, 
                             QSizePolicy, QSpacerItem, QComboBox)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage

from ui.ui_styles import StyleManager, FontManager, WidgetStyler
from config import MESSAGES


class TitleWidget(QWidget):
    """Application title and subtitle widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Main title
        self.title_label = QLabel()
        WidgetStyler.style_title_label(self.title_label, "🤟 Sign Tutor AI")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle
        self.subtitle_label = QLabel()
        WidgetStyler.style_subtitle_label(self.subtitle_label, "Your AI-Powered Sign Language Tutor")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)


class CurrentSignWidget(QWidget):
    """Widget for displaying current sign information"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "📚 Current Lesson")
        
        layout = QVBoxLayout(self)
        sign_layout = QVBoxLayout(self.group_box)
        
        # Current sign label
        self.current_sign_label = QLabel("No sign selected")
        WidgetStyler.style_current_sign_label(self.current_sign_label)
        self.current_sign_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Instruction label (hidden by default)
        self.instruction_label = QLabel("Click 'New Sign' to start learning!")
        WidgetStyler.style_instruction_label(self.instruction_label)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.hide()
        
        # Tip label
        self.tip_label = QLabel("")
        WidgetStyler.style_tip_label(self.tip_label)
        self.tip_label.hide()
        
        sign_layout.addWidget(self.current_sign_label)
        sign_layout.addWidget(self.instruction_label)
        sign_layout.addWidget(self.tip_label)
        
        layout.addWidget(self.group_box)
    
    def update_sign(self, sign_name: str):
        """Update current sign display"""
        self.current_sign_label.setText(f"Learn: {sign_name}")
    
    def show_tip(self, tip_text: str):
        """Show tip for current sign"""
        self.tip_label.setText(f"💡 Tip: {tip_text}")
        self.tip_label.show()
    
    def hide_tip(self):
        """Hide tip"""
        self.tip_label.hide()
    
    def reset(self):
        """Reset to default state"""
        self.current_sign_label.setText("No sign selected")
        self.tip_label.hide()


class ProgressWidget(QWidget):
    """Widget for displaying learning progress"""
    
    def __init__(self, required_detections: int = 15):
        super().__init__()
        self.required_detections = required_detections
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "📊 Learning Progress")
        
        layout = QVBoxLayout(self)
        progress_layout = QVBoxLayout(self.group_box)
        
        # Score display frame
        score_frame = QFrame()
        score_layout = QHBoxLayout(score_frame)
        score_layout.setContentsMargins(0, 0, 0, 0)
        
        self.score_label = QLabel("Score: 0 / 0")
        WidgetStyler.style_score_label(self.score_label)
        
        self.accuracy_label = QLabel("Accuracy: ---%")
        WidgetStyler.style_accuracy_label(self.accuracy_label)
        
        score_layout.addWidget(self.score_label)
        score_layout.addStretch()
        score_layout.addWidget(self.accuracy_label)
        
        # Progress bar
        progress_label = QLabel("Detection Progress:")
        progress_label.setFont(FontManager.get_font('small'))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.required_detections)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v/%m detections")
        
        progress_layout.addWidget(score_frame)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.group_box)
    
    def update_score(self, score: int, attempts: int):
        """Update score display"""
        self.score_label.setText(f"Score: {score} / {attempts}")
        
        if attempts > 0:
            accuracy = (score / attempts) * 100
            self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
    
    def update_progress(self, current: int):
        """Update progress bar"""
        self.progress_bar.setValue(current)
    
    def reset_progress(self):
        """Reset progress bar"""
        self.progress_bar.setValue(0)


class ModelSelectionWidget(QWidget):
    """Widget for model selection"""
    
    model_changed = pyqtSignal(str)  # Signal emitted when model is changed
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "🤖 AI Model Selection")
        
        layout = QVBoxLayout(self)
        selection_layout = QVBoxLayout(self.group_box)
        
        # Model selection dropdown
        self.model_combo = QComboBox()
        WidgetStyler.style_combo_box(self.model_combo)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        
        # Refresh button for models
        self.refresh_models_btn = QPushButton("🔄 Refresh")
        WidgetStyler.style_secondary_button(self.refresh_models_btn, "🔄 Refresh", 30)
        
        # Model info label
        self.model_info_label = QLabel("No model selected")
        WidgetStyler.style_info_label(self.model_info_label)
        
        # Layout for combo and refresh button
        model_row = QHBoxLayout()
        model_row.addWidget(self.model_combo, 1)
        model_row.addWidget(self.refresh_models_btn)
        
        selection_layout.addWidget(QLabel("Select Model:"))
        selection_layout.addLayout(model_row)
        selection_layout.addWidget(self.model_info_label)
        
        layout.addWidget(self.group_box)
    
    def update_models(self, models_dict):
        """Update available models in the dropdown"""
        print(f"Updating models widget with: {models_dict}")  # Debug
        self.model_combo.clear()
        
        for display_name, path in models_dict.items():
            self.model_combo.addItem(display_name, path)
            print(f"Added model: {display_name} -> {path}")  # Debug
            
            # Add tooltip showing the full path
            index = self.model_combo.count() - 1
            tooltip_text = f"Model: {display_name}\nPath: {path}"
            self.model_combo.setItemData(index, tooltip_text, Qt.ItemDataRole.ToolTipRole)
        
        # Force the combobox to update and show all items
        self.model_combo.setCurrentIndex(0 if models_dict else -1)
        print(f"Model combobox count after update: {self.model_combo.count()}")
        
        # Set tooltip for the combo box itself
        if models_dict:
            first_model = list(models_dict.keys())[0]
            self.model_combo.setToolTip(f"Current model: {first_model}\nClick to select a different model")
            self.model_info_label.setText(f"Found {len(models_dict)} model(s)")
        else:
            self.model_combo.setToolTip("No models available")
            self.model_info_label.setText("No models found")
    
    def on_model_changed(self, model_name):
        """Handle model selection change"""
        if model_name:
            model_path = self.model_combo.currentData()
            self.model_changed.emit(model_path)
            self.model_info_label.setText(f"Selected: {model_name}")


class CameraSelectionWidget(QWidget):
    """Widget for camera selection"""
    
    camera_changed = pyqtSignal(int)  # Signal emitted when camera is changed
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "📹 Camera Selection")
        
        layout = QVBoxLayout(self)
        selection_layout = QVBoxLayout(self.group_box)
        
        # Camera selection dropdown
        self.camera_combo = QComboBox()
        WidgetStyler.style_combo_box(self.camera_combo)
        self.camera_combo.currentIndexChanged.connect(self.on_camera_changed)
        
        # Refresh button for cameras
        self.refresh_cameras_btn = QPushButton("🔄 Refresh")
        WidgetStyler.style_secondary_button(self.refresh_cameras_btn, "🔄 Refresh", 30)
        
        # Camera info label
        self.camera_info_label = QLabel("No cameras detected")
        WidgetStyler.style_info_label(self.camera_info_label)
        
        # Layout for combo and refresh button
        camera_row = QHBoxLayout()
        camera_row.addWidget(self.camera_combo, 1)
        camera_row.addWidget(self.refresh_cameras_btn)
        
        selection_layout.addWidget(QLabel("Select Camera:"))
        selection_layout.addLayout(camera_row)
        selection_layout.addWidget(self.camera_info_label)
        
        layout.addWidget(self.group_box)
    
    def update_cameras(self, cameras_dict):
        """Update available cameras in the dropdown"""
        print(f"Updating cameras widget with: {cameras_dict}")  # Debug
        self.camera_combo.clear()
        
        for camera_index, camera_name in cameras_dict.items():
            self.camera_combo.addItem(camera_name, camera_index)
            print(f"Added camera: {camera_index} -> {camera_name}")  # Debug
            
            # Add tooltip showing the camera details
            index = self.camera_combo.count() - 1
            tooltip_text = f"Camera: {camera_name}\nIndex: {camera_index}\nClick to select this camera"
            self.camera_combo.setItemData(index, tooltip_text, Qt.ItemDataRole.ToolTipRole)
        
        # Force the combobox to update and show all items
        self.camera_combo.setCurrentIndex(0 if cameras_dict else -1)
        print(f"Combobox count after update: {self.camera_combo.count()}")
        
        # Set tooltip for the combo box itself
        if cameras_dict:
            first_camera = list(cameras_dict.values())[0]
            self.camera_combo.setToolTip(f"Current camera: {first_camera}\nClick to select a different camera")
            self.camera_info_label.setText(f"Found {len(cameras_dict)} camera(s)")
        else:
            self.camera_combo.setToolTip("No cameras available")
            self.camera_info_label.setText("No cameras detected")
    
    def on_camera_changed(self, index):
        """Handle camera selection change"""
        if index >= 0:
            camera_index = self.camera_combo.currentData()
            camera_name = self.camera_combo.currentText()
            self.camera_changed.emit(camera_index)
            self.camera_info_label.setText(f"Selected: {camera_name}")


class ControlsWidget(QWidget):
    """Widget for control buttons"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "🎮 Controls")
        
        layout = QVBoxLayout(self)
        controls_layout = QVBoxLayout(self.group_box)
        
        # New sign button
        self.new_sign_btn = QPushButton()
        WidgetStyler.style_primary_button(self.new_sign_btn, "🎯 New Sign Challenge")
        
        # Camera button
        self.camera_btn = QPushButton()
        WidgetStyler.style_primary_button(self.camera_btn, "📹 Start Camera")
        
        # Hint button
        self.hint_btn = QPushButton()
        WidgetStyler.style_secondary_button(self.hint_btn, "💡 Show Hint")
        self.hint_btn.setEnabled(False)
        
        controls_layout.addWidget(self.new_sign_btn)
        controls_layout.addWidget(self.camera_btn)
        controls_layout.addWidget(self.hint_btn)
        
        layout.addWidget(self.group_box)
    
    def set_camera_state(self, is_active: bool):
        """Update camera button state"""
        if is_active:
            self.camera_btn.setText("📹 Stop Camera")
        else:
            self.camera_btn.setText("📹 Start Camera")
    
    def enable_hint(self, enabled: bool):
        """Enable/disable hint button"""
        self.hint_btn.setEnabled(enabled)
    
    def toggle_hint_text(self, showing: bool):
        """Toggle hint button text"""
        if showing:
            self.hint_btn.setText("🙈 Hide Hint")
        else:
            self.hint_btn.setText("💡 Show Hint")


class VideoDisplayWidget(QWidget):
    """Widget for video display"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Video section header
        self.video_header = QLabel()
        WidgetStyler.style_header_label(self.video_header, "📹 Live Camera Feed")
        self.video_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Video display frame
        self.video_frame = QFrame()
        self.video_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.video_frame.setLineWidth(2)
        self.video_frame.setStyleSheet(StyleManager.get_video_frame_style())
        self.video_frame.setMinimumHeight(250)  # Reduced minimum height
        # Remove maximum height to allow flexible sizing
        self.video_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        video_layout = QVBoxLayout(self.video_frame)
        video_layout.setContentsMargins(10, 10, 10, 10)
        
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Don't scale contents automatically - we handle scaling manually to preserve aspect ratio
        self.video_label.setScaledContents(False)
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_label.setStyleSheet(StyleManager.get_video_label_style())
        self.video_label.setText(MESSAGES['camera_off'])
        # Set minimum size for the video area
        self.video_label.setMinimumSize(320, 240)
        
        video_layout.addWidget(self.video_label)
        
        layout.addWidget(self.video_header)
        layout.addWidget(self.video_frame, 1)
    
    def update_frame(self, frame: np.ndarray):
        """Update video display with new frame"""
        try:
            # Convert frame to Qt format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Get the available size in the container
            container_size = self.video_frame.size()
            available_width = container_size.width() - 20  # Account for margins
            available_height = container_size.height() - 20  # Account for margins
            
            # Scale image to fit available space while maintaining aspect ratio
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                available_width, 
                available_height,
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Center the scaled image in the label
            self.video_label.setPixmap(scaled_pixmap)
            self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        except Exception as e:
            print(f"Video display error: {e}")
    
    def show_camera_off_message(self):
        """Show camera off message"""
        self.video_label.clear()
        self.video_label.setText(MESSAGES['camera_off'])


class DetectionStatusWidget(QWidget):
    """Widget for displaying AI detection status"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main group box
        self.group_box = QGroupBox()
        WidgetStyler.style_group_box(self.group_box, "🤖 AI Detection Status")
        
        layout = QVBoxLayout(self)
        status_layout = QVBoxLayout(self.group_box)
        
        self.detection_label = QLabel(MESSAGES['ready_detect'])
        WidgetStyler.style_detection_label(self.detection_label)
        self.detection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_layout.addWidget(self.detection_label)
        layout.addWidget(self.group_box)
    
    def update_status(self, message: str):
        """Update detection status message"""
        self.detection_label.setText(message)
    
    def show_no_detection(self):
        """Show no detection message"""
        self.detection_label.setText(MESSAGES['no_detection'])
    
    def show_perfect_detection(self, sign_name: str, confidence: float):
        """Show perfect detection message"""
        message = MESSAGES['perfect_detection'].format(sign_name)
        message += f"\nConfidence: {confidence:.0%}"
        self.detection_label.setText(message)
    
    def show_wrong_detection(self, detected: str, target: str):
        """Show wrong detection message"""
        message = MESSAGES['wrong_detection'].format(detected, target)
        self.detection_label.setText(message)
    
    def show_completion(self, sign_name: str):
        """Show completion message"""
        message = MESSAGES['completion'].format(sign_name)
        self.detection_label.setText(message)

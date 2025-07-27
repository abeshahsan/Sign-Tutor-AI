"""
Main Application Class
Clean, modular main application using separated components
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QStatusBar)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

from config import (APP_NAME, APP_VERSION, ORGANIZATION_NAME, WINDOW_TITLE, 
                   WINDOW_SIZE, WINDOW_MIN_SIZE, MESSAGES)
from model_manager import ModelManager
from video_processor import CameraManager
from game_logic import GameLogic
from ui_styles import StyleManager
from ui_components import (TitleWidget, CurrentSignWidget, ProgressWidget, 
                          ControlsWidget, VideoDisplayWidget, DetectionStatusWidget)


class SignLanguageApp(QMainWindow):
    """
    Main application class with clean separation of concerns
    Uses modular components and follows SOLID principles
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.model_manager = ModelManager()
        self.camera_manager = CameraManager()
        self.game_logic = GameLogic()
        
        # UI state
        self.camera_active = False
        self.hint_visible = False
        
        # Setup application
        self.setup_window()
        self.setup_components()
        self.setup_connections()
        self.setup_styling()
        
        # Initialize systems
        self.initialize_model()
        self.initialize_camera()
        self.setup_game_callbacks()
    
    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, *WINDOW_SIZE)
        self.setMinimumSize(*WINDOW_MIN_SIZE)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(MESSAGES['welcome'])
    
    def setup_components(self):
        """Setup UI components"""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Left panel components
        left_panel = self.create_left_panel()
        left_panel.setMaximumWidth(400)
        left_panel.setMinimumWidth(350)
        
        # Right panel components
        right_panel = self.create_right_panel()
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self):
        """Create left control panel with components"""
        from PyQt6.QtWidgets import QFrame, QSpacerItem, QSizePolicy
        
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Initialize components
        self.title_widget = TitleWidget()
        self.current_sign_widget = CurrentSignWidget()
        self.progress_widget = ProgressWidget()
        self.controls_widget = ControlsWidget()
        
        # Add components to layout
        layout.addWidget(self.title_widget)
        layout.addWidget(self.current_sign_widget)
        layout.addWidget(self.progress_widget)
        layout.addWidget(self.controls_widget)
        
        # Add stretch to push everything to top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        
        return panel
    
    def create_right_panel(self):
        """Create right video panel with components"""
        from PyQt6.QtWidgets import QFrame
        
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Initialize components
        self.video_widget = VideoDisplayWidget()
        self.detection_widget = DetectionStatusWidget()
        
        # Add components to layout
        layout.addWidget(self.video_widget, 1)  # Give most space to video
        layout.addWidget(self.detection_widget)
        
        return panel
    
    def setup_connections(self):
        """Setup signal-slot connections"""
        # Control button connections
        self.controls_widget.new_sign_btn.clicked.connect(self.select_new_sign)
        self.controls_widget.camera_btn.clicked.connect(self.toggle_camera)
        self.controls_widget.hint_btn.clicked.connect(self.toggle_hint)
    
    def setup_styling(self):
        """Apply styling to the application"""
        self.setStyleSheet(StyleManager.get_main_stylesheet())
    
    def initialize_model(self):
        """Initialize AI model"""
        if self.model_manager.load_model():
            self.status_bar.showMessage("AI Model loaded successfully!")
        else:
            self.status_bar.showMessage("Warning: AI Model not available")
    
    def initialize_camera(self):
        """Initialize camera system"""
        self.video_thread = self.camera_manager.initialize(self.model_manager)
        
        # Connect video thread signals
        self.video_thread.frame_ready.connect(self.video_widget.update_frame)
        self.video_thread.detection_result.connect(self.process_detections)
        self.video_thread.error_occurred.connect(self.handle_camera_error)
    
    def setup_game_callbacks(self):
        """Setup game logic callbacks"""
        self.game_logic.register_callback('new_sign_selected', self.on_new_sign_selected)
        self.game_logic.register_callback('progress_updated', self.on_progress_updated)
        self.game_logic.register_callback('sign_completed', self.on_sign_completed)
    
    def select_new_sign(self):
        """Select a new random sign to learn"""
        sign_id, sign_name = self.game_logic.select_new_sign()
        
        # Update camera target
        self.camera_manager.set_target_sign(sign_id)
        
        # Enable hint button
        self.controls_widget.enable_hint(True)
        
        # Update status
        self.status_bar.showMessage(MESSAGES['new_challenge'].format(sign_name))
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera capture"""
        if self.camera_manager.start():
            self.camera_active = True
            self.controls_widget.set_camera_state(True)
            self.status_bar.showMessage(MESSAGES['camera_start'])
        else:
            self.status_bar.showMessage("❌ Failed to start camera")
    
    def stop_camera(self):
        """Stop camera capture"""
        self.camera_manager.stop()
        self.camera_active = False
        self.controls_widget.set_camera_state(False)
        self.video_widget.show_camera_off_message()
        self.status_bar.showMessage(MESSAGES['camera_stop'])
    
    def toggle_hint(self):
        """Toggle hint display"""
        if self.hint_visible:
            self.current_sign_widget.hide_tip()
            self.hint_visible = False
            self.controls_widget.toggle_hint_text(False)
        else:
            sign_info = self.game_logic.get_current_sign_info()
            if sign_info:
                self.current_sign_widget.show_tip(sign_info.get('tip', ''))
                self.hint_visible = True
                self.controls_widget.toggle_hint_text(True)
    
    def process_detections(self, detections):
        """Process detection results from camera"""
        result = self.game_logic.process_detections(detections)
        
        # Update UI based on result
        if result['status'] == 'no_detection':
            self.detection_widget.show_no_detection()
        elif result['status'] == 'correct_detection':
            self.detection_widget.show_perfect_detection(
                self.game_logic.progress.current_sign_name,
                result['confidence']
            )
        elif result['status'] == 'wrong_detection':
            detected_text = ", ".join(result['detected'])
            self.detection_widget.show_wrong_detection(
                detected_text,
                self.game_logic.progress.current_sign_name
            )
        elif result['status'] == 'completed':
            self.detection_widget.show_completion(result['sign_name'])
            # Auto-select new sign after delay
            QTimer.singleShot(3000, self.select_new_sign)
    
    def handle_camera_error(self, error_message):
        """Handle camera errors"""
        self.status_bar.showMessage(f"❌ Camera error: {error_message}")
        if self.camera_active:
            self.stop_camera()
    
    # Game logic callback handlers
    def on_new_sign_selected(self, sign_id, sign_name):
        """Handle new sign selection"""
        self.current_sign_widget.update_sign(sign_name)
        self.current_sign_widget.hide_tip()
        self.hint_visible = False
        self.controls_widget.toggle_hint_text(False)
        self.progress_widget.reset_progress()
    
    def on_progress_updated(self, progress):
        """Handle progress updates"""
        self.progress_widget.update_progress(progress.detection_count)
        self.progress_widget.update_score(progress.score, progress.attempts)
    
    def on_sign_completed(self, sign_name, progress):
        """Handle sign completion"""
        self.status_bar.showMessage(MESSAGES['congratulations'].format(sign_name))
    
    def closeEvent(self, event):
        """Handle application closing"""
        if self.camera_active:
            self.stop_camera()
        event.accept()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORGANIZATION_NAME)
    
    # Check for model file
    if not os.path.exists('best.pt'):
        print("⚠️ Warning: Model file 'best.pt' not found!")
    
    # Create and show main window
    window = SignLanguageApp()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

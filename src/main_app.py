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
from core.model_manager import ModelManager
from core.video_processor import CameraManager
from core.game_logic import GameLogic
from ui.ui_styles import StyleManager
from ui.ui_components import (TitleWidget, CurrentSignWidget, ProgressWidget, 
                          ControlsWidget, VideoDisplayWidget, DetectionStatusWidget,
                          ModelSelectionWidget, CameraSelectionWidget)


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
        self.video_thread = None
        
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
        left_panel.setMaximumWidth(450)  # Increased from 400 to 450
        left_panel.setMinimumWidth(400)  # Increased from 350 to 400
        
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
        from PyQt6.QtWidgets import QFrame, QHBoxLayout
        
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Create main content area with horizontal layout
        main_content = QHBoxLayout()
        
        # Left side: Video and detection (center area)
        video_section = QVBoxLayout()
        self.video_widget = VideoDisplayWidget()
        self.detection_widget = DetectionStatusWidget()
        
        video_section.addWidget(self.video_widget, 1)  # Video gets most space
        video_section.addWidget(self.detection_widget)
        
        # Right side: Selection controls
        controls_section = QVBoxLayout()
        self.model_selection_widget = ModelSelectionWidget()
        self.camera_selection_widget = CameraSelectionWidget()
        
        # Set maximum width for the controls to accommodate wider dropdowns
        self.model_selection_widget.setMaximumWidth(350)
        self.camera_selection_widget.setMaximumWidth(350)
        
        controls_section.addWidget(self.model_selection_widget)
        controls_section.addWidget(self.camera_selection_widget)
        controls_section.addStretch()  # Push controls to top
        
        # Add both sections to main content
        main_content.addLayout(video_section, 3)  # Video section gets more space
        main_content.addLayout(controls_section, 1)  # Controls get less space
        
        # Add main content to panel layout
        layout.addLayout(main_content, 1)
        
        return panel
    
    def setup_connections(self):
        """Setup signal-slot connections"""
        # Control button connections
        self.controls_widget.new_sign_btn.clicked.connect(self.select_new_sign)
        self.controls_widget.camera_btn.clicked.connect(self.toggle_camera)
        self.controls_widget.hint_btn.clicked.connect(self.toggle_hint)
        
        # Model and camera selection connections
        self.model_selection_widget.model_changed.connect(self.on_model_changed)
        self.camera_selection_widget.camera_changed.connect(self.on_camera_changed)
        
        # Refresh button connections
        self.model_selection_widget.refresh_models_btn.clicked.connect(self.refresh_models)
        self.camera_selection_widget.refresh_cameras_btn.clicked.connect(self.refresh_cameras)
    
    def setup_styling(self):
        """Apply styling to the application"""
        self.setStyleSheet(StyleManager.get_main_stylesheet())
    
    def initialize_model(self):
        """Initialize AI model"""
        # Populate model selection widget
        available_models = self.model_manager.get_available_models()
        self.model_selection_widget.update_models(available_models)
        
        # Load default model if available - prioritize yolov5_v0.pt
        if available_models:
            # Try to find the original working model first
            preferred_model_path = None
            for display_name, path in available_models.items():
                if "yolov5_v0" in path.lower() or "Yolov5 V0" in display_name:
                    preferred_model_path = path
                    break
            
            # If preferred model not found, use the first available
            if not preferred_model_path:
                preferred_model_path = list(available_models.values())[0]
            
            # Set the dropdown to show the selected model
            for i in range(self.model_selection_widget.model_combo.count()):
                if self.model_selection_widget.model_combo.itemData(i) == preferred_model_path:
                    self.model_selection_widget.model_combo.setCurrentIndex(i)
                    break
            
            if self.model_manager.load_model(preferred_model_path):
                model_name = os.path.basename(preferred_model_path)
                self.status_bar.showMessage(f"AI Model loaded: {model_name}")
            else:
                self.status_bar.showMessage("Warning: AI Model failed to load")
        else:
            self.status_bar.showMessage("Warning: No AI Models found")
    
    def initialize_camera(self):
        """Initialize camera system"""
        # Populate camera selection widget
        available_cameras = self.camera_manager.get_available_cameras()
        self.camera_selection_widget.update_cameras(available_cameras)
        
        # Initialize video thread
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
    
    def on_model_changed(self, model_path):
        """Handle model selection change"""
        # Stop camera if active
        was_active = self.camera_active
        if was_active:
            self.stop_camera()
        
        # Load new model
        if self.model_manager.load_model(model_path):
            model_info = self.model_manager.get_current_model_info()
            self.status_bar.showMessage(f"Loaded model: {model_info['name']} ({model_info['classes']} classes)")
            
            # Update video thread with new model manager (only if it exists)
            if hasattr(self, 'video_thread') and self.video_thread:
                self.video_thread.set_model_manager(self.model_manager)
            
            # Restart camera if it was active
            if was_active:
                self.start_camera()
        else:
            self.status_bar.showMessage("Failed to load selected model")
    
    def on_camera_changed(self, camera_index):
        """Handle camera selection change"""
        # Stop current camera if active
        was_active = self.camera_active
        if was_active:
            self.stop_camera()
        
        # Set new camera index
        if self.camera_manager.set_camera_index(camera_index):
            self.status_bar.showMessage(f"Selected camera index: {camera_index}")
            
            # Restart camera if it was active
            if was_active:
                self.start_camera()
        else:
            self.status_bar.showMessage("Failed to select camera")
    
    def refresh_models(self):
        """Refresh available models"""
        self.status_bar.showMessage("Refreshing models...")
        available_models = self.model_manager.discover_models()
        self.model_selection_widget.update_models(available_models)
        self.status_bar.showMessage(f"Found {len(available_models)} model(s)")
    
    def refresh_cameras(self):
        """Refresh available cameras"""
        self.status_bar.showMessage("Refreshing cameras...")
        available_cameras = self.camera_manager.discover_cameras()
        self.camera_selection_widget.update_cameras(available_cameras)
        self.status_bar.showMessage(f"Found {len(available_cameras)} camera(s)")
    
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
    
    # Create and show main window
    window = SignLanguageApp()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

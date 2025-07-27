"""
UI Styles and Theme Management
Centralizes all styling and UI constants
"""

from config import COLORS, FONTS


class StyleManager:
    """Manages application styling and themes"""
    
    @staticmethod
    def get_main_stylesheet() -> str:
        """Get the main application stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['border']};
                border-radius: 10px;
                margin: 5px;
                padding-top: 15px;
                background-color: {COLORS['white']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: {COLORS['secondary']};
                background-color: {COLORS['white']};
            }}
            
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {COLORS['primary_pressed']};
            }}
            
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['muted']};
            }}
            
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
            }}
            
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
            }}
            
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 6px;
            }}
        """
    
    @staticmethod
    def get_video_frame_style() -> str:
        """Get video frame styling"""
        return """
            QFrame {
                background-color: #2c3e50;
                border: 3px solid #34495e;
                border-radius: 15px;
            }
        """
    
    @staticmethod
    def get_video_label_style() -> str:
        """Get video label styling"""
        return """
            QLabel {
                background-color: #000000;
                color: #ffffff;
                font-size: 16px;
                border-radius: 10px;
                border: 2px solid #555555;
            }
        """
    
    @staticmethod
    def get_detection_label_style() -> str:
        """Get detection status label styling"""
        return f"""
            QLabel {{
                padding: 15px;
                background-color: {COLORS['light']};
                border-radius: 8px;
                border: 2px solid #dee2e6;
                color: {COLORS['dark']};
            }}
        """
    
    @staticmethod
    def get_sign_label_style() -> str:
        """Get current sign label styling"""
        return f"""
            color: {COLORS['danger']};
            padding: 10px;
            background-color: #fdf2f2;
            border-radius: 8px;
        """
    
    @staticmethod
    def get_instruction_label_style() -> str:
        """Get instruction label styling"""
        return f"""
            color: {COLORS['secondary']};
            padding: 15px;
            background-color: {COLORS['light']};
            border-radius: 8px;
            margin: 5px;
        """
    
    @staticmethod
    def get_tip_label_style() -> str:
        """Get tip label styling"""
        return f"""
            color: {COLORS['warning']};
            background-color: #fefcf0;
            padding: 8px;
            border-radius: 5px;
            border-left: 3px solid {COLORS['warning']};
        """
    
    @staticmethod
    def get_score_label_style() -> str:
        """Get score label styling"""
        return f"""
            color: {COLORS['success']};
            padding: 5px;
        """
    
    @staticmethod
    def get_accuracy_label_style() -> str:
        """Get accuracy label styling"""
        return f"""
            color: {COLORS['muted']};
        """


class FontManager:
    """Manages font settings"""
    
    @staticmethod
    def get_font(font_type: str):
        """Get font by type"""
        from PyQt6.QtGui import QFont
        
        font_config = FONTS.get(font_type, FONTS['normal'])
        family, size, weight = font_config
        
        font = QFont(family, size)
        if weight == 'bold':
            font.setWeight(QFont.Weight.Bold)
        
        return font


class WidgetStyler:
    """Utility class for applying styles to widgets"""
    
    @staticmethod
    def style_title_label(label, text: str):
        """Style a title label"""
        label.setText(text)
        label.setFont(FontManager.get_font('title'))
        label.setStyleSheet(f"color: {COLORS['secondary']}; padding: 10px;")
    
    @staticmethod
    def style_subtitle_label(label, text: str):
        """Style a subtitle label"""
        label.setText(text)
        label.setFont(FontManager.get_font('subtitle'))
        label.setStyleSheet(f"color: {COLORS['muted']}; margin-bottom: 10px;")
    
    @staticmethod
    def style_header_label(label, text: str):
        """Style a header label"""
        label.setText(text)
        label.setFont(FontManager.get_font('header'))
        label.setStyleSheet(f"color: {COLORS['secondary']}; padding: 10px;")
    
    @staticmethod
    def style_current_sign_label(label):
        """Style current sign label"""
        label.setFont(FontManager.get_font('large'))
        label.setStyleSheet(StyleManager.get_sign_label_style())
    
    @staticmethod
    def style_instruction_label(label):
        """Style instruction label"""
        label.setFont(FontManager.get_font('normal'))
        label.setStyleSheet(StyleManager.get_instruction_label_style())
        label.setWordWrap(True)
    
    @staticmethod
    def style_tip_label(label):
        """Style tip label"""
        label.setFont(FontManager.get_font('tiny'))
        label.setStyleSheet(StyleManager.get_tip_label_style())
        label.setWordWrap(True)
    
    @staticmethod
    def style_score_label(label):
        """Style score label"""
        label.setFont(FontManager.get_font('large'))
        label.setStyleSheet(StyleManager.get_score_label_style())
    
    @staticmethod
    def style_accuracy_label(label):
        """Style accuracy label"""
        label.setFont(FontManager.get_font('small'))
        label.setStyleSheet(StyleManager.get_accuracy_label_style())
    
    @staticmethod
    def style_detection_label(label):
        """Style detection status label"""
        label.setFont(FontManager.get_font('medium'))
        label.setStyleSheet(StyleManager.get_detection_label_style())
    
    @staticmethod
    def style_primary_button(button, text: str, height: int = 50):
        """Style a primary button"""
        button.setText(text)
        button.setFont(FontManager.get_font('normal'))
        button.setMinimumHeight(height)
    
    @staticmethod
    def style_secondary_button(button, text: str, height: int = 35):
        """Style a secondary button"""
        button.setText(text)
        button.setFont(FontManager.get_font('small'))
        button.setMinimumHeight(height)
    
    @staticmethod
    def style_group_box(group_box, title: str):
        """Style a group box"""
        group_box.setTitle(title)
        group_box.setFont(FontManager.get_font('medium'))

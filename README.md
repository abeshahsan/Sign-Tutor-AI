# Sign Language Learning Studio

A professional desktop application for learning sign language using AI-powered recognition with YOLOv5.

## 🏗️ Architecture

The application follows clean coding principles with proper separation of concerns:

### Core Components

- **`config.py`** - Configuration and constants
- **`model_manager.py`** - AI model loading and inference
- **`video_processor.py`** - Camera handling and video processing
- **`game_logic.py`** - Game state management and scoring
- **`ui_styles.py`** - Styling and theme management
- **`ui_components.py`** - Modular UI components
- **`main_app.py`** - Main application orchestration

### Design Patterns Used

- **Single Responsibility Principle**: Each module has one clear purpose
- **Dependency Injection**: Components receive dependencies through constructors
- **Observer Pattern**: Callbacks for game events and UI updates
- **Strategy Pattern**: Modular UI components and styling
- **Factory Pattern**: Component creation and initialization

## 🚀 Features

- **Real-time Sign Detection**: AI-powered recognition using YOLOv5
- **Interactive Learning**: Gamified experience with scoring and progress tracking
- **Professional UI**: Modern PyQt6 interface with clean design
- **Modular Architecture**: Easy to extend and maintain
- **Error Handling**: Robust error handling and user feedback

## 📁 File Structure

```
├── app.py                   # Main application entry point
├── src/                     # Source code directory
│   ├── config.py           # Configuration and constants
│   ├── main_app.py         # Main application orchestration
│   ├── core/               # Core functionality
│   │   ├── model_manager.py    # AI model management
│   │   ├── video_processor.py  # Camera and video processing
│   │   └── game_logic.py       # Game logic and scoring
│   └── ui/                 # User interface components
│       ├── ui_styles.py        # Styling and themes
│       └── ui_components.py    # Modular UI widgets
├── weights/                 # Model weights directory
│   └── yolov5_v0.pt        # YOLOv5 trained model
└── yolov5/                 # YOLOv5 framework
```

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install PyQt6 torch torchvision opencv-python ultralytics Pillow numpy
   ```

2. **Ensure Model File**: Make sure `yolov5_v0.pt` is in the `weights/` directory

3. **Run Application**:
   ```bash
   python app.py
   ```

## 🎯 Usage

1. **Start the Application**: Run `python app.py`
2. **Select a Sign**: Click "New Sign Challenge" to get a random sign
3. **Start Camera**: Click "Start Camera" to begin detection
4. **Practice**: Show the sign to the camera until you reach 15 detections
5. **Get Hints**: Click "Show Hint" for tips on how to perform the sign

## 🧩 Component Details

### ModelManager
- Handles YOLOv5 model loading and inference
- Preprocesses camera frames for detection
- Returns structured detection results

### VideoProcessor
- Manages camera capture in separate thread
- Handles real-time video processing
- Emits signals for UI updates

### GameLogic
- Tracks learning progress and scoring
- Manages sign database and selection
- Provides callback system for events

### UI Components
- **TitleWidget**: Application branding
- **CurrentSignWidget**: Shows current learning target
- **ProgressWidget**: Displays score and progress
- **ControlsWidget**: Action buttons
- **VideoDisplayWidget**: Camera feed display
- **DetectionStatusWidget**: AI feedback

## 🎨 Styling System

The application uses a centralized styling system:
- **StyleManager**: Provides CSS-like stylesheets
- **FontManager**: Manages font configurations
- **WidgetStyler**: Utility functions for consistent styling

## 🔧 Extension Points

The modular architecture makes it easy to:
- Add new sign types (update `config.py`)
- Implement new UI themes (extend `ui_styles.py`)
- Add new detection models (extend `model_manager.py`)
- Create new UI components (add to `ui_components.py`)

## 🐛 Error Handling

- Model loading failures are gracefully handled
- Camera errors are reported to the user
- UI remains responsive during processing
- Comprehensive logging for debugging

## 📈 Performance

- Video processing runs in separate thread
- UI remains responsive during AI inference
- Memory-efficient frame processing
- Optimized for real-time performance

## 🏆 Code Quality

- **Type hints** for better code documentation
- **Docstrings** for all classes and methods
- **Clean separation** of concerns
- **SOLID principles** implementation
- **Modular design** for easy testing and maintenance

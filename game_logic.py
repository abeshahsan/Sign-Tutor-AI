"""
Game Logic Manager for Sign Language Learning
Handles scoring, progress tracking, and game state management
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from config import SIGNS_DATABASE, REQUIRED_DETECTIONS


@dataclass
class GameProgress:
    """Data class to track game progress"""
    score: int = 0
    attempts: int = 0
    detection_count: int = 0
    current_sign_id: Optional[int] = None
    current_sign_name: str = ""
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.attempts == 0:
            return 0.0
        return (self.score / self.attempts) * 100
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage for current sign"""
        return (self.detection_count / REQUIRED_DETECTIONS) * 100


class SignDatabase:
    """Manages sign language data and operations"""
    
    def __init__(self):
        self.signs = SIGNS_DATABASE.copy()
    
    def get_sign_info(self, sign_id: int) -> Dict:
        """Get sign information by ID"""
        return self.signs.get(sign_id, {})
    
    def get_sign_name(self, sign_id: int) -> str:
        """Get sign name by ID"""
        return self.signs.get(sign_id, {}).get("name", "Unknown")
    
    def get_sign_instruction(self, sign_id: int) -> str:
        """Get sign instruction by ID"""
        return self.signs.get(sign_id, {}).get("instruction", "")
    
    def get_sign_tip(self, sign_id: int) -> str:
        """Get sign tip by ID"""
        return self.signs.get(sign_id, {}).get("tip", "")
    
    def get_all_sign_ids(self) -> List[int]:
        """Get list of all available sign IDs"""
        return list(self.signs.keys())
    
    def get_random_sign_id(self) -> int:
        """Get a random sign ID"""
        return random.choice(self.get_all_sign_ids())
    
    def is_valid_sign_id(self, sign_id: int) -> bool:
        """Check if sign ID is valid"""
        return sign_id in self.signs


class GameLogic:
    """
    Manages game logic, scoring, and progress tracking
    """
    
    def __init__(self):
        self.progress = GameProgress()
        self.sign_database = SignDatabase()
        self.required_detections = REQUIRED_DETECTIONS
        self._callbacks = {
            'sign_completed': [],
            'progress_updated': [],
            'new_sign_selected': []
        }
    
    def register_callback(self, event: str, callback) -> None:
        """Register callback for game events"""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _trigger_callback(self, event: str, *args, **kwargs) -> None:
        """Trigger registered callbacks"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Callback error for {event}: {e}")
    
    def select_new_sign(self) -> Tuple[int, str]:
        """
        Select a new random sign for learning
        
        Returns:
            Tuple[int, str]: Sign ID and name
        """
        self.progress.current_sign_id = self.sign_database.get_random_sign_id()
        self.progress.current_sign_name = self.sign_database.get_sign_name(
            self.progress.current_sign_id
        )
        self.progress.detection_count = 0
        
        self._trigger_callback('new_sign_selected', 
                              self.progress.current_sign_id, 
                              self.progress.current_sign_name)
        
        return self.progress.current_sign_id, self.progress.current_sign_name
    
    def process_detections(self, detections: List[Dict]) -> Dict:
        """
        Process detection results and update game state
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Dict: Processing result with status and message
        """
        if not detections:
            return self._handle_no_detection()
        
        # Check if current target sign is detected
        target_detected = False
        best_confidence = 0.0
        detected_signs = []
        
        for detection in detections:
            sign_name = detection.get('name', f"Class_{detection['class']}")
            confidence = detection['confidence']
            detected_signs.append(f"{sign_name} ({confidence:.0%})")
            
            # Check if this is our target sign
            if (detection['class'] == self.progress.current_sign_id and 
                confidence > 0.5):
                target_detected = True
                best_confidence = max(best_confidence, confidence)
        
        if target_detected:
            return self._handle_correct_detection(best_confidence)
        else:
            return self._handle_wrong_detection(detected_signs)
    
    def _handle_no_detection(self) -> Dict:
        """Handle case when no signs are detected"""
        # Decrease detection count but don't go below 0
        self.progress.detection_count = max(0, self.progress.detection_count - 1)
        self._trigger_callback('progress_updated', self.progress)
        
        return {
            'status': 'no_detection',
            'message': "🔍 No signs detected\nTry adjusting your position or lighting",
            'progress': self.progress.detection_count
        }
    
    def _handle_correct_detection(self, confidence: float) -> Dict:
        """Handle correct sign detection"""
        self.progress.detection_count += 1
        self._trigger_callback('progress_updated', self.progress)
        
        # Check for completion
        if self.progress.detection_count >= self.required_detections:
            return self._complete_sign()
        
        return {
            'status': 'correct_detection',
            'message': f"✅ Perfect! Keep holding '{self.progress.current_sign_name}'\nConfidence: {confidence:.0%}",
            'progress': self.progress.detection_count,
            'confidence': confidence
        }
    
    def _handle_wrong_detection(self, detected_signs: List[str]) -> Dict:
        """Handle wrong sign detection"""
        # Decrease detection count more aggressively for wrong signs
        self.progress.detection_count = max(0, self.progress.detection_count - 2)
        self._trigger_callback('progress_updated', self.progress)
        
        detected_text = ", ".join(detected_signs)
        return {
            'status': 'wrong_detection',
            'message': f"❌ Detected: {detected_text}\nTarget: {self.progress.current_sign_name}",
            'progress': self.progress.detection_count,
            'detected': detected_signs
        }
    
    def _complete_sign(self) -> Dict:
        """Handle sign completion"""
        self.progress.score += 1
        self.progress.attempts += 1
        self.progress.detection_count = 0
        
        self._trigger_callback('sign_completed', 
                              self.progress.current_sign_name, 
                              self.progress)
        
        return {
            'status': 'completed',
            'message': f"🎉 Excellent! You mastered '{self.progress.current_sign_name}'!\nGet ready for the next challenge...",
            'sign_name': self.progress.current_sign_name,
            'score': self.progress.score,
            'attempts': self.progress.attempts
        }
    
    def get_current_sign_info(self) -> Dict:
        """Get information about current sign"""
        if self.progress.current_sign_id is None:
            return {}
        
        return self.sign_database.get_sign_info(self.progress.current_sign_id)
    
    def get_game_stats(self) -> Dict:
        """Get current game statistics"""
        return {
            'score': self.progress.score,
            'attempts': self.progress.attempts,
            'accuracy': self.progress.accuracy,
            'current_progress': self.progress.detection_count,
            'required_detections': self.required_detections,
            'progress_percentage': self.progress.progress_percentage
        }
    
    def reset_game(self) -> None:
        """Reset game progress"""
        self.progress = GameProgress()
    
    def set_required_detections(self, count: int) -> None:
        """Set number of required detections to complete a sign"""
        self.required_detections = max(1, count)


class LearningSession:
    """
    Manages a complete learning session
    Tracks long-term progress and provides session statistics
    """
    
    def __init__(self):
        self.session_start_time = None
        self.signs_learned = []
        self.total_attempts = 0
        self.successful_signs = 0
        
    def start_session(self) -> None:
        """Start a new learning session"""
        import time
        self.session_start_time = time.time()
        self.signs_learned = []
        self.total_attempts = 0
        self.successful_signs = 0
    
    def record_sign_completion(self, sign_name: str, attempts: int) -> None:
        """Record completion of a sign"""
        self.signs_learned.append({
            'name': sign_name,
            'attempts': attempts,
            'timestamp': time.time()
        })
        self.total_attempts += attempts
        self.successful_signs += 1
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        if not self.session_start_time:
            return {}
        
        import time
        session_duration = time.time() - self.session_start_time
        
        return {
            'duration_minutes': session_duration / 60,
            'signs_learned': len(self.signs_learned),
            'total_attempts': self.total_attempts,
            'average_attempts_per_sign': (
                self.total_attempts / len(self.signs_learned) 
                if self.signs_learned else 0
            ),
            'signs_per_minute': (
                len(self.signs_learned) / (session_duration / 60) 
                if session_duration > 0 else 0
            )
        }

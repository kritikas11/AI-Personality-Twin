"""
Emotion Detector Module
Detects emotions from facial images using DeepFace
"""
import cv2
import numpy as np
from deepface import DeepFace
from typing import Dict, Optional, Tuple, Any, Union, List
import tempfile
import os

class EmotionDetector:
    """Detect emotions from facial images"""
    
    EMOTION_EMOJIS = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'surprise': '😲',
        'fear': '😨',
        'disgust': '🤢',
        'neutral': '😐'
    }
    
    def __init__(self):
        """Initialize emotion detector"""
        self.models = ['opencv', 'ssd']  # Fallback models
    
    def preprocess_image(self, image_data: np.ndarray) -> np.ndarray:
        """Preprocess image for better detection"""
        # Convert to RGB if needed
        if len(image_data.shape) == 2:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_GRAY2RGB)
        elif image_data.shape[2] == 4:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGRA2RGB)
        
        return image_data
    
    def detect_emotion(
        self,
        image_path: Optional[str] = None,
        image_array: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Detect emotion from image
        
        Args:
            image_path: Path to image file
            image_array: Numpy array of image
            
        Returns:
            Dictionary with emotion analysis results
        """
        try:
            # Use provided image or path
            if image_array is not None:
                # Save array to temp file for DeepFace
                with tempfile.NamedTemporaryFile(
                    suffix='.jpg',
                    delete=False
                ) as tmp:
                    cv2.imwrite(tmp.name, image_array)
                    image_path = tmp.name
            
            if not image_path or not os.path.exists(image_path):
                return {
                    'error': 'Invalid image path',
                    'success': False,
                    'dominant_emotion': 'neutral',
                    'emoji': '😐'
                }
            
            # Analyze emotion using DeepFace
            # Result can be Dict or List[Dict]
            result: Union[Dict[str, Any], List[Dict[str, Any]]] = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            # Handle both single face and multiple faces
            # DeepFace returns list when multiple faces or dict for single face
            analysis: Dict[str, Any]
            
            if isinstance(result, list):
                if len(result) > 0:
                    analysis = result[0]
                else:
                    # No faces detected
                    if image_array is not None and image_path:
                        try:
                            os.unlink(image_path)
                        except:
                            pass
                    return {
                        'success': False,
                        'error': 'No face detected',
                        'dominant_emotion': 'neutral',
                        'emoji': '😐',
                        'message': 'Could not detect face. Using neutral emotion.'
                    }
            else:
                analysis = result
            
            # Now analysis is guaranteed to be a Dict
            # Safely get emotion data with defaults
            emotions: Dict[str, float] = analysis.get('emotion', {})
            dominant_emotion: str = analysis.get('dominant_emotion', 'neutral')
            
            # Get confidence score for dominant emotion
            confidence: float = emotions.get(dominant_emotion, 0.0) if emotions else 0.0
            
            # Clean up temp file if created
            if image_array is not None and image_path:
                try:
                    os.unlink(image_path)
                except:
                    pass
            
            return {
                'success': True,
                'dominant_emotion': dominant_emotion,
                'all_emotions': emotions,
                'emoji': self.EMOTION_EMOJIS.get(
                    dominant_emotion.lower(),
                    '😐'
                ),
                'confidence': round(confidence, 2)
            }
            
        except Exception as e:
            # Clean up temp file on error
            if image_array is not None and image_path:
                try:
                    os.unlink(image_path)
                except:
                    pass
            
            return {
                'success': False,
                'error': str(e),
                'dominant_emotion': 'neutral',
                'emoji': '😐',
                'message': 'Could not detect face. Using neutral emotion.'
            }
    
    def detect_from_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """Detect emotion from image bytes"""
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return {
                'success': False,
                'error': 'Could not decode image',
                'dominant_emotion': 'neutral',
                'emoji': '😐'
            }
        
        return self.detect_emotion(image_array=image)
    
    def get_emotion_description(self, emotion: str) -> str:
        """Get description for detected emotion"""
        descriptions = {
            'happy': 'You appear joyful and content!',
            'sad': 'You seem a bit down. Hope things get better!',
            'angry': 'You appear frustrated. Take a deep breath!',
            'surprise': 'You look surprised or amazed!',
            'fear': 'You seem worried. Everything will be okay!',
            'disgust': 'You appear displeased about something.',
            'neutral': 'You have a calm, neutral expression.'
        }
        return descriptions.get(emotion.lower(), 'Interesting expression!')
    
    def validate_image(self, image_path: str) -> Tuple[bool, str]:
        """Validate if image is suitable for analysis"""
        if not os.path.exists(image_path):
            return False, "Image file not found"
        
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False, "Could not read image"
            
            height, width = img.shape[:2]
            if width < 50 or height < 50:
                return False, "Image too small (minimum 50x50)"
            
            return True, "Image valid"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
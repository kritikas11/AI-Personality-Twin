"""
Backend Package
AI Personality Twin backend components
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from backend.nlp.pipeline import NLPPipeline
from backend.vision.emotion_detector import EmotionDetector
from backend.avatar.generator import AvatarGenerator
from backend.db.database import Database

__all__ = [
    'NLPPipeline',
    'EmotionDetector',
    'AvatarGenerator',
    'Database'
]
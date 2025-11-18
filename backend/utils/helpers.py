"""
Helper Utilities
Common utility functions used across the application
"""
import re
from typing import Dict, Any, Tuple, Optional, Union
from datetime import datetime

def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate user name input
    
    Returns:
        (is_valid, error_message)
    """
    if not name or len(name.strip()) == 0:
        return False, "Name cannot be empty"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 50:
        return False, "Name must be less than 50 characters"
    
    # Allow letters, spaces, hyphens, apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""

def validate_text_input(text: str, min_length: int = 10) -> Tuple[bool, str]:
    """
    Validate text input for analysis
    
    Returns:
        (is_valid, error_message)
    """
    if not text or len(text.strip()) == 0:
        return False, "Please provide some text to analyze"
    
    if len(text.strip()) < min_length:
        return False, f"Text must be at least {min_length} characters"
    
    if len(text) > 5000:
        return False, "Text is too long (maximum 5000 characters)"
    
    return True, ""

def format_confidence(confidence: float) -> str:
    """Format confidence score as percentage"""
    return f"{confidence:.1f}%"

def format_timestamp(timestamp: Optional[Union[str, datetime]] = None) -> str:
    """Format timestamp to readable string"""
    if timestamp is None:
        timestamp = datetime.now()
    
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except:
            return timestamp
    
    return timestamp.strftime("%B %d, %Y at %I:%M %p")

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potential harmful characters
    text = text.strip()
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def calculate_profile_score(
    sentiment_score: float,
    trait_count: int,
    text_length: int
) -> int:
    """
    Calculate overall profile score (0-100)
    
    Args:
        sentiment_score: Sentiment polarity (-1 to 1)
        trait_count: Number of detected traits
        text_length: Length of input text
        
    Returns:
        Score from 0 to 100
    """
    # Normalize sentiment to 0-40 range
    sentiment_points = ((sentiment_score + 1) / 2) * 40
    
    # Trait points (0-40)
    trait_points = min(trait_count * 8, 40)
    
    # Text length points (0-20)
    text_points = min((text_length / 100) * 20, 20)
    
    total_score = sentiment_points + trait_points + text_points
    return int(min(100, max(0, total_score)))

def get_color_from_emotion(emotion: str) -> str:
    """Get color hex code based on emotion"""
    emotion_colors = {
        'happy': '#FFD700',      # Gold
        'sad': '#4169E1',        # Royal Blue
        'angry': '#DC143C',      # Crimson
        'surprise': '#FF69B4',   # Hot Pink
        'fear': '#9370DB',       # Medium Purple
        'disgust': '#8B4513',    # Saddle Brown
        'neutral': '#708090'     # Slate Gray
    }
    return emotion_colors.get(emotion.lower(), '#808080')

def get_color_from_trait(trait: str) -> str:
    """Get color hex code based on personality trait"""
    trait_colors = {
        'Creative': '#9B59B6',      # Purple
        'Optimistic': '#F39C12',    # Orange
        'Friendly': '#3498DB',      # Blue
        'Analytical': '#16A085',    # Teal
        'Adventurous': '#E74C3C',   # Red
        'Calm': '#95A5A6',          # Gray
        'Energetic': '#E67E22',     # Dark Orange
        'Empathetic': '#E91E63'     # Pink
    }
    return trait_colors.get(trait, '#34495E')

def create_response(
    success: bool,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create standardized API response
    
    Args:
        success: Whether operation was successful
        data: Response data
        error: Error message if failed
        message: Success message
        
    Returns:
        Standardized response dictionary
    """
    response: Dict[str, Any] = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    if error is not None:
        response['error'] = error
    
    if message is not None:
        response['message'] = message
    
    return response
"""
Avatar Generator Module
Generates DiceBear avatar URLs based on personality traits
"""
import hashlib
from typing import Dict, List, Optional

class AvatarGenerator:
    """Generate DiceBear avatars based on personality"""
    
    DICEBEAR_BASE_URL = "https://api.dicebear.com/7.x"
    
    # Avatar styles mapped to personality traits
    STYLE_MAPPING = {
        'creative': 'avataaars',
        'optimistic': 'bottts',
        'friendly': 'big-smile',
        'analytical': 'personas',
        'adventurous': 'adventurer',
        'calm': 'lorelei',
        'energetic': 'fun-emoji',
        'default': 'avataaars'
    }
    
    @staticmethod
    def generate_seed(name: str, traits: List[str]) -> str:
        """Generate a unique seed based on name and traits"""
        combined = f"{name}{''.join(sorted(traits))}"
        return hashlib.md5(combined.encode()).hexdigest()[:10]
    
    @staticmethod
    def get_style_from_traits(traits: Dict[str, float]) -> str:
        """Determine avatar style based on dominant trait"""
        if not traits:
            return AvatarGenerator.STYLE_MAPPING['default']
        
        # Get the trait with highest score
        dominant_trait = max(traits, key=lambda k: traits[k]).lower()
        
        # Map to avatar style
        for key, style in AvatarGenerator.STYLE_MAPPING.items():
            if key in dominant_trait:
                return style
        
        return AvatarGenerator.STYLE_MAPPING['default']
    
    @staticmethod
    def generate_avatar_url(
        name: str = "user",
        traits: Optional[Dict[str, float]] = None,
        emotion: str = "neutral"
    ) -> str:
        """
        Generate DiceBear avatar URL
        
        Args:
            name: User name for seed generation
            traits: Dictionary of personality traits with scores
            emotion: Detected emotion
            
        Returns:
            Complete DiceBear avatar URL
        """
        if traits is None:
            traits = {}
        
        # Determine style based on traits
        style = AvatarGenerator.get_style_from_traits(traits)
        
        # Generate unique seed
        trait_list = list(traits.keys())
        seed = AvatarGenerator.generate_seed(name, trait_list)
        
        # Build URL with parameters
        url = f"{AvatarGenerator.DICEBEAR_BASE_URL}/{style}/svg"
        params = [
            f"seed={seed}",
            "size=200",
            "backgroundColor=b6e3f4,c0aede,d1d4f9"
        ]
        
        # Add mood-based customization
        if emotion.lower() == "happy":
            params.append("mood[]=happy")
        elif emotion.lower() == "sad":
            params.append("mood[]=sad")
        
        return f"{url}?{'&'.join(params)}"
    
    @staticmethod
    def generate_multiple_avatars(
        name: str,
        traits: Dict[str, float],
        count: int = 3
    ) -> List[str]:
        """Generate multiple avatar variations"""
        avatars = []
        styles = ['avataaars', 'bottts', 'big-smile', 'personas']
        
        for i, style in enumerate(styles[:count]):
            seed = AvatarGenerator.generate_seed(name, list(traits.keys()))
            url = f"{AvatarGenerator.DICEBEAR_BASE_URL}/{style}/svg"
            params = [
                f"seed={seed}{i}",
                "size=150",
                "backgroundColor=b6e3f4,c0aede,d1d4f9"
            ]
            avatars.append(f"{url}?{'&'.join(params)}")
        
        return avatars
"""
NLP Models Module
Text analysis for personality trait extraction
"""
from textblob import TextBlob
import re
from typing import Dict, List, Tuple, Any

class PersonalityAnalyzer:
    """Analyze text to extract personality traits"""
    
    # Keyword mappings for personality traits
    TRAIT_KEYWORDS = {
        'Creative': [
            'create', 'imagine', 'art', 'design', 'innovative', 'original',
            'unique', 'inventive', 'artistic', 'creative', 'ideas', 'inspire'
        ],
        'Optimistic': [
            'happy', 'positive', 'hope', 'bright', 'excited', 'love',
            'great', 'wonderful', 'amazing', 'best', 'enjoy', 'passionate'
        ],
        'Friendly': [
            'friend', 'people', 'help', 'kind', 'care', 'social',
            'together', 'team', 'share', 'support', 'community', 'connect'
        ],
        'Analytical': [
            'think', 'analyze', 'logic', 'reason', 'solve', 'strategy',
            'plan', 'detail', 'organize', 'systematic', 'data', 'research'
        ],
        'Adventurous': [
            'adventure', 'explore', 'travel', 'new', 'challenge', 'risk',
            'bold', 'brave', 'discover', 'experience', 'outdoor', 'journey'
        ],
        'Calm': [
            'peace', 'quiet', 'relax', 'calm', 'serene', 'tranquil',
            'meditate', 'mindful', 'balance', 'harmony', 'gentle', 'patient'
        ],
        'Energetic': [
            'energy', 'active', 'dynamic', 'enthusiastic', 'vigorous',
            'lively', 'spirited', 'fast', 'action', 'sport', 'exercise'
        ],
        'Empathetic': [
            'understand', 'feel', 'empathy', 'compassion', 'sensitive',
            'emotion', 'listen', 'care', 'concern', 'warm', 'heart'
        ]
    }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text.strip()
    
    @staticmethod
    def analyze_sentiment(text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        
        Returns:
            (sentiment_label, polarity_score)
        """
        blob = TextBlob(text)
        polarity: float = blob.sentiment.polarity  # type: ignore[attr-defined]
        
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return sentiment, polarity
    
    @staticmethod
    def extract_traits(text: str) -> Dict[str, float]:
        """
        Extract personality traits from text
        
        Returns:
            Dictionary of traits with confidence scores (0-100)
        """
        cleaned_text = PersonalityAnalyzer.clean_text(text)
        words = cleaned_text.split()
        
        trait_scores: Dict[str, float] = {}
        
        for trait, keywords in PersonalityAnalyzer.TRAIT_KEYWORDS.items():
            score = 0
            matches = 0
            
            for keyword in keywords:
                if keyword in cleaned_text:
                    matches += 1
                    # Higher score for exact word matches
                    if keyword in words:
                        score += 2
                    else:
                        score += 1
            
            if matches > 0:
                # Normalize score to 0-100 range
                confidence = min(100, (score / len(keywords)) * 100 + 20)
                trait_scores[trait] = round(confidence, 1)
        
        # If no traits detected, assign default based on sentiment
        if not trait_scores:
            blob = TextBlob(text)
            blob_polarity: float = blob.sentiment.polarity  # type: ignore[attr-defined]
            if blob_polarity > 0:
                trait_scores['Optimistic'] = 60.0
            else:
                trait_scores['Calm'] = 50.0
        
        # Sort by score and return top traits
        sorted_traits = dict(
            sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        
        return sorted_traits
    
    @staticmethod
    def get_personality_summary(traits: Dict[str, float]) -> str:
        """Generate a text summary of personality"""
        if not traits:
            return "Your personality is unique and multifaceted!"
        
        top_traits = list(traits.keys())[:3]
        
        if len(top_traits) == 1:
            summary = f"You are primarily {top_traits[0]}."
        elif len(top_traits) == 2:
            summary = f"You are {top_traits[0]} and {top_traits[1]}."
        else:
            summary = f"You are {', '.join(top_traits[:-1])}, and {top_traits[-1]}."
        
        return summary
    
    @staticmethod
    def analyze_full(text: str) -> Dict[str, Any]:
        """
        Complete text analysis
        
        Returns:
            Dictionary with sentiment, traits, and summary
        """
        sentiment, polarity = PersonalityAnalyzer.analyze_sentiment(text)
        traits = PersonalityAnalyzer.extract_traits(text)
        summary = PersonalityAnalyzer.get_personality_summary(traits)
        
        # Calculate subjectivity
        blob = TextBlob(text)
        subjectivity: float = blob.sentiment.subjectivity  # type: ignore[attr-defined]
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 2),
            'subjectivity': round(subjectivity, 2),
            'traits': traits,
            'summary': summary,
            'word_count': len(text.split())
        }
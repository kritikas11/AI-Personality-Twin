"""
NLP Pipeline Module
Orchestrates the complete text analysis pipeline
"""
from backend.nlp.models import PersonalityAnalyzer
from typing import Dict

class NLPPipeline:
    """Pipeline for processing text input"""
    
    def __init__(self):
        """Initialize pipeline components"""
        self.analyzer = PersonalityAnalyzer()
    
    def process(self, text: str) -> Dict:
        """
        Process text through complete NLP pipeline
        
        Args:
            text: Input text to analyze
            
        Returns:
            Complete analysis results
        """
        if not text or len(text.strip()) < 10:
            return {
                'error': 'Text too short. Please provide at least 10 characters.',
                'success': False
            }
        
        try:
            # Perform full analysis
            results = self.analyzer.analyze_full(text)
            
            # Add success flag
            results['success'] = True
            results['processed_text'] = text[:500]  # Store first 500 chars
            
            return results
            
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'success': False
            }
    
    def get_trait_descriptions(self) -> Dict[str, str]:
        """Get descriptions for each personality trait"""
        return {
            'Creative': 'You have an imaginative mind and love to create new things.',
            'Optimistic': 'You see the bright side of life and maintain a positive outlook.',
            'Friendly': 'You enjoy connecting with others and building relationships.',
            'Analytical': 'You approach problems logically and enjoy problem-solving.',
            'Adventurous': 'You seek new experiences and embrace challenges.',
            'Calm': 'You maintain composure and bring peace to situations.',
            'Energetic': 'You have high energy and enthusiasm for activities.',
            'Empathetic': 'You understand and share the feelings of others.'
        }
    
    def get_trait_emojis(self) -> Dict[str, str]:
        """Get emoji representations for traits"""
        return {
            'Creative': '🎨',
            'Optimistic': '🌟',
            'Friendly': '🤝',
            'Analytical': '🧠',
            'Adventurous': '🗺️',
            'Calm': '🧘',
            'Energetic': '⚡',
            'Empathetic': '❤️'
        }
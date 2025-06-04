from typing import List
import spacy
from .interfaces import Tokenizer as TopicSummarizerTokenizer

class SpacyTokenizer(TopicSummarizerTokenizer):
    """Implementation of tokenizer interfaces using spaCy."""
    
    def __init__(self):
        """Initialize the SpacyTokenizer with the en_core_web_sm model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model is not found, download it
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Disable unnecessary components for better performance
        self.nlp.disable_pipes(["parser", "ner"])

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the given text using spaCy.
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of token strings
        """
        doc = self.nlp(text)
        return [token.text for token in doc]

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.
        
        Args:
            text: The text to count tokens in
            
        Returns:
            Number of tokens
        """
        doc = self.nlp(text)
        return len(doc) 

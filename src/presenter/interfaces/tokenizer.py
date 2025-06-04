"""Interface for text tokenization in the presenter module."""

from abc import abstractmethod
from typing import List
from topic_summarizer import Tokenizer as TopicSummarizerTokenizer

class Tokenizer(TopicSummarizerTokenizer):
    """Abstract interface for text tokenization."""
    
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the given text into a list of tokens.
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of tokens
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.
        
        Args:
            text: The text to count tokens in
            
        Returns:
            Number of tokens
        """
        pass 

"""Interface for JSON generation in the presenter module."""

from abc import abstractmethod
from typing import Type, TypeVar
from pydantic import BaseModel
from utils.result import Result
from topic_summarizer import JsonGenerator as TopicSummarizerJsonGeneratorABC

T = TypeVar("T", bound=BaseModel)

class JsonGenerator(TopicSummarizerJsonGeneratorABC):
    """Abstract interface for JSON generation."""
    
    @abstractmethod
    def json_query(self, context: str, query: str, expected_schema: Type[T]) -> Result[T, str]:
        """
        Generate a JSON response based on the given prompt and expected schema.
        
        Args:
            context: The context for the query
            query: The query to process
            expected_schema: The expected schema for the response
            
        Returns:
            Result containing either the parsed response of type T or an error message
        """
        pass 

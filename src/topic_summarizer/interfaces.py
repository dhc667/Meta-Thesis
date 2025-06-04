from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type, TypeVar
from pydantic import BaseModel
from utils.result import Result

T = TypeVar("T", bound=BaseModel)

class JsonGenerator(ABC):
    @abstractmethod
    def json_query(self, context: str, query: str, expected_schema: Type[T]) -> Result[T, str]:
        """
        Generate a JSON response based on the given prompt and expected schema.
        
        Returns:
            Result containing either the parsed response of type T or an error message
        """
        pass

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        """Tokenize the given text into a list of tokens."""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        pass 

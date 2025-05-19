from abc import ABC, abstractmethod
from typing import Type, TypeVar
from pydantic import BaseModel
from utils.result import Result

T = TypeVar("T", bound=BaseModel)

class LlmJsonQuerier(ABC):
    @abstractmethod
    def json_query(self, context: str, query: str, expected_schema: Type[T]) -> Result[T, str]:
        pass


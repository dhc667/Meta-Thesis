from abc import ABC, abstractmethod
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from enum import Enum

from utils.result import Result

class ExtractorError(Enum):
    BadLlmOutput = "Llm bad output"
    NoTopicsFound = "No topics found"

class TopicExtractor(ABC):
    @abstractmethod
    def extract_topic(self, doc: ReadDocument) -> Result[str, ExtractorError]:
        pass

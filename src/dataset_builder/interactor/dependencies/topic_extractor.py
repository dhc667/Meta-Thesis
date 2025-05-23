from abc import ABC, abstractmethod

from src.dataset_builder.interactor.dependencies.read_document import ReadDocument

class TopicExtractor(ABC):
    @abstractmethod
    def extract_topic(self, doc: ReadDocument) -> str:
        pass

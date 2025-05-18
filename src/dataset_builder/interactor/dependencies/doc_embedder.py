from abc import ABC, abstractmethod

from dataset_builder.interactor.dependencies.embedded_document import Embedding
from dataset_builder.interactor.dependencies.read_document import ReadDocument

class DocumentEmbedder(ABC):
    @abstractmethod
    def embed_documents(self, documents: list[ReadDocument]) -> list[Embedding]:
        pass

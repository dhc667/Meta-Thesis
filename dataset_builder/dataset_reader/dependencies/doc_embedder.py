from abc import ABC, abstractmethod

from dataset_builder.interactor.dependencies.embedded_document import EmbeddedDocument
from dataset_builder.interactor.dependencies.read_document import ReadDocument

class DocumentEmbedder(ABC):
    @abstractmethod
    def embed_document(self, document: ReadDocument) -> EmbeddedDocument:
        pass

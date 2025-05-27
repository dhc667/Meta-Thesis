from abc import ABC, abstractmethod

from dataset_builder.interactor.dependencies.embedded_document import Embedding
from dataset_builder.interactor.dependencies.read_document import ReadDocument

class Embedder(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[Embedding]:
        pass

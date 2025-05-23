from abc import ABC, abstractmethod
from pathlib import Path

from dataset_builder.interactor.dependencies.embedded_document import PersistenceDocument

class DocumentRepository(ABC):
    @abstractmethod
    def store_documents(self, documents: list[PersistenceDocument]):
        """Stores the given documents in persistent storage"""
        pass

    @abstractmethod
    def get_documents(self) -> list[PersistenceDocument]:
        """Returns all documents stored"""
        pass

    @abstractmethod
    def document_exists(self, path: Path) -> bool:
        """Returns true iff the document with the given path exists in the repository"""
        pass


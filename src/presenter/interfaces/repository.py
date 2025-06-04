"""Interface for document repository in the presenter module."""

from abc import ABC, abstractmethod
from typing import List, Type, TypeVar
from dataclasses import dataclass
import numpy as np

from dataset_builder.interactor.dependencies.embedded_document import Embedding, PersistenceDocument

T = TypeVar("T", bound=Embedding)

@dataclass
class DocumentMetadata:
    """Metadata for a document in the visualization."""
    path: str
    title: str
    authors: List[str]
    topic: str | None
    embedding: np.ndarray

class DocumentRepository(ABC):
    """Abstract interface for document repository access."""
    
    @abstractmethod
    def get_documents(self, embedding_type: Type[T]) -> List[PersistenceDocument]:
        """
        Retrieve all documents with their embeddings from the repository.
        
        Args:
            embedding_type: The type of embedding to retrieve
            
        Returns:
            List of documents with their embeddings
        """
        pass 
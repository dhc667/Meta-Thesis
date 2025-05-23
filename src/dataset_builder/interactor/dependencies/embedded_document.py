from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self
import numpy as np

from dataset_builder.interactor.dependencies.read_document import ReadDocument

class Embedding(ABC):
    @abstractmethod
    def similarity(self, other: Self) -> float:
        pass

    @abstractmethod
    def serialize(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(blob: bytes) -> Embedding:
        pass

    @abstractmethod
    def get_vector(self) -> np.ndarray:
        pass


class PersistenceDocument:
    def __init__(self, source: ReadDocument, embedding: Embedding, topic: str) -> None:
        self._source = source
        self.topic = topic
        self.embedding = embedding

    @property
    def path(self):
        return self._source.file_path

    @property
    def title(self):
        return self._source.title

    @property
    def abstract(self):
        return self._source.abstract
    
    @property
    def authors(self):
        return self._source.authors

    @property
    def tutors(self):
        return self._source.tutors

    @property
    def date(self):
        return self._source.date

    @property
    def full_text(self):
        return self._source.full_text





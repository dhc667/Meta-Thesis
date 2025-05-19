from abc import ABC, abstractmethod
from typing import Self

from dataset_builder.interactor.dependencies.read_document import ReadDocument

class Embedding(ABC):
    @abstractmethod
    def similarity(self, other: Self) -> float:
        pass
    
class EmbeddedDocument:
    def __init__(self, source: ReadDocument, embedding: Embedding) -> None:
        self.source = source
        self.embedding = embedding

    @property
    def abstract(self):
        return self.source.abstract
    
    @property
    def authors(self):
        return self.source.authors

    @property
    def tutors(self):
        return self.source.tutors

    @property
    def date(self):
        return self.source.date

    @property
    def full_text(self):
        return self.source.full_text



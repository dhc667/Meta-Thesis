from abc import ABC, abstractmethod

from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.dataset_reader.dependencies.document import Document

class DocumentParser(ABC):
    @abstractmethod
    def parse_documents(self, buffers: list[DocumentBuffer]) -> list[Document]:
        """Parses the given documents and returns a list with the results"""
        pass

    

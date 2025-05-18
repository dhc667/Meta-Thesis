from abc import ABC, abstractmethod
from enum import Enum

from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.dataset_reader.dependencies.document import Document
from utils.result import Result

class ParsingError(Enum):
    EmptyDocument = "Empty document"
    CouldNotParse = "Could not parse"

class DocumentParser(ABC):
    @abstractmethod
    def parse_documents(self, buffers: list[DocumentBuffer]) -> list[Result[Document, ParsingError]]:
        """Parses the given documents and returns a list with the results"""
        pass

    

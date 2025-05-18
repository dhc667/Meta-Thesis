from abc import ABC, abstractmethod
from pathlib import Path
from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer

class FileReader(ABC):
    @abstractmethod
    def read_file(self, full_path: Path) -> DocumentBuffer:
        """Returns a buffer to read the given document"""
        pass

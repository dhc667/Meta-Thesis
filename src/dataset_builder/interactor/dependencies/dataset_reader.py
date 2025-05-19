from abc import ABC, abstractmethod
from pathlib import Path
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from utils.result import Result


class DatasetReader(ABC):
    @abstractmethod
    def read_pdf_file(self, path: Path) -> Result[ReadDocument, str]:
        """Returns a list of fully parsed documents from a file dataset rooted at the
        root_path parameter, i.e. a folder containing a set of .pdf files"""
        pass

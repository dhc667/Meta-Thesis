from dataset_builder.dataset_reader.dependencies.doc_parser import DocumentParser
from dataset_builder.dataset_reader.dependencies.file_reader import FileReader
from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader as DatasetReaderABC

class PdfDatasetReader(DatasetReaderABC):
    def __init__(self, file_reader: FileReader, document_parser: DocumentParser) -> None:
        self.file_reader = file_reader
        self.document_parser = document_parser
        raise NotImplementedError()

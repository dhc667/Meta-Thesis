from pathlib import Path

from dataset_builder.dataset_reader.dependencies.doc_parser import DocumentParser
from dataset_builder.dataset_reader.dependencies.file_reader import FileReader
from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader as DatasetReaderABC
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from utils.result import Result

class PdfDatasetReader(DatasetReaderABC):
    def __init__(self, file_reader: FileReader, document_parser: DocumentParser) -> None:
        self.file_reader = file_reader
        self.document_parser = document_parser

    def read_pdf_file(self, path: Path) -> Result[ReadDocument, str]:
        buffer = self.file_reader.read_file(path)
        doc = self.document_parser.parse_documents([buffer])[0]
        doc = doc.map(lambda doc: doc.to_read_document(str(path))).map_err(lambda err: str(err))
        return doc



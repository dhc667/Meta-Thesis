from pathlib import Path
from typing import Iterator, List

from dataset_builder.dataset_reader.dependencies.doc_parser import DocumentParser
from dataset_builder.dataset_reader.dependencies.file_reader import FileReader
from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader as DatasetReaderABC
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from utils.result import Result

class PdfDatasetReader(DatasetReaderABC):
    def __init__(self, file_reader: FileReader, document_parser: DocumentParser) -> None:
        self.file_reader = file_reader
        self.document_parser = document_parser

    def read_pdf_dataset(self, root_path: Path) -> List[Result[ReadDocument, str]]:
        buffers = []
        paths = []
        for path in self._find_pdf_files(root_path):
            buffers += [self.file_reader.read_file(path)]
            paths += [path]

        documents = self.document_parser.parse_documents(buffers)

        result: List[Result[ReadDocument, str]] = []
        for doc, path in zip(documents, paths):
            path: Path
            if doc.is_ok():
                result += [Result.new_ok(doc.unwrap().to_read_document(str(path)))]
            else:
                print(f"Error parsing document at {path}: {doc.unwrap_err()}")
                result += [Result.new_err(doc.unwrap_err())]

        return result

        # ok_indexes = [i for i in range(len(documents)) if documents[i].is_ok()]

        # ok_documents = [documents[i].unwrap() for i in ok_indexes]

        # embedded_ok_documents = self.document_embedder.embed_documents(ok_documents)
        # embedded_ok_documents = {k: embedded_ok_documents[i] for i, k in enumerate(ok_indexes) }

        # return [
        #     Result.new_ok(embedded_ok_documents[i])
        #         if i in embedded_ok_documents
        #     else Result.new_err(documents[i].unwrap_err())
        #     for i in range(len(documents))
        # ]

    def _find_pdf_files(self, root_path: Path) -> Iterator[Path]:
        root_path = root_path.resolve()
        return root_path.rglob("*.pdf")

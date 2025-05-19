from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.dataset_reader.dependencies.doc_parser import DocumentParser
from dataset_builder.dataset_reader.dependencies.document import Document

class MixedParser(DocumentParser):
    def __init__(self) -> None:
        pass

    def parse_documents(self, buffers: list[DocumentBuffer]) -> list[Document]:
        raise NotImplementedError()


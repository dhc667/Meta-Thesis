from typing import Optional
from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer

class AlgorithmicParser:
    def __init__(self, buffer: DocumentBuffer) -> None:
        self.buffer = buffer
        raise NotImplementedError()

    def try_parse_abstract(self) -> Optional[str]:
        raise NotImplementedError()

    def parse_full_text(self) -> str:
        raise NotImplementedError()
        

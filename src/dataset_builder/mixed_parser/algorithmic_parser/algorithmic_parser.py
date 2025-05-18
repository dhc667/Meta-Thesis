from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer

class AlgorithmicParser:
    def __init__(self, buffer: DocumentBuffer) -> None:
        self.buffer = buffer

    def parse_full_text(self) -> str:
        text = ""
        for page in self.buffer.get_pages():
            text += "\n" + page

        return text

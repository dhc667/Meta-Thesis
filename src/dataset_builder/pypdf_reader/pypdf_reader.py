from pathlib import Path
from pypdf import PdfReader
from dataset_builder.dataset_reader.dependencies.file_reader import FileReader
from dataset_builder.pypdf_reader.pdf_buffer import PdfBuffer

class PypdfReader(FileReader):
    def __init__(self) -> None:
        pass

    def read_file(self, full_path: Path) -> PdfBuffer:
        pdf = PdfReader(full_path)
        return PdfBuffer(pdf)



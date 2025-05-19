from typing import Iterator, Optional
from pypdf import PdfReader
from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer


class PdfBuffer(DocumentBuffer):
    def __init__(self, pdf: PdfReader) -> None:
        self.pdf = pdf
        self.len = len(self.pdf.pages)
        self.page_cache: list[str | None] = [None] * self.len

    def get_page(self, page_number: int) -> Optional[str]:
        return self._get_from_cache(page_number)

    def get_pages(self) -> Iterator[str]:
        for i in range(self.len):
            page = self._get_from_cache(i)
            assert page != None
            yield page

    def _get_from_cache(self, page_number: int) -> Optional[str]:
        if self.len <= page_number:
            return None

        if not self.page_cache[page_number]:
            self.page_cache[page_number] = self.pdf.pages[page_number].extract_text()

        return self.page_cache[page_number]

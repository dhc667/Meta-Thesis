from abc import ABC, abstractmethod
from typing import Iterator, Optional

class DocumentBuffer(ABC):
    @abstractmethod
    def get_page(self, page_number: int) -> Optional[str]:
        """Gets a given page of a document, if it exists, None if not"""
        pass

    @abstractmethod
    def get_pages(self) -> Iterator[str]:
        """Returns an iterator over the pages of the document"""
        pass

    @abstractmethod
    def page_count(self) -> int:
        pass

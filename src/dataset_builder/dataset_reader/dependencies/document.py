from dataset_builder.interactor.dependencies.read_document import ReadDocument
from utils.partial_date import PartialDate

class Document:
    def __init__(self, title: str, abstract: str, authors: list[str], tutors: list[str], date: PartialDate, full_text: str) -> None:
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.tutors = tutors
        self.date = date
        self.full_text = full_text

    def to_read_document(self, file_path: str) -> ReadDocument:
        return ReadDocument(file_path, self.title, self.abstract, self.authors, self.tutors, self.date, self.full_text)


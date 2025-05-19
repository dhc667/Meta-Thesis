from utils.partial_date import PartialDate

class ReadDocument:
    def __init__(self, file_name: str, title: str, abstract: str, authors: list[str], tutors: list[str], date: PartialDate, full_text: str) -> None:
        self.file_path = file_name
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.tutors = tutors
        self.date = date
        self.full_text = full_text



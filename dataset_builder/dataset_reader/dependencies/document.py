class Document:
    def __init__(self, abstract: str, authors: str, tutors: list[str], date: str, full_text: str) -> None:
        self.abstract = abstract
        self.authors = authors
        self.tutors = tutors
        self.date = date
        self.full_text = full_text


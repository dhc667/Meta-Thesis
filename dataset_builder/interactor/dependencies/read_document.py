class ReadDocument:
    def __init__(self, abstract: str, authors: list[str], tutors: list[str], date: str, full_text: str) -> None:
        self.abstract = abstract
        self.authors = authors
        self.tutors = tutors
        self.date = date
        self.full_text = full_text


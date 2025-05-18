from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader
from dataset_builder.interactor.dependencies.repository import DocumentRepository

class Interactor:
    def __init__(self, reader: DatasetReader, repository: DocumentRepository) -> None:
        self.reader = reader
        self.repository = repository
        raise NotImplementedError()


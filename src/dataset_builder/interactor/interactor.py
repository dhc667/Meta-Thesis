from pathlib import Path
from typing import Iterator
from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader
from dataset_builder.interactor.dependencies.repository import DocumentRepository
from dataset_builder.interactor.dependencies.doc_embedder import Embedder
from dataset_builder.interactor.dependencies.embedded_document import PersistenceDocument
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from dataset_builder.interactor.dependencies.topic_extractor import TopicExtractor

class Interactor:
    def __init__(self, reader: DatasetReader, repository: DocumentRepository, embedder: Embedder, topic_extractor: TopicExtractor) -> None:
        self.reader = reader
        self.repository = repository
        self.embedder = embedder
        self.topic_extractor = topic_extractor

    def build_dataset(self, dataset_root: Path) -> None:
        log_prefix = "Dataset Builder Interactor: "

        print(log_prefix + "Reading pdfs...")

        for pdf_path in self._find_pdf_files(dataset_root):

            if self.repository.document_exists(pdf_path):
                print(f"Cache hit: {pdf_path}")
                continue

            print(f"Cache miss: {pdf_path}")

            result = self.reader.read_pdf_file(pdf_path)
            if result.is_err():
                print(f"Error parsing pdf at {pdf_path}: {result.unwrap_err()}")
                continue

            doc = result.unwrap()
            topic = self.topic_extractor.extract_topic(doc)
            if topic.is_err():
                print(f"Error extracting topic of {pdf_path}: {topic.unwrap_err()}")
                continue
            else:
                topic = topic.unwrap()

            embedding = self.embedder.embed_texts([doc.abstract])[0]
            embedded_doc = PersistenceDocument(doc, embedding, topic)

            self.repository.store_documents([embedded_doc])

    def _find_pdf_files(self, root_path: Path) -> Iterator[Path]:
        root_path = root_path.resolve()
        return root_path.rglob("*.pdf")






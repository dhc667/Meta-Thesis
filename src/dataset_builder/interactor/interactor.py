from pathlib import Path
from dataset_builder.interactor.dependencies.dataset_reader import DatasetReader
from dataset_builder.interactor.dependencies.repository import DocumentRepository
from dataset_builder.interactor.dependencies.doc_embedder import DocumentEmbedder
from dataset_builder.interactor.dependencies.embedded_document import EmbeddedDocument
from dataset_builder.interactor.dependencies.read_document import ReadDocument

class Interactor:
    def __init__(self, reader: DatasetReader, repository: DocumentRepository, embedder: DocumentEmbedder) -> None:
        self.reader = reader
        self.repository = repository
        self.embedder = embedder

    def build_dataset(self, dataset_root: Path) -> None:
        log_prefix = "Dataset Builder Interactor: "

        print(log_prefix + "Reading pdfs...")
        documents = self.reader.read_pdf_dataset(dataset_root)
        ok_docs: list[ReadDocument] = []
        for doc in documents:
            if doc.is_ok():
                ok_docs.append(doc.unwrap())

        print(log_prefix + "Embedding documents...")
        embeddings = self.embedder.embed_documents(ok_docs)

        embedded_docs = [EmbeddedDocument(doc, embedding) for doc, embedding in zip(ok_docs, embeddings)]

        print(log_prefix + "Storing documents...")
        self.repository.store_documents(embedded_docs)






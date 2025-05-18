import sqlite3
import json
import pickle
from pathlib import Path
from typing import List

from dataset_builder.interactor.dependencies.embedded_document import EmbeddedDocument
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from dataset_builder.interactor.dependencies.embedded_document import Embedding
from dataset_builder.interactor.dependencies.repository import DocumentRepository
from utils.partial_date import PartialDate

class SQLiteDocumentRepository(DocumentRepository):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_table(self):
        with self._connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                title TEXT NOT NULL,
                abstract TEXT,
                authors TEXT NOT NULL,       -- JSON list
                tutors TEXT NOT NULL,        -- JSON list
                full_text TEXT NOT NULL,
                date_year INTEGER NOT NULL,
                date_month INTEGER NULL,
                date_day INTEGER NULL,
                embedding BLOB NOT NULL
            ) strict
            """)
            conn.commit()

    def store_documents(self, documents: List[EmbeddedDocument]):
        with self._connect() as conn:
            for doc in documents:
                conn.execute("""
                    INSERT INTO documents (
                        path, title, abstract, authors, tutors, full_text,
                        date_year, date_month, date_day, embedding
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc.path,
                    doc.title,
                    doc.abstract,
                    json.dumps(doc.authors),
                    json.dumps(doc.tutors),
                    doc.full_text,
                    doc.date.year,
                    doc.date.month,
                    doc.date.day,
                    pickle.dumps(doc.embedding)
                ))
            conn.commit()

    def get_documents(self) -> List[EmbeddedDocument]:
        with self._connect() as conn:
            rows = conn.execute("SELECT path, title, abstract, authors, tutors, full_text, date_year, date_month, date_day, embedding FROM documents")
            result = []
            for row in rows:
                path, title, abstract, authors, tutors, full_text, year, month, day, embedding_blob = row
                document = EmbeddedDocument(
                    source=ReadDocument(
                        file_name=path,
                        title=title,
                        abstract=abstract,
                        authors=json.loads(authors),
                        tutors=json.loads(tutors),
                        date=PartialDate(year, month, day),
                        full_text=full_text
                    ),
                    embedding=Embedding.deserialize(embedding_blob)
                )
                result.append(document)
            return result

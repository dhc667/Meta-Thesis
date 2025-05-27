import sqlite3
import json
from pathlib import Path
from typing import List, Type, TypeVar

from dataset_builder.interactor.dependencies.embedded_document import PersistenceDocument
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from dataset_builder.interactor.dependencies.embedded_document import Embedding
from dataset_builder.interactor.dependencies.repository import DocumentRepository
from utils.partial_date import PartialDate

T = TypeVar("T", bound=Embedding)

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
                topic TEXT,
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

    def store_documents(self, documents: List[PersistenceDocument]):
        with self._connect() as conn:
            for doc in documents:
                conn.execute("""
                    INSERT INTO documents (
                        path, title, abstract, topic, authors, tutors, full_text,
                        date_year, date_month, date_day, embedding
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc.path,
                    doc.title,
                    doc.abstract,
                    doc.topic,
                    json.dumps(doc.authors),
                    json.dumps(doc.tutors),
                    doc.full_text,
                    doc.date.year,
                    doc.date.month,
                    doc.date.day,
                    doc.embedding.serialize()
                ))
            conn.commit()


    def get_documents(self, embedding_type: Type[T]) -> List[PersistenceDocument]:
        with self._connect() as conn:
            rows = conn.execute("SELECT path, title, abstract, topic, authors, tutors, full_text, date_year, date_month, date_day, embedding FROM documents")
            result = []
            for row in rows:
                path, title, abstract, topic, authors, tutors, full_text, year, month, day, embedding_blob = row
                document = PersistenceDocument(
                    source=ReadDocument(
                        file_name=path,
                        title=title,
                        abstract=abstract,
                        authors=json.loads(authors),
                        tutors=json.loads(tutors),
                        date=PartialDate(year, month, day),
                        full_text=full_text
                    ),
                    embedding=embedding_type.deserialize(embedding_blob),
                    topic=topic,
                )
                result.append(document)
            return result

    def update_document(self, doc: PersistenceDocument):
        with self._connect() as conn:
            conn.execute("""
                UPDATE documents 
                SET embedding = ?
                WHERE path = ?
            """, (
                doc.embedding.serialize(),
                doc.path
            ))
            conn.commit()

    def document_exists(self, path: Path) -> bool:
        with self._connect() as conn:
            rows = conn.execute("SELECT 1 FROM documents WHERE path = ?", (str(path),))
            result = False
            for _ in rows:
                result = True

            conn.commit()
            return result
            

from typing import Self
from dataset_builder.interactor.dependencies.embedded_document import Embedding
import pickle

class MockEmbedding(Embedding):
    def __init__(self) -> None:
        pass

    def similarity(self, other: Self) -> float:
        return 1

    def serialize(self) -> bytes:
        return pickle.dumps("a")

    @staticmethod
    def deserialize(blob: bytes) -> Embedding:
        assert pickle.loads(blob) == "a"

        return MockEmbedding()



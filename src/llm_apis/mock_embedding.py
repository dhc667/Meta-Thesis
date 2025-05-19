from typing import Self
from dataset_builder.interactor.dependencies.embedded_document import Embedding
import pickle
import numpy as np

class MockEmbedding(Embedding):
    def __init__(self) -> None:
        pass

    def similarity(self, other: Self) -> float:
        return self.get_vector().dot(other.get_vector())

    def serialize(self) -> bytes:
        return pickle.dumps("a")

    @staticmethod
    def deserialize(blob: bytes) -> Embedding:
        assert pickle.loads(blob) == "a"

        return MockEmbedding()
    
    def get_vector(self) -> np.ndarray:
        return np.array([1, 2, 3])



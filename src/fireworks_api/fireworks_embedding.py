from __future__ import annotations
from typing import Self
import numpy as np
import pickle
from dataset_builder.interactor.dependencies.embedded_document import Embedding


class FireworksEmbedding(Embedding):
    def __init__(self, vector: np.ndarray) -> None:
        self.vector = vector
        self.norm = np.linalg.norm(self.vector)

    def similarity(self, other: Self) -> float:
        return other.get_vector().dot(self.get_vector()) / (self.norm * other.norm)

    def get_vector(self) -> np.ndarray:
        return self.vector

    def serialize(self) -> bytes:
        return pickle.dumps(self.vector)

    @staticmethod
    def deserialize(blob: bytes) -> FireworksEmbedding:
        # print("got document with embedding", blob)
        vector = pickle.loads(blob)
        return FireworksEmbedding(vector)

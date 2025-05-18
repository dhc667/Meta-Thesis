from abc import ABC, abstractmethod

class LlmApi(ABC):
    @abstractmethod
    def query_llm(self, context: str, query: str) -> str:
        pass

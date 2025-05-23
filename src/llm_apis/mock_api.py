from typing import Type, TypeVar

from pydantic import BaseModel
import config
from dataset_builder.interactor.dependencies.doc_embedder import LlmEmbedder
from dataset_builder.interactor.dependencies.embedded_document import PersistenceDocument, Embedding
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import LlmJsonQuerier
from llm_apis.mock_embedding import MockEmbedding
from utils.result import Result


T = TypeVar("T", bound=BaseModel)

class MockLlmApi(LlmEmbedder, LlmJsonQuerier):
    def __init__(self) -> None:
        pass

    def json_query(self, context: str, query: str, expected_schema: Type[T]) -> Result[T, str]:
        if config.inspect_query():
            self._inspect_query(query, context)

        example_data = generate_example_from_schema(expected_schema.model_json_schema())
        try:
            parsed = expected_schema(**example_data)  # Instantiate the Pydantic model
            if config.inspect_query():
                self._inspect_response(parsed)

            return Result.new_ok(parsed)
        except Exception as e:
            return Result.new_err(f"Failed to create model: {e}")

    def embed_text(self, text: str) -> Embedding:
        return MockEmbedding()

    def embed_texts(self, texts: list[str]) -> list[Embedding]:
        return [self.embed_text(doc) for doc in texts]

    def _inspect_query(self, query: str, context: str):
        print("="*60)
        print("="*60)
        print(f"Querying LLM:")
        print("-"*60)
        print(f"Context:\n")
        print(context)
        print("-"*60)
        print(f"Query:\n")
        print(query)
        input()

    def _inspect_response(self, response: BaseModel):
            print("-"*60)
            print("Reponse:\n")
            print(response.model_dump_json(indent=2))
            input()

def generate_example_from_schema(schema: dict) -> dict:
    """
    Generate a single example JSON object from a JSON Schema.
    Assumes each property has an 'examples' list and uses the first one.
    """
    example = {}
    for prop, details in schema.get("properties", {}).items():
        examples = details.get("examples")
        if examples and isinstance(examples, list):
            example.__setitem__(prop, examples[0])
        else:
            raise ValueError(f"Missing or invalid 'examples' for property: {prop}")
    return example

import os
from typing import Type, TypeVar
import fireworks.client
from dotenv import load_dotenv
from openai import OpenAI, responses
from pydantic import BaseModel
import numpy as np
import time

import config

from dataset_builder.interactor.dependencies.doc_embedder import Embedder
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import JsonGenerator
from dataset_builder.interactor.dependencies.embedded_document import Embedding
from fireworks_api.fireworks_embedding import FireworksEmbedding
from utils.result import Result

T = TypeVar("T", bound=BaseModel)

models = [
    'accounts/fireworks/models/llama4-scout-instruct-basic', # $0.15 input, $0.60 output
    'accounts/fireworks/models/qwen3-30b-a3b', # $0.22 input, $0.60 output
    'accounts/fireworks/models/qwen3-235b-a22b', # $0.22 input, $0.88 output 
    'accounts/fireworks/models/deepseek-r1' # $3.00 input, $8.00 output
]

class FireworksApi(Embedder, JsonGenerator):
    def __init__(self):
        dotenv_path = '../env/.env'

        load_dotenv(dotenv_path)
        fireworks_api_key = os.getenv("FIREWORKS_API_KEY")

        if not fireworks_api_key:
            raise ValueError("No API key found in the .env file. Please add your FIREWORKS_API_KEY to the .env file.")

        fireworks.client.api_key = fireworks_api_key
        self.fireworks_api_key = fireworks_api_key

    def json_query(self, context: str, query: str, expected_schema: Type[T]) -> Result[T, str]:
        if config.inspect_query():
            print("="*60)
            print(context)
            print("-"*60)
            print(query)
            input()

        client = fireworks.client.Fireworks(api_key=self.fireworks_api_key)
        try:
            response = client.chat.completions.create(
                model=models[0],
                response_format={"type": "json_object", "schema": expected_schema.model_json_schema()},
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": query}
                ],
                temperature=0.2,
            )
            print("Waiting 5 seconds...")
            time.sleep(5)
            print("Wait is up")
            response = response.choices[0].message.content
            if config.inspect_query():
                print("-"*60)
                print(response)
                print("="*60)
                input()
            response = expected_schema.model_validate_json(response)
            return Result.new_ok(response)
        except Exception as e:
            return Result.new_err("Fireworks api: " + str(e))

    def embed_texts(self, texts: list[str]) -> list[Embedding]:
        client = OpenAI(
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=self.fireworks_api_key
        )

        answ = []
        for text in texts:
            vector = client.embeddings.create(
                model="nomic-ai/nomic-embed-text-v1.5",
                input=text
            ).data[0].embedding
            print("Waiting 5 seconds...")
            time.sleep(5)
            print("Wait is up")
            embedding = FireworksEmbedding(np.array(vector))
            answ += [embedding]

        return answ

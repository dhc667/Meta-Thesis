from enum import Enum


class ExtractorError(Enum):
    BadLlmOutput = "Llm bad output"
    NoTopicsFound = "No topics found"

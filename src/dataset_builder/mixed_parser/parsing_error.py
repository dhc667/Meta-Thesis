from enum import Enum


class ParsingError(Enum):
    AbstractNotFound = "Abstract not found"
    BadLlmOutput = "Llm bad output"
    NoFirstPage = "No first page"

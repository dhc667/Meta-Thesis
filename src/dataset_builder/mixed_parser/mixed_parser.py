from enum import Enum
from typing import Any, TypeVar
from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.dataset_reader.dependencies.doc_parser import DocumentParser, ParsingError as InterfaceParsingErrror
from dataset_builder.dataset_reader.dependencies.document import Document
from dataset_builder.mixed_parser.algorithmic_parser.algorithmic_parser import AlgorithmicParser
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import LlmJsonQuerier
from dataset_builder.mixed_parser.llm_parser.parser import LlmParser
from dataset_builder.mixed_parser.parsing_error import ParsingError
from utils.result import Result


class MixedParser(DocumentParser):
    def __init__(self, llm_api: LlmJsonQuerier) -> None:
        self.llm_api = llm_api

    def parse_documents(self, buffers: list[DocumentBuffer]) -> list[Result[Document, InterfaceParsingErrror]]:
        answ = []
        for buffer in buffers:
            llm_parser = LlmParser(self.llm_api, buffer)

            title = llm_parser.parse_title()
            authors = llm_parser.parse_authors()
            tutors = llm_parser.parse_tutors()
            date = llm_parser.parse_date()
            abstract = llm_parser.parse_abstract()

            full_text = AlgorithmicParser(buffer).parse_full_text()

            err = return_first_error([title, authors, tutors, date, abstract])
            if err:
                if err == ParsingError.NoFirstPage:
                    answ += [Result.new_err(InterfaceParsingErrror.EmptyDocument)]
                elif err == ParsingError.BadLlmOutput or err == ParsingError.AbstractNotFound:
                    answ += [Result.new_err(InterfaceParsingErrror.CouldNotParse)]
            else:
                title = title.unwrap()
                authors = authors.unwrap()
                tutors = tutors.unwrap()
                date = date.unwrap()
                abstract = abstract.unwrap()

                answ += [Result.new_ok(Document(title, abstract, authors, tutors, date, full_text))]

        return answ


E = TypeVar("E")

def return_first_error(results: list[Result[Any, E]]) -> E | None:
    for r in results:
        if r.is_err():
            return r.unwrap_err()

    return None


from typing import Iterator
from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import LlmJsonQuerier
from dataset_builder.mixed_parser.llm_parser.prompts.find_abstract import FIND_ABSTRACT_CONTEXT, FIND_ABSTRACT_QUERY, OutputSchema as FindAbstractOutput
from dataset_builder.mixed_parser.llm_parser.prompts.get_metadata import FIND_THESIS_METADATA_CONTEXT, FIND_THESIS_METADATA_QUERY, OutputSchema as FindMetadataOuput
from dataset_builder.mixed_parser.parsing_error import ParsingError
from utils.partial_date import PartialDate
from utils.result import Result


class LlmParser:
    def __init__(self, llm_api: LlmJsonQuerier, buffer: DocumentBuffer) -> None:
        self.llm_api = llm_api
        self.buffer = buffer
        self.metadata: Result[FindMetadataOuput, ParsingError] | None = None

    def parse_abstract(self) -> Result[str, ParsingError]:
        """Parses metadata from the first page of the thesis, caches the result, returns the abstract"""
        for possible_abstract in self._get_possible_abstracts():
            answ = self.llm_api.json_query(FIND_ABSTRACT_CONTEXT(), FIND_ABSTRACT_QUERY(possible_abstract), FindAbstractOutput)

            if answ.is_err():
                print(answ.unwrap_err())
                return Result.new_err(ParsingError.BadLlmOutput)

            answ = answ.unwrap()
            if answ.is_abstract:
                return Result.new_ok(answ.abstract)

        return Result.new_err(ParsingError.AbstractNotFound)

    def parse_tutors(self) -> Result[list[str], ParsingError]:
        """Parses metadata from the first page of the thesis, caches the result, returns the tutors"""
        if self.metadata != None:
            if self.metadata.is_err():
                return Result.new_err(self.metadata.unwrap_err())
            return Result.new_ok(self.metadata.unwrap().tutors)
        
        self._fill_metadata()

        return self.parse_tutors()

    def parse_authors(self) -> Result[list[str], ParsingError]:
        """Parses metadata from the first page of the thesis, caches the result, returns the authors"""
        if self.metadata != None:
            if self.metadata.is_err():
                return Result.new_err(self.metadata.unwrap_err())
            return Result.new_ok(self.metadata.unwrap().authors)
        
        self._fill_metadata()

        return self.parse_authors()


    def parse_title(self) -> Result[str, ParsingError]:
        """Parses metadata from the first page of the thesis, caches the result, returns the title"""
        if self.metadata != None:
            if self.metadata.is_err():
                return Result.new_err(self.metadata.unwrap_err())
            return Result.new_ok(self.metadata.unwrap().title)
        
        self._fill_metadata()

        return self.parse_title()

    def parse_date(self) -> Result[PartialDate, ParsingError]:
        """Parses metadata from the first page of the thesis, caches the result, returns the date"""
        if self.metadata != None:
            if self.metadata.is_err():
                return Result.new_err(self.metadata.unwrap_err())

            date = self.metadata.unwrap().date

            year = date[0]
            month = date[1] if len(date) > 1 else None
            day = date[2] if len(date) > 2 else None

            date = PartialDate(year, month, day)

            return Result.new_ok(date)
        
        self._fill_metadata()

        return self.parse_date()

    def _fill_metadata(self) -> None:
        first_page = self.buffer.get_page(0)
        if first_page == None:
            self.metadata = Result.new_err(ParsingError.NoFirstPage)
            return

        answ = self.llm_api.json_query(FIND_THESIS_METADATA_CONTEXT(), FIND_THESIS_METADATA_QUERY(first_page), FindMetadataOuput)

        if answ.is_err():
            print(answ.unwrap_err())
            self.metadata = Result.new_err(ParsingError.BadLlmOutput)

        self.metadata = Result.new_ok(answ.unwrap())

    def _get_possible_abstracts(self) -> Iterator[str]:
        pages_lower = []

        for text in self.buffer.get_pages():
            pages_lower += [text.lower()]
            page_lower = pages_lower[-1]

            if page_lower.__contains__("resumen") or page_lower.__contains__("abstract"):
                yield text

        for i, text in enumerate(self.buffer.get_pages()):
            page_lower = pages_lower[i]

            if page_lower.__contains__("introducci") or page_lower.__contains__("introduction"):
                yield text


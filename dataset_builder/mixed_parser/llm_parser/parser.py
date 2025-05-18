from dataset_builder.dataset_reader.dependencies.doc_buffer import DocumentBuffer
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import LlmApi


class LlmParser:
    def __init__(self, llm_api: LlmApi, buffer: DocumentBuffer) -> None:
        self.llm_api = llm_api
        self.buffer = buffer
        raise NotImplementedError()

    def parse_abstract(self) -> str:
        raise NotImplementedError()

    def parse_tutors(self) -> list[str]:
        """Parses tutors from the first page of the thesis, caches the result, 
        also parses authors and caches the result if that cache is empty"""
        raise NotImplementedError()

    def parse_auhors(self) -> str:
        """Parses authors from the first page of the thesis, caches the result, 
        also parses tutors and caches the result if that cache is empty"""
        raise NotImplementedError()


    def _get_possible_abstracts(self) -> list[str] | None:
        possible_abstracts = []
        possible_introductions = []

        page_texts = [page for page in self.buffer.get_pages()]

        for text, next_text in zip(page_texts[:-1], page_texts[1:]):
            textlower = text.lower()
            if textlower.__contains__("resumen") or textlower.__contains__("abstract"):
                possible_abstracts += [text + "\n" + next_text]
            if textlower.__contains__("introducci"):
                possible_introductions += [text + "\n" + next_text]

        if len(possible_abstracts) > 0:
            return possible_abstracts
        if len(possible_introductions) > 0:
            return possible_introductions
        else: return None





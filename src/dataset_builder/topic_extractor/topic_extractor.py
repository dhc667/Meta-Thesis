from dataset_builder.topic_extractor.prompts.extract_keywords import FIND_KEYWORDS_CONTEXT, FIND_KEYWORDS_QUERY, OutputSchema as FindTopicsOutput
from dataset_builder.mixed_parser.llm_parser.depedencies.llm_api import JsonGenerator
from dataset_builder.interactor.dependencies.topic_extractor import ExtractorError, TopicExtractor
from dataset_builder.interactor.dependencies.read_document import ReadDocument
from utils.result import Result

class LlmExtractor(TopicExtractor):
    def __init__(self, llm_api: JsonGenerator):
        self.llm_api = llm_api

    def extract_topic(self, doc: ReadDocument) -> Result[str, ExtractorError]:
        result = self.llm_api.json_query(FIND_KEYWORDS_CONTEXT(), FIND_KEYWORDS_QUERY(doc.abstract), FindTopicsOutput)

        if result.is_err():
            print(result.unwrap_err())
            return Result.new_err(ExtractorError.BadLlmOutput)

        result = result.unwrap()
        if result.topics:
            return Result.new_ok(','.join(result.topics))

        return Result.new_err(ExtractorError.NoTopicsFound)

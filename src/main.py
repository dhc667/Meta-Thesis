from pathlib import Path

from dataset_builder.dataset_reader.dataset_reader import PdfDatasetReader
from dataset_builder.interactor.interactor import Interactor
from dataset_builder.mixed_parser.mixed_parser import MixedParser
from dataset_builder.pypdf_reader.pypdf_reader import PypdfReader
from sqlite_repository.sqlite_repository import SQLiteDocumentRepository
import config
from fireworks_api.fireworks_api import FireworksApi
from dataset_builder.topic_extractor.topic_extractor import LlmExtractor

def index():
    llm_api = FireworksApi()
    mixed_parser = MixedParser(llm_api)
    topic_extractor = LlmExtractor(llm_api)
    pdf_reader = PypdfReader()
    dataset_reader = PdfDatasetReader(pdf_reader, mixed_parser)
    repository = SQLiteDocumentRepository(Path("./db"))
    interactor = Interactor(dataset_reader, repository, llm_api, topic_extractor)
    interactor.build_dataset(Path("../theses/"))

def main():
    config.init()

    args = config.get_args()

    if args.index:
        index()

if __name__ == "__main__":
    main()

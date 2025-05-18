import argparse
from pathlib import Path

from dataset_builder.dataset_reader.dataset_reader import PdfDatasetReader
from dataset_builder.interactor.interactor import Interactor
from dataset_builder.mixed_parser.mixed_parser import MixedParser
from dataset_builder.pypdf_reader.pypdf_reader import PypdfReader
from dataset_builder.sqlite_repository.sqlite_repository import SQLiteDocumentRepository
from llm_apis.mock_api import MockLlmApi

def index():
    llm_api = MockLlmApi()
    mixed_parser = MixedParser(llm_api)
    pdf_reader = PypdfReader()
    dataset_reader = PdfDatasetReader(pdf_reader, mixed_parser)
    repository = SQLiteDocumentRepository(Path("./db"))
    interactor = Interactor(dataset_reader, repository, llm_api)

    interactor.build_dataset(Path("../theses/"))

def analyze():
    print("Running analysis...")

def main():
    parser = argparse.ArgumentParser(description="Document analysis pipeline")
    parser.add_argument('--index', action='store_true', help='Run the indexing step')
    parser.add_argument('--analyze', action='store_true', help='Run the analysis step')

    args = parser.parse_args()

    if args.index:
        index()
    if args.analyze:
        analyze()

if __name__ == "__main__":
    main()

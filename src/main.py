from pathlib import Path

from dataset_builder.dataset_reader.dataset_reader import PdfDatasetReader
from dataset_builder.interactor.interactor import Interactor
from dataset_builder.mixed_parser.mixed_parser import MixedParser
from dataset_builder.pypdf_reader.pypdf_reader import PypdfReader
from sqlite_repository.sqlite_repository import SQLiteDocumentRepository
import config
from fireworks_api.fireworks_api import FireworksApi
from dataset_builder.topic_extractor.topic_extractor import LlmExtractor
from presenter import StreamlitPresenter
from topic_summarizer import SpacyTokenizer
from fireworks_api.fireworks_embedding import FireworksEmbedding
from presenter.interfaces import JsonGenerator, Tokenizer, DocumentRepository

def index(args):
    """Run the indexing process."""
    llm_api = FireworksApi()
    mixed_parser = MixedParser(llm_api)
    topic_extractor = LlmExtractor(llm_api)
    pdf_reader = PypdfReader()
    dataset_reader = PdfDatasetReader(pdf_reader, mixed_parser)
    repository = SQLiteDocumentRepository(Path("./db"))
    interactor = Interactor(dataset_reader, repository, llm_api, topic_extractor)
    interactor.build_dataset(Path("../theses/"))

def present(args):
    """Run the visualization presenter."""
    # Initialize dependencies
    repository: DocumentRepository = SQLiteDocumentRepository(Path("./db"))
    json_generator: JsonGenerator = FireworksApi()
    tokenizer: Tokenizer = SpacyTokenizer()
    
    # Create and run presenter
    presenter = StreamlitPresenter(repository, json_generator, tokenizer)
    presenter.run(
        embedding_type=FireworksEmbedding,
    )

def main():
    # Initialize configuration
    config.init()
    
    # Get parsed arguments
    args = config.get_args()
    
    # Execute the appropriate command
    if args.command == 'index':
        index(args)
    elif args.command == 'present':
        present(args)
    else:
        print("Please specify a command (index or present)")
        print("Use --help for more information")

if __name__ == "__main__":
    main()

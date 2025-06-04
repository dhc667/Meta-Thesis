import argparse

_args = None

def init():
    global _args
    if _args is None:
        parser = argparse.ArgumentParser(description="Document analysis pipeline")
        subparsers = parser.add_subparsers(dest='command', help='Command to run')
        
        # Index command
        index_parser = subparsers.add_parser('index', help='Run the indexing step')
        index_parser.add_argument('--inspect-query', action='store_true', help='Inspect LLM queries one by one')
        
        # Present command
        present_parser = subparsers.add_parser('present', help='Run the visualization presenter')
        present_parser.add_argument('--inspect-query', action='store_true', help='Inspect LLM queries and responses')
        
        _args = parser.parse_args()

def get_args():
    if _args is None:
        raise RuntimeError("Config not initialized. Call config.init() first.")
    return _args

# def get_verbose():
#     if _args is None:
#         raise RuntimeError("Config not initialized. Call config.init() first.")
#     return _args.verbose

def inspect_query():
    if _args is None:
        raise RuntimeError("Config not initialized. Call config.init() first.")
    return _args.inspect_query



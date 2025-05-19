import argparse

_args = None

def init():
    global _args
    if _args is None:
        parser = argparse.ArgumentParser(description="Document analysis pipeline")
        parser.add_argument('-i', '--index', action='store_true', help='Run the indexing step')
        parser.add_argument('-a', '--analyze', action='store_true', help='Run the analysis step')
        # parser.add_argument('-v', '--verbose', action='store_true', help='Increase logging')
        parser.add_argument('--inspect-query', action='store_true', help='Inspect llm queries one by one')
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



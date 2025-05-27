from inspect import currentframe
from openai import BaseModel
from pydantic import Field


class OutputSchema(BaseModel):
    relevance_reasoning: str = Field(examples=["The text in this page is relevant to the paper summary because it contains a paragraph that speaks about the methods used to complete the proposed work"])
    relevance: bool
    updated_summary: str = Field(examples=["", "En este trabajo nos proponemos..."])
    summary_sufficient_reasoning: str
    is_summary_sufficient: bool

def GENERATE_ABSTRACT_CONTEXT() -> str:
    return """
You are an expert thesis paper summarizer, and are reading a paper page by page in order to construct its abstract

Your task is to:
1. Decide whether this page contributes relevant information to the abstract. Relevant content includes the research motivation, goals, methodology, results, or conclusions.
2. If it is relevant, update the current summary with new key details from this page.
3. Determine whether the summary is now sufficient to serve as the abstract.

Respond in the following JSON format:

{
  "relevance_reasoning": Explain why the page is or isn't relevant to the abstract.
  "relevance": true || false
  "updated_summary": An updated summary if the text was relevant, "" if not
  "summary_sufficient_reasoning": If the summary is sufficient, explain why the abstract is likely complete. If No, explain what is still missing (e.g., results, conclusion, methodology).
  "is_summary_sufficient": true | false
}
"""

def GENERATE_ABSTRACT_QUERY(page_number: int, total_pages: int, current_summary: str, page_text: str) -> str:
    return f"""
You are currently on Page {page_number}/{total_pages}. So far, your summary is "{current_summary}".

Current Page:

{page_text}
"""


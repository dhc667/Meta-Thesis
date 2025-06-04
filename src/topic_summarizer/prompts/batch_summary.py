"""Prompts to analyze a batch of abstracts and identify common themes and topics"""

from pydantic import BaseModel, Field

class BatchSummaryResponse(BaseModel):
    topic_description: str = Field(
        examples=[
            "The documents explore various applications of machine learning in healthcare, focusing on early disease detection, patient monitoring, and treatment optimization. Common methodologies include deep learning for medical imaging and predictive analytics for patient outcomes.",
            "These works examine urban sustainability initiatives, emphasizing green infrastructure development, public transportation optimization, and community engagement in city planning. Key themes include environmental impact reduction and quality of life improvement."
        ],
        description="A detailed description of the common themes, methodologies, and findings across the documents"
    )
    topic_title: str = Field(
        examples=[
            "Machine Learning Applications in Healthcare",
            "Sustainable Urban Development Strategies"
        ],
        description="A concise title that captures the main theme across the documents"
    )

CONTEXT_PROMPT = """
-- Role --

You are an expert academic analyst specializing in identifying common themes and patterns across research documents.

-- Task --

Your task is to analyze a set of academic abstracts and identify the main themes that connect them. You should:
1. Identify common research areas, methodologies, and findings
2. Synthesize these into a coherent topic title and description
3. Focus on substantive connections rather than superficial similarities

-- Output Format --

Provide a JSON response in English with:
- "topic_description": A detailed description of common themes, methodologies, and findings
- "topic_title": A concise, specific title that captures the main theme

-- Guidelines --

- All output must be in English
- The description should highlight both theoretical and methodological connections
- The title should be specific and informative, not generic
- Focus on significant patterns that appear across multiple documents
- Include both high-level themes and specific shared elements
"""

def BATCH_SUMMARY_CONTEXT() -> str:
    """Returns the context for batch summarization"""
    return CONTEXT_PROMPT

def BATCH_SUMMARY_QUERY(abstracts: str) -> str:
    """Returns the query for batch summarization"""
    return f"""
### Analyze These Abstracts ###

{abstracts}

Identify and summarize the common themes across these documents. Provide your response in English.
""" 
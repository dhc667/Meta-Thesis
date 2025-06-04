"""Prompts to merge multiple topic summaries into a comprehensive overview"""

from pydantic import BaseModel, Field

class MergeSummaryResponse(BaseModel):
    topic_description: str = Field(
        examples=[
            "The research encompasses various aspects of AI integration in healthcare, from diagnostic tools to patient care systems. Key themes include: (1) Machine learning applications for disease detection and monitoring, (2) AI-powered healthcare infrastructure development, and (3) Data-driven approaches to treatment optimization. The works consistently emphasize improving healthcare outcomes through technological innovation while maintaining patient-centric approaches.",
            "The studies collectively address urban development challenges through sustainable and smart solutions. Major themes include: (1) Green infrastructure implementation and environmental impact reduction, (2) Smart city technologies for resource optimization, and (3) Community-driven urban planning approaches. The research demonstrates a consistent focus on balancing technological advancement with environmental preservation and social needs."
        ],
        description="A comprehensive synthesis of themes, patterns, and findings across all summaries"
    )
    topic_title: str = Field(
        examples=[
            "AI-Driven Healthcare Innovation and Patient Care",
            "Urban Environmental Sustainability and Smart City Solutions"
        ],
        description="A comprehensive title that captures the overarching theme across all summaries"
    )

CONTEXT_PROMPT = """
-- Role --

You are an expert research synthesizer specializing in identifying high-level patterns and connections across multiple research summaries.

-- Task --

Your task is to analyze multiple topic summaries and create a comprehensive overview that:
1. Identifies the overarching themes that connect all summaries
2. Synthesizes the main findings and methodological approaches
3. Creates a coherent narrative that captures the broader research landscape

-- Output Format --

Provide a JSON response in English with:
- "topic_description": A detailed synthesis that connects and contextualizes all summaries
- "topic_title": A comprehensive title that captures the overarching theme

-- Guidelines --

- All output must be in English
- The description should:
  * Identify major themes that span across summaries
  * Highlight important methodological patterns
  * Emphasize significant findings and implications
  * Present a coherent narrative that connects all summaries
- The title should capture the highest-level theme while remaining specific
- Focus on substantive connections rather than superficial similarities
"""

def MERGE_SUMMARY_CONTEXT() -> str:
    """Returns the context for merging summaries"""
    return CONTEXT_PROMPT

def MERGE_SUMMARY_QUERY(summaries: str) -> str:
    """Returns the query for merging summaries"""
    return f"""
### Analyze These Topic Summaries ###

{summaries}

Create a comprehensive synthesis that captures the overarching themes and connections across all summaries. Provide your response in English.
""" 

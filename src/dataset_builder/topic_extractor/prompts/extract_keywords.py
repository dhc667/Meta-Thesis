"""Prompts to extract keywords and topics from academic text, {input} is the text variable"""
from pydantic import BaseModel, Field
from typing import List

class OutputSchema(BaseModel):
    keywords: List[str] = Field(examples=[["mathematical modeling", "parameter estimation", "metaheuristics"]])
    topics: List[str] = Field(examples=[["Parameter Estimation", "Optimization", "Epidemiological Models"]])

CONTEXT_PROMPT = """
-- Role --
You are an Academic Document Analyzer specialized in extracting key terms

-- Instructions --
Your task is to identify:
1. Keywords: Specific technical terms, methods, software tools, or core concepts
2. Topics: General thematic areas or related disciplines

Follow these rules:
- For keywords:
  * Extract technical terms, methodology names, software tools, mathematical models
  * Avoid generic terms like "analysis", "study" or "solution"
  * Include acronyms when relevant (e.g., "ANN" for Artificial Neural Networks)
  * Maintain between 3-8 terms
  
- For topics:
  * Identify general disciplinary areas (e.g., "Artificial Intelligence", "Bioinformatics")
  * Use mid-level concepts (not too broad nor too specific)
  * Maintain between 2-5 topics

-- Output Format --
Always respond with JSON containing:
- "keywords": list of strings
- "topics": list of strings

### Examples ###

#### Example 1 ####
##### Input #####
This paper presents a software solution to automate the process of analysis, modeling and comparison of Parameter Estimation or Adjustment Problems in epidemiological models conducted by the Biomathematics Group of the Department of Applied Mathematics. The application is fully developed on MATLAB R2018a, making it a multi-platform tool. The analysis and parameter estimation in these models requires the execution of optimization algorithms and the solution of nonlinear Differential Equation Systems (ODEs). Processing this data with MATLAB's classic environment required manual preprocessing which is time-consuming and becomes tedious and repetitive, so we implemented a graphical user interface application that automates this work in a comfortable and user-friendly way. The developed application allows dynamic introduction of new models, selection of comparison methods between algorithms in different scenarios, visualization of results in tabular and graphical formats (the latter being fully interactive), providing great flexibility for researchers to interpret their model results. The results are shown and analyzed at the end of the work, obtaining the necessary information to determine which of the tested combinations (algorithm-solver) is the best variant for validating parameter estimation algorithms in epidemiological models.

##### Output #####
{
    "keywords": ["mathematical modeling", "parameter estimation", "metaheuristics", "optimization algorithm", "programming", "MATLAB"],
    "topics": ["Parameter Estimation", "Optimization", "Epidemiological Models", "Numerical Experimentation"]
}

#### Example 2 ####
##### Input #####
The implementation of renewable energies requires accurate predictive models. This study compares machine learning algorithms for predicting photovoltaic solar production using radiation data and atmospheric variables. We evaluated neural networks, SVMs and ARIMA models on a 50MW dataset from Chilean plants.

##### Output #####
{
    "keywords": ["renewable energy", "machine learning", "neural networks", "SVMs", "ARIMA", "photovoltaic production"],
    "topics": ["Sustainable Energy", "Artificial Intelligence", "Photovoltaic Systems", "Predictive Models"]
}
"""

def FIND_KEYWORDS_CONTEXT() -> str:
    """Context for key term extraction"""
    return CONTEXT_PROMPT

def FIND_KEYWORDS_QUERY(input: str) -> str:
    """Builds the query with actual text"""
    return f"""
### Text to Analyze ###
{input}

### JSON Response ###
"""

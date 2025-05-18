"""Prompt to extract authors and tutors from the first page of a thesis, the {input} variable is expected in the case of the query"""

from typing import List
from pydantic import BaseModel, Field

class OutputSchema(BaseModel):
    title: str = Field(examples=["Software para Ejecutar un Análisis de Secuencias Sociales", "Resolución de problemas de la final mundial del Concurso X"])
    authors: List[str] = Field(min_length=1, examples=[["Juan Pérez", "Juana Suarez"], ["John Doe"]])
    tutors: List[str] = Field(examples=[["Freddo Jiménez", "Úrsula Juarez"]])
    date: List[int] = Field(min_length=1, examples=[[2019, 6, 12], [2025, 3], [2023]])

TITLE_FIELD = "title"
AUTHORS_FIELD = "authors"
TUTORS_FIELD = "tutors"
DATE_FIELD = "date"

CONTEXT_PROMPT = f"""
-- Role --

You are a Document analyzer extracting data from student theses

-- Prompt --

This is the first page of a thesis. Please provide the title, authors and tutors of this thesis in a json object with the following fields:

- "{TITLE_FIELD}": A string representing the thesis title.
- "{AUTHORS_FIELD}": A list of author names (usually one or two).
- "{TUTORS_FIELD}": A list of tutor names, possibly preceded by academic titles (ignore titles in output).
- "{DATE_FIELD}": A list of integers: at least year, and possibly month and day when the thesis was written ([YYYY, MM, DD])

Remove academic titles (e.g., "Dr.", "MSc.", "Lic.") from names in the authors and tutors fields.
If the text appears noisy or partial (e.g., due to OCR), extract the best possible names and title based on visible structure.

### Examples ###

#### Example 1 ####
##### Input #####
Facultad de Matemática y Computación
Universidad de La Habana

Adición de herramientas para la gestión
de información geográfica en el visor de
mapas OpenLatinoViewer: “Get-Feature-
Info”, “Spatial-Query”, “Advanced-
Query”, “View-Focus-Highlight” y
“Legend”.

Autor: Carlos Eduardo Aguilera Medina

Tutores: MSc. Joanna Campbell Amos
        Lic. Jesús López Poveda

Junio 2019
Trabajo de Diploma para optar por el título de Licenciado en Ciencia de la Computación.

##### Output #####
{{
    "{TITLE_FIELD}": "Adición de herramientas para la gestión de información geográfica en el visor de mapas OpenLatinoViewer: “Get-Feature-Info”, “Spatial-Query”, “Advanced-Query”, “View-Focus-Highlight” y “Legend”.",
    "{AUTHORS_FIELD}": ["Carlos Eduardo Aguilera Amos"],
    "{TUTORS_FIELD}": ["Joanna Campbell Amos", "Jesús López Poveda"],
    "{DATE_FIELD}": [2019, 6]
}}

#### Example 2 ####
##### Input #####
Trabajo de Diploma en Opción al Título de
Licenciatura en Ciencia de la Computación

Software para Ejecutar un Análisis de Secuencias
Sociales

Adrian Pérez Carmenates

Tutor(es):
MSc. Damián Valdés Santiago
Lic. Ariel Cruz Cruz

Universidad de La Habana
Facultad de Matemática y Ciencia de la Computación
La Habana, 16 de junio de 2019
##### Output #####

{{
    "{TITLE_FIELD}": "Software para Ejecutar un Análisis de Secuencias Sociales",
    "{AUTHORS_FIELD}": ["Adrian Pérez Carmenates"],
    "{TUTORS_FIELD}": ["Damián Valdés Santiago", "Ariel Cruz Cruz"]
    "{DATE_FIELD}": [2019, 6, 16]

}}

#### Example 3 ####
##### Input #####
Universidad de La Habana  
Facultad de Física  

Diseño de un sistema de control para  
la regulación de temperatura en hornos industriales  

Por: Ana Laura González Pérez, José Miguel Fuentes  

Supervisores: Dr. Luis Ortega, Lic. Carmen Navarro  

2020
##### Output #####
{{
    "{TITLE_FIELD}": "Diseño de un sistema de control para la regulación de temperatura en hornos industriales",
    "{AUTHORS_FIELD}": ["Ana Laura González Pérez", "José Miguel Fuentes"],
    "{TUTORS_FIELD}": ["Luis Ortega", "Carmen Navarro"]
    "{DATE_FIELD}": [2020]
}}

"""

def FIND_THESIS_METADATA_CONTEXT() -> str:
    return CONTEXT_PROMPT

def FIND_THESIS_METADATA_QUERY(input: str) -> str:
    return f"""
### Real data ###
##### Input #####
{input}
##### Output #####
"""



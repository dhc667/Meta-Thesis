"""Prompt to extract authors and tutors from the first page of a thesis, the {input} variable is expected"""

AUTHOR_TUTOR_PROMPT = """

-- Role --

You are a Document analyzer extracting data from student theses

-- Prompt --

This is the first page of a thesis. Please provide the title, authors and tutors of this thesis in a json object with the following fields:

- "title": A string representing the thesis title.
- "authors": A list of author names (usually one or two).
- "tutors": A list of tutor names, possibly preceded by academic titles (ignore titles in output).

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
{
    "title": "Adición de herramientas para la gestión de información geográfica en el visor de mapas OpenLatinoViewer: “Get-Feature-Info”, “Spatial-Query”, “Advanced-Query”, “View-Focus-Highlight” y “Legend”.",
    "authors": ["Carlos Eduardo Aguilera Amos"],
    "tutors": ["Joanna Campbell Amos", "Jesús López Poveda"],
}

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
La Habana, junio 2019
##### Output #####

{
    "title": "Software para Ejecutar un Análisis de Secuencias Sociales",
    "authors": ["Adrian Pérez Carmenates"],
    "tutors": ["Damián Valdés Santiago", "Ariel Cruz Cruz"]

}

#### Example 3 ####
##### Input #####
Universidad de La Habana  
Facultad de Física  

Diseño de un sistema de control para  
la regulación de temperatura en hornos industriales  

Por: Ana Laura González Pérez, José Miguel Fuentes  

Supervisores: Dr. Luis Ortega, Lic. Carmen Navarro  

Junio 2020

##### Output #####
{
    "title": "Diseño de un sistema de control para la regulación de temperatura en hornos industriales",
    "authors": ["Ana Laura González Pérez", "José Miguel Fuentes"],
    "tutors": ["Luis Ortega", "Carmen Navarro"]
}

### Real data ###
##### Input #####
{input}
##### Output #####
"""

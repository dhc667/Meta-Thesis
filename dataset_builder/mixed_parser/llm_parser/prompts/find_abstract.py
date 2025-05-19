"""Prompt to find and extract the abstract of a paper, the {input} variable is expected"""

FIND_ABSTRACT_PROMPT = """

-- Role --

You are a Document analyzer extracting data from student theses

-- Prompt --

This is an early page of a thesis (within the first 10 pages). Your task is to determine whether the page contains the abstract of the thesis. The abstract is a summary that typically includes the research problem, methodology, and key findings.

Only return the abstract if the page contains a full paragraph or section that summarizes the whole thesis.

Determine if the text contains a substantive summary of the thesis (abstract). Use these rules:

- Accept if it describes the objective, method, and findings.
- Reject if it only includes a heading or table of contents.
- Reject if it only describes motivation or background.
- Reject if it only contains acknowledgements
- Reject if it only contains introductions that do not summarize the thesis entirely.

Your output must be a json object with the following fields:

- "is_abstract": true or false, whether or not the page contains an abstract
- "content": "" if is_abstract is false, the text of the abstract without modifications

### Examples ###
#### Example 1 ####
##### Input #####
Resumen
El presente trabajo de diploma, propone dar continuidad  al desarro llo del visor
cartográfico para la web OpenLatinoViewer. Surge de la necesidad de extender este visor,
para incorporar nuevas herramientas que permitan mayor interacción con el sistema. Por
ejemplo, se propone la implementación de herramientas que permitan realizar consultas
espaciales y avanzadas y que además permita la visualización y procesamiento de los
resultados a dichas consultas.
Para lograr los objetivos propuestos, se realiza un estudio del estado del arte, para
conocer los distintos visores de mapas en la web. De esta forma se pueden obtener
ideas y patrones para adoptar en el desarrollo de OpenLatinoViewer. A partir de este
estudio y del análisis de "OpenLatinoViewer" se propone una abstracción de solución al
problema que luego sirve como base para la implementación de la misma.
Una vez implementadas las herramientas requeridas, se realizan una serie de pruebas
para comprobar el correcto funcionamiento de las mismas. De esta forma se obtiene un
software de calidad, que cumple con los requerimientos establecidos y sirve de utilidad
para los usuarios y programadores que lo usarán en el futuro.

##### Output #####
{
    "is_abstract": true,
    "content": "El presente trabajo de diploma, propone dar continuidad  al desarro llo del visor
cartográfico para la web \\"OpenLatinoViewer\\". Surge de la necesidad de extender este visor,
para incorporar nuevas herramientas que permitan mayor interacción con el sistema. Por
ejemplo, se propone la implementación de herramientas que permitan realizar consultas
espaciales y avanzadas y que además permita la visualización y procesamiento de los
resultados a dichas consultas.
Para lograr los objetivos propuestos, se realiza un estudio del estado del arte, para
conocer los distintos visores de mapas en la web. De esta forma se pueden obtener
ideas y patrones para adoptar en el desarrollo de OpenLatinoViewer. A partir de este
estudio y del análisis de OpenLatinoViewer se propone una abstracción de solución al
problema que luego sirve como base para la implementación de la misma.
Una vez implementadas las herramientas requeridas, se realizan una serie de pruebas
para comprobar el correcto funcionamiento de las mismas. De esta forma se obtiene un
software de calidad, que cumple con los requerimientos establecidos y sirve de utilidad
para los usuarios y programadores que lo usarán en el futuro."
}

#### Exmple 2 ####
##### Input #####

Índice
Opinión del tutor: ........................................................................................................................................ 3
Agradecimientos: ........................................................................................................................................ 4
Resumen ....................................................................................................................................................... 5
Índice ............................................................................................................................................................. 6
Índice de Figuras ........................................................................................................................................... 8
Índice de Tablas ............................................................................................................................................ 9
Capítulo 1: Introducción ............................................................................................................................. 10
Objeto de Estudio. .................................................................................................................................. 11
Motivación y Justificación. ...................................................................................................................... 12
Problema ................................................................................................................................................. 13
Objetivos Generales ................................................................................................................................ 13
Objetivos Específicos............................................................................................................................... 13
Estructura del Trabajo. ............................................................................................................................ 14
Capítulo 2: Estado del Arte ......................................................................................................................... 15
OSM Viewer ............................................................................................................................................ 15
Abbotsford Map Viewer: ........................................................................................................................ 16
OpenLayers Search Viewer with GeoJSON graphic index: ...................................................................... 18
Conclusiones ........................................................................................................................................... 19
Capítulo 3: Solución Teórico-Conceptual-Computacional ............................................................................. 20
Arquitectura de las Herramientas implementadas ................................................................................. 21
Comunicación con el Servidor. ................................................................................................................ 23
Protocolos. .............................................................................................................................................. 24
##### Output #####

{
    "is_abstract": false,
    "content": ""
}

#### Example 3 ####
##### Input #####

Introducción
En la sociedad existen muchos problemas que requieren utilizar un con-
junto de vehículos para satisfacer, de manera óptima, las necesidades de un
conjunto de clientes. Ejemplos de estas situaciones son la distribución logís-
tica de una empresa para entregar mercancías, la recogida eﬁciente de un
grupo de alumnos para llevarlos a su centro de estudio o el recorrido de un
grupo de turistas por una ciudad, de forma que se pueda visitar la mayor
cantidad de lugares posibles. Este tipo de problemas se estudian bajo el
nombre genérico de Problema de Enrutamiento de Vehículos.
El problema de enrutamiento de vehículos (VRP , por sus siglas en in-
glés) es un problema de optimización combinatoria, que se deﬁne por un
conjunto o ﬂota de vehículos y un conjunto de clientes geográﬁcamente
dispersos.

##### Output #####

{
    "is_abstract": false,
    "content": ""
}

### Real Data ###
##### Input #####
{input}
##### Output #####


"""

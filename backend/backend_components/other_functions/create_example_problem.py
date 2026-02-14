"""
ES: Este script define una función que devuelve un problema ejemplo (Enunciado, Procedimiento, Respuesta Corta).

EN: This script defines a function that returns an example problem (Formulation, Procedure, Final Answer).
"""


import inspect


def create_example_problem() -> tuple[str, str, str]:
    """
    ES: Devuelve un problema ejemplo.

    EN: Returns an example problem .
    
    :return: Example problem with the structure (Formulation, Procedure, Short Solution).
    :rtype: tuple[str, str, str]
    """
    
    # cleandoc limpia los espacios de indentación
    # cleandoc cleans indentation spaces
    example_formulation = inspect.cleandoc(r"""
    \documentclass[12pt]{article}
    \usepackage[fontsize=14pt]{scrextend}
    \usepackage[utf8]{inputenc}
    \usepackage[spanish]{babel}
    \usepackage[papersize={500pt,650pt}, margin=1in]{geometry}

    \begin{document}

    \begin{center}
        \huge \textbf{Enunciado del Ejercicio} \\
        \large \textit{Problema Ejemplo para Epsilon OME Trainer}
    \end{center}

    \vspace{2cm}

    \noindent \textbf{Enunciado:} \\
    Este es un texto de ejemplo diseñado para probar las capacidades de renderizado del visor PDF.

    \vspace{1cm}

    \noindent El resultado es 10; prueba las distintas maneras de introducir la respuesta (10, 5+5, $\sqrt{100}$ , ...).

    \end{document}
    """
    )

    example_procedure = inspect.cleandoc(r"""
    \documentclass[12pt]{article}
    \usepackage[fontsize=14pt]{scrextend}
    \usepackage[utf8]{inputenc}
    \usepackage[spanish]{babel}
    \usepackage[papersize={500pt,650pt}, margin=1in]{geometry}

    \begin{document}

    \begin{center}
        \huge \textbf{Resolución del Ejercicio} \\
        \large \textit{Problema Ejemplo para Epsilon OME Trainer}
    \end{center}

    \vspace{1cm}

    \noindent \textbf{Enunciado:} \\
    Este es un texto de ejemplo diseñado para probar las capacidades de renderizado del visor PDF.

    \vspace{1cm}

    \noindent Puedes descargar este documento con el botón inferior.

    \end{document}
    """
    )
    
    short_solution = "10"
    
    problem = (example_formulation, example_procedure, short_solution)
    
    # el problema se devuelve como una tupla para que sea guardado con facilidad
    # the problem is returned as a tuple for it to be stored easily
    return problem 

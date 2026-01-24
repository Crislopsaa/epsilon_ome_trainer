"""
ES: Este script define una función que hace una comprobación rápida para evitar errores evidentes en el código LaTeX de los problemas que genera la IA.

EN: This script defines a function that performs a validation to avoid evident errors in the AI-generated problems' LaTeX code.
"""


def check_latex(latex_code: str):
    """
    ES: Hace una comprobación rápida para evitar errores evidentes en el código LaTeX de los problemas que genera la IA.

    EN: Performs a validation to avoid evident errors in the AI-generated problems' LaTeX code.
    
    Warning:
        ES: Si el código LaTeX no es válido, se lanza una ValueError.
        EN: If the LaTeX code is not valid, a ValueError is raised.
    
    :param latex_code: LaTeX code to check.
    :type latex_code: str
    """
    
    # comprobando si todos los comandos "begin" se corresponden con uno "end"
    # checking if all "begin" commands have an "end" one
    if latex_code.count(r"\begin{") != latex_code.count(r"\end{"):
        raise ValueError(r"[check_latex] ERROR: Los comandos \begin{ y \end{ no están parejos.")
    
    # comprobando si todos los modos de matemáticas se han cerrado
    # checking if all math modes have been closed
    if latex_code.count("$") % 2 != 0:
        raise ValueError(r"[check_latex] ERROR: Los comandos del modo de matemáticas ($) no están parejos.")
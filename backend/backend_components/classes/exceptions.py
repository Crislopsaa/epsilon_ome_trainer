"""
ES: Este script implementa excepciones personalizadas para mejorar el flujo y control de la aplicación.

EN: This script implements custom exceptions to improve the app's flow and control. 
"""


# AI-POWERED PROBLEM GENERATION

class GenerationStopException(Exception):
    """
    ES: Esta excepción indica que el usuario ha interrumpido la generación de problemas con IA antes de que esta termine.
    
    EN: This exception indicates that the user has interrupted the AI-powered problem generation before it finishes.
    """
    pass


class ProblemStructureError(Exception):
    """
    ES: Esta excepción indica que el problema generado por la IA no se ha dividido correctamente.
    
    EN: This exception indicates that the AI-generated problem has not been split successfully.
    """
    pass


class InvalidLaTeXError(Exception):
    """
    ES: Esta excepción indica que el código LaTeX generado por la IA contiene errores de sintaxis.
    
    EN: This exception indicates that the AI-generated LaTeX code contains syntax errors.
    """
    pass
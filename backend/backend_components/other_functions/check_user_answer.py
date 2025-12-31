"""
ES: Este script define una función que compara la respuesta del usuario con la correcta.\n
EN: This script defines a function that compares the user's answer to the correct one.
"""

import math
from sympy import simplify, SympifyError

# importando funciones personalizadas
# importing custom functions
from backend.backend_components.other_functions.safe_parse import safe_parse


def check_user_answer(correct_answer: str, user_answer: str) -> bool:
    """
    ES: Comprueba si la respuesta del usuario coincide con la correcta.\n
    EN: Checks if the user's answer is the same as the correct one.
    
    :param correct_answer: The correct answer to the problem.
    :type correct_answer: str
    :param user_answer: The answer provided by the user.
    :type user_answer: str
    :return: Whether the user answer is correct (True) or not (False).
    :rtype: bool
    """
    
    # intento de comparación matemática segura
    # safe mathematical comparison attempt
    try:
        correct_expr = safe_parse(correct_answer)
        user_expr = safe_parse(user_answer)
        
        # 1º Comparación numérica
        # 1º Numerical comparison
        try:
            correct_val = float(correct_expr.evalf())
            user_val = float(user_expr.evalf())

            # comparando con una tolerancia para evitar errores          
            # comparing with a tolerance to avoid errors
            return math.isclose(correct_val, user_val, rel_tol=1e-5)
            
        # 2º Comparación simbólica
        # 2º Symbolical comparison
        except (TypeError, ValueError):
            return simplify(correct_expr - user_expr) == 0
        
    # 3º FALLBACK: Comparación textual
    # 3º FALLBACK: Textual comparison
    except (ValueError, SympifyError):
        return correct_answer.strip().lower() == user_answer.strip().lower()
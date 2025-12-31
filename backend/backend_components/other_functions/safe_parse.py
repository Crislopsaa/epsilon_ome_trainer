"""
ES: Este script define una función que convierte una expresión dada en un objeto SymPy de forma segura.\n
EN: This script defines a function that turns a given expression into a SymPy object in a safe way.
"""


from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import Expr, sqrt, __dict__ as sympy_dict

import re


def safe_parse(expr: str) -> Expr:
    """
    ES: Convierte una expresión dada en un objeto SymPy de forma segura.\n
    EN: Turns a given expression into a SymPy object in a safe way.
    
    Warning:
        ES: Si la expresión contiene una palabra prohibida o no es una expresión matemática, se lanzará un ValueError.
        EN: If the expression contains a forbidden word or is not a mathematical expression, a ValueError will be raised.
    
    :param expr: Expresion to turn into a Sympy object.
    :type expr: str
    
    :return: SymPy object
    :rtype: Expr
    """
    
    # permitiendo las transformaciones estándar y la multiplicación sin el símbolo "*"
    # allowing standard transformations and multiplication without the symbol "*"
    transformations = standard_transformations + (implicit_multiplication_application,)

    allowed_functs = {
        "sqrt": sqrt,
    }

    # bloqueando palabras clave potencialmente peligrosas (inyección de código)
    # blocking potentially dangerous key words (code inyection)
    blocked = {
        "true", "false", "none",
        "__builtins__", "__import__", "__loader__",
        "__file__", "__package__", "__class__", "__classes__",
        "__dict__", "__globals__", "__getattribute__",
        "__subclasses__", "__mro__", "__bases__",
        "lambda", "import", "eval", "exec", "open",
        "os", "sys", "exit", "quit"
    }

    
    # limpieza previa
    # previous cleanup
    expr = expr.strip().replace("√", "sqrt").lower()
    
    # buscando palabras prohibidas
    # searching for forbidden words
    for name in blocked:
        if re.search(rf"\b{re.escape(name)}\b", expr):
            raise ValueError(f"Palabra prohibida detectada al convertir la solución en objeto SymPy: {name}")
    
    # si no hay palabras prohibidas, se devuelve la expresión evaluada y convertida en objeto SymPy
    # if no forbidden words are found, the SymPy expression is evaluated and returned
    return parse_expr(
        expr,
        local_dict = allowed_functs,
        global_dict = {"__builtins__": {}, **sympy_dict},
        transformations = transformations,
        evaluate = True
        )
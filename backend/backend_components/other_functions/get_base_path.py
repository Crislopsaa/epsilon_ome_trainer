"""
ES: Este script define una función para obtener la ruta del directorio principal (compatible con PyInstaller).\n
EN: This script defines a function to get the main directory's path (PyInstaller compatible).
"""


import sys
from pathlib import Path


def get_base_path():
    """
    ES: Retorna la ruta base dependiendo de si el script está empaquetado o no.\n
    EN: Returns the base path depending on whether the script is packed or not.
    
    Returns:
        Path: Absolute path to the main dir
    """

    # si detecta _MEIPASS, estamos en el ejecutable (.exe)
    # if _MEIPASS is detected, we are in the executable (.exe)
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    
    return Path(__file__).resolve().parents[3]
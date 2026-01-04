"""
ES: Este script define una función que obtiene de la base de datos local los datos mostrados en el gráfico simple.

EN: This script defines the function that gets from the local database the data displayed in the simple graphic.
"""


from pathlib import Path
import sqlite3


def get_simple_graphic_data(db_path: Path | str) -> list[int]:
    """
    ES: Obtiene de la base de datos local los datos mostrados en el gráfico simple.
    
    EN: Gets from the local database the data displayed in the simple graphic.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path | str
    :return: List composed of two elements: the user's correct answers, first, and then the number of mistakes.
    :rtype: list[int]
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
                SELECT
                    COALESCE(SUM(correct_answers), 0),
                    COALESCE(SUM(incorrect_answers), 0)
                FROM
                    User_Stats
            """)
        
        # el uso de COALESCE evita que fetchone devuelva None (fallaría al usar list)
        # COALESCE usage avoids fetchone returns None (the function list would throw an exception)
        simple_graphic_data = cursor.fetchone()
        
        return list(simple_graphic_data)
"""
ES: Este script define una función que obtiene de la base de datos local los datos mostrados en el gráfico por dificultades.

EN: This script defines the function that gets from the local database the data displayed in the difficulty graphic.
"""


from pathlib import Path
import sqlite3


def get_difficulty_graphic_data(db_path: Path | str) -> list[dict]:
    """
    ES: Obtiene de la base de datos local los datos mostrados en el gráfico por dificultades.
    
    EN: Gets from the local database the data displayed in the difficulty graphic.
    
    Warning:
        ES: Si no hay suficientes datos para crear el gráfico, se lanza una ValueError.
        EN: If there is not enough data to create the chart, a ValueError is raised.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path | str
    :return: List of dictionaries that contains the user's correct answers and mistakes grouped by difficulty.
    :rtype: list[dict]
    """
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        difficulty_graphic_data = []
            
        cursor.execute(
            """
            SELECT
                difficulty, 
                COALESCE(SUM(correct_answers), 0),
                COALESCE(SUM(incorrect_answers), 0)
            FROM user_stats GROUP BY difficulty
            """
            )
        rows = cursor.fetchall()
        
        
        total_problems_solved = 0
        for row in rows:
            total_problems_solved += row[1]
            total_problems_solved += row[2]
        
        # si no hay suficientes datos para crear el gráfico, se lanza una excepción
        # if there is not enough data to create the chart, an exception is raised    
        if total_problems_solved == 0:
            raise ValueError("[get_difficulty_graphic_data] AVISO: No hay suficientes datos para mostrar el gráfico por temáticas")
        
        
        for row in rows:
            difficulty_graphic_data.append({'DIFICULTAD': row[0], 'TIPO': 'Correcto', 'VALOR': row[1]})
            difficulty_graphic_data.append({'DIFICULTAD': row[0], 'TIPO': 'Incorrecto', 'VALOR': row[2]})
            
        return difficulty_graphic_data
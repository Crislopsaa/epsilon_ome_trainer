"""
ES: Este script define una función que obtiene de la base de datos local los datos mostrados en el gráfico completo.

EN: This script defines the function that gets from the local database the data displayed in the full graphic.
"""

from pathlib import Path
import sqlite3


def get_all_user_data(db_path: Path | str, abbreviated_topics: dict) -> list[dict]:
    """
    ES: Obtiene de la base de datos local los datos mostrados en el gráfico completado.
    
    EN: Gets from the local database the data displayed in the full graphic.
    
    Warning:
        ES: Si no hay suficientes datos para crear el gráfico, se lanza una ValueError.
        EN: If there is not enough data to create the chart, a ValueError is raised.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path | str
    :param abbreviated_topics: Dictionary that relates the topics with its abbreviation.
    :type abbreviated_topics: dict
    :return: List of dictionaries that contains the user's correct answers and mistakes grouped by course, difficulty, and topic.
    :rtype: list[dict]
    """
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
            
        cursor.execute("""
                        SELECT grade, difficulty, topic, correct_answers, incorrect_answers
                        FROM user_stats
                        """)
        rows = cursor.fetchall()
        
        number_of_answers = 0
        for row in rows:
            number_of_answers += row[3]
            number_of_answers += row[4]
        
        # si no hay suficientes datos para crear el gráfico, se lanza una excepción
        # if there is not enough data to create the chart, an exception is raised  
        if number_of_answers == 0:
            raise ValueError("[get_full_graphic_data] AVISO: No hay suficientes datos para mostrar el gráfico por temáticas")
        
        all_user_data = []
        for row in rows:
            topic = row[2]
            
            # usando abreviaturas para ahorrar espacio en el gráfico
            # using abbreviations to save space in the chart
            abbreviated_topic = abbreviated_topics.get(topic, topic)
            
            correct_answers = {'CURSO': row[0], 'DIFICULTAD': row[1], 'TEMÁTICA':abbreviated_topic, 'TIPO': 'Corr.', 'VALOR': row[3]}
            incorrect_answers = {'CURSO': row[0], 'DIFICULTAD': row[1], 'TEMÁTICA': abbreviated_topic, 'TIPO':'Incorr.', 'VALOR': row[4]}
            all_user_data.extend([correct_answers, incorrect_answers])
        
        return all_user_data
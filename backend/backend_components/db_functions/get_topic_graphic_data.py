"""
ES: Este script define una función que obtiene de la base de datos local los datos mostrados en el gráfico por temáticas.

EN: This script defines the function that gets from the local database the data displayed in the topic graphic.
"""


from pathlib import Path
import sqlite3


def get_topic_graphic_data(db_path: Path | str, abbreviated_topics: dict[str, str]) -> list[dict]:
    """
    ES: Obtiene de la base de datos local los datos mostrados en el gráfico por temáticas.
    
    EN: Gets from the local database the data displayed in the topic graphic.
    
    Warning:
        ES: Si no hay suficientes datos para crear el gráfico, se lanza una ValueError.
        EN: If there is not enough data to create the chart, a ValueError is raised.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path | str
    :param abbreviated_topics: Dictionary that relates the topics with its abbreviation.
    :type abbreviated_topics: dict[str, str]
    :return: List of dictionaries that contains the user's correct answers and mistakes grouped by topic.
    :rtype: list[dict]
    """
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                topic,
                COALESCE(SUM(correct_answers), 0),
                COALESCE(SUM(incorrect_answers), 0)
            FROM user_stats
            GROUP BY topic
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
            raise ValueError("[get_topic_graphic_data] AVISO: No hay suficientes datos para mostrar el gráfico por temáticas")

        topic_graphic_data = []
        for row in rows:
            topic = row[0]
            
            # usando abreviaturas para ahorrar espacio en el gráfico
            # using abbreviations to save space in the chart
            abbreviated_topic = abbreviated_topics.get(topic, topic)
            
            topic_graphic_data.append({'TEMÁTICA': abbreviated_topic, 'TIPO': 'Correcto', 'VALOR': row[1]})
            topic_graphic_data.append({'TEMÁTICA': abbreviated_topic, 'TIPO': 'Incorrecto', 'VALOR': row[2]})
        
        return topic_graphic_data
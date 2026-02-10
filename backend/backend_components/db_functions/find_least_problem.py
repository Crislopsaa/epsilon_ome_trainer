"""
ES: Este script define una función que encuentra cuál es el tipo de problema menos generado por la IA.

EN: This script defines a function that finds the least AI-generated problem type.
"""


import sqlite3
from typing import Iterable


def find_least_problem(cursor: sqlite3.Cursor, combinations: Iterable[tuple[str, str, str]]) -> tuple[str, str, str]:
        """
        ES: Encuentra cuál es el tipo de problema menos generado por la IA.

        EN: Finds the least AI-generated problem type.
        
        Usage:
            ES: Debería ser ejecutado dentro de un bloque with para manejar la conexión con la base de datos.
            EN: It should be executed inside a with block to manage the database connection.
        
        :param cursor: The cursor to interact with the local database where the problems are stored.
        :type cursor: sqlite3.Cursor
        :param combinations: All possible combinations of problem types (Grade, Difficulty, Topic) that the AI can generate.
        :type combinations: Iterable[tuple[str, str, str]]
        
        :return: The least generated problem type (Grade, Difficulty, Topic).
        :rtype: tuple[str, str, str]
        """
        
        cursor.execute(
            """
            SELECT grade, difficulty, topic, COUNT(*)
            FROM generated_problems
            GROUP BY grade, difficulty, topic
            """
            )
        
        generated_problems = cursor.fetchall()
        
        # si no se ha generado ningún problema, se devuelve una combinación cualquiera
        # if no problems have been generated, any combination is returned
        if not generated_problems:
            return tuple(combinations)[0]
        
        problem_types = [problem[0:3] for problem in generated_problems]
        
        not_generated_problems = set(combinations) - set(problem_types)
        
        # si hay combinaciones que nunca han sido generadas, se devuelve cualquiera de ellas
        # if there are combinations that have never been generated, any of them is returned       
        if not_generated_problems:
            return tuple(not_generated_problems)[0]
        
        else:
            return min(generated_problems, key = lambda x:x[3])[0:3]
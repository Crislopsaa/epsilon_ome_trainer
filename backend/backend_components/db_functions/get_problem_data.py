"""
ES: Este script define una función que obtiene un problema de la base de datos local con el curso, dificultad y temática dadas.\n
EN: This script defines a function that gets a problem from the local database with the given course, difficulty and topic.
"""


from pathlib import Path
import sqlite3


def get_problem_data(db_path: Path, course: str, difficulty: str, topic: str):
    """
    ES: Obtiene un problema de la base de datos local con un curso, dificultad y temática dadas.\n
    EN: Gets a problem from the local database with the given course, difficulty and topic.
    
    Warning:
        ES: Si no hay ningún problema disponible con esas características, se lanza un LookupError.
        EN: If there is no problem available with the given characteristics, a LookupError is raised.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path
    :param course: The course of the problem to get.
    :type course: str
    :param difficulty: The difficulty of the problem to get.
    :type difficulty: str
    :param topic: The topic of the problem to get.
    :type topic: str
    """
    
    # DEBUGGING
    if not all([db_path, course, difficulty, topic]):
        print(f"AVISO: Se le ha pasado algún parámetro nulo a la función que obtiene los datos de problema. Datos recibidos: {db_path=}, {course=}, {difficulty=}, {topic=}")
        return
    
    problem_type = (course, difficulty, topic)
    
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT rowid, formulation, procedure, short_solution
                    FROM generated_problems
                    WHERE course=? AND difficulty=? AND topic=?
                    ORDER BY rowid
                    LIMIT 1
                    """, problem_type)
        
        problem_row = cursor.fetchone()
    
    
        # si se encuentra el problema, este se elimina de la base de datos para que no aparezca de nuevo
        # if the problem is found, it is deleted from the database so it does not appear again
        if problem_row:
            db_id = problem_row[0]
            problem_data = problem_row[1:4]
            
            cursor.execute("""
                            DELETE FROM generated_problems
                            WHERE rowid = ?
                            """, (db_id,))
            
            conn.commit()
            return problem_data
    
    
        # si no se encuentra el problema, se lanza un error
        # if the problem is not found, an error is raised
        else:
            raise LookupError(f"NO PROBLEM AVAILABLE for {course} - {difficulty} - {topic}")
"""
ES: Este script define una función que guarda los problemas que genera la IA en la base de datos local.

EN: This script defines a function that stores the AI-generated problems in the local database.
"""


import sqlite3


def save_problem(problem: list | tuple, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
    """
    ES: Guarda los problemas que genera la IA en la base de datos local.

    EN: Stores the AI-generated problems in the local database.
    
    Warning:
        ES: Si el problema no se guarda correctamente, se lanza un RuntimeError
        EN: If the problem is not stored correctly, a RuntimeError is raised.
    
    :param problem: The problem's type and sections: Grade, Difficulty, Topic, Formulation, Procedure, and Short Solution.
    :type problem: list | tuple
    :param conn: Connection to the SQLite local database.
    :type conn: sqlite3.Connection
    :param cursor: Cursor to interact with the SQLite local database. This function does not create it to avoid creating multiple cursor when using multiple database-related, custom functions.
    :type cursor: sqlite3.Cursor
    """
    
    try:
        cursor.execute(
            """
            INSERT INTO generated_problems (grade, difficulty, topic, formulation, procedure, short_solution)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            problem
            )
        
        conn.commit()
        
        
    except Exception as e:
        raise RuntimeError(f"[save_problem] ERROR: Me temo que ha ocurrido un error a la hora de guardar el problema en la base de datos local:\n\n{e}")
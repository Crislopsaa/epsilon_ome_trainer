"""
ES: Este script define una función que registra un acierto o fallo en una base de datos local dada.\n
EN: This script defines a function that registers a right answer or a mistake in a given local database.
"""


from pathlib import Path
import sqlite3


def register_success_or_mistake(db_path: Path, grade: str, difficulty: str, topic: str, user_answer_status: bool = False):
    """
    ES: Registra un acierto o fallo en una base de datos local dada.\n
    EN: Registers a right answer or a mistake in a given local database.
    
    Usage:
        ES: Si user_answer_status es True, se registra un acierto; si no, se registra un error.
        EN: If user_answer_status is True, a success is registered; else, a mistake is registered.
    
    :param db_path: Absolute path to the local database.
    :type db_path: Path
    :param grade: The grade of the problem solved.
    :type grade: str
    :param difficulty: The difficulty of the problem solved.
    :type difficulty: str
    :param topic: The topic of the problem solved.
    :type topic: str
    :param user_answer_status: Whether to register a success or a failure. Optional: False by default.
    :type user_answer_status: bool
    """
    
    # DEBUGGING
    if not all([db_path, grade, difficulty, topic]):
        print(f"AVISO: Se le ha pasado algún parámetro nulo a la función que registra los aciertos y fallos. Datos recibidos: {db_path=}, {grade=}, {difficulty=}, {topic=}")
        return
    
    problem_type = (grade, difficulty, topic)


    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # si no existe una fila con ese tipo de problema, se crea
        # if it does not exist a row with that problem type, it is created
        cursor.execute(
            """
            INSERT OR IGNORE INTO user_stats (grade, difficulty, topic, correct_answers, incorrect_answers)
            VALUES (?, ?, ?, 0, 0)
            """,
            problem_type
        )
    
        # registrando acierto o fallo
        # registering success or failure
        if user_answer_status:
            cursor.execute(
                """
                UPDATE user_stats
                SET correct_answers = correct_answers + 1
                WHERE grade=? AND difficulty=? AND topic=?;
                """,
                problem_type
                )
            
        else:
            cursor.execute(
                """
                UPDATE user_stats
                SET incorrect_answers = incorrect_answers + 1
                WHERE grade=? AND difficulty=? AND topic=?;
                """,
                problem_type
                )
          
        conn.commit()
"""
ES: Este script define una función para inicializar la base de datos.\n
EN: this script defines a function to initialize the database.
"""


import sqlite3

from backend.backend_components.db_functions.get_db_path import get_db_path


def init_db():
    """
    ES: Inicializa la base de datos.\n
    EN: Initializes the database.
    """
    
    db_path = get_db_path()
    
    # conectando con la base de datos y creando el cursor
    # connecting to the database and creating the cursor
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # creando la tabla de los problemas generados si no se ha creado ya
        # creating the generated problems' table if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_problems(
                course TEXT,
                difficulty TEXT,
                topic TEXT,
                formulation TEXT,
                procedure TEXT,
                short_solution TEXT
            ) 
            """
            )
        
        # creando la tabla de las estadísticas del usuario si no se ha creado ya
        # creating the user's stats' table if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_stats(
            course TEXT,
            difficulty TEXT,
            topic TEXT,
            correct_answers INTEGER DEFAULT 0,
            incorrect_answers INTEGER DEFAULT 0 
            )
            """
            )
        
        # guardando los cambios
        # saving the changes
        conn.commit()
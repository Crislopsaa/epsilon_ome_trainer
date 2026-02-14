"""
ES: Esta script define una función que maneja la generación de problemas teniendo en cuenta si la IA ya ha sido entrenada y si el modo automático de generación de problemas está activo.

EN: This script defines a function that manages problem generation taking into account if the AI has already been trained and if problem generation's automatic mode is activated
"""


import itertools, sqlite3, time
from pathlib import Path
from llama_cpp import Llama

# importando funciones personalizadas
# importing custom functions
from backend.backend_components.other_functions.create_example_problem import create_example_problem
from backend.backend_components.db_functions.find_least_problem import find_least_problem
from backend.backend_components.db_functions.save_problem import save_problem
from backend.problem_generator.problem_generator import generate_problem

# importando clases personalizadas
# importing custom functions
from backend.backend_components.classes.worker import Worker


def manage_problem_generation(ai_path: Path, db_path: Path | str,  generation_request: tuple[str, str, str, int] | int, worker: Worker, progress_callback: callable = None):        
    """
    ES: Maneja la generación de problemas teniendo en cuenta si la IA ya ha sido entrenada y si el modo automático de generación de problemas está activo.

    EN: Manages problem generation taking into acount if the AI has already been trained and if problem generation's automatic mode is activated
    
    Usage:
        ES: Debe ser ejecutado en un QThread secundario para que no se congele la UI.
        EN: It must be executed in a secondary QThread to avoid freezing the UI. 
    
    :param ai_path: The absolute path of the AI's GGUF file.
    :type ai_path: Path
    :param db_path: Absolute path to the local SQLite database.
    :type db_path: Path | str
    :param generation_request: Problem generation request. To specify a certain problem type, a tuple (Grade, Difficulty, Topic, Quantity) must be given; else, the quantity must be provided.
    :type generation_request: tuple[str, str, str, int] | int
    :param worker: QObject that will execute this function in an asynchronous QThread.
    :type worker: Worker
    :param progress_callback: A function to track the problem generation's progress.
    :type progress_callback: callable
    """
    
    # en la demo, no hay IA, por lo que se usan problemas ejemplo
    # in the demo, there is no AI, so example problems are used
    demo_mode = not ai_path.exists() 
    
    # en el modo automático, el tipo del problema a generar debe ser calculado
    # in automatic mode, the type of the problem to generate must be calculated
    automatic_mode = isinstance(generation_request, int)
    
    if automatic_mode:
        quantity = generation_request
        combinations = set(itertools.product(
            ("1º y 2º ESO",),
            ("Provincial", "Regional", "Nacional"),
            (
                "Aritmética y Teoría de Números",
                "Álgebra",
                "Geometría",
                "Combinatoria y Probabilidad",
                "Lógica y Razonamiento"
                )
            )
        )
        
    else:
        grade, difficulty, topic, quantity = generation_request
    
    
    if not demo_mode:
        llm = Llama(model_path= str(ai_path), n_gpu_layers = -1)   
        
        
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        for i in range(quantity):
            
            if automatic_mode:
                problem_to_generate = find_least_problem(cursor, combinations)
            
            else:
                problem_to_generate = (grade, difficulty, topic)
        
            
            if demo_mode:
                problem_data = create_example_problem()
                   
            else:
                problem_data = generate_problem(
                    problem_to_generate = problem_to_generate,
                    llm = llm,
                    worker = worker
                    )
                
            
            save_problem(problem_to_generate + problem_data, conn, cursor)
             
            # actualizando el progreso
            # updating the progress
            if progress_callback:   
                progress_callback(i+1)
                
            # esto evita un bucle agresivo con la CPU
            # this avoids a CPU-aggresive loop
            time.sleep(0)
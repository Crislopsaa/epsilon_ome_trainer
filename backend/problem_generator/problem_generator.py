"""
ES: Este script define una función que utiliza llama_cpp para hacer una inferencia con la IA guardada localmente: generar un problema matemático programado en LaTeX, el núcleo de la aplicación.

EN: This script defines a function that uses llama_cpp to make an inference with the locally stored AI: generate a mathematical problem coded in LaTeX, the app's core.
"""


from llama_cpp import Llama

# importando funciones personalizadas
# importing custom functions
from backend.backend_components.other_functions.check_latex import check_latex


def generate_problem(problem_to_generate: list | tuple, llm: Llama) -> tuple[str, str, str]:
    """
    ES: Utiliza llama_cpp para hacer una inferencia con la IA guardada localmente: generar un problema matemático programado en LaTeX, el núcleo de la aplicación.
    
    EN: Uses llama_cpp to make an inference with the locally stored AI: generate a mathematical problem coded in LaTeX, the app's core.
    
    Warning:
        ES: Si el código LaTeX de los problemas contiene un error evidente, se lanza un ValueError.
        EN: If the problem's LaTeX code contains an evident error, a ValueError is raised.
    
    :param problem_to_generate: The type (grade, difficulty and topic) of the problem to generate.
    :type problem_to_generate: list | tuple
    :param llm: Instance of the LLM (Large Language Model) that will be used to generate the problem. Inference uses custom parameters:\n
        - max_tokens: to establish an extension limit.
        - top_p: for the AI to use a more diverse vocabulary.
        - temperature: to increase creativity.
        - presence_penalty: to avoid the repetition of words between problems (mainly for people's names)
        - stop: to ensure that only one problem is generated.
        - echo: to prevent the answer from containing the instruction.
        
    :type llm: Llama
    :return: The problem divided by sections: Formulation, Procedure and Short Solution.
    :rtype: tuple[str, str, str]
    """
    
    grade, difficulty, topic = problem_to_generate

    # se usa system para darle el suficiente contexto a la IA para que identifique esta inferencia con su Low Rank Adaptation (LoRA, adaptación de bajo rango en español)
    # system is used to give the AI enough context for it to associate this inference with its Low Rank Adaptation (LoRA)
    system = "Eres un entrenador de la Olimpiada Matemática Española de 2ºESO que genera problemas de esa competición con su solución."
    
    # esta instrucción también es la misma que se usó durante el entrenamiento LoRA
    # this instruction is also the same as the one used during LoRA training
    instruction = f"Genera un problema con las siguientes características: Curso: {grade} | Dificultad: {difficulty} | Temática: {topic}"
    
    prompt = (
        f"### Instrucción:\n{system}\n\n"
        f"### Mensaje:\n{instruction}\n\n"
        "### Respuesta:\n\n"
        )   
    

    completion = llm.create_completion(
        prompt,
        max_tokens=2048,
        top_p = 0.9,
        temperature=0.7,
        presence_penalty = 0.1,
        stop=["###", "Instrucción:", "Mensaje:"],
        echo = False
        )

    problem = completion['choices'][0]['text'].strip()
    
    # "-----" se usa como separador entre las partes del problema: enunciado, procedimiento y solución final
    # "-----" is used as a separator between the different problem parts: formulation, procedure and final answer
    sections = [s.strip() for s in problem.split("-----") if s.strip()]

    if len(sections) != 3:
        raise ValueError("[generate_problem] ERROR: No se dividieron las partes del problema correctamente")
    
    
    for i, section in enumerate(sections):
        try:
            check_latex(section)
    
        except Exception as e:
            raise ValueError(f"[generate_problem] ERROR: El código LaTeX generado no es válido en la sección número {i}:\n\n{e}")
    
    
    formulation = sections[0]
    procedure = sections[1]
    final_answer = sections[2]
    
    problem = (formulation, procedure, final_answer)
    
    # el problema se devuelve como una tupla para que sea guardado con facilidad
    # the problem is returned as a tuple for it to be stored easily
    return problem
"""
ES: Este script define una función que crea un gráfico de anillos consecutivos de Plotly que muestra los aciertos y fallos del usuario agrupados por curso, dificultad y temática.

EN: This script defines a function that creates a Plotly sunburst chart that displays the user's correct answers and mistakes grouped by course, difficulty, and topic.
"""


import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.set_graphic_style import set_graphic_style


def create_full_graphic(all_user_data: list[dict]) -> Figure:
    """
    ES: Crea un gráfico de anillos consecutivos de Plotly que muestra los aciertos y fallos del usuario agrupados por curso, dificultad y temática.
    
    EN: Creates a Plotly sunburst chart that displays the user's correct answers and mistakes grouped by course, difficulty, and topic.
    
    Warning:
        ES: Si se le pasan datos vacíos, se lanza un ValueError.
        EN: If null values are given, a ValueError is raised.
    
    :param all_user_data: List of dictionaries that contains the user's correct answers and mistakes grouped by course, difficulty, and topic.
    :type all_user_data: list[dict]
    :return: Plotly sunburst chart that displays the user's correct answers and mistakes grouped by course, difficulty, and topic. 
    :rtype: Figure
    """
    
    # DEBUGGING
    if not all_user_data:
        raise ValueError("[create_full_graphic] ERROR: Se le han pasado datos vacíos/nulos")
    
    df = pd.DataFrame(all_user_data)

    full_graphic = px.sunburst(
        df,
        path=['CURSO', 'DIFICULTAD', 'TEMÁTICA', 'TIPO'],
        values='VALOR',
        title = 'Gráfico Completo'
        )
    
    set_graphic_style(full_graphic)
    
    return full_graphic
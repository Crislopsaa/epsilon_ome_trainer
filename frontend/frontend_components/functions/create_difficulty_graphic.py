"""
ES: Este script define una función que crea un gráfico de barras de Plotly que muestra los aciertos y fallos del usuario agrupados por dificultad.

EN: This script defines a function that creates a Plotly stacked bar chart that displays the user's correct answers and mistakes grouped by difficulty.
"""


import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.set_graphic_style import set_graphic_style


def create_difficulty_graphic(difficulty_graphic_data: list[dict]) -> Figure:
    """
    ES: Crea un gráfico de barras de Plotly que muestra los aciertos y fallos del usuario agrupados por dificultad.
    
    EN: Creates a Plotly bar graphic that displays the user's correct answers and mistakes grouped by difficulty.
    
    Warning:
        ES: Si se le pasan datos vacíos, se lanza un ValueError.
        EN: If null values are given, a ValueError is raised.
    
    :param difficulty_graphic_data: List of dictionaries that contains the user's correct answers and mistakes grouped by difficulty.
    :type difficulty_graphic_data: list[dict]
    :return: Plotly stacked bar chart that displays the user's correct answers and mistakes grouped by topic. 
    :rtype: Figure
    """
    
    # DEBUGGING
    if not difficulty_graphic_data:
        raise ValueError("[create_difficulty_graphic] ERROR: Se le han pasado datos vacíos/nulos") 
                
    df = pd.DataFrame(difficulty_graphic_data)
    
    difficulty_graphic = px.bar(
        df,
        x = 'DIFICULTAD',
        y = 'VALOR',
        category_orders={"DIFICULTAD": ["Provincial", "Regional", "Nacional"]},
        color='TIPO',
        title = 'Gráfico agrupado por dificultad',
        barmode = 'stack'
        )

    
    set_graphic_style(difficulty_graphic)
    
    difficulty_graphic.update_layout(
        xaxis_title = "Dificultades",
        yaxis_title = "Número de respuestas",
        )

    return difficulty_graphic
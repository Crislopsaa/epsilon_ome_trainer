"""
ES: Este script define una función que crea un gráfico de barras de Plotly que muestra los aciertos y fallos del usuario agrupados por temática.

EN: This script defines a function that creates a Plotly stacked bar chart that displays the user's correct answers and mistakes grouped by topic.
"""


import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.set_graphic_style import set_graphic_style


def create_topic_graphic(topic_graphic_data: list[dict]) -> Figure:
    """
    ES: Crea un gráfico de barras de Plotly que muestra los aciertos y fallos del usuario agrupados por temática.
    
    EN: Creates a Plotly bar graphic that displays the user's correct answers and mistakes grouped by topic.
    
    :param topic_graphic_data: List of dictionaries that contains the user's correct answers and mistakes grouped by topic.
    :type topic_graphic_data: list[dict]
    :return: Plotly stacked bar chart that displays the user's correct answers and mistakes grouped by topic. 
    :rtype: Figure
    """
    
    # DEBUGGING
    if not topic_graphic_data:
        raise ValueError("[create_topic_graphic] ERROR: Se le han pasado datos vacíos/nulos")
    
    df = pd.DataFrame(topic_graphic_data)
       
    topic_graphic = px.bar(
        df,
        x = 'TEMÁTICA',
        y= 'VALOR',
        color = 'TIPO',
        title = 'Gráfico agrupado por temática',
        barmode = 'stack'
        )
    
    topic_graphic.update_layout(xaxis_title="Temática", yaxis_title="Número de Respuestas")
    
    set_graphic_style(topic_graphic)
    
    return topic_graphic
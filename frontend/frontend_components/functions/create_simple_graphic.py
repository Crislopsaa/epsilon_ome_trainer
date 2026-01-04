"""
ES: Este script define una función que crea un gráfico circular de Plotly que muestra los aciertos y los fallos del usuario.\n
EN: This script defines a function that creates a Plotly pie chart that displays the user's correct answers and mistakes.
"""


import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.set_graphic_style import set_graphic_style


def create_simple_graphic(simple_data: list) -> Figure:
    """
    ES: Crea un gráfico circular de Plotly que muestra los aciertos y los fallos del usuario.\n
    EN: Creates a Plotly pie chart that displays the user's correct answers and mistakes.
    
    Warning:
        ES: Si no hay suficientes datos para crear el gráfico, se lanza una ValueError.
        EN: If there is not enough data to create the chart, a ValueError is raised.
    
    :param simple_data: A list of two elements that contains the number of user's correct answers and mistakes in that order.
    :type simple_data: list
    :return: The Plotly pie chart that displays the user's correct answers and mistakes.
    :rtype: Figure
    """
    
    # si no hay suficientes datos, se lanza una excepción
    # if there is not enough data, an exception is raised
    if simple_data[0] + simple_data[1] == 0:
        raise ValueError("[create_simple_graphic] AVISO: No hay suficientes datos para mostrar el gráfico")
    
    
    organised_data = {
        'sections': ['Correcto', 'Incorrecto'],
        'values': simple_data
    }
    
    df = pd.DataFrame(organised_data)
        
    simple_graphic = px.pie(
        df,
        names = 'sections',
        values = 'values',
        color = 'sections',
        color_discrete_map= {'Correcto': 'green', 'Incorrecto': 'red'},
        title = 'Gráfico Sencillo'
    )
    
    set_graphic_style(simple_graphic)
    
    return simple_graphic
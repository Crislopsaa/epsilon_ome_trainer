"""
ES: Este script define una función que establece características de estilo comunes para todos los gráficos Plotly.\n
EN: This script defines a function that applies common style settings to all Plotly graphics.
"""


from plotly.graph_objects import Figure


def set_graphic_style(fig: Figure) -> None:
    """
    ES: Establece características de estilo comunes para todos los gráficos Plotly.\n
    EN: Applies common style settings to all Plotly graphics.
    
    :param fig: Plotly graphics which theses style settings are going to be set to.
    :type fig: Figure
    """
    
    fig.update_layout(
            title={
                'font': {
                    'size': 24,
                    'family': 'Impact'
                }
            },
            paper_bgcolor="#ADACAB",
        )
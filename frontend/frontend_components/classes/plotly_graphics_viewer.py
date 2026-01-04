"""
ES: Este script implementa la clase de un visor de gráficos de Plotly basado en QtWebEngine.\n
EN: This script implements the class of a Plotly graphics viewer based on QtWebEngine.
"""


from pathlib import Path
from plotly.graph_objects import Figure
import tempfile
import os

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PlotlyGraphicsViewer(QWidget):
    """
    ES: Visor de gráficos Plotly basado en QtWebEngine.\n
    EN: Plotly graphics viewer based on QtWebEngine.
    
    Warning:
        ES: Para evitar problemas de compatibilidad y que el visor se quede en blanco, se debe usar una versión antigua de Plotly (5.15.0).
        EN: To avoid compatibility problems where the viewer appears blank, an old version of Plotly (5.15.0) must be used.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    """
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path
        
        self.main_layout = QVBoxLayout()
        
        self.viewing_pane = QFrame(parent=self)
        self.viewing_pane.setStyleSheet("""
                                     background-color : #ffffff;
                                     border-radius: 10px;
                                     padding: 5px;
                                     """)
        
        self.viewer_layout = QVBoxLayout()
        self.graphic_viewer = QWebEngineView()
        self.viewer_layout.addWidget(self.graphic_viewer)
        
        self.viewing_pane.setLayout(self.viewer_layout)
        
        self.main_layout.addWidget(self.viewing_pane)
        
        self.setLayout(self.main_layout)
        
        
    def show_graphic(self, fig: Figure):
        """
        ES: Muestra un gráfico Plotly en el visor.\n
        EN: Displays a Plotly graphic in the viewer.
        
        :param fig: The Plotly graphic to display.
        :type fig: Figure
        """
        
        # si existen residuos de un gráfico cargado anteriormente, se borran
        # if there are residues from a previous graphic, they are deleted
        if hasattr(self, "_tempfile_name"):
            try:
                os.remove(self._tempfile_name)
                
            except Exception as e:
                print(f"[PlotlyGraphicsViewer] ERROR: No se pudo eliminar el archivo temporal que contiene el HTML del gráfico mostrado:\n{e}")
        
        
        # convirtiendo el gráfico en código HTML para asegurar que QWebEngineView lo muestre
        # turning the graphic into HTML code to ensure that QWebEngineView displays it
        div = fig.to_html(full_html=False, include_plotlyjs=False)

        # obteniendo ruta del JavaScript local para evitar conflictos entre Plotly y QWebEngineView
        # getting the local JavaScript path to avoid conflicts between Plotly and QWebEngineView
        plotly_js_path = (self.base_path / "assets" / "js" / "plotly.min.js").resolve().as_posix()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="file:///{plotly_js_path}"></script>
        </head>
        <body>
            {div}
        </body>
        </html>
        """

        # guardando el HTML en un archivo temporal
        # saving the HTML in a temporary file
        self.temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        self.temp.write(html.encode("utf-8"))
        self._tempfile_name = self.temp.name
        self.temp.close()
        
        self.graphic_viewer.load(QUrl.fromLocalFile(self.temp.name))
    
    def closeEvent(self, event):
        if hasattr(self, "_tempfile_name"):
            try:
                os.remove(self._tempfile_name)
            
            except Exception as e:
                print(f"[PlotlyGraphicsViewer] ERROR: No se pudo eliminar el archivo temporal que contiene el HTML del gráfico mostrado:\n{e}")
        
        return super().closeEvent(event)
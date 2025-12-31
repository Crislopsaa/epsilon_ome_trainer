"""
ES: Este script implementa la clase de un botón que muestra una ventana con información al ser pulsado.\n
EN: This script implements the class of a button that displays information in a pop-up window when it is clicked.
"""


from pathlib import Path

from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background


class InfoButton(QPushButton):
    """
    ES: Botón que muestra una ventana con información al ser pulsado.\n
    EN: Button that displays information in a pop-up window when it is clicked.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param window_title: The title of the pop-up window that will be displayed.
    :type window_title: str
    :param information: The information that the will be display in the pop-up window.
    :type information: str
    """
    def __init__(self, base_path: Path, window_title: str, information: str):
        super().__init__()
        
        # DEBUGGING
        if not all([information]):
            print("AVISO: A un botón de información se le ha pasado algún parámetro nulo.")
        
        self.window_title = window_title
        self.information = information
        
        self.background_path = base_path / "assets" / "images" / "info_button_background.png"
        self.background = QPixmap(str(self.background_path))
        
        # DEBUGGING
        if self.background.isNull():
            print("ERROR: No se encuentra la imagen de un botón de información.")
        
        self.setFixedSize(30, 30)
        self.setStyleSheet("border-radius: 1px")
        
        self.clicked.connect(self.show_info)
    
    def show_info(self):
        """
        ES: Muestra la información dada en una ventana emergente.
        EN: Displays the given information in a pop-up window.
        """
        
        QMessageBox.information(
            self.window(),
            self.window_title,
            self.information
            )
    
    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo con una imagen.\n
        EN: Paints the background with an image.
        """
        
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        return super().paintEvent(event)
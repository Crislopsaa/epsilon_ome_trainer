"""
ES: Este script define la clase de la página de información.\n
EN: This script implements the information page class.
"""


from pathlib import Path

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import pyqtSignal

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.back_button import BackButton
from frontend.frontend_components.classes.pdf_viewer import PDFViewer

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background


class InformationPage(QWidget):
    """
    ES: La página que muestra información sobre Epsilon.\n
    EN: The page that displays information about Epsilon.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path
        
        # creando el pixmap del fondo
        # creating the background pixmap
        self.background_path = self.base_path / "assets" / "images" / "information_page_background.png"
        self.background = QPixmap(str(self.background_path))
        
        
        self.back_button = BackButton(self.go_back_to_home)
        self.back_button.setParent(self)
        self.back_button.setGeometry(20, 20, 40, 40)
        
             
        self.pdf_path = self.base_path / "assets" / "documents" / "epsilon_information.pdf"
        self.pdf_viewer = PDFViewer(str(self.pdf_path))
        self.pdf_viewer.setGeometry(1070, 100, 665, 800)
        self.pdf_viewer.setParent(self)
        
    
    def go_back_to_home(self):
        """
        ES: Cambia la página por la página de inicio.
        EN: Switches the page to the home page.
        """
        self.change_page_signal.emit("home page")
    
    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo con una imagen.\n
        EN: Paints the background with an image.
        """

        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        return super().paintEvent(event)
"""
ES: Este script define la clase de la página de inicio.\n
EN: This script implements the main home page class.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import pyqtSignal

from frontend.frontend_components.classes.hover_opacity_button import HoverOpacityButton

from frontend.frontend_components.functions.paint_background import paint_background

class HomePage(QWidget):
    """
    ES: Página de inicio que permite navegar a la configuración de problemas, información y estadísticas.\n
    EN: Main home page providing navigation to problem configuration, info, and user stats.
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path

        # obteniendo las rutas de las imágenes
        # getting the paths of the images
        self.background_path = self.base_path / "assets" / "images" / "home_page_background.png"
        self.problems_sign_path = self.base_path / "assets" / "images" / "home_page_problems_sign.png"
        self.info_sign_path = self.base_path / "assets" / "images" / "home_page_information_sign.png"
        self.stats_sign_path = self.base_path / "assets" / "images" / "home_page_stats_sign.png"

        self.background = QPixmap(str(self.background_path))


        # creando los botones con efecto hover
        # creating the hover buttons
        self.problems_button = HoverOpacityButton(
            image_path = self.problems_sign_path,
            on_click_function = self.go_to_problem_configuration,
            )
        self.problems_button.setParent(self)
        
        self.info_button = HoverOpacityButton(
            image_path = self.info_sign_path,
            on_click_function = self.go_to_info,
            )
        self.info_button.setParent(self)
        
        self.stats_button = HoverOpacityButton(
            image_path = self.stats_sign_path,
            on_click_function =  self.go_to_stats,
            )
        self.stats_button.setParent(self)


    # definiendo los métodos que envían una señal para cambiar de página
    # defining the methods that send a signal to change the current page
    def go_to_problem_configuration(self):
        self.change_page_signal.emit("problem configuration page")
    
    def go_to_info(self):
        self.change_page_signal.emit("information page")
    
    def go_to_stats(self):
        self.change_page_signal.emit("user stats page")
    
    
    # rescribiendo el método que pinta el fondo
    # overriding to paint the background
    def paintEvent(self, event):
        painter = QPainter(self)
        paint_background(
            widget = self,
            painter = painter,
            pixmap = self.background
            )
        super().paintEvent(event)
    
    
    # rescribiendo el método que reajusta los tamaños
    # overriding the resizeEvent to handle window scaling
    def resizeEvent(self, event):
        self.resize_signs()


    # definiendo una función que ajusta los tamaños y posiciones de los carteles
    # defining a function that adjusts the signs' sizes and positions
    def resize_signs(self):
        w, h = self.width(), self.height()

        # definiendo el tamaño relativo de los carteles
        # defining the signs' relative sizes
        sign_w = int(w * 0.3)
        sign_h = int(h * 0.27)
        
        # posición vertical
        # vertical position
        y_position = int(h * 0.315 - sign_h)

        # posiciones horizontales
        # horizontal positions
        x_positions = (
            int(w * 0.17 - sign_w // 2),
            int(w * 0.507 - sign_w // 2),
            int(w * 0.84 - sign_w // 2)
        )

        # asignar geometría y posición a cada botón
        # assigning geometry and position to every button
        for button, x_position in zip(
            (self.problems_button, self.info_button, self.stats_button),
            x_positions
        ):
            button.setGeometry(x_position, y_position, sign_w, sign_h)
            button.image_label.setGeometry(0, 0, sign_w, sign_h)
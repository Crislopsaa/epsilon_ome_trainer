"""
ES: Este script crea la clase de un botón que cambia de imagen cuando el ratón está sobre él.\n
EN: This script implements the class of a button that changes its image when the mouse is on it.
"""


from pathlib import Path

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background


class HoverImageSwapButton(QPushButton):
    """
    ES: Un botón cuya imagen de fondo se cambia por otra cuando el ratón está sobre él.\n
    EN: A button whose background image is switched for another when the mouse is on it.
    
    :param static_image_path: Absolute path to the image displayed when the mouse is not on the button.
    :type static_image_path: Path
    :param swap_image_path: Absolute path to the image displayed when the mouse is on the button.
    :type swap_image_path: Path
    :param on_click_function: Function executed when the button is clicked.
    :type on_click_function: callable
    """
    def __init__(self, static_image_path: Path, swap_image_path: Path, on_click_function: callable):
        super().__init__()
        
        # DEBUGGING
        if not all([static_image_path,swap_image_path, on_click_function]):
            print("AVISO: Un botón de imagen cambiante ha recibido algún parámetro vacío.")
        
        self.on_click_function = on_click_function
        
        self.static_pixmap = QPixmap(str(static_image_path))
        self.swap_pixmap = QPixmap(str(swap_image_path))
        
        # DEBUGGING
        if self.static_pixmap.isNull() or self.swap_pixmap.isNull():
            print("ERROR: No se encuentra la imagen en un botón de imagen cambiante")
        
        self.setCursor(Qt.PointingHandCursor)
        
        # el botón solo se seleccionará visualmente cuando se pulse el TAB
        # the button will only be visually focused when TAB is pressed
        self.setFocusPolicy(Qt.TabFocus)
        
        self.pixmap_in_use = self.static_pixmap
        
        self.clicked.connect(self.handle_click)
      

    def enterEvent(self, event):
        """
        ES: Cuando el ratón está sobre el botón, se cambia la imagen estática por la de cambio.\n
        EN: When the mouse is on the button, the static image is switched for the swap one.
        """
        self.pixmap_in_use = self.swap_pixmap
        self.update()


    def leaveEvent(self, event):
        """
        ES: Cuando el ratón ya no está sobre el botón, se cambia la imagen de cambio por la estática.\n
        EN: When the mouse is no longer on the button, the swap image is switched for the static one.
        """
        self.pixmap_in_use = self.static_pixmap
        self.update()
    
    
    def handle_click(self):
        """
        ES: Deshabilita el botón durante 1 segundo tras el clic.
        EN: Disables the button for a second post-click.
        """
        
        self.setEnabled(False)
        
        if self.on_click_function:
            self.on_click_function()
        
        QTimer.singleShot(1000, lambda: self.setEnabled(True))
    

    def paintEvent(self, event):
        """
        ES: Pinta el fondo del botón con la imagen en uso.\n
        EN: Paints the background of the widget with the image in use.
        """
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.pixmap_in_use)
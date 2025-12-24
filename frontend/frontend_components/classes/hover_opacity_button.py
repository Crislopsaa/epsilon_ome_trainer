"""
ES: Este script crea la clase de un botón con una imagen que disminuye su opacidad cuando el ratón está sobre él.\n
EN: This script implements the class of a button with an image that lessens its opacity when the mouse is on it.
"""


from pathlib import Path

from PyQt5.QtWidgets import QPushButton, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HoverOpacityButton(QPushButton):
    """
    ES: Un botón cuya imagen se vuelve más transparente cuando el ratón está encima.\n
    EN: A button whose image becomes more transparent when the mouse is on it.
    
    :param image_path: Path to the icon image.
    :type image_path: Path
    :param on_click_function: Function to execute when clicked.
    :type on_click_function: callable
    """
    def __init__(self, image_path: Path, on_click_function: callable):
        super().__init__()
        
        # DEBUGGING
        if not all([image_path, on_click_function]):
            print("AVISO: Un botón de opacidad cambiante ha recibido algún parámetro vacío.")
        
        # eliminando bordes y fondo de la imagen
        # eliminating the image's borders and background
        self.setStyleSheet("border: none; background: transparent;")
        
        self.setCursor(Qt.PointingHandCursor)
        
        # el botón solo se seleccionará visualmente cuando se pulse el TAB
        # the button will only be visually focused when TAB is pressed
        self.setFocusPolicy(Qt.TabFocus)
        
        self.clicked.connect(on_click_function)

        # creando el contenedor de la imagen
        # creating the image label
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(str(image_path))
        
        # DEBUGGING
        if self.pixmap.isNull():
            print("ERROR: No se encuentra la imagen en un botón de opacidad cambiante")
        
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)

        # aplicando efecto de opacidad a la imagen
        # applying an opacity effect to the image
        self.opacity_effect = QGraphicsOpacityEffect()
        self.image_label.setGraphicsEffect(self.opacity_effect)

        self.opacity_effect.setOpacity(1)


    def enterEvent(self, event):
        """
        ES: Al pasar el ratón, la imagen se vuelve más transparente
        EN: When the mouse passes, the image becomes more transparent
        """
    
        self.opacity_effect.setOpacity(0.75)
        return super().enterEvent(event)
    

    def leaveEvent(self, event):
        """
        ES: Volviendo la imagen opaca de nuevo
        EN: aking the image opaque again
        """
        
        self.opacity_effect.setOpacity(1)
        return super().leaveEvent(event)
    
    
    def resizeEvent(self, event):
        """
        ES: Cuando la ventana cambia de tamaño, se ajusta la imagen
        EN: When the window changes its size, the image adapts
        """
        
        self.image_label.setFixedSize(self.width(), self.height())
        return super().resizeEvent(event)
"""
ES: Este script crea la clase de un botón con una imagen que disminuye su opacidad cuando el ratón está sobre él.\n
EN: This script creates the class of a button with an image that lessens its opacity when the mouse is on it.
"""


from PyQt5.QtWidgets import QPushButton, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HoverOpacityButton(QPushButton):
    """
    ES: Un botón cuya imagen se vuelve más transparente cuando el ratón está encima.\n
    EN: A button whose image becomes more transparent when the mouse is on it.
    
    :param image_path: Path to the icon image.
    :type image_path: str
    :param on_click_function: Function to execute when clicked.
    :type on_click_function: callable
    """
    def __init__(self, image_path: str, on_click_function: callable):
        super().__init__()
        
        # eliminando bordes y fondo de la imagen
        # eliminating the image's borders and background
        self.setStyleSheet("border: none; background: transparent;")
        
        self.setCursor(Qt.PointingHandCursor)
        
        # el botón solo se seleccionará visualmente cuando se pulse el TAB
        # the button will only be selected when TAB is clicked
        self.setFocusPolicy(Qt.TabFocus)
        
        self.clicked.connect(on_click_function)

        # creando el contenedor de la imagen
        # creating the image label
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # aplicando efecto de opacidad a la imagen
        # applying an opacity effect to the image
        self.opacity_effect = QGraphicsOpacityEffect()
        self.image_label.setGraphicsEffect(self.opacity_effect)

        self.opacity_effect.setOpacity(1)


    def enterEvent(self, event):
        # al pasar el ratón, la imagen se vuelve más transparente
        # when the mouse passes, the image becomes more transparent
        self.opacity_effect.setOpacity(0.75)
        return super().enterEvent(event)
    

    def leaveEvent(self, event):
        # volviendo la imagen opaca de nuevo
        # making the image opaque again
        self.opacity_effect.setOpacity(1)
        return super().leaveEvent(event)
    
    # cuando la ventana cambia de tamaño, se ajusta la imagen
    # when the window changes its size, the image adapts
    def resizeEvent(self, event):
        self.image_label.setFixedSize(self.width(), self.height())
        return super().resizeEvent(event)
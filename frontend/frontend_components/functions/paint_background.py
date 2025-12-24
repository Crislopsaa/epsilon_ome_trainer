"""
ES: Este script define una función que pinta el fondo de un widget con una imagen.\n
EN: This script defines a function that paints the background of a widget with an image.
"""


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt


def paint_background(widget: QWidget, painter: QPainter, pixmap: QPixmap):
    """
    ES: Pinta el fondo del widget con una imagen dada.\n
    EN: Paints the background of the widget with a given image.
    
    Usage:
        ES: Se debe ejecutar dentro del paintEvent del widget.
        EN: It must be executed inside the paintEvent of the widget.
    
    Warning:
        ES: El objeto QPainter debe estar activo (dentro de begin() y end() o un paintEvent).
        EN: The QPainter object must be active (inside begin() and end() or a paintEvent).
    
    :param widget: The widget to paint.
    :type widget: QWidget
    :param painter: The object that paints the image.
    :type painter: QPainter
    :param pixmap: The image that will be painted.
    :type pixmap: QPixmap
    """
    
    # si la imagen es nula, la función no hace nada
    # if the image is Null, the function does nothing
    if not pixmap.isNull():
        # escalando la imagen
        # scaling the image
        scaled_pixmap = pixmap.scaled(
            widget.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        
        # pintando la imagen
        # painting the image
        painter.drawPixmap(0, 0, scaled_pixmap)
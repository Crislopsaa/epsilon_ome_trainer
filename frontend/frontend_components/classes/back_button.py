"""
ES: Este script crea la clase del botón de retroceso.\n
EN: This script implements the class of the back button.
"""


from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush


class BackButton(QPushButton):
    """
    ES: Un botón para ir a la página anterior.\n
    EN: A button to return to the previous page.
    
    :param go_back_function: Function to return to the previous page.
    :type go_back_function: callable
    """
    def __init__(self, go_back_function: callable, parent: QWidget = None):
        super().__init__(parent)
        
        self.setFixedSize(55, 55)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4A90E2,
                    stop: 1 #2C6FBF
                );
                border: none;
                border-radius: 14px;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5BA0F0,
                    stop: 1 #3A80D0
                );
            }

            QPushButton:pressed {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1A4F8A,
                    stop: 1 #2C6FBF
                );
            }

            QPushButton:focus {
                border: 2px solid #A0C8FF;
                outline: none;
            }

            QPushButton:disabled {
                background-color: #CCCCCC;
            }
            """
        )
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)
        self.clicked.connect(go_back_function)

    def paintEvent(self, event):
        """
        ES: Pinta el fondo del botón con una flecha apuntando hacia la izquierda personalizada hecha con QPainter.
        
        EN: Paints the button's background with a custom QPainter-made left arrow.
        """

        # haciendo el paintEvent normal para que se aplique el QSS
        # executing the regular paintEvent for QSS application
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        # desplazamiento sutil al pulsar
        # slight movement when pulsed
        offset = 1 if self.isDown() else 0


        arrow_w = w * 0.44   # longitud total / total length
        arrow_h = h * 0.17   # grosor del cuerpo / shaft thickness
        head_w  = w * 0.20   # profundidad de la punta / arrowhead depth
        head_h  = h * 0.44   # altura total de la punta / arrowhead height

        ax = cx - arrow_w * 0.04 + offset
        ay = cy + offset

        tip_x   = ax - arrow_w / 2     # vértice de la punta / arrowhead vertex
        neck_x  = tip_x + head_w       # unión punta-cuerpo / where arrowhead and shaft join
        rect_end = ax + arrow_w / 2    # extremo derecho / right end (shaft end)

        tip_top = ay - head_h / 2
        tip_bot = ay + head_h / 2
        rect_top = ay - arrow_h / 2
        rect_bot = ay + arrow_h / 2

        path = QPainterPath()
        path.moveTo(tip_x,   ay)          # vértice izquierdo / tip vertex
        path.lineTo(neck_x,  tip_top)     # esquina superior punta / top arrowhead corner
        path.lineTo(neck_x,  rect_top)    # unión punta-cuerpo superior / top arrowhead-shaft join
        path.lineTo(rect_end, rect_top)   # extremo superior derecho / top right end
        path.lineTo(rect_end, rect_bot)   # extremo inferior derecho / bottom right end
        path.lineTo(neck_x,  rect_bot)    # unión punta-cuerpo inferior / bottom arrowhead-shaft join
        path.lineTo(neck_x,  tip_bot)     # esquina inferior punta / bottom arrowhead corner
        path.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawPath(path)
        painter.end()
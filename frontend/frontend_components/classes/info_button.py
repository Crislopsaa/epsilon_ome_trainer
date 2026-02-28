"""
ES: Este script implementa la clase de un botón que muestra una ventana con información al ser pulsado.

EN: This script implements the class of a button that displays information in a pop-up window when it is clicked.
"""


from pathlib import Path

from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, QRectF


class InfoButton(QPushButton):
    """
    ES: Botón que muestra una ventana con información al ser pulsado.
    
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
        
        self.window_title = window_title
        self.information = information
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)
        
        self.setFixedSize(30, 30)
        self.clicked.connect(self.show_info)
        
        self.apply_styles()
    
    
    def apply_styles(self):
        self.setStyleSheet(
            """
            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4A90E2,
                    stop: 1 #2C6FBF
                );
                border: none;
                border-radius: 7px;
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
        ES: Pinta el fondo del botón con un icono de información personalizado hecho con QPainter.
        
        EN: Paints the button's background with a custom QPainter-made information icon.
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
        scale = min(w, h)
        
        # parámetros de diseño del icono
        # icon design parameters
        dot_radius = scale * 0.11    
        body_w     = scale * 0.16       
        base_w     = scale * 0.40       
        cap_w      = scale * 0.28   # sobresale más a la izquierda / extends further left
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FFFFFF")))

        # 1. punto superior / top dot
        dot_y = cy - scale * 0.30 + offset
        painter.drawEllipse(QRectF(cx - dot_radius + offset, dot_y - dot_radius, dot_radius * 2, dot_radius * 2))

        # 2. cuerpo de la "i" / body of the "i"
        path = QPainterPath()
        
        top_y    = cy - scale * 0.12 + offset
        bottom_y = cy + scale * 0.32 + offset
        neck_y   = top_y + (scale * 0.08)
        base_h   = scale * 0.09    

        # trazado del cuerpo / path of the body
        path.moveTo(cx - cap_w / 2 + offset, top_y + (scale * 0.06)) # punta bandera / serif tip
        path.lineTo(cx + body_w / 2 + offset, top_y)                 # hombro derecho / right shoulder
        path.lineTo(cx + body_w / 2 + offset, bottom_y - base_h)     # lado derecho mástil / right shaft side
        path.lineTo(cx + base_w / 2 + offset, bottom_y - base_h)     # ala derecha base / right base wing
        path.lineTo(cx + base_w / 2 + offset, bottom_y)              # suelo derecho / right bottom
        path.lineTo(cx - base_w / 2 + offset, bottom_y)              # suelo izquierdo / left bottom
        path.lineTo(cx - base_w / 2 + offset, bottom_y - base_h)     # techo izquierdo base / left base top
        path.lineTo(cx - body_w / 2 + offset, bottom_y - base_h)     # lado izquierdo mástil / left shaft side
        path.lineTo(cx - body_w / 2 + offset, neck_y)                # cuello bandera / serif neck
        
        path.closeSubpath()
        painter.drawPath(path)

        painter.end()
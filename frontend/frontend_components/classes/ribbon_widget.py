"""
ES: Este script crea la clase del widget donde se muestra la configuración del problema.\n
EN: This script implements the class of the widget where the problem configuration is shown.
"""


from pathlib import Path

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background


class RibbonWidget(QWidget):
    """
    ES: El widget que muestra la configuración de problemas (sin botones).\n
    EN: A widget that displays problem configuration (without buttons).
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param current_option: The text to display.
    :type current_option: str
    """
    
    def __init__(self, base_path: Path, current_option: str):
        super().__init__()
        
        if not all([base_path, current_option]):
            print("AVISO: Un widget de lazo ha recibido algún parámetro vacío.")
        
        self.base_path = base_path
        
        # medida de seguridad por si el paintEvent se dispara antes que self.update_text_and_image()
        # security measure if the paintEvent is triggered before self.update_text_and_image()
        self.basic_ribbon_path = self.base_path / "assets" / "images" / "ribbon.png"
        self.basic_ribbon = QPixmap(str(self.basic_ribbon_path))
        
        self.pixmap_in_use = self.basic_ribbon
        
        
        # DEBUGGING
        if self.basic_ribbon.isNull():
            print("ERROR: No se encuentra la imagen del lazo básico.")
            

        main_layout = QHBoxLayout(self)

        # creando el contenedor donde se muestran las opciones
        # creating the label where the options are shown
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 25px; color: white; font-family: 'Rockwell Condensed'")
        
        main_layout.addWidget(self.text_label, alignment=Qt.AlignCenter)

        self.update_text_and_image(current_option)

    # definiendo un método que actualiza la imagen y el texto
    # defining a method that updates the widget's image and text
    def update_text_and_image(self, text: str):
        """
        ES: Actualiza el texto y la imagen del widget según el texto dado.\n
        EN: Updates the text and the image based on the given text.
        
        :param text: Option to display
        :type text: str
        """
        
        # actualizando el texto
        # updating the text
        self.text_label.setText(text)
        
        
        # actualizando la imagen
        # updating the image
        if text == "Regional":
            if not hasattr(self, "damaged_ribbon_path"):
                self.damaged_ribbon_path = self.base_path / "assets" / "images" / "damaged_ribbon.png"
                self.damaged_ribbon = QPixmap(str(self.damaged_ribbon_path))
            
            # DEBUGGING
            if self.damaged_ribbon.isNull():
                print("ERROR: No se encuentra la imagen del lazo dañado.")
                
            self.pixmap_in_use = self.damaged_ribbon    
            
            
        elif text == "Nacional":
            if not hasattr(self, "shattered_ribbon_path"):
                self.shattered_ribbon_path = self.base_path / "assets" / "images" / "shattered_ribbon.png"
                self.shattered_ribbon = QPixmap(str(self.shattered_ribbon_path))
            
            # DEBUGGING
            if self.shattered_ribbon.isNull():
                print("ERROR: No se encuentra la imagen del lazo destruido.")
            
            self.pixmap_in_use = self.shattered_ribbon
              
                
        elif text == "COMING SOON":
            if not hasattr(self, "old_ribbon_path"):
                self.old_ribbon_path = self.base_path / "assets" / "images" / "old_ribbon.png"
                self.old_ribbon = QPixmap(str(self.old_ribbon_path))
            
            # DEBUGGING
            if self.old_ribbon.isNull():
                print("ERROR: No se encuentra la imagen del lazo viejo.")
            
            self.pixmap_in_use =self.old_ribbon
            
        else:
            self.pixmap_in_use = self.basic_ribbon
        
        self.update()
    
 
    def paintEvent(self, event):
        """
        ES: Pinta el fondo del botón con la imagen en uso.\n
        EN: Paints the background of the widget with the image in use.
        """
        
        painter = QPainter(self)
        paint_background(widget = self, pixmap = self.pixmap_in_use, painter = painter)
        super().paintEvent(event)
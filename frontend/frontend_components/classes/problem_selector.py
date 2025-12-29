"""
ES: Este script crea la clase del selector de configuración de problemas.\n
EN: This script implements the class of the problem configuration selector.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.hover_opacity_button import HoverOpacityButton
from frontend.frontend_components.classes.ribbon_widget import RibbonWidget


class ProblemSelector(QWidget):
    """
    ES: Un selector de la configuración de problemas que usa imágenes de flechas como botones.\n
    EN: A problem configuration selector that uses arrow images as buttons.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param options: Options to display.
    :type options: list
    :param title: Title of the section.
    :type title: str
    """
    
    def __init__(self, base_path: Path, options: list, title: str = ""):
        super().__init__()
        
        self.options = options
        self.current_index = 0
        
        self.main_layout = QVBoxLayout()
        
        # estableciendo el título que indica de qué se trata la selección
        # setting the title that indicates what this section is about
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 40px; font-weight: bold; color: white; font-family: 'Rockwell Condensed'")
        self.main_layout.addWidget(self.title_label, alignment = Qt.AlignCenter)
        

        # obteniendo las rutas de las imágenes de las flechas
        # getting the arrow images paths
        self.left_arrow_path = base_path / "assets" / "images" / "left_arrow.png"
        self.right_arrow_path = base_path / "assets" / "images" / "right_arrow.png"
        
        # creando los botones "flecha"
        # creating the arrow buttons
        self.left_arrow = HoverOpacityButton(
            image_path = self.left_arrow_path,
            on_click_function = self.previous_option,
            )
        self.left_arrow.setFixedSize(100, 100)
        
        self.right_arrow = HoverOpacityButton(
            image_path = self.right_arrow_path,
            on_click_function = self.next_option,
            )
        self.right_arrow.setFixedSize(100, 100)
        
        
        # creando la sección donde se muestra lo que se ha elegido
        # creating the section where the chosen options is displayed
        self.option_label = RibbonWidget(base_path = base_path, current_option = self.get_value())
        self.option_label.setFixedSize(1000, 100)

        # usando layouts para organizar los widgets de manera flexible
        # using layouts to organize the widgets in a flexible way
        self.selector_layout = QHBoxLayout()
        self.selector_layout.addWidget(self.left_arrow)
        self.selector_layout.addSpacing(150)
        self.selector_layout.addWidget(self.option_label)
        self.selector_layout.addSpacing(150)
        self.selector_layout.addWidget(self.right_arrow)
        
        self.main_layout.addLayout(self.selector_layout)
        self.selector_layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(self.main_layout)


    def previous_option(self):
        """
        ES: Ir a la opción anterior.\n
        EN: Displays the previous option.
        """
        
        # uso del módulo para navegación circular
        # using modulo for circular navigation
        self.current_index = (self.current_index - 1) % len(self.options)
        self.update_display()
        

    def next_option(self):
        """
        ES: Ir a la opción siguiente.\n
        EN: Displays the next option.
        """
        
        # uso del módulo para navegación circular
        # using modulo for circular navigation
        self.current_index = (self.current_index + 1) % len(self.options)
        self.update_display()
        

    def update_display(self):
        """
        ES: Actualiza lo que se ve.\n
        EN: Updates what is displayed.
        """
        
        self.option_label.update_text_and_image(self.options[self.current_index])
        

    def get_value(self):
        """
        ES: Obtiene el valor mostrado.
        EN: Gets the value displayed.
        """
        
        return self.options[self.current_index]
"""
ES: Este script crea la clase del botón de retroceso.\n
EN: This script implements the class of the back button.
"""


from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


class BackButton(QPushButton):
    """
    ES: Un botón para ir a la página anterior.\n
    EN: A button to return to the previous page.
    
    :param go_back_function: Function to return to the previous page.
    :type go_back_function: callable
    """
    def __init__(self, go_back_function: callable):
        super().__init__()
        
        # DEBUGGING
        if not go_back_function:
            print("AVISO: No se le ha pasado ninguna función a un botón de retroceso.")
        
        self.setFixedSize(40, 40)
        self.setText("⬅")
        self.setStyleSheet("font-size: 20px; padding: 6px")
        
        self.setCursor(Qt.PointingHandCursor)
        
        # el botón solo se seleccionará visualmente cuando se pulse el TAB
        # the button will only be visually focused when TAB is pressed
        self.setFocusPolicy(Qt.TabFocus)
        
        self.clicked.connect(go_back_function)
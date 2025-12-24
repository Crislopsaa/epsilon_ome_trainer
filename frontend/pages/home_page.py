"""
ES: Este script define la clase de la página de inicio.\n
EN: This script defines the home page class.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class HomePage(QWidget):
    """
    ES: Página de inicio que permite navegar a la configuración de problemas, información y estadísticas.\n
    EN: The main entry point, providing navigation to problem configuration, information, and user statistics.
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path):
        super().__init__()
        
        self.base_path = base_path
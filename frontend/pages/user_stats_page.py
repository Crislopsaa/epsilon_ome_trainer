"""
ES: Este script define la clase de la página de estadísticas del usuario.\n
EN: This script defines the user stats page class.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class UserStatsPage(QWidget):
    """
    ES: La página que muestra las estadísticas del usuario.\n
    EN: The page that displays the user stats.
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path):
        super().__init__()
        
        self.base_path = base_path
"""
ES: Este script define la clase de la página de información.\n
EN: This script implements the information page class.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

from pathlib import Path

class InformationPage(QWidget):
    """
    ES: La página que muestra información sobre Epsilon.\n
    EN: The page that displays information about Epsilon.
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path
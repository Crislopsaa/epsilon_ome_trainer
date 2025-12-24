"""
ES: Este script define la clase de la página de configuración de problemas.\n
EN: This script defines the problem configuration page class.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

from pathlib import Path

from frontend.pages.generated_problem_page import GeneratedProblemPage

class ProblemConfigurationPage(QWidget):
    """
    ES: La página donde se configuran los ajustes del problema.\n
    EN: The page for configuring the problem settings.
    """
    
    change_page_signal = pyqtSignal(str)
    create_generated_problem_page_signal = pyqtSignal(GeneratedProblemPage)
    
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path
"""
ES: Este script define la clase de la página de problemas generados.\n
EN: This script implements the problem page class.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class GeneratedProblemPage(QWidget):
    """
    ES: La página que muestra los problemas que el usuario tiene que resolver.\n
    EN: The page that displays the problems for the user to solve.
    """
    
    change_page_signal = pyqtSignal(str)
    user_stats_changed_signal = pyqtSignal()
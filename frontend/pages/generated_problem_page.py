"""
ES: Este script define la clase de la página de problemas generados.\n
EN: This script implements the problem page class.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class GeneratedProblemPage(QWidget):
    """
    ES: La página que muestra los problemas que el usuario tiene que resolver.\n
    EN: The page that displays the problems for the user to solve.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param course: Course of the problem to display.
    :type course: str
    :param difficulty: Difficulty of the problem to display.
    :type difficulty: str
    :param topic: Topic of the problem to display
    :type topic: str
    """
    
    change_page_signal = pyqtSignal(str)
    user_stats_changed_signal = pyqtSignal()
    
    def __init__(self, base_path: Path, course_selected: str, difficulty_selected: str, topic_selected: str):
        super().__init__()
        pass
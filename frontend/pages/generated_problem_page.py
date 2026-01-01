"""
ES: Este script implementa la clase de la página de problemas generados.\n
EN: This script implements the problem page class.
"""


from pathlib import Path
import tempfile

from PyQt5.QtWidgets import QWidget, QStackedWidget, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import pyqtSignal, Qt

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.back_button import BackButton
from frontend.frontend_components.classes.formulation_widget import FormulationWidget
from frontend.frontend_components.classes.procedure_widget import ProcedureWidget

# importando funciones personalizadas
# importing custom functions
from backend.backend_components.db_functions.get_problem_data import get_problem_data
from backend.backend_components.db_functions.register_success_or_mistake import register_success_or_mistake
from backend.backend_components.db_functions.get_db_path import get_db_path
from backend.backend_components.other_functions.check_user_answer import check_user_answer
from backend.backend_components.other_functions.latex2pdf import latex2pdf
from frontend.frontend_components.functions.paint_background import paint_background


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
        
        self.base_path = base_path
        self.db_path = get_db_path()

        # creando el pixmap del fondo
        # creating the background's pixmap
        self.background_path = self.base_path / "assets" / "images" / "problems_page_background.png"
        self.background = QPixmap(str(self.background_path))
        
        self.course_selected = course_selected
        self.difficulty_selected = difficulty_selected
        self.topic_selected = topic_selected
        
        # no se manejan las excepciones aquí por que ya se hace en la página de configuración
        # exceptions are not managed here because they are done so in the configuration page
        self.formulation, self.procedure, self.short_solution = get_problem_data(
            db_path = self.db_path,
            course = course_selected,
            difficulty = difficulty_selected,
            topic = topic_selected,
            )            
        

        self.main_layout = QVBoxLayout()
        
        self.back_button = BackButton(self.go_back)
        self.main_layout.addWidget(self.back_button, alignment = Qt.AlignTop | Qt.AlignLeft)
        
        # creando el stack donde se muestra el enunciado y el procedimiento del problema
        # creating the stack where the problem formulation and procedure are shown
        self.problem_stack = QStackedWidget()
        self.main_layout.addWidget(self.problem_stack, alignment = Qt.AlignCenter)
        
        # creando un directorio temporal para guardar el PDF del enunciado
        # creating a temporary directory to save the formulation's PDF
        self.formulation_temp_dir = tempfile.TemporaryDirectory()
        self.formulation_temp_dir_path = Path(self.formulation_temp_dir.name)
        
        # convirtiendo el enunciado en un PDF
        # turning the formulation into a PDF    
        self.formulation_pdf_path = self.formulation_temp_dir_path / "problem_formulation.pdf"
        
        # creando el PDF del enunciado
        # creating the formulation PDF
        latex2pdf(latex_code = self.formulation, output_path = self.formulation_pdf_path)
        
        self.formulation_widget = FormulationWidget(
            base_path = self.base_path,
            pdf_path = str(self.formulation_pdf_path),
            verify_function = self.show_procedure
            )
        self.problem_stack.addWidget(self.formulation_widget)
        
        self.setLayout(self.main_layout)


    # definiendo la función que cambia el enunciado por el procedimiento
    # defining a function that changes the formulation for the procedure    
    def show_procedure(self):
        """
        ES: Comprueba si la respuesta del usuario es correcta y cambia el widget del enunciado por el del procedimiento.\n
        EN: Checks if the user answer is correct and switches the formulation widget for the procedure one.
        """
        
        self.user_answer = self.formulation_widget.user_answer_field.text().strip()
        
        # si el campo de respuesta está vacío, se muestra un mensaje de aviso
        # if the answer's field is empty, a warning message is shown
        if not self.user_answer:
            QMessageBox.warning(
                self.window(),
                "DEBE INGRESAR UNA RESPUESTA",
                "Por favor, ingrese una respuesta."
                )
            return
        
        # obteniendo la respuesta del usuario y comprobándola
        # getting the user's answer and checking it
        self.user_answer_status = check_user_answer(
            correct_answer = self.short_solution,
            user_answer = self.user_answer
            )
        
        # registrando el resultado en la base de datos local
        # registering the result in he local database
        register_success_or_mistake(
            db_path = self.db_path,
            user_answer_status = self.user_answer_status,
            course = self.course_selected, 
            difficulty = self.difficulty_selected,
            topic = self.topic_selected
            )
        
        # borrando la página de estadísticas del usuario porque las estadísticas han cambiado
        # deleting user's stats' page because the stats have changed
        self.user_stats_changed_signal.emit()
        
        # creando un directorio temporal para guardar el PDF del procedimiento
        # creating a temporary directory to save the procedure's PDF
        self.procedure_temp_dir = tempfile.TemporaryDirectory()
        self.procedure_temp_dir_path = Path(self.procedure_temp_dir.name)
        
        self.procedure_pdf_path = self.procedure_temp_dir_path / "problem_procedure.pdf"
        
        # creando el PDF del enunciado
        # creating the formulation PDF
        latex2pdf(latex_code = self.procedure, output_path = self.procedure_pdf_path)
        
        # creando y mostrando el widget del procedimiento
        # creating and showing the procedure's widget
        procedure_widget = ProcedureWidget(
            pdf_path = self.procedure_pdf_path,
            user_answer_status = self.user_answer_status
            )
        
        self.problem_stack.addWidget(procedure_widget)
        self.problem_stack.setCurrentWidget(procedure_widget)            
        
           
    def go_back(self):
        """
        ES: Cambia la página por la página de configuración de problemas.\n
        EN: Switches the page to the problem configuration page.
        """
        
        self.change_page_signal.emit("problem configuration page")
    
    
    def closeEvent(self, event):
        """
        ES: Cuando se elimina el widget, también se eliminan los directorios temporales.\n
        EN: Cuando the widget is deleted, the temporary directories are also deleted.
        """
        if hasattr(self, "formulation_temp_dir"):
            try:
                self.formulation_temp_dir.cleanup()
                del self.formulation_temp_dir
                
            except Exception as e:
                print(f"ERROR: No se ha podido borrar el PDF del enunciado:\n{e}")
            
        if hasattr(self, "procedure_temp_dir"):
            try:
                self.procedure_temp_dir.cleanup()
                del self.procedure_temp_dir
                
            except Exception as e:
                print(f"ERROR: No se ha podido borrar el PDF del procedimiento:\n{e}")
            
        return super().closeEvent(event)
    
    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo con una imagen.\n
        EN: Paints the background with an image.
        """
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        return super().paintEvent(event)

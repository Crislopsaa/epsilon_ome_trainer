"""
ES: Este script define la clase de la página de configuración de problemas.\n
EN: This script implements the problem configuration page class.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal

# importando clases personalizadas
# importing custom classes
from frontend.pages.generated_problem_page import GeneratedProblemPage
from frontend.frontend_components.classes.problem_selector import ProblemSelector
from frontend.frontend_components.classes.hover_image_swap_button import HoverImageSwapButton
from frontend.frontend_components.classes.back_button import BackButton

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background


class ProblemConfigurationPage(QWidget):
    """
    ES: La página donde se configuran los ajustes del problema.\n
    EN: The page for configuring the problem settings.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    """
    
    change_page_signal = pyqtSignal(str)
    create_generated_problem_page_signal = pyqtSignal(GeneratedProblemPage)
    
    def __init__(self, base_path: Path):
        super().__init__()
        self.base_path = base_path
        
        self.main_layout = QVBoxLayout()
        
        # creando el pixmap del fondo
        # creating the background's pixmap
        self.background_path = base_path / "assets" / "images" / "problems_page_background.png"
        self.background = QPixmap(str(self.background_path))
        
        self.back_button = BackButton(self.go_back_to_home)
        self.main_layout.addWidget(self.back_button, alignment = Qt.AlignTop | Qt.AlignLeft)
        
        # creando el título principal
        # creating the main title
        self.title = QLabel("PROBLEMAS")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
                                font-size: 75px;
                                font-weight: bold;
                                font-family: 'Rockwell Condensed';
                                color: #ffffff;
                                """)
        self.main_layout.addWidget(self.title)
        self.main_layout.addStretch()

        # creando los selectores de las opciones d eproblema
        # creating the selectors of problem options
        self.grade_select = ProblemSelector(
            base_path = self.base_path,
            options = ["1º y 2º ESO", "COMING SOON"],
            title="Curso"
            )
        self.main_layout.addWidget(self.grade_select, alignment = Qt.AlignCenter)
        
        
        self.difficulty_select = ProblemSelector(
            base_path = self.base_path,
            options = ["Provincial", "Regional", "Nacional"],
            title="Dificultad"
            )
        self.main_layout.addWidget(self.difficulty_select, alignment = Qt.AlignCenter)
        
        
        self.topic_select = ProblemSelector(
            base_path = self.base_path,
            options = [
                "Aritmética y Teoría de Números",
                "Álgebra",
                "Geometría",
                "Combinatoria y Probabilidad",
                "Lógica y Razonamiento"
                ],
            title="Temática"
            )
        self.main_layout.addWidget(self.topic_select, alignment = Qt.AlignCenter)
        self.main_layout.addStretch()
        
        
        # obteniendo las rutas de las imágenes del botón cambia a la siguiente página
        # obtaining the paths of the images of the button that changes the current page to the next one
        self.black_anvil_path = base_path / "assets" / "images" / "black_anvil.png"
        self.golden_anvil_path = base_path / "assets" / "images" / "golden_anvil.png"
        
        # creando ese botón
        # creating that button
        self.generate_button = HoverImageSwapButton(
            static_image_path = self.black_anvil_path,
            swap_image_path = self.golden_anvil_path,
            on_click_function = self.generate_problem
            )
        self.generate_button.setFixedSize(200, 100)
        self.main_layout.addWidget(self.generate_button, alignment = Qt.AlignCenter)
        self.main_layout.addStretch()
        
        self.setLayout(self.main_layout)

    
    def generate_problem(self):
        """
        ES: Crea la página que muestra el problema generado.\n
        EN: Creates the problem page that displays the generated problem.
        """
        
        # si no se selecciona un curso válido, se muetra una ventana informándolo
        # if a valid course is not selected, a warning window is displayed
        if self.grade_select.get_value() == "COMING SOON":
            QMessageBox.warning(
                self.window(),
                "CURSO NO DISPONIBLE",
                "En el futuro se añadirán más cursos, pero de momento solo están disponibles los mostrados."
            )
            return
        
        # obteniendo las características del problema
        # getting the problem settings
        self.grade_selected = self.grade_select.get_value()
        self.difficulty_selected = self.difficulty_select.get_value()
        self.topic_selected = self.topic_select.get_value()
        
        # creando la página que muestra problema con estas características
        # creating the page that displays a problem with these settings
        try:
            self.generated_problem_page = GeneratedProblemPage(
                base_path = self.base_path,
                grade_selected = self.grade_selected,
                difficulty_selected = self.difficulty_selected,
                topic_selected = self.topic_selected
                )
            self.emit_generated_problem_page_to_epsilon()
            return
        
        # manejando las excepciones posibles
        # managing posible exceptions
        
        # get_problem_data error
        except LookupError:
            QMessageBox.warning(
                self.window(),
                "NO HAY PROBLEMAS",
                "Lo siento, ahora mismo no hay ningún problema generado que cumpla esas características, inténtalo más tarde."
                )
        
        # latex2pdf error
        except RuntimeError as e:
            QMessageBox.critical(
                self.window(),
                "ERROR AL CREAR EL PROBLEMA",
                f"Me temo que ha ocurrido un error al crear el PDF del problema:\n{e}"
                )
        
        # FALLBACK
        except Exception as e:
            QMessageBox.critical(
                self.window(),
                "ERROR AL CREAR LA PÁGINA",
                f"Me temo que ha ocurrido un error a la hora de crear la página con el problema:\n{e}"
            )
        
        # si ha habido un error, se elimina la página de problemas
        # if an error has happened, the problem page is eliminated   
        try:
            if hasattr(self, "generated_problem_page"):
                self.generated_problem_page.setParent(None)
                self.generated_problem_page.deleteLater()
                del self.generated_problem_page
        
        except Exception as e:
            # DEBUGGING
            print(f"ERROR: No se ha podido eliminar una página con problemas defectuosos con éxito:\n {e}")
            

    
    def go_back_to_home(self):
        """
        ES: Cambia la página por la página de inicio.\n
        EN: Switches the page to the home page.
        """
        
        self.change_page_signal.emit("home page")


    def emit_generated_problem_page_to_epsilon(self):
        """
        ES: Envía la página que muestra el problema al script principal.\n
        EN: Emits the page that displays the problem to the main script.
        """
        
        self.create_generated_problem_page_signal.emit(self.generated_problem_page)
        
        # eliminando su referencia para evitar conflictos futuros
        # deleting its reference to avoid future conflicts
        del self.generated_problem_page

    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo con una imagen.\n
        EN: Paints the background with an image.
        """
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        super().paintEvent(event)
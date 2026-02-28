"""
ES: Este script define la clase de la página de configuración de problemas.

EN: This script implements the problem configuration page class.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal

# CLASES / CLASSES
from frontend.pages.generated_problem_page import GeneratedProblemPage

from frontend.frontend_components.classes.problem_selector import ProblemSelector
from frontend.frontend_components.classes.hover_image_swap_button import HoverImageSwapButton
from frontend.frontend_components.classes.back_button import BackButton
from frontend.frontend_components.classes.problem_generation_button import ProblemGenerationButton

from backend.backend_components.classes.exceptions import PDFLatexNotFoundError

# FUNCIONES / FUNCTIONS
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
    
    def __init__(self, base_path: Path, db_path: Path | str):
        super().__init__()
        self.base_path = base_path
        self.db_path = db_path
        
        self.main_layout = QVBoxLayout()
        
        self.background_path = base_path / "assets" / "images" / "problems_page_background.png"
        self.background = QPixmap(str(self.background_path))
        
        self.back_button = BackButton(self.go_back_to_home, self)
        self.back_button.setGeometry(20, 20, 40, 40)
        
        self.problem_generation_button = ProblemGenerationButton(
            base_path = self.base_path,
            db_path = self.db_path,
            parent = self
            )
        self.problem_generation_button.setGeometry(1845, 20, 55, 55)


        self.main_layout.addSpacing(50)
        self.title = QLabel("PROBLEMAS")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(
            """
            font-size: 75px;
            font-weight: bold;
            font-family: 'Rockwell Condensed';
            color: #ffffff;
            """
            )
        self.title.setMaximumWidth(1200)
        self.main_layout.addWidget(self.title, alignment = Qt.AlignCenter)
        self.main_layout.addStretch()


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
        
        
        self.black_anvil_path = base_path / "assets" / "images" / "black_anvil.png"
        self.golden_anvil_path = base_path / "assets" / "images" / "golden_anvil.png"
        
        self.generate_button = HoverImageSwapButton(
            static_image_path = self.black_anvil_path,
            swap_image_path = self.golden_anvil_path,
            on_click_function = self.init_problem_page
            )
        self.generate_button.setFixedSize(200, 100)
        self.main_layout.addWidget(self.generate_button, alignment = Qt.AlignCenter)
        self.main_layout.addStretch()
        
        self.setLayout(self.main_layout)

    
    def init_problem_page(self) -> None:
        """
        ES: Crea la página que muestra el problema generado.
        
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
        
        
        # get_problem_data error
        except LookupError:
            QMessageBox.warning(
                self.window(),
                "NO HAY PROBLEMAS",
                "Lo siento, ahora mismo no hay ningún problema generado que cumpla esas características, inténtalo más tarde."
                )


        # latex2pdf error
        except PDFLatexNotFoundError:
            QMessageBox.critical(
                self.window(),
                "NO SE ENCUENTRA PDFLATEX",
                "Lo siento, no se encuentra pdflatex. Si usted está en Windows, Ubuntu, Debian o Fedora, este se debería haber instalado automáticamente. En caso de que esté en Mac, debe instalar MacTex por su cuenta y ejecutar su instalador."
                )
            
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
        
        # Limpieza de recursos en caso de error para evitar fugas de memoria
        # Resource cleanup on error to prevent memory leaks  
        try:
            if hasattr(self, "generated_problem_page"):
                self.generated_problem_page.setParent(None)
                self.generated_problem_page.deleteLater()
                del self.generated_problem_page
        
        except Exception as e:
            # DEBUGGING
            print(f"ERROR: No se ha podido eliminar una página con problemas defectuosos con éxito:\n {e}")
            

    
    def go_back_to_home(self) -> None:
        """
        ES: Cambia la página por la página de inicio.
        
        EN: Switches the page to the home page.
        """
        self.change_page_signal.emit("home page")


    def emit_generated_problem_page_to_epsilon(self) -> None:
        """
        ES: Envía la página que muestra el problema al script principal.
        
        EN: Emits the page that displays the problem to the main script.
        """
        self.create_generated_problem_page_signal.emit(self.generated_problem_page)
        
        # eliminando su referencia para evitar conflictos futuros
        # deleting its reference to avoid future conflicts
        del self.generated_problem_page

    
    def paintEvent(self, event) -> None:
        """
        ES: Pinta el fondo con una imagen.
        
        EN: Paints the background with an image.
        """
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        super().paintEvent(event)
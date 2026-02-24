"""
ES: Este script implementa un botón personalizado que permite al usuario solicitar la generación de problemas.

EN: This script implements a custom button that allows the user to request problem generation.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QThread, QRectF

# importando funciones personalizadas
# importing custom functions
from backend.problem_generator.manage_problem_generation import manage_problem_generation

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.problem_generation_dialog import ProblemGenerationDialog
from frontend.frontend_components.classes.generation_loading_screen import GenerationLoadingScreen

from backend.backend_components.classes.worker import Worker
from backend.backend_components.classes.exceptions import GenerationStopException


class ProblemGenerationButton(QPushButton):
    """
    ES: Botón personalizado que permite al usuario solicitar la generación de problemas.

    EN: Custom button that allows the user to request problem generation.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param db_path: Absolute path to the local SQLite database.
    :type db_path: Path | str
    :param parent: The widget that contains this custom button.
    :type parent: QWidget
    """
    def __init__(self, base_path: Path, db_path: Path | str, parent: QWidget = None):
        super().__init__(parent)
        
        self.base_path = base_path
        self.db_path = db_path
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)
        
        self.setStyleSheet(
            """
            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #7DB63A,
                    stop: 1 #5A8F20
                );
                border: none;
                border-radius: 12px;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #8ECC44,
                    stop: 1 #6AA028
                );
            }

            QPushButton:pressed {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #3D6610,
                    stop: 1 #5A8F20
                );
            }

            QPushButton:focus {
                border: 2px solid #AEDD6A;
                outline: none;
            }

            QPushButton:disabled {
                background-color: #CCCCCC;
            }
            """
        )
        
        self.clicked.connect(self.display_dialog)
    
    
    
    def display_dialog(self):
        """
        ES: Muestra un ProblemGenerationDialog, que permite al usuario gestionar la generación de problemas.
        
        EN: Displays a ProblemGenerationDialog, which allows the user to manage problem generation.
        """
        self.problem_generation_window = ProblemGenerationDialog(self.window(), self.base_path)
        
        # la selección de problemas del usuario se envía por pyqtSignal
        # the user's problem selection is sent through pyqtSignal
        self.problem_generation_window.generation_request[int].connect(self.manage_threads)
        self.problem_generation_window.generation_request[tuple].connect(self.manage_threads)
        
        self.problem_generation_window.exec_()
        
    
    def manage_threads(self, generation_request: tuple[str, str, str, int] | int):
        """
        ES: Maneja el hilo secundario y el objeto Worker para poder generar problemas asíncronamente.
        
        EN: Manages the secondary thread and the Worker object to generate problems asynchronously.
        
        :param generation_request: Problem to generate. Either a tuple (Grade, Difficulty, Topic, Quantity) to specify the problem type or just a quantity (int) can be provided.
        :type generation_request: tuple[str, str, str, int] | int
        """
        
        ai_path = self.base_path / "assets" / "ai" / "epsilon.gguf"
        
        if self.problem_generation_window is not None:
            self.problem_generation_window.close()
        
        self._generation_finished = False
        
        quantity = generation_request if isinstance(generation_request, int) else generation_request[3]
        
        self.loading_screen = GenerationLoadingScreen(parent = self.window(), number_of_problems = quantity)
        self.loading_screen.early_close_signal.connect(self.handle_close)
        
        self.problem_generation_thread = QThread()
        self.worker = Worker()
        self.worker.function_to_run = manage_problem_generation
        
        # los argumentos deben estar en el orden definido en function_to_run
        # the arguments must be in the same order as they were defined in function_to_run
        self.worker.args = (
        ai_path,
        self.db_path, 
        generation_request,
        self.worker,
        self.worker.progress_signal.emit
        )  

        self.worker.error_signal.connect(self.handle_errors)
        self.worker.finish_signal.connect(self.finish_problem_generation)
        self.worker.progress_signal.connect(self.loading_screen.update_loading_screen)
        self.worker.moveToThread(self.problem_generation_thread)
        
        self.problem_generation_thread.finished.connect(self.problem_generation_thread.deleteLater)
        self.problem_generation_thread.started.connect(self.worker.run)
        
        self.loading_screen.show()
        QApplication.processEvents()
        self.problem_generation_thread.start()
    
    
    def _cleanup_worker(self):
        """
        ES: Desconecta señales y agenda la destrucción del worker.
        
        EN: Disconnects signals and schedules worker destruction.
        """
        worker = getattr(self, "worker", None)
        if worker:
            try:
                worker.progress_signal.disconnect()
                worker.finish_signal.disconnect()
                worker.error_signal.disconnect()
            except (RuntimeError, TypeError):
                pass

            worker.setParent(None)
            worker.deleteLater()
    
    
    def _cancel_thread(self):
        """
        ES: Elimina el hilo secundario junto con el Worker.
        
        EN: Deletes the secondary thread along with the Worker.
        """
        thread = getattr(self, "problem_generation_thread", None)
        if thread and thread.isRunning():
            thread.requestInterruption()
            thread.quit()
            thread.wait()

        self._cleanup_worker()

        self.problem_generation_thread = None
        self.worker = None  
        
    
    def finish_problem_generation(self):
        """
        ES: Cuando la generación termina, se eliminan el hilo secundario y Worker.
        
        EN: When generation ends, both the thread and the Worker are deleted.
        """
        self._generation_finished = True
        self._cancel_thread()
        
    
    def handle_close(self):
        """
        ES: Gestiona la eliminación del hilo secundario y el Worker el usuario cierra la pantalla de carga antes de tiempo.
        
        EN: Manages the deletion of the secondary thread and the Worker if the user closes the loading screen before the generation ends.
        """
        if self._generation_finished:
            return
        self._cancel_thread()
    
    
    def handle_errors(self, error: Exception):
        """
        ES: gestiona la eliminación del hilo secundario y del Worker si ocurre un error en la generación.
        
        EN: Manages elimination of the secondary thread and the Worker when an error occurs during problem generation.
        """
        self._generation_finished = True
        self._cancel_thread()

        # error guardando un problema
        # error when saving a problem
        if isinstance(error, RuntimeError):
            QMessageBox.critical(
                self.window(),
                "ERROR AL GUARDAR LOS PROBLEMAS",
                f"Me temo que ha ocurrido un error al guardar un problema:\n\n{error}"
            )

        # el usuario para la generación de problemas
        # the user stops problem generation
        elif isinstance(error, GenerationStopException):
            pass

        # FALLBACK
        else:
            QMessageBox.critical(
                self.window(),
                "ERROR AL GENERAR LOS PROBLEMAS",
                f"Me temo que ha ocurrido un error a la hora de generar los problemas:\n\n{error}"
            )
    
    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo del botón con una cruz personalizado hecho con QPainter.
        
        EN: Paints the button's background with a custom QPainter-made cross.
        """
        
        # haciendo el paintEvent normal para que se aplique el QSS
        # executing the regular paintEvent for QSS application
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        # desplazamiento sutil al pulsar
        # slight movement when pulsed
        offset = 1 if self.isDown() else 0


        arm_long = w * 0.29
        arm_thick = w * 0.09
        radius = arm_thick * 0.4


        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FFFFFF")))

        h_rect = QRectF(
            cx - arm_long  + offset,
            cy - arm_thick + offset,
            arm_long * 2,
            arm_thick * 2
        )
        painter.drawRoundedRect(h_rect, radius, radius)

        v_rect = QRectF(
            cx - arm_thick + offset,
            cy - arm_long  + offset,
            arm_thick * 2,
            arm_long * 2
        )
        painter.drawRoundedRect(v_rect, radius, radius)
        
        painter.end()
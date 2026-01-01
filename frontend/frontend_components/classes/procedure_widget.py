"""
ES: Este script implementa la clase del widget en el que se muestra el procedimiento de los problemas.\n
EN: This script implements the class of the widget where the problems' procedure is displayed.
"""


from pathlib import Path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.classes.pdf_viewer import PDFViewer


class ProcedureWidget(QWidget):
    """
    ES: El widget donde se muestra el procedimiento del problema y un botón para descargarlo.\n
    EN: The widget where the problem procedure and a button to download it are displayed.
    
    :param pdf_path: Absolute path of the PDF that contains the problem procedure.
    :type pdf_path: str | Path
    :param user_answer_status: Whether the user's answer was right (True) or not (False). Optional: False by default.
    :param user_answer_status: bool
    """
    def __init__(self, pdf_path: str | Path, user_answer_status: bool = False):
        super().__init__()
        self.pdf_path_str = str(pdf_path) # required by PDFViewer and shutil.copy
        self.pdf_path_pathlib = Path(pdf_path) # required to check if the PDF exists
        
        self.main_layout = QVBoxLayout()

        self.procedure_title = QLabel()
        self.procedure_title.setText("SOLUCIÓN DEL PROBLEMA")
        self.procedure_title.setStyleSheet("""
                                            font-size: 75px;
                                            font-weight: bold;
                                            font-family: 'Rockwell Condensed';
                                            color: #ffffff;
                                            """)
        self.main_layout.addWidget(self.procedure_title, alignment = Qt.AlignCenter | Qt.AlignTop)
        
        # creando un mensaje de acierto o error
        # creating an success or mistake message
        self.status_label = QLabel()
        self.status_label.setFixedSize(500, 50)
        
        if user_answer_status:
            self.status_label.setText("Muy bien, has contestado correctamente el problema.")
            self.status_label.setStyleSheet(
                """
                font-size: 20px;
                color: #ffffff;
                background-color: #53f5a1;
                font-family: 'Rockwell Condensed';
                padding: 5px;
                border-radius: 10px;
                """
                )

        else:
            self.status_label.setText("Lo siento, pero te has equivocado. Revisa la solución.")
            self.status_label.setStyleSheet(
                """
                font-size: 20px;
                color: #ffffff;
                background-color: #fa4141;
                font-family: 'Rockwell Condensed';
                padding: 5px;
                border-radius: 10px;
                """
                )

        self.main_layout.addWidget(self.status_label, alignment = Qt.AlignCenter)
        

        self.pdf_viewer = PDFViewer(self.pdf_path_str)
        self.pdf_viewer.setFixedSize(500, 650)
        self.main_layout.addWidget(self.pdf_viewer, alignment = Qt.AlignCenter)
        
        # creando el botón para descargar el procedimiento problema como PDF
        # creating the button to download the problem's procedure as a PDF
        self.download_button = QPushButton()
        self.download_button.setText("DESCARGAR PROBLEMA COMO PDF")
        self.download_button.setFixedSize(500, 50)
        self.download_button.setStyleSheet(
            """
            font-family: 'Rockwell Condensed';
            font-size: 20px;
            color: #ffffff;
            background-color: #3140e8;
            border-radius: 15px;
            """
            )
        self.download_button.clicked.connect(self.download_problem)
        self.main_layout.addWidget(self.download_button, alignment = Qt.AlignCenter)
        

        self.setLayout(self.main_layout)
        
    
    def download_problem(self):
        """
        ES: Descarga el problema como un PDF en la ruta que el usuario elija.\n
        EN: Downloads the problem as a PDF in the path that the user chooses. 
        """
        
        # si no se encuentra el PDF, se muestra un mensaje de error
        # if the PDF is not found, an error message is shown
        if not self.pdf_path_pathlib.exists():
            QMessageBox.critical(self.window(), "PDF NO ENCONTRADO", "Lo siento, pero no se encuentra el PDF.")
            return

        # creando el diálogo para elegir dónde guardar el PDF
        # creating the dialogue to choose where to save the PDF
        destination_path, _ = QFileDialog.getSaveFileName(
            self.window(),
            "GUARDAR PROBLEMA COMO PDF",
            "problema_epsilon.pdf",
            "Archivos PDF (*.pdf)"
        )

        # cuando se elige una ruta, se intenta guardar el PDF
        # when a path is chosen, the program tries to save the PDF
        if destination_path:
            try:
                shutil.copyfile(self.pdf_path_str, destination_path)
                # si no hay ningún error, se informa al usuario de que el PDF se ha guardado exitosamente
                # if there is no error, the user is informed that the PDF has been saved successfully
                QMessageBox.information(
                    self.window(),
                    "PDF GUARDADO EXITOSAMENTE",
                    f"El problema en PDF ha sido guardado en:\n{destination_path}"
                    )
                
            # si hay un error, se muestra un mensaje de error
            # if an error happens, an error message is shown    
            except Exception as e:
                QMessageBox.critical(
                    self.window(),
                    "ERROR AL COPIAR EL PDF",
                    f"No se pudo copiar el PDF:\n{e}"
                    )
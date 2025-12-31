"""
ES: Este script implementa la clase del widget que muestra el enunciado de los problemas.\n
EN: This script implements the class of the widget that displays the problems' formulation.
"""


from pathlib import Path

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.pdf_viewer import PDFViewer
from frontend.frontend_components.classes.info_button import InfoButton


class FormulationWidget(QWidget):
    """
    ES: El widget donde se muestra el enunciado del problema y una sección para la entrada de la respuesta.\n
    EN: The widget where the problem formulation and a section for the answer input are displayed.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    :param pdf_path: Absolute path to the PDF that contains the problem's formulation.
    :type pdf_path: str
    :param verify_function: The function that checks if the user's answer is correct and switches to the procedure widget.
    :type verify_function: callable
    """
    
    def __init__(self, base_path: Path, pdf_path: str, verify_function: callable):      
        super().__init__()
        
        self.main_layout = QVBoxLayout()
        
        self.title = QLabel()
        self.title.setText("ENUNCIADO DEL PROBLEMA")
        self.title.setStyleSheet(
            """
            font-size: 75px;
            font-weight: bold;
            font-family: 'Rockwell Condensed';
            color: #ffffff;
            """
            )
        self.main_layout.addWidget(self.title, alignment = Qt.AlignCenter | Qt.AlignTop)
        
        
        self.pdf_viewer = PDFViewer(pdf_path)
        self.pdf_viewer.setFixedSize(500, 650)
        self.main_layout.addWidget(self.pdf_viewer, alignment = Qt.AlignCenter)
        self.main_layout.addStretch()
        
        
        # creando la zona de respuesta del usuario
        # creating the user's answer section
        self.answer_layout = QHBoxLayout()
        
        self.instructions ="""
        A la hora de contestar, SOLO Y EXCLUSIVAMENTE se debe poner la RESPUESTA FINAL, siendo esta solamente el número del resultado. En caso de que la respuesta de la pregunta requiera texto (como una expresión algebraica),  se debe ingresar esta. Puede utilizar sqrt() para hacer raíces cuadradas, ^ para potencias y / para divisiones. Aún así, se recomienda dar el resultado como decimal (si no es entero). En caso de que el número posea muchos decimales, redondee a las milésimas.
        Ejemplos de respuestas válidas:
            2
            7.45
            2/4
            sqrt(2)
            x^2 + 7x - 4
            Verdadero
        
        Ejemplos de respuestas inválidas:
            2 m^2
            Raíz de 2
            El enunciado es verdadero
            
        """
        
        self.info_button = InfoButton(
            base_path = base_path,
            window_title = "FORMAS DE DAR LA SOLUCIÓN",
            information = self.instructions
            )
        
        self.answer_layout.addWidget(self.info_button)
        
        self.user_answer_field = QLineEdit()
        self.user_answer_field.setPlaceholderText("Dé la solución final del problema:")
        self.user_answer_field.setMaxLength(50)
        self.user_answer_field.setFixedSize(450, 30)
        self.answer_layout.addWidget(self.user_answer_field)
        
        self.main_layout.addLayout(self.answer_layout)
        self.answer_layout.setAlignment(Qt.AlignCenter)
        

        self.verify_button = QPushButton("Verificar")
        self.verify_button.setFixedSize(500, 50)
        self.verify_button.setStyleSheet(
            """
            font-family: 'Rockwell Condensed';
            font-size: 30px;
            border-radius: 10px;
            background-color: #3acf55;
            color: #ffffff;
            """
            )
        self.verify_button.clicked.connect(verify_function)
        self.main_layout.addWidget(self.verify_button, alignment = Qt.AlignCenter | Qt.AlignBottom)
        
        self.setLayout(self.main_layout)
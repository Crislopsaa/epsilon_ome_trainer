"""
ES: Este script implementa un QDialog personalizado en el que el usuario elige el tipo y la cantidad de problemas a generar con IA.

EN: This script implements a custom QDialog in which the user chooses the type and quantity of AI problems to generate.
"""

from pathlib import Path

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QFrame, QLabel, QComboBox, QSlider, QVBoxLayout, QHBoxLayout, QMainWindow, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QEvent


class ProblemGenerationDialog(QDialog):
    """
    ES: QDialog personalizado en el que el usuario elige el tipo y la cantidad de problemas a generar con IA.

    EN: Custom QDialog in which the user chooses the type and quantity of AI problems to generate.
    """
    generation_request = pyqtSignal([tuple], [int])
    
    def __init__(self, parent: QMainWindow, base_path: Path):
        """
        :param parent: Main Window that contains this QDialog.
        :type parent: QMainWindow
        :param base_path: Absolute path to the main directory
        :type base_path: Path
        """
        super().__init__(parent)

        self.base_path = base_path

        self.setObjectName("problemGenerationDialog")
        self.setWindowTitle("GENERACIÓN DE PROBLEMAS")
        self.setFixedSize(1000, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.initUI()
        
        self.setStyleSheet(
            """               
            QLabel {
                font-size: 30px;
                font-family: 'sans-serif';
                }
            
            
            QComboBox {
                    font-family: 'sans-serif';
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c2c2e;
                    background-color: white;
                    border: 2px solid #2c2c2e;
                    border-radius: 8px;
                    padding-left: 10px;
                }

            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #f7e7ce;
                selection-color: #2c2c2e;
                border: 1px solid #2c2c2e;
                outline: 0px;
                }
            
            
            QSlider::groove:horizontal {
                border: 1px solid #2c2c2e;
                height: 12px;
                background: white;
                border-radius: 6px;
                }
            
            QSlider::handle:horizontal {
                background: #1a1a1b;
                border: 1px solid #1a1a1b;
                width: 18px;
                height: 18px;
                margin: -14px 0; 
                border-radius: 9px;
                }
            
            QSlider {
                padding-left: 10px;
                padding-right: 10px;
                }
            
            
            QDialogButtonBox QPushButton {
                background-color: white;
                color: #1a1a1b;
                font-family: 'sans-serif';
                font-size: 18px;
                font-weight: bold;
                padding: 10px 25px;
                border: 3px solid #1a1a1b;
                border-radius: 8px;
            }
            
            QDialogButtonBox QPushButton:hover {
                background-color: #2c2c2e;
                color: white;
            }
            
            
            #problemGenerationDialog {
                background-color: #f7e7ce
                }
                
            #automaticModeTitle {
                font-size: 40px;
                font-weight: bold;
                }
            
            #automaticModeButton {
                font-weight: bold;
                font-size: 35px;
                font-family: 'sans-serif';
                border: 3px solid #1a1a1b;
                border-radius: 5px; 
                }
            
            #automaticModeButton[state="off"] {
                background-color: #ff0000;
                color: #f8f9fa;
            }
            
            #automaticModeButton[state="on"] {
                background-color: #39ff14;
                color: #0b0c10;
            }
            
            #divisionFrame {
                background-color: #2c2c2e;
                }
                
            #valueIndicator {
                font-size: 35px;
                font-weight: bold;
                color: #2c2c2e;
            }
            """
        )
    
    
    def initUI(self):
        """
        ES: Esta función define los componentes del QDialog por legibilidad.
        
        EN: This function defines the QDialog's components for legibility.
        
        Note:
            ES: Se usan diferentes frames para distribuir el espacio y para poder ocultarlos cuando sea necesario.
            EN: Different frames are used to distribute space and to be able to hide them when needed.
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(50)
        
        self.problem_selection_layout = QHBoxLayout()
        
        # SECCIÓN DEL MODO AUTOMÁTICO
        # AUTOMATIC MODE SECTION
        self.left_frame = QFrame()
        self.left_frame_layout = QVBoxLayout()
        
        self.automatic_mode_title = QLabel(text = "MODO AUTOMÁTICO")
        self.automatic_mode_title.setObjectName("automaticModeTitle")
        
        self.left_frame_layout.addWidget(self.automatic_mode_title, alignment = Qt.AlignCenter)
        
        self.automatic_mode_button = QPushButton("OFF")
        self.automatic_mode_button.setObjectName("automaticModeButton")
        self.automatic_mode_button.setProperty("state", "off")
        self.automatic_mode_button.setCheckable(True)
        self.automatic_mode_button.setFixedSize(275, 150)
        self.automatic_mode_button.setCursor(Qt.PointingHandCursor)
        self.automatic_mode_button.clicked.connect(self.change_automatic_mode)
        self.left_frame_layout.addWidget(self.automatic_mode_button, alignment = Qt.AlignCenter)
        
        self.left_frame.setLayout(self.left_frame_layout)
        self.problem_selection_layout.addWidget(self.left_frame)
        
        
        self.division_frame = QFrame()
        self.division_frame.setObjectName("divisionFrame")
        self.division_frame.setFixedSize(5, 400)
        self.problem_selection_layout.addWidget(self.division_frame)
        
        
        # SECCIÓN DE TIPOS DE PROBLEMAS: esta sección es ocultable
        # PROBLEM TYPE SECTION: this section can be hidden
        self.right_frame = QFrame()
        size_retain = self.right_frame.sizePolicy()
        size_retain.setRetainSizeWhenHidden(True)
        self.right_frame.setSizePolicy(size_retain)
        
        self.right_frame_layout = QVBoxLayout()
        
        self.grade_selector_layout = QHBoxLayout()
        
        self.grade_label = QLabel(text = "Curso: ")
        self.grade_selector_layout.addWidget(self.grade_label)
        
        self.grade_selector = QComboBox()
        self.grade_selector.addItems(["1º y 2º ESO"])
        self.grade_selector_layout.addWidget(self.grade_selector)
        
        self.right_frame_layout.addLayout(self.grade_selector_layout)
        self.grade_selector_layout.setAlignment(Qt.AlignTop)
        
        
        self.difficulty_selector_layout = QHBoxLayout()
        
        self.difficulty_label = QLabel(text = "Dificultad: ")
        self.difficulty_selector_layout.addWidget(self.difficulty_label)
        
        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(["Provincial", "Regional", "Nacional"])
        self.difficulty_selector_layout.addWidget(self.difficulty_selector)
        
        self.right_frame_layout.addLayout(self.difficulty_selector_layout)
        self.difficulty_selector_layout.setAlignment(Qt.AlignCenter)
        
        
        self.topic_selector_layout = QHBoxLayout()
        
        self.topic_label = QLabel(text = "Temática: ")
        self.topic_selector_layout.addWidget(self.topic_label)
        
        self.topic_selector = QComboBox()
        self.topic_selector.addItems([
            "Aritmética",
            "Álgebra",
            "Geometría",
            "Combinatoria",
            "Lógica"
            ])
        self.topic_selector_layout.addWidget(self.topic_selector)
        
        
        for label in (self.grade_label, self.difficulty_label, self.topic_label):
            label.setFixedWidth(180)
        
        for combo_box in (self.grade_selector, self.difficulty_selector, self.topic_selector):
            combo_box.setFixedSize(225, 50)
        
        self.right_frame_layout.addLayout(self.topic_selector_layout)
        self.topic_selector_layout.setAlignment(Qt.AlignBottom)
        
        self.right_frame.setLayout(self.right_frame_layout)
        self.problem_selection_layout.addWidget(self.right_frame)
        
        
        self.main_layout.addLayout(self.problem_selection_layout)
        self.problem_selection_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addSpacing(75)
        
        # SECCIÓN DE CANTIDAD
        # QUANTITY SECTION
        self.quantity_selection_layout = QVBoxLayout()
        
        self.value_indicator = QLabel(text = "CANTIDAD DE PROBLEMAS: 50")
        self.value_indicator.setObjectName("valueIndicator")
        self.quantity_selection_layout.addWidget(self.value_indicator, alignment = Qt.AlignCenter)
        
        self.quantity_slider_layout = QHBoxLayout()
        self.min_quantity_label = QLabel(text = "1")
        self.quantity_slider_layout.addWidget(self.min_quantity_label, alignment = Qt.AlignLeft)
        
        self.quantity_slider = QSlider(Qt.Horizontal)
        self.quantity_slider.setFixedSize(500, 100)
        self.quantity_slider.setRange(1, 200)
        self.quantity_slider.setValue(50)
        
        self.quantity_slider.setCursor(Qt.SizeHorCursor)
        self.quantity_slider.valueChanged.connect(self.manage_slider_moved)
        self.quantity_slider_layout.addWidget(self.quantity_slider, alignment = Qt.AlignCenter)
        
        self.max_quantity_label = QLabel(text = "200")
        self.quantity_slider_layout.addWidget(self.max_quantity_label, alignment = Qt.AlignRight)
        
        self.quantity_selection_layout.addLayout(self.quantity_slider_layout)
        self.quantity_slider_layout.setAlignment(Qt.AlignCenter)
        
        self.main_layout.addLayout(self.quantity_selection_layout, stretch=1)
        self.quantity_slider_layout.setAlignment(Qt.AlignCenter)
        
        # BOTONES DE ACEPTAR Y CANCELAR (FOOTER)
        # ACCEPT AND CANCEL BUTTONS (FOOTER)
        self.footer = QFrame()
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(0, 10, 20, 20)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("GENERAR PROBLEMAS")
        self.button_box.button(QDialogButtonBox.Cancel).setText("CERRAR")
        self.button_box.accepted.connect(self.send_data)
        self.button_box.rejected.connect(self.reject)
        
        self.button_box.button(QDialogButtonBox.Ok).setCursor(Qt.PointingHandCursor)
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(Qt.PointingHandCursor)
        
        self.footer_layout.addWidget(self.button_box, alignment = Qt.AlignRight)
        self.main_layout.addWidget(self.footer, stretch = 1)
        
        self.setLayout(self.main_layout)
    
    
    def manage_slider_moved(self):
        """
        ES: Actualiza el indicador de la cantidad de problemas conforme se mueve el QSlider.
        
        EN: Updates the problem quantity indicator as the QSlider moves.
        """
        self.value_indicator.setText("CANTIDAD DE PROBLEMAS: " + str(self.quantity_slider.value()))
    
    
    def change_automatic_mode(self):
        """
        ES: Actualiza el botón de modo automático y los frames según si este modo está activado o no.
        
        EN: Updates the automatic mode button and the frames depending on whether this mode is activated or not. 
        """
        if self.automatic_mode_button.isChecked():
            self.automatic_mode_button.setText("ON")
            self.automatic_mode_button.setProperty("state", "on")
            
            self.right_frame.setVisible(False)
            
        else:
            self.automatic_mode_button.setText("OFF")
            self.automatic_mode_button.setProperty("state", "off")

            self.right_frame.setVisible(True)
        
        self.automatic_mode_button.style().unpolish(self.automatic_mode_button)
        self.automatic_mode_button.style().polish(self.automatic_mode_button)
        self.update()
    
    
    def get_selection(self, automatic_mode: bool) -> tuple[str, str, str, int] | int:
        """
        ES: Devuelve la selección de problema del usuario.
        
        EN: Returns user's problem selection.
        
        :param automatic_mode: Whether automatic mode is active (True) or not (False).
        :type automatic_mode: bool
        :return: If the automatic mode is active, an integer (quantity) is returned; else, a tuple (grade, difficulty, topic, quantity) is returned.
        :rtype: tuple | int
        """
        quantity = self.quantity_slider.value()
        
        if automatic_mode:
            return quantity
        
        return (
            self.grade_selector.currentText(),
            self.difficulty_selector.currentText(),
            self.topic_selector.currentText(),
            quantity
            )

    
    def send_data(self):
        """
        ES: Usa pyqtSignal para enviar la selección de problemas del usuario.
        
        EN: Uses pyqtSignal to send user's problem selection. 
        """
        if self.automatic_mode_button.isChecked():
            self.generation_request[int].emit(self.get_selection(True))
            
        else:
            self.generation_request[tuple].emit(self.get_selection(False))
    
    
    def changeEvent(self, event):
        # si el usuario pulsa fuera de la ventana, suena un "beep"
        # if the user clicks outside of the QDialog, a "beep" sounds
        if event.type() == QEvent.WindowDeactivate:
            QApplication.beep()
        
        super().changeEvent(event)
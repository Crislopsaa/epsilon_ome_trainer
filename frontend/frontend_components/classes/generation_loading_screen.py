"""
ES: Este script implementa una página de carga personalizada para la generación de problemas.

EN: This script implements a custom loading screen for problem generation.
"""


from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout, QPushButton, QGraphicsOpacityEffect, QMainWindow, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, QEvent, QParallelAnimationGroup


class GenerationLoadingScreen(QDialog):
    """
    ES: Página de carga personalizada para la generación de problemas.

    EN: Custom loading screen for problem generation.
    
    :param number_of_problems: Number of problems to generate.
    :type  number_of_problems: int
    :param parent: MainWindow that contains this QDialog.
    :type parent: QMainWindow
    """
    early_close_signal = pyqtSignal()
    
    def __init__(self, number_of_problems: int, parent: QMainWindow = None):
        super().__init__(parent)

        self.setWindowTitle("GENERANDO LOS PROBLEMAS...")
        self.setFixedSize(900, 500) 
        self.setAttribute(Qt.WA_DeleteOnClose)
            
        # el modo modal evita que el usuario pueda minimizar o esconder la ventana
        # modal mode prevents the user from hiding or minimizing the window
        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.number_of_problems = number_of_problems
        self.initUI()
        self.apply_styles()
    
    
    def initUI(self):
        """
        ES: Crea y coloca todos los elementos de la UI.
        
        EN: Creates and arranges all UI elements.
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(80, 40, 80, 40)
        self.main_layout.addStretch(1)


        self.success_icon = QLabel("✔")
        self.success_icon.setObjectName("successIcon")
        self.success_icon.setFixedSize(140, 140)
        self.success_icon.setAlignment(Qt.AlignCenter)
        self.success_icon.hide()
        
        # efecto de opacidad para la animación del icono de éxito
        # opacity effect for the success's icon animation
        self.opacity_effect = QGraphicsOpacityEffect(self.success_icon)
        self.success_icon.setGraphicsEffect(self.opacity_effect)

        self.main_layout.addWidget(self.success_icon, alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(20)


        self.title_label = QLabel("GENERANDO CONTENIDO")
        self.title_label.setObjectName("loadingTitle")
        self.main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        
        self.status_label = QLabel("Cargando problemas, por favor espere...")
        self.status_label.setObjectName("statusLabel")
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.number_of_problems)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v / %m") # limpiando el texto / cleaning text
        self.progress_bar.setFixedHeight(45)
        
        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(self.progress_bar)

        
        
        self.continue_button = QPushButton("CONTINUAR")
        self.continue_button.setObjectName("continueButton")
        self.continue_button.setFixedSize(280, 70)
        self.continue_button.setCursor(Qt.PointingHandCursor)
        self.continue_button.hide()
        self.continue_button.clicked.connect(self.accept)
        
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)
        
        
        self.main_layout.addStretch(1)
        self.setLayout(self.main_layout)


    def apply_styles(self):
        """
        ES: Aplica QSS a la interfaz.
        EN: Applies QSS to the UI.
        """
        self.setStyleSheet("""
            QDialog { 
                background-color: #f7e7ce; 
            }
            
            #successIcon {
                font-size: 90px;
                background-color: #39ff14;
                color: #2c2c2e;
                border-radius: 70px;
                border: 4px solid #2c2c2e;
            }
            
            #loadingTitle {
                font-size: 44px;
                font-weight: bold;
                font-family: 'sans-serif';
                color: #2c2c2e;
                letter-spacing: 1px;
            }
            
            #statusLabel {
                font-size: 20px;
                font-family: 'sans-serif';
                color: #5a5a5a;
                font-style: italic;
            }
            
            QProgressBar {
                border: 3px solid #2c2c2e;
                border-radius: 12px;
                background-color: #ffffff;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: #2c2c2e;
            }

            QProgressBar::chunk {
                background-color: #39ff14;
                width: 15px; /* Tamaño de la barrita */
                margin: 2px; /* Espacio entre barritas */
                border-radius: 4px;
            }

            #continueButton {
                background-color: #2c2c2e;
                color: #f7e7ce;
                font-size: 22px;
                font-weight: bold;
                border-radius: 15px;
                border: 3px solid #1a1a1b;
            }

            #continueButton:hover {
                background-color: #39ff14;
                color: #2c2c2e;
                border: 3px solid #2c2c2e;
            }
        """)


    def update_loading_screen(self, value):
        """
        ES: Actualiza el valor mostrado en la barra de carga y activa el cambio en la interfaz si el proceso ha terminado.
        
        EN: Updates the value shown in the loading bar and triggers the UI change if the process has finished.
        
        :param value: Value to update.
        :type value: int
        """
        self.progress_bar.setValue(value)
        if value >= self.progress_bar.maximum():
            self.finish_ui()


    def finish_ui(self):
        """
        ES: Reemplaza la barra de carga por un texto final.
        
        EN: Replaces the loading bar with the final completion text.
        """
        self.setWindowTitle("¡PROBLEMAS LISTOS!")
        self.title_label.setText("¡GENERACIÓN FINALIZADA!")
        self.status_label.hide()
        self.progress_bar.hide()
        self.continue_button.show()
        self.animate_success()


    def animate_success(self):
        """
        ES: Anima el icono de éxito.
        
        EN: Animates the success icon.
        """
        self.success_icon.show()
        
        # animación de movimiento (Pop-up)
        # movement animation (Pop-up)
        self.pop_anim = QPropertyAnimation(self.success_icon, b"geometry")
        self.pop_anim.setDuration(600)
        final_geo = self.success_icon.geometry()
        self.pop_anim.setStartValue(QRect(final_geo.center().x(), final_geo.center().y(), 0, 0))
        self.pop_anim.setEndValue(final_geo)
        self.pop_anim.setEasingCurve(QEasingCurve.OutBack)

        # animación de opacidad
        # opacity animation
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)

        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.pop_anim)
        self.anim_group.addAnimation(self.fade_anim)

        self.anim_group.start()
    
    
    def changeEvent(self, event):
        """
        ES: Si el usuario hace click fuera del QDialog, suena un beep.
        
        EN: If the user clicks outside the QDialog, a beep sounds.
        """
        if event.type() == QEvent.WindowDeactivate:
            QApplication.beep()
        super().changeEvent(event)
    
    
    def closeEvent(self, event):
        """
        ES: Cuando se cierra la ventana, se emite una señal de aviso si el proceso no ha terminado.
        
        EN: When the window is closed, a warning signal is emitted if the process is not finished.
        """
        if self.progress_bar.value() < self.number_of_problems:
            self.early_close_signal.emit()
        super().closeEvent(event)
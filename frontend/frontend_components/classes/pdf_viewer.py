"""
ES: Este script implementa la clase de un visor PDF basado en QtWebEngine.\n
EN: This script implements the class of a PDF viewer based on QtWebEngine.
"""


from PyQt5.QtWidgets import QWidget, QFrame, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PDFViewer(QWidget):
    """
    ES: Un visor PDF basado en QtWebEngine.\n
    EN: A PDF viewer based on QtWebEngine.
    
    Warning:
        ES: Los plugings de QtWebEngine deben ser activados en el script principal (epsilon.py); si no, se verá en blanco.
        EN: QtWebEngine plugins must be activated in the main script (epsilon.py); otherwise, the viewer will appear blank. 
    
    :param pdf_path: Absolute path to the PDF to display.
    :type pdf_path: str
    """
    
    def __init__(self, pdf_path: str):
        super().__init__()
        
        self.main_layout = QVBoxLayout()
        
        self.viewing_pane = QFrame()
        self.viewing_pane.setStyleSheet("""
                                     background-color : #ffffff;
                                     border-radius: 10px;
                                     padding: 15px;
                                     """)
        
        self.pdf_viewer = QWebEngineView()
    
        # cargando el PDF
        # loading the PDF
        try:
            self.pdf_viewer.load(QUrl.fromLocalFile(pdf_path))
        
        # si hay un error, se muestra un mensaje de error
        # if an error happens, an error message is shown   
        except Exception as e:
            QMessageBox.critical(
                self.window(),
                "ERROR AL CARGAR EL PDF EN EL VISOR",
                f"Lo siento, ha ocurrido un error al cargar el PDF en el visor PDF:\n\n{e}"
                )


        self.viewer_layout = QVBoxLayout()
        self.viewer_layout.addWidget(self.pdf_viewer)
        
        self.viewing_pane.setLayout(self.viewer_layout)

        self.main_layout.addWidget(self.viewing_pane)
        
        self.setLayout(self.main_layout)
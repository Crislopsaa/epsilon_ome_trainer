"""
ES: Este es el script principal, que controla que página se está mostrando, su creación y su eliminación.

EN: This is the main script, which controls which page is being shown, its creation and its deletion.
"""


import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

# GUI
from frontend.pages import (home_page, problem_configuration_page, information_page,
                            user_stats_page, generated_problem_page)

# FUNCIONES / FUNCTIONS
from backend.backend_components.db_functions.init_db import init_db
from backend.backend_components.other_functions.get_base_path import get_base_path
from backend.backend_components.db_functions.get_db_path import get_db_path


class MainWindow(QMainWindow):
    """
    ES: La ventana principal de la aplicación que gestiona el flujo de navegación.
    
    EN: The main window's app that manages the navigation flux.
    """
    def __init__(self):
        super().__init__()
        
        self.base_path = get_base_path()
        self.db_path = get_db_path()
        
        # los plugins de QtWebEngine son necesarios para mostrar PDFs
        # QtWebEngine plugins are required for PDF display
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True
        )
        
        epsilon_logo_path = self.base_path / "assets" / "images" / "epsilon_logo.png"
        
        self.setWindowTitle("Epsilon OME Trainer")
        epsilon_logo = QIcon(str(epsilon_logo_path))
        self.setWindowIcon(epsilon_logo)
        self.setGeometry(100, 100, 800, 600)


        # las páginas se manejan con un "stack"
        # the pages are managed with a "stack"
        self.pages_stack = QStackedWidget()
        self.setCentralWidget(self.pages_stack)


        self.home_page = home_page.HomePage(base_path = self.base_path)
        self.home_page.change_page_signal.connect(self.change_page)
        
        self.problem_configuration_page = problem_configuration_page.ProblemConfigurationPage(base_path = self.base_path, db_path = self.db_path)
        self.problem_configuration_page.change_page_signal.connect(self.change_page)
        self.problem_configuration_page.create_generated_problem_page_signal.connect(self.arrange_generated_problem_page)
        
        self.information_page = information_page.InformationPage(base_path = self.base_path)
        self.information_page.change_page_signal.connect(self.change_page)
        

        self.pages_stack.addWidget(self.home_page)
        self.pages_stack.addWidget(self.problem_configuration_page)
        self.pages_stack.addWidget(self.information_page)
                
        self.change_page("home page")


    def change_page(self, page_name: str) -> None:
        """
        ES: Este método cambia entre páginas.
        
        EN: This method switches between pages.
        """
        
        if page_name == "home page":
            self.pages_stack.setCurrentWidget(self.home_page)
            
        elif page_name == "problem configuration page":
            self.pages_stack.setCurrentWidget(self.problem_configuration_page)
            self.delete_generated_problem_page()
        
        elif page_name == "information page":
            self.pages_stack.setCurrentWidget(self.information_page)
        
        elif page_name == "user stats page":
            # si no existe, se crea
            # if it doesn't exist, it is created
            if not hasattr(self, "user_stats_page"):
                self.user_stats_page = user_stats_page.UserStatsPage(base_path = self.base_path, db_path = self.db_path)
                self.user_stats_page.change_page_signal.connect(self.change_page)
                self.pages_stack.addWidget(self.user_stats_page)
            
            self.pages_stack.setCurrentWidget(self.user_stats_page)


    def arrange_generated_problem_page(self, generated_problem_page: generated_problem_page.GeneratedProblemPage) -> None:
        """
        ES: Guarda la página de problemas generados y conecta sus señales.
        
        EN: Stores the generated problem's page and connects its signals.
        
        :param generated_problem_page: Page that displays AI-powered problems.
        :type generated_problem_page: GeneratedProblemPage
        """
        self.generated_problem_page = generated_problem_page
        self.generated_problem_page.change_page_signal.connect(self.change_page)
        self.generated_problem_page.user_stats_changed_signal.connect(self.delete_user_stats_page)
        
        self.pages_stack.addWidget(self.generated_problem_page)
        self.pages_stack.setCurrentWidget(self.generated_problem_page)
    
    
    def delete_generated_problem_page(self) -> None:
        """
        ES: Borra la página de problemas generados.
        
        EN: Deletes the generated problem page.
        """
        
        try:
            if hasattr(self, "generated_problem_page"):
                self.generated_problem_page.setParent(None)
                self.generated_problem_page.deleteLater()
                del self.generated_problem_page
                
        except Exception as e:
            print(f"Lo siento, me temo que ha ocurrido un error al intentar borrar la página de problemas:\n{e}")
    
    
    def delete_user_stats_page(self) -> None:
        """
        ES: Borra la página de estadísticas del usuario.
        
        EN: Deletes the user's stats page.
        """
        
        try:
            if hasattr(self, "user_stats_page"):
                self.user_stats_page.setParent(None)
                self.user_stats_page.deleteLater()
                del self.user_stats_page
                
        except Exception as e:
            print(f"Lo siento, me temo que ha ocurrido un error al intentar borrar la página de estadísticas del usuario:\n{e}")



if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
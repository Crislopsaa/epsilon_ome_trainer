"""
ES: Este es el script principal, que controla que página se está mostrando, su creación y su eliminación.\n
EN: This is the main script, which controls which page is being shown, its creation and its deletion.
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

# importando la GUI de cada página
# importing every page's GUI
from frontend.pages import (home_page, problem_configuration_page, information_page,
                            user_stats_page, generated_problem_page)


# importando funciones personalizadas
# importing customized functions
from backend.backend_components.db_functions.init_db import init_db
from backend.backend_components.other_functions.get_base_path import get_base_path



class MainWindow(QMainWindow):
    """
    ES: La ventana principal de la aplicación que gestiona el flujo de navegación.\n
    EN: The main window's app that manages the navigation flux.
    """
    def __init__(self):
        super().__init__()
        
        self.base_path = get_base_path()
        
        # activando plugins de QtWebEngine       
        # activating QtWebEngine plugins
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True
        )
        
        epsilon_logo_path = self.base_path / "assets" / "images" / "epsilon_logo.png"
        
        self.setWindowTitle("Epsilon OME Trainer")
        epsilon_logo = QIcon(str(epsilon_logo_path))
        self.setWindowIcon(epsilon_logo)
        self.setGeometry(100, 100, 800, 600)


        # creando un "stack" para manejar las páginas
        # creating a stack to manage the pages
        self.pages_stack = QStackedWidget()
        self.setCentralWidget(self.pages_stack)


        # creando las páginas y conectando sus señales
        # creating the pages and connecting their signals
        self.home_page = home_page.HomePage(base_path = self.base_path)
        self.home_page.change_page_signal.connect(self.change_page)
        
        self.problem_configuration_page = problem_configuration_page.ProblemConfigurationPage(base_path = self.base_path)
        self.problem_configuration_page.change_page_signal.connect(self.change_page)
        self.problem_configuration_page.create_generated_problem_page_signal.connect(self.create_generated_problem_page)
        
        self.information_page = information_page.InformationPage(base_path = self.base_path)
        self.information_page.change_page_signal.connect(self.change_page)
        

        self.pages_stack.addWidget(self.home_page)
        self.pages_stack.addWidget(self.problem_configuration_page)
        self.pages_stack.addWidget(self.information_page)
                
        # cuando se ejecuta la app, se muestra la página de inicio
        # when the app is executed, the home page is shown
        self.change_page("home page")


    def change_page(self, page_name: str):
        """
        ES: Este método cambia entre páginas.\n
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
                self.user_stats_page = user_stats_page.UserStatsPage(base_path = self.base_path)
                self.user_stats_page.change_page_signal.connect(self.change_page)
                self.pages_stack.addWidget(self.user_stats_page)
            
            self.pages_stack.setCurrentWidget(self.user_stats_page)


    def create_generated_problem_page(self, generated_problem_page: generated_problem_page.GeneratedProblemPage):
        """
        ES: guarda la página de problemas generados y conecta sus señales.\n
        EN: stores the generated problem's page and connects its signals.
        """
        self.generated_problem_page = generated_problem_page
        self.generated_problem_page.change_page_signal.connect(self.change_page)
        self.generated_problem_page.user_stats_changed_signal.connect(self.delete_user_stats_page)
        
        self.pages_stack.addWidget(self.generated_problem_page)
        self.pages_stack.setCurrentWidget(self.generated_problem_page)
    
    
    def delete_generated_problem_page(self):
        """
        ES: borra la página de problemas generados.\n
        EN: deletes the generated problem page.
        """
        
        try:
            if hasattr(self, "generated_problem_page"):
                self.generated_problem_page.setParent(None)
                self.generated_problem_page.deleteLater()
                del self.generated_problem_page
                
        except Exception as e:
            print(f"Lo siento, me temo que ha ocurrido un error al intentar borrar la página de problemas:\n{e}")
    
    
    def delete_user_stats_page(self):
        """
        ES: borra la página de estadísticas del usuario.\n
        EN: deletes the user's stats page.
        """
        
        try:
            if hasattr(self, "user_stats_page"):
                self.user_stats_page.setParent(None)
                self.user_stats_page.deleteLater()
                del self.user_stats_page
                
        except Exception as e:
            print(f"Lo siento, me temo que ha ocurrido un error al intentar borrar la página de estadísticas del usuario:\n{e}")


# ejecutando la app
# executing the app
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
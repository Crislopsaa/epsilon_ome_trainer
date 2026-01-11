"""
ES: Este script define la clase de la página de estadísticas del usuario.\n
EN: This script implements the user stats page class.
"""


from pathlib import Path

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QStackedWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal

# importando clases personalizadas
# importing custom classes
from frontend.frontend_components.classes.back_button import BackButton
from frontend.frontend_components.classes.info_button import InfoButton
from frontend.frontend_components.classes.plotly_graphics_viewer import PlotlyGraphicsViewer

# importando funciones personalizadas
# importing custom functions
from frontend.frontend_components.functions.paint_background import paint_background
from frontend.frontend_components.functions.create_simple_graphic import create_simple_graphic
from frontend.frontend_components.functions.create_topic_graphic import create_topic_graphic
from frontend.frontend_components.functions.create_difficulty_graphic import create_difficulty_graphic
from frontend.frontend_components.functions.create_full_graphic import create_full_graphic
from backend.backend_components.db_functions.get_simple_graphic_data import get_simple_graphic_data
from backend.backend_components.db_functions.get_topic_graphic_data import get_topic_graphic_data
from backend.backend_components.db_functions.get_difficulty_graphic_data import get_difficulty_graphic_data
from backend.backend_components.db_functions.get_all_user_data import get_all_user_data
from backend.backend_components.db_functions.get_db_path import get_db_path


class UserStatsPage(QWidget):
    """
    ES: La página que muestra las estadísticas del usuario.\n
    EN: The page that displays the user stats.
    
    :param base_path: Absolute path to the main directory.
    :type base_path: Path
    """
    
    change_page_signal = pyqtSignal(str)
    
    def __init__(self, base_path: Path):
        super().__init__()
        
        self.base_path = base_path
        self.db_path = get_db_path()
        

        self.background_path = self.base_path / "assets" / "images" / "stats_page_background.png"
        self.background = QPixmap(str(self.background_path))
        
        main_layout = QVBoxLayout()
        
        self.back_button = BackButton(self.go_back)
        main_layout.addWidget(self.back_button, alignment = Qt.AlignLeft | Qt.AlignTop)

        
        self.title = QLabel()
        self.title.setText("TUS ESTADÍSTICAS")
        self.title.setStyleSheet("""
                                font-size: 75px;
                                font-weight: bold;
                                font-family: 'Rockwell Condensed';
                                color: #ffffff;
                                """)
        main_layout.addWidget(self.title, alignment = Qt.AlignCenter)
        
        
        # creando la sección de elección de gráfico
        # creating the chart selection section
        self.chart_selection_section = QHBoxLayout()
        self.explanation = """
                        <p>
                            Esta sección está dedicada a mostrar gráficos con tus estadísticas, siendo estas la cantidad de problemas que has hecho bien y mal por tipo (curso, dificultad y categoría).<br>
                            
                            Abajo puedes ver un selectbox en el que puedes elegir entre los siguientes gráficos:
                            <ul>
                                <li>Sencillo: Solo muestra cuántos problemas has hecho bien y cuántos mal.</li>
                                <li>Por temática: Muestra cuántos problemas has hecho bien y cuántos mal, agrupando los datos por temática (Álgebra, Geometría...).</li>
                                <li>Por dificultad: Muestra cuántos problemas has hecho bien y cuántos mal, agrupando los datos por dificultad (Provincial, Regional y Nacional).</li>
                                <li>Completo: Muestra cuántos problemas has hecho bien y cuántos mal, agrupando los datos por curso, dificultad y temática.</li>
                            </ul>
                            
                            Además, se utilizarán abreviaturas para las distintos categorías:
                            <ul>
                                <li> A.T.N.: Aritmética y Teoría de Números</li>
                                <li> Al.: Álgebra</li>
                                <li> Geo.: Geometría</li>
                                <li> C.P.: Combinatoria y Probabilidad</li>
                                <li> L.R.: Lógica y Razonamiento</li>
                            </ul>
                        </p>
                        """
        self.explanation_button = InfoButton(
            base_path = self.base_path,
            window_title = "TIPOS DE GRÁFICOS",
            information = self.explanation
        )
        self.explanation_button.setFixedSize(50, 50)
        self.chart_selection_section.addWidget(self.explanation_button)
                  
        self.chart_selector = QComboBox()   
        chart_types = ["Sencillo", "Agrupado por temática", "Agrupado por dificultad", "Completo"]
        self.chart_selector.addItems(chart_types)
        self.chart_selector.setFixedSize(1300, 50)
        self.chart_selector.setStyleSheet("""
                                            font-family: 'Rockwell Condensed';
                                            font-size: 24px;
                                            """)
        
        self.chart_selection_section.addWidget(self.chart_selector)
        
        main_layout.addLayout(self.chart_selection_section)
        self.chart_selection_section.setAlignment(Qt.AlignCenter)


        # creando la zona de gráficos
        # creating the chart section
        self.chart_viewer_stack = QStackedWidget()
        
        self.chart_viewer = PlotlyGraphicsViewer(base_path = base_path)
        self.chart_viewer_stack.addWidget(self.chart_viewer)
        
        self.no_chart_message = QLabel(text= "Lo siento, pero este gráfico no está disponible")
        self.no_chart_message.setStyleSheet("""
            font-family: 'Rockwell Condensed';
            font-size: 40px;
            background-color: #ffffff;
            color: #000000;
            border-radius: 5px;
            padding: 10px;
            """)
        self.chart_viewer_stack.addWidget(self.no_chart_message)
        
        main_layout.addWidget(self.chart_viewer_stack, alignment = Qt.AlignCenter)
        main_layout.addSpacing(110)
        
        self.abbreviated_topics = {
            'Aritmética y Teoría de Números': 'A.T.N.',
            'Álgebra': 'Ál.', 
            'Geometría': 'Geo.',
            'Combinatoria y Probabilidad': 'C.P.',
            'Lógica y Razonamiento': 'L.R.'
            }
        
        # conectando el selector para que actualice los gráficos según la elección del usuario
        # connecting the selector so that it updates the chart depending on the user's selction
        self.chart_selector.currentIndexChanged[str].connect(self.update_chart)
        
        self.setLayout(main_layout)
        
        self.update_chart("Sencillo")
    
    
    def go_back(self):
        """
        ES: Cambia la página por la página de inicio.\n
        EN: Switches the page to the home page.
        """
        self.change_page_signal.emit("home page")
    
    
    def paintEvent(self, event):
        """
        ES: Pinta el fondo con una imagen.\n
        EN: Paints the background with an image.
        """
        painter = QPainter(self)
        paint_background(widget = self, painter = painter, pixmap = self.background)
        return super().paintEvent(event)
    
    
    def update_chart(self, selected_chart: str):
        """
        ES: Actualiza el gráfico mostrado según lo que elija el usuario.
        
        EN: Updates the chart displayed depending on the user's selection.
        
        :param selected_chart: Chart to display.
        :type selected_chart: str
        """
        
        try:   
            if selected_chart == "Sencillo":
                if not hasattr(self, "simple_chart"):
                    simple_chart_data = get_simple_graphic_data(self.db_path)
                    self.simple_chart = create_simple_graphic(simple_chart_data)
                
                self.current_chart = self.simple_chart
            
            
            elif selected_chart == "Agrupado por temática":
                if not hasattr(self, "topic_chart"):
                    topic_chart_data = get_topic_graphic_data(self.db_path, self.abbreviated_topics)
                    self.topic_chart = create_topic_graphic(topic_chart_data)
                
                self.current_chart= self.topic_chart
                    
            
            elif selected_chart == "Agrupado por dificultad":
                if not hasattr(self, "difficulty_chart"):
                    difficulty_chart_data = get_difficulty_graphic_data(self.db_path)
                    self.difficulty_chart = create_difficulty_graphic(difficulty_chart_data)
                
                self.current_chart = self.difficulty_chart
            
            
            elif selected_chart == "Completo":
                if not hasattr(self, "full_chart"):
                    all_user_data = get_all_user_data(self.db_path, self.abbreviated_topics)
                    self.full_chart = create_full_graphic(all_user_data)
                
                self.current_chart = self.full_chart
                
                                
            self.chart_viewer.show_graphic(self.current_chart)
            self.chart_viewer_stack.setCurrentWidget(self.chart_viewer)
        
        
        except ValueError as e:
            self.set_insufficient_data_message(e)    
            
        except Exception as e:
            self.set_error_message(e)
    
    
    def set_insufficient_data_message(self, error: ValueError):
        """
        ES: Avisa al usuario de que no ha resuelto suficientes problemas.
        EN: Alerts the user that they have not solved enough problems.
        
        :param error: Exception derived from the lack of problems.
        :type error: ValueError
        """
        
        self.chart_viewer_stack.setCurrentWidget(self.no_chart_message)
        QMessageBox.warning(
            self.window(),
            "NO HAY SUFICIENTES DATOS",
            f"Me temo que no has resuelto suficientes problemas como para poder ver este gráfico:\n\n{error}"
        )

   
    def set_error_message(self, error: Exception):
        """
        ES: Avisa al usuario de que ha habido un error.
        EN: Alerts the user that an error has occurred.
        
        :param error: Exception produced while creating a chart.
        :type error: Exception
        """
        
        self.chart_viewer_stack.setCurrentWidget(self.no_chart_message)
        QMessageBox.critical(
            self.window(),
            "ERROR AL CREAR EL GRÁFICO",
            f"Me temo que ha ocurrido un error al intentar mostrar este gráfico:\n\n{error}"
        )